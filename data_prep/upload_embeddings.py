from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

def upload_files(files, connection_string, container_name, output_dir):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    for file in files:
        blob_client = container_client.get_blob_client(file)
        with open(os.path.join(output_dir, file), 'rb') as f:
            blob_client.upload_blob(f)
            
def main():
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = 'eramusbot-container'
    output_dir = './erasmusbot/chunks/data'
    files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    upload_files(files, connection_string, container_name, output_dir)
    
if __name__ == '__main__':
    main()