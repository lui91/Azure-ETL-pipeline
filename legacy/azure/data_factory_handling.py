# from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import DefaultAzureCredential
from airflow.decorators import task
from airflow.sensors.base import PokeReturnValue
import os


@task(task_id="etl_pipeline_run")
def run_data_factory_pipeline(resource_group, factory_name, pipeline_name) -> DataFactoryManagementClient:
    ''' Call a pipeline previously defined in Azure Data Factory '''
    default_credential = DefaultAzureCredential()
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    adf_client = DataFactoryManagementClient(
        default_credential, subscription_id)
    pipeline_run = adf_client.pipelines.create_run(
        resource_group, factory_name, pipeline_name)
    return pipeline_run.run_id


@task.sensor(task_id="pipeline_monitor", poke_interval=60, timeout=3600, mode="reschedule")
def pipeline_run_check(resource_group, factory_name, pipeline_run_id):
    default_credential = DefaultAzureCredential()
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    adf_client = DataFactoryManagementClient(
        default_credential, subscription_id)
    pipeline_run = adf_client.pipeline_runs.get(
        resource_group, factory_name, pipeline_run_id)
    print("\n\tPipeline run status: {}".format(pipeline_run.status))
    if pipeline_run.status in ["Succeeded", "Failed"]:
        return PokeReturnValue(is_done=True, xcom_value="done")
