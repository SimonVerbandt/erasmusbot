import os
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.docstore.document import Document
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient

# Load environment variables from .env file
load_dotenv()
STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = 'eramusbot-container'
search_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
search_api_key = os.getenv('AZURE_SEARCH_API_KEY')
search_index_name = os.getenv('AZURE_SEARCH_INDEX_NAME')

blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
indexer_client = SearchIndexerClient(search_endpoint, AzureKeyCredential(search_api_key))
indexer_name = 'indexer1717610357330'

# Function to clean and process HTML files
def process_html_file(file_path):
    bs_transformer = BeautifulSoupTransformer()

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
                
    # Limit the context length to 1000 characters
    context_length = 1000
    
    document = [Document(page_content=html_content)]
    doc_transformed = bs_transformer.transform_documents(
        document, 
        tags_to_extract=["span", "table", "li", "d", "h1", "h2", "h3", "h4", "h5", "p"], 
        unwanted_tags=["a"]
    )[0]
    
    chunks = []
    # split the content into chunks of 1000 characters
    for i in range(0, len(doc_transformed.page_content), context_length):
        chunks.append(doc_transformed.page_content[i:i + context_length])

    return chunks

# Delete all blobs in the container
def delete_blobs():
    print(f'Deleting blobs in container ...')
    blobs = container_client.list_blobs()
    for blob in blobs:
        container_client.delete_blob(blob.name)
        print(f"Deleted blob: {blob.name}")

# Upload files to the container and delete local files
def upload_files(files, output_dir):
    delete_blobs()
    for file in files:
        print(f"Uploading {file}...")
        blob_client = container_client.get_blob_client(file)
        with open(os.path.join(output_dir, file), 'rb') as f:
            blob_client.upload_blob(f)
        os.remove(os.path.join(output_dir, file))
        print(f"Removed local chunk: {file}")
        
def save_file(file_index, chunks):
    output_dir = './data_prep/embeddings'
    sub_index = 0
    for chunk in chunks:
        filename = str(file_index) + '_' + str(sub_index) + '.txt'
        with open(os.path.join(output_dir, filename), 'w+') as f:
            f.write(chunk)
            print(f"Saved file: {filename}")
        sub_index += 1

def main():
    data_path = './erasmus-bot/erasmus-site-parsed'
    output_dir = './data_prep/embeddings'
    os.makedirs(output_dir, exist_ok=True)
    
    filenames = [file for file in os.listdir(data_path) if file.endswith('.html')]
    count = 0
    # delete old files
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    for file in files:
        os.remove(os.path.join(output_dir, file))
    for item in filenames:
        file_path = os.path.join(data_path, item)
        cleaned_content = process_html_file(file_path)
        save_file(count, cleaned_content)
        count += 1
    
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    upload_files(files, output_dir)
    indexer_client.run_indexer(indexer_name)
    

if __name__ == '__main__':
    main()
