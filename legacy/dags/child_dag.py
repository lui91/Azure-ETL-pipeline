# from pendulum import datetime
# from airflow.decorators import dag, task_group
# from airflow.sensors.external_task import ExternalTaskSensor
# from airflow.operators.bash import BashOperator
# import json


# @dag(dag_id="xcom_child",
#      start_date=datetime(2023, 3, 1),
#      schedule_interval=None,
#      catchup=False,
#      render_template_as_native_obj=True,)
# def main_dag():

#     resources = None
#     with open('/opt/airflow/includes/terraform/first_stage/resources.txt') as json_file:
#         resources = json.load(json_file)

#     resources_generated = ExternalTaskSensor(task_id='wait_for_resources',
#                                              external_dag_id='xcom_parent',
#                                              external_task_id='resource_writter',
#                                              start_date=datetime(2020, 4, 29),
#                                              #  execution_delta=timedelta(hours=1),
#                                              timeout=3600)

#     @task_group
#     def add_resources_to_terraform():
#         for resource in resources.keys():
#             register = BashOperator(task_id=f"tf_import_{resource}",
#                                     cwd="/opt/airflow/includes/terraform/second_stage/",
#                                     bash_command=f"echo {resources[resource]}")

#     resources_generated >> add_resources_to_terraform()


# main_dag()

# '''                     '''

# @dag(dag_id="xcom_parent",
#      start_date=datetime(2023, 3, 1),
#      schedule_interval=None,
#      catchup=False,
#      render_template_as_native_obj=True,)
# def dags_test():
#     @task(task_id='create_commands')
#     def create_commands():
#         return {
#             'a': 'command-a',
#             'b': 'command-b',
#         }

#     @task(task_id='resource_writter')
#     def write_commands(commands):
#         with open("/opt/airflow/includes/terraform/first_stage/resources.txt", "w") as comm_writter:
#             comm_writter.write(json.dumps(commands))

#     exit_status = BashOperator(
#         task_id="exiting_task", bash_command=" echo Process ended")

#     write_commands(create_commands()) >> exit_status


# dags_test()
