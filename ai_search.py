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
EMB_NAME = os.getenv('EMBEDDING_MODEL_NAME')

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
def search_documents(query):
    embedding = model_client.embeddings.create(input=query, model=EMB_NAME).data[0].embedding
    vector_query = VectorizedQuery(vector=embedding, fields="content_vector")
    results = search_client.search(search_text=query, vector_queries=[vector_query])
    documents = []
    for result in results:
    #     print(f"Raw result: {result}")
            documents.append({
                "id": result['id'],
                "content": result['content'],
                "score": result['@search.score']
            })
    context = ""
    for document in documents:
        if len(context) + len(document['content']) > 30000:
            break
        context += document['content'] + "\n"
    return context

history = [
            {"role": "system", "content": "You are a helpful assistant made for Erasmushogeschool Brussel. You can only answer about the school or its services."}]

def generate_response(query):
    context = search_documents(query)
    history.append({"role": "user", "content": query})
    response = model_client.chat.completions.create(
        model=MODEL_NAME,
        messages=history + [{"role": "system", "content": "Based on this context answer the user's question. If the answer is not in the context, refuse to answer: " + context}],
        max_tokens=1000
    )
    history.append({"role": "assistant", "content": response.choices[0].message.content})
    return history

#history = generate_response("Do students ‘Toegepaste Informatica’ have business related courses?")
#for entry in history:
#    print(f"{entry['role']}: {entry['content']}")