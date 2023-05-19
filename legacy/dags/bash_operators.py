from airflow.operators.bash import BashOperator
from airflow.models import DAG

def set_bash_operator(task_id: str, bash_command: str, dag: DAG):
    return BashOperator(task_id=task_id,
                        bash_command=bash_command,
                        dag=dag)