from airflow.decorators import dag
from pendulum import datetime
import json
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup


def _read_file(task_id='get_data'):
    with open("/opt/airflow/includes/terraform/first_stage/resources.txt") as f:
        data = json.load(f)
        return data


def _process_obtained_data(ti):
    list_of_resources = ti.xcom_pull(task_ids='get_data')
    Variable.set(key='commands',
                 value=list_of_resources, serialize_json=True)


@dag(dag_id="dynamic_tasks",
     start_date=datetime(2023, 3, 1),
     schedule_interval=None,
     catchup=False,
     render_template_as_native_obj=True,)
def dags_test():

    tf_get_resources = BashOperator(task_id="tf_get_resources",
                                    cwd="/opt/airflow/includes/terraform/first_stage/",
                                    bash_command="terraform output -json >> resources.txt")

    get_data = PythonOperator(
        task_id='get_data',
        python_callable=_read_file)

    preparation_task = PythonOperator(
        task_id='preparation_task',
        python_callable=_process_obtained_data)

    # Top-level code within DAG block
    resource_list = Variable.get('commands',
                                 default_var=['default_resource'],
                                 deserialize_json=True)

    with TaskGroup('resources_group', prefix_group_id=False,) as resources_group:
        for resource in resource_list.keys():
            resource_value = resource_list[resource]["value"]
            tf_resources = BashOperator(task_id=f"tf_get_{resource}",
                                        cwd="/opt/airflow/includes/terraform/second_stage/",
                                        bash_command=f"echo Creating:{resource} ID: {resource_value}")

    delete_file = BashOperator(task_id="tf_rm_resources",
                               cwd="/opt/airflow/includes/terraform/first_stage/",
                               bash_command="rm resources.txt")

    exit_status = BashOperator(
        task_id="exiting_task", bash_command=" echo Process ended")

    tf_get_resources >> get_data >> preparation_task >> resources_group >> delete_file >> exit_status


dags_test()
