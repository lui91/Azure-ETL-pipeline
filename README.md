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

## Data factory pipeline

![Data factory](/imgs/pipeline.png "Data factory pipeline")

## Data factory transformation

![Data factory](/imgs/azure_data_factory.png "Data factory transformation")

## Airflow DAG

![Airflow process](/imgs/airflow_dag.png "Airflow process")

## Warehouse design

![Warehouse design](/diagram/shema%20diagram.drawio.png "Schema design")

# Docker image creation

1. Define DockerFile
2. Download docker-compose.yml
3. docker compose build
4. docker compose up -d

# Log in Azure CLI on running image

1. az login --use-device-code

# Create env file

Azure data needed for the connections

- TF_VAR_BLOB_STORAGE= storage account
- TF_VAR_FACTORY_NAME= desired data factory name
- TF_VAR_RESOURCE_GROUP= resource group name
- TF_VAR_POSTGRE_HOST= X.postgres.database.azure.com, postrge server hostname
- TF_VAR_POSTGRE_DB= database name
- TF_VAR_POSTGRE_LOGIN= postgre login
- TF_VAR_POSTGRE_PASSWORD= postgre password

# Run project

- Run dag.
- Verify that the linked services are correctly configured.
- Publish the automatically provisioned pipeline.
- Run the pipeline
