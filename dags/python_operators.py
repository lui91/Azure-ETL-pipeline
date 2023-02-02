from airflow.operators.python import PythonOperator
from airflow.models import DAG

def set_python_operator(task_id:str, dag: DAG,  callable=None):
    return PythonOperator(task_id=task_id,
                          python_callable=callable,
                          dag=dag)