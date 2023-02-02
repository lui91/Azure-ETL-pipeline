from dags.python_operators import set_python_operator
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from datetime import datetime


def test_python_operator():
    dummy_dag = DAG(dag_id="dummy_dag",
                    start_date=datetime.now())
    dummy_callable = lambda x: print("ok")
    original_py_operator = PythonOperator(task_id="or_operator",
                          python_callable=dummy_callable,
                          dag=dummy_dag)
    class_py_operator = set_python_operator(task_id="test_operator",
                               dag=dummy_dag,
                               callable=dummy_callable)
    assert type(original_py_operator), type(class_py_operator)
