from airflow.models.baseoperator import chain
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from includes.azure.postgre_handling import call_stored_procedure, create_postgre_schema
from includes.azure.blob_handling import upload_blob_to_container
from datetime import datetime
import os


@dag(dag_id="etl_process",
     start_date=datetime(2023, 2, 11),
     schedule_interval=None,
     default_view="graph",
     template_searchpath="/opt/airflow/include/")
def main_pipeline() -> None:
    ''' Azure IaC -> Blob staging -> Data Factory data traformation -> Data load to PostgreSQL'''
    # ETL variables
    file_path = os.getenv('FILE_PATH')
    files_to_sense = ["messages", "categories"]
    blobs_url = "https://" + \
        os.getenv('TF_VAR_BLOB_STORAGE') + ".blob.core.windows.net"
    resource_group = os.getenv('DF_RESOURCE_GROUP')
    factory_name = os.getenv('FACTORY_NAME')
    pipeline_name = os.getenv('PIPELINE_NAME')

    start_node = EmptyOperator(task_id="start_task")

    tf_create_inf = BashOperator(task_id="tf_create_inf",
                                 cwd="/opt/airflow/includes/terraform/one_stage/",
                                 bash_command="terraform apply -auto-approve")

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

    end_node = EmptyOperator(task_id="completed")

    chain(start_node, tf_create_inf, py_postgre_schema,
          postgre_stored_procedure, csv_sensors, csv_uploads_azure, end_node)


dag = main_pipeline()
