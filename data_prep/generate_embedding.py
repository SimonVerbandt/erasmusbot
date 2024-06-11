from dotenv import load_dotenv
import os
from openai import AzureOpenAI

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
ENDPOINT = os.getenv('AZURE_OPENAI_API_ENDPOINT')
API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME')

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    azure_deployment='erasmusbot-embedding',
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
)

# Generate embedding for text
def generate_embedding(text):
    response = openai_client.embeddings.create(
        model=MODEL_NAME,
        input=text
    )
    return response.data[0].embedding
