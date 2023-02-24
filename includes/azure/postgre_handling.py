import psycopg2
import os
from airflow.decorators import task
import pandas as pd


def get_connection():
    host = os.getenv('DB_HOST')
    dbname = os.getenv('DBNAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    sslmode = 'require'

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(
        host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    return conn


@task(task_id="postgre_call_stored_procedure")
def call_stored_procedure():
    ''' Call stored procedure to add current date to date dim'''
    conn = get_connection()
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute("CALL insert_date();")
    conn.commit()
    cursor.close()
    conn.close()
