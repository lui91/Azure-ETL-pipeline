# Airflow orchestration of disaster data analysis on Azure

Process:

- Dimensional design of database.
- Azure Database for MySQL servers stored procedure calling.
- Data pre-processing in Azure data Factory.
- Machine learning Pipeline implementation in Machine Learning studio.
- Endpoint creation for trained model calls.
- Docker containerization of flask app.
- Image upload to Azure container registry.
- Image deployment using Azure Web App service.
- CI/CD using github actions.

# Docker image creation

1. Define DockerFile
2. Download docker-compose.yml
3. docker compose build
4. docker compose up

# Install Azure CLI on running image as root

1. docker exec -it -u root baeldung bash
2. curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Register local packages

1. Define setup.py

```python
python setup.py install
```

# Upload file to blob storage

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
