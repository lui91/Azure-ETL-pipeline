# Airflow orchestration of disaster data analysis on Azure

# Tasks on this project:

- Dimensional design of database.
- Azure Database for MySQL servers stored procedure calling.
- Data pre-processing in Azure data Factory.
- Machine learning Pipeline implementation in Machine Learning studio.
- Endpoint creation for trained model calls.
- Docker containerization of flask app.
- Image upload to Azure container registry.
- Image deployment using Azure Web App service.
- CI/CD using github actions.

## Airflow process

![Airflow process](/imgs/airflow_dag.png "Airflow process")

## Data factory transformation

![Data factory](/imgs/azure_data_factory.png "Data factory pipeline")

# Docker image creation

1. Define DockerFile
2. Download docker-compose.yml
3. docker compose build
4. docker compose up

# Log in Azure CLI on running image

1. az login --use-device-code

# Register local packages (Before creating docker image)

1. Define setup.py

```python
python setup.py install
```

# (Optional) Upload file to blob storage

1. Grant accesss to user on blob storache IAM
2. Sign in and connect the app to Azure on Azure CLI

```powershell
az login
```

2. Get stprage resource id

```powershell
az storage account show --resource-group dataf_resource --name datastoragetweets --query id
```

3. Assign access role to user

```powershell
az role assignment create --assignee Luis.RamirezSolis@cinvestav.mx --role "Storage Blob Data Contributor" --scope "<your-resource-id>"
```
