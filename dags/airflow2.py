from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.utils.task_group import TaskGroup
from datetime import datetime
from airflow.sensors.filesystem import FileSensor
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from include.blob_handling import upload_blob_to_container


@dag(dag_id="azure_tweets_processing",
     start_date=datetime(2023, 2, 11),
     default_view="graph",
     template_searchpath="/opt/airflow/include/")
def main_pipeline() -> None:
    ''' Azure ETL -> ML training -> Model deployment '''
    sense_path = "/opt/airflow/data/"
    files_to_sense = ["messages", "categories"]

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
        for file in file_sensors:
            uploader = PythonOperator(task_id=f"{file}_uploader",
                                      python_callable=upload_blob_to_container)

    chain(start_node, csv_sensors, end_node)


dag = main_pipeline()
