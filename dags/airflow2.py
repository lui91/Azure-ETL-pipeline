from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from airflow.decorators import dag
from includes.azure.blob_handling import upload_blob_to_container


@dag(dag_id="azure_tweets_processing",
     start_date=datetime(2023, 2, 11),
     default_view="graph",
     template_searchpath="/opt/airflow/include/")
def main_pipeline() -> None:
    ''' Azure ETL -> ML training -> Model deployment '''
    sense_path = "/opt/airflow/data/"
    files_to_sense = ["messages", "categories"]
    blobs_url = "https://datastoragetweets.blob.core.windows.net"

    start_node = EmptyOperator(task_id="start_task")

    file_sensors = []
    with TaskGroup('csv_sensors') as csv_sensors:
        for file in files_to_sense:
            file_sensor = FileSensor(task_id=f"sensor_{file}",
                                     filepath=sense_path + file + ".csv",
                                     poke_interval=30,
                                     mode='poke',
                                     recursive=False)
            file_sensors.append(file_sensor)

    end_node = EmptyOperator(task_id="completed")

    with TaskGroup('csv_uploads_azure') as csv_uploads_azure:
        for file_name in files_to_sense:
            uploader = PythonOperator(task_id=f"{file_name}_uploader",
                                      python_callable=upload_blob_to_container,
                                      op_kwargs={
                                          'local_file_name': file_name + ".csv",
                                          'local_data_path': sense_path,
                                          'container_name': "csvs",
                                          'account_url': blobs_url
                                      })

    chain(start_node, csv_sensors, csv_uploads_azure, end_node)


dag = main_pipeline()
