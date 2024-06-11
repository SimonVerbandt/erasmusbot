import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery

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
    credential=AzureKeyCredential(SEARCH_API_KEY)
)

model_client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)

# Perform hybrid search
def search_documents(query, query_vector):
    vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=3, fields='content_vector')
    results = search_client.search(search_text=query, vector_queries=[vector_query])
    documents = []
    for result in results:
        documents.append({
            "id": result['id'],
            "content_text": result['content_text'],
            "score": result['@search.score']
        })
    return documents

# TODO: Implement response generation
# def generate_response(prompt):
#     response = model_client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=200
#     )
#     return response.choices[0].message.content
