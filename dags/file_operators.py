from airflow.sensors.filesystem import FileSensor
from airflow.models import DAG

def set_file_sensor(task_id: str, 
                    filepath:str,
                    file_name: str,
                    dag: DAG,
                    poke_interval: int=45):
    ''' Template for defining filse senors given the file type to search '''
    return FileSensor(task_id=task_id,
                    filepath=filepath + file_name,
                    dag=dag,
                    poke_interval=poke_interval)
