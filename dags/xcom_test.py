from airflow.decorators import dag, task
from pendulum import datetime
from airflow.operators.bash import BashOperator
from pathlib import Path


@dag(dag_id="xcom_tests",
     start_date=datetime(2023, 3, 1),
     schedule_interval=None,
     catchup=False,
     render_template_as_native_obj=True,)
def dags_test():
    @task(task_id='create_commands')
    def create_commands():
        return {
            'a': 'command-a',
            'b': 'command-b',
        }

    @task
    def write_commands(dict):
        with open('resources.txt', "w") as r_file:
            r_file.writelines(dict)

    cr_comms = write_commands(create_commands())
    # 1. save to file inside task
    # 2 read in main process and create task

    # commands = "{{{{ task_instance.xcom_pull(task_ids='create_commands', dag_id='xcom_tests', key='return_value') }}}}"
    command = "test"
    file_exists = Path('resources.txt').exists()
    bash_test = BashOperator(task_id=f"tf_infra_{command}",
                             cwd="/opt/airflow/includes/terraform/first_stage/",
                             #  bash_command="echo You did it!!!! {{ task_instance.xcom_pull(task_ids='create_commands', dag_id='xcom_tests', key='return_value') }}")
                             bash_command=f"The file exists: {file_exists} ")

    cr_comms >> bash_test


dags_test()
