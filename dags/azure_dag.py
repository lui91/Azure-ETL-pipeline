from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.decorators import task
from datetime import datetime
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from airflow.decorators import dag
from includes.azure.blob_handling import upload_blob_to_container
from includes.azure.data_factory_handling import run_data_factory_pipeline, pipeline_run_check
from includes.azure.postgre_handling import call_stored_procedure, create_postgre_schema
import json
from airflow.models import Variable
# from includes.ml.ml_training import ml_pipeline
import os

''' 
First run: - Init terraform files
           - Log in Azure
'''


def _read_file(task_id='get_data'):
    with open("/opt/airflow/includes/terraform/first_stage/resources.txt") as f:
        data = json.load(f)
        return data


def _process_obtained_data(ti):
    list_of_resources = ti.xcom_pull(task_ids='get_data')
    Variable.set(key='commands',
                 value=list_of_resources, serialize_json=True)


@dag(dag_id="azure_tweets_processing",
     start_date=datetime(2023, 2, 11),
     default_view="graph",
     template_searchpath="/opt/airflow/include/")
def main_pipeline() -> None:
    # with DAG("azure_tweets_processing", start_date=datetime(2023, 2, 11), catchup=False) as dag:
    ''' Azure IaC -> Azure ETL -> ML training -> Model deployment '''
    # ETL variables
    file_path = os.getenv('FILE_PATH')
    files_to_sense = ["messages", "categories"]
    blobs_url = os.getenv('BLOBS_URL')
    resource_group = os.getenv('DF_RESOURCE_GROUP')
    factory_name = os.getenv('FACTORY_NAME')
    pipeline_name = os.getenv('PIPELINE_NAME')

    start_node = EmptyOperator(task_id="start_task")

    tf_apply_first_stage = BashOperator(task_id="tf_apply_first_stage",
                                        cwd="/opt/airflow/includes/terraform/first_stage/",
                                        bash_command="terraform apply -auto-approve")

    tf_get_resources = BashOperator(task_id="tf_get_resources",
                                    cwd="/opt/airflow/includes/terraform/first_stage/",
                                    bash_command="terraform output -json >> resources.txt")

    get_data = PythonOperator(
        task_id='get_data',
        python_callable=_read_file)

    resource_data_preparation_task = PythonOperator(
        task_id='resource_data_preparation_task',
        python_callable=_process_obtained_data)

    py_postgre_schema = create_postgre_schema()

    postgre_stored_procedure = call_stored_procedure()

    file_sensors = []
    with TaskGroup('csv_sensors') as csv_sensors:
        for file in files_to_sense:
            file_sensor = FileSensor(task_id=f"sensor_{file}",
                                     filepath=file_path + file + ".csv",
                                     poke_interval=30,
                                     mode='poke',
                                     recursive=False)
            file_sensors.append(file_sensor)

    with TaskGroup('csv_uploads_azure') as csv_uploads_azure:
        for file_name in files_to_sense:
            uploader = PythonOperator(task_id=f"{file_name}_uploader",
                                      python_callable=upload_blob_to_container,
                                      op_kwargs={
                                          'local_file_name': file_name + ".csv",
                                          'local_data_path': file_path,
                                          'container_name': "csvs",
                                          'account_url': blobs_url
                                      })

    resource_list = Variable.get('commands',
                                 default_var=['default_resource'],
                                 deserialize_json=True)

    with TaskGroup('resources_group', prefix_group_id=False,) as resources_group:
        for resource in resource_list.keys():
            resource_type = resource.replace('-', '.')
            resource_value = resource_list[resource]["value"]
            tf_resources = BashOperator(task_id=f"tf_get_{resource}",
                                        cwd="/opt/airflow/includes/terraform/second_stage/",
                                        bash_command=f"terraform import {resource_type} {resource_value}")

    delete_file = BashOperator(task_id="tf_rm_resources",
                               cwd="/opt/airflow/includes/terraform/first_stage/",
                               bash_command="rm resources.txt")

    tf_apply_second_stage = BashOperator(task_id="tf_apply_second_stage",
                                         cwd="/opt/airflow/includes/terraform/second_stage/",
                                         bash_command="terraform apply -auto-approve")

    # trigger_azdf_pipeline = run_data_factory_pipeline(
    #     resource_group, factory_name, pipeline_name)

    # monitor_azdf_pipeline = pipeline_run_check(
    #     resource_group, factory_name, trigger_azdf_pipeline)

    # ml_task = ml_pipeline()

    end_node = EmptyOperator(task_id="completed")

    # chain(start_node, csv_sensors, csv_uploads_azure, trigger_azdf_pipeline, monitor_azdf_pipeline,
    #       end_node)

    chain(start_node, tf_apply_first_stage, tf_get_resources, get_data, resource_data_preparation_task, py_postgre_schema,
          postgre_stored_procedure, csv_sensors, csv_uploads_azure, resources_group, delete_file, tf_apply_second_stage, end_node)


dag = main_pipeline()
