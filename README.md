# Airflow orchestration of disaster data analysis on Azure ![Main workflow](https://github.com/lui91/airflow_ingestion/actions/workflows/docker-image.yml/badge.svg)

# Tasks on this project:

- Dimensional design of Warehouse.
- Terraform storage, RBAC, and infrastructure provisioning.
- Airflow orchestration.
- Azure Data factory transform and load pipeline.
- Azure Database for PostgreSQL servers stored procedure calling.
- CI/CD using GitHub actions.

## Structure

![General process](/diagram/general.drawio.png "General process")

## Data factory pipeline

![Data factory](/imgs/pipeline.png "Data factory pipeline")

## Data flow transformation

![Data factory](/imgs/azure_data_factory.png "Data factory transformation")

## Airflow DAG

![Airflow process](/imgs/airflow_dag.png "Airflow process")

## Warehouse design

![Warehouse design](/diagram/shema%20diagram.drawio.png "Schema design")

# Run project

# 1. Create .env file

Azure data needed for the connections, create the .en file in root folder

- TF_VAR_BLOB_STORAGE= storage account
- TF_VAR_FACTORY_NAME= desired data factory name
- TF_VAR_RESOURCE_GROUP= resource group name
- TF_VAR_POSTGRE_HOST= X.postgres.database.azure.com, postrges server hostname
- TF_VAR_POSTGRE_DB= database name
- TF_VAR_POSTGRE_LOGIN= postgres login
- TF_VAR_POSTGRE_PASSWORD= postgres password

# 2. Docker compile

1. docker compose build
2. docker compose up -d
3. Attach to one of the created docker containers.

# 3. Log in to Azure CLI on running image

1. az login --use-device-code

# 4. Use Ariflow to provision the Azure infrastructure.

- Run dag using airflow CLI or web UI on localhost:8080.

# 5. Go to the created data factory on the Azure portal.

- Verify that the linked services are correctly configured.
- Publish the automatically provisioned pipeline.
- Run the pipeline.
