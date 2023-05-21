# Airflow orchestration of disaster data analysis on Azure ![Main workflow](https://github.com/lui91/airflow_ingestion/actions/workflows/python-app.yml/badge.svg)

# Tasks on this project:

- Dimensional design of Warehouse.
- Terraform storage, RBAC, and infrastructure provisioning.
- Airflow orchestraition.
- Azure Data factory transform and load pipeline.
- Azure Database for PostgreSQL servers stored procedure calling.
- CI/CD using github actions.

## Structure

![General process](/diagram/general.drawio.png "General process")

## Airflow DAG

![Airflow process](/imgs/airflow_dag.png "Airflow process")

## Data factory pipeline

![Data factory](/imgs/pipeline.png "Data factory pipeline")

## Data factory transformation

![Data factory](/imgs/azure_data_factory.png "Data factory transformation")

## Warehouse design

![Warehouse design](/diagram/shema%20diagram.drawio.png "Schema design")

# Register local packages (Before creating docker image)

1. Define setup.py

```python
python setup.py install
```

# Docker image creation

1. Define DockerFile
2. Download docker-compose.yml
3. docker compose build
4. docker compose up -d

# Run bash in conainer

# Log in Azure CLI on running image

1. az login --use-device-code

# Run project

- Run dag.
- Verify that the linked services are correctly configured.
- Publish the automatically provisioned pipeline.
- Run the pipeline
