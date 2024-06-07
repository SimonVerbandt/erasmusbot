import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
ENDPOINT = os.getenv('AZURE_OPENAI_API_ENDPOINT')
API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME')
STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = 'eramusbot-container'

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Get parsed HTML files
def load_filenames(data_path):
    return [f for f in os.listdir(data_path) if f.endswith('.html')]

# Extract text from HTML
def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Generate embedding for chunk
def generate_embedding(text):
    url = f"{ENDPOINT}/openai/deployments/{MODEL_NAME}/embeddings?api-version={API_VERSION}"
    headers = {
        'Content-Type': 'application/json',
        'api-key': API_KEY
    }
    data = {
        "input": text
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['data'][0]['embedding']

# Chunk HTML file text into smaller pieces
def chunk_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Save generated chunk embedding to JSON file
def save_vector(vector, filename, chunk_index, output_dir):
    vector_filename = os.path.splitext(filename)[0] + f'_vector_{chunk_index}.json'
    data = {
        'id': f'{os.path.splitext(filename)[0]}_{chunk_index}',
        'content_vector': vector
    }
    with open(os.path.join(output_dir, vector_filename), 'w') as f:
        json.dump(data, f)

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
        print(f"Deleted local file: {file}")

def main():
    data_path = './erasmus-bot/erasmus-site-parsed'
    output_dir = './chunks/data'
    os.makedirs(output_dir, exist_ok=True)
    
    filenames = load_filenames(data_path)
    for item in filenames:
        with open(os.path.join(data_path, item), 'r', encoding='utf-8') as f:
            html = f.read()
            text = extract_text(html)
            chunks = chunk_text(text)
            for index, chunk in enumerate(chunks):
                vector = generate_embedding(chunk)
                save_vector(vector, item, index, output_dir)
    
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    upload_files(files, output_dir)

if __name__ == '__main__':
    main()
