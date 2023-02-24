from airflow.models import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from dags.data_loader import read_name
from pathlib import Path

dag = DAG(dag_id='etl_update')

sensor = FileSensor(task_id='sense_file', 
                    filepath=Path("D:/data_sets/airlines/flights_parquet/airflow/").as_posix(),
                    poke_interval=60,
                    dag=dag)

python_task = PythonOperator(task_id='reading_file', 
                             python_callable=read_name,
                             provide_context=True,
                             dag=dag)

sensor >> python_task