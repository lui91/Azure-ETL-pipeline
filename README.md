# airflow_ingestion
Airflow automated parquet file ingestion to DB

# Docker image creation

```bash
docker run --name=airflow -p 8080:8080 -v local_folder_path:/opt/airflow/dags/ -d apache/airflow airflow standalone
```

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
