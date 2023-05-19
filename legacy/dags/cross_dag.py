'''
code from: https://github.com/dariusgm/airflow-test/blob/main/plugins/cross_dag.py
'''
import json
from airflow.models import BaseOperator
from airflow.operators.bash import BashOperator
from airflow.utils.decorators import apply_defaults


class TriggerDagOperator(BaseOperator):
    @apply_defaults
    def __init__(self, trigger_dag_id: str, data: dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trigger_dag_id = trigger_dag_id
        self.ui_color = '#ff0'  # type str
        self.data = data

    def execute(self, context):
        conf_str = json.dumps(self.data)
        command = f"airflow trigger_dag --conf '{conf_str}' {self.trigger_dag_id}"
        operator = BashOperator(
            task_id=f'execute_{self.trigger_dag_id}',
            bash_command=command
        )
        operator.execute(context)


class FetchDagOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ui_color = '#ff0'  # type str

    def execute(self, context):
        config = context['dag_run'].conf
        self.do_xcom_push = True
        return config
