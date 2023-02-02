from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobBlock
import os

def delete_file_from_container():
    pass

def upload_blob_to_container(local_file_name: str,
                             local_data_path: str,
                             container_name: str= "csvs",
                             search_exists: bool= True, 
                             account_url:str = "https://datastoragetweets.blob.core.windows.net") -> bool:
    try:
        account_url = account_url
        default_credential = DefaultAzureCredential()

        if search_exists:
            container = ContainerClient(account_url=account_url, credential=default_credential, container_name=container_name)
            blob_list = container.list_blobs()
            for blob in blob_list:
                if blob.name == local_file_name:
                    print("File already exists")
                    return False

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        # Set a name for the container
        container_name = container_name

        local_data = local_data_path
        local_file_name = local_file_name
        upload_file_path = os.path.join(local_data, local_file_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data)

        print(f"{local_file_name} uploaded to {container_name} container \n")
        return True

    except Exception as ex:
        print('Exception:')
        print(ex)
    return False
