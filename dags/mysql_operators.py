from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.models import DAG


def set_mysql_operator(task_id: str,
                       dag: DAG,
                       query: str,
                       db: str = "disaster_data"):
    return MySqlOperator(task_id=task_id, mysql_conn_id="mysql_azure", sql=query, dag=dag)


def call_stored_procedure(task_id: str,
                          dag: DAG):
    sql_query = "CALL insert_date();"
    mysql = set_mysql_operator(task_id=task_id,
                               dag=dag,
                               query=sql_query)
    return mysql
