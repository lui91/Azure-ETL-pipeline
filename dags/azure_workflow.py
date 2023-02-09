from datetime import datetime
from airflow.models import DAG
from file_operators import set_file_sensor
from python_operators import set_python_operator
# from azure_code import blob_handling
# from py_process import process
from mysql_operators import call_stored_procedure


default_args = {
    'owner': 'lramirez',
    'start_date': datetime(2023, 1, 28),
    'retries': 2,
    'tag': "tweets_pipeline"
}

sense_path = "/Users/luisramirez/airflow/dags/airflow_ingestion/files_to_sense/"

azure_dag = DAG('azure_pipeline', default_args=default_args)

# messages_sensor = set_file_sensor(task_id="message_sensor",
#                                   dag=azure_dag,
#                                   filepath=sense_path,
#                                   file_name="messages.csv")

# categories_sensor = set_file_sensor(task_id="categories_sensor",
#                                     dag=azure_dag,
#                                     filepath=sense_path,
#                                     file_name="categories.csv")

# py_up_messages= set_python_operator(task_id="py_up_messages",
#                                     dag=azure_dag,
#                                     callable=blob_handling.upload_blob_to_container(local_file_name="messages.csv",
# local_data_path=sense_path))

# py_up_categories = set_python_operator(task_id="py_up_categories",
#                                        dag=azure_dag,
#                                        callable=process.print_params)


mysql_opeator = call_stored_procedure(task_id="mysql_operator", dag=azure_dag)

# messages_sensor >> py_up_messages

# categories_sensor >> py_up_categories

mysql_opeator
