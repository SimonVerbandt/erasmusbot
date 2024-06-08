import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
ENDPOINT = os.getenv('AZURE_OPENAI_API_ENDPOINT')
API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
SEARCH_ENDPOINT = os.getenv('AZURE_SEARCH_ENDPOINT')
SEARCH_API_KEY = os.getenv('AZURE_SEARCH_API_KEY')
SEARCH_INDEX_NAME = os.getenv('AZURE_SEARCH_INDEX_NAME')
MODEL_NAME = os.getenv('CHAT_MODEL_NAME')

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT, 
    index_name=SEARCH_INDEX_NAME, 
    credential=AzureKeyCredential(SEARCH_API_KEY))
model_client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)

def search_documents(query_vector):
    vector_query = {
            "kind": "vector",
            "vector": query_vector,
            "fields": "content_vector",
            "k": 5
    }
    results = search_client.search(vector_queries=[vector_query])
    documents = [result for result in results if result['@search.score'] > 0.1]
    return documents

def generate_response(prompt):
    response = model_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

def get_document_vector(document_id):
    result = search_client.get_document(document_id)
    return result['content_vector']
