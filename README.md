# ErasmusBot

ErasmusBot is a project designed to answer questions about Erasmushogeschool Brussel.

## Installation
1. Clone this repo.
2. Navigate to the project directory:
    ```bash
    cd erasmusbot
    ```
3. Set up the virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
## Create a .env file
In the project root, create a .env file with the following values
```bash
AZURE_OPENAI_API_KEY=8d6dabf01c1e4c0a9545ed1638bd413d
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=blobdbsimon;AccountKey=66Gjrg5TwEC2E4mM1acIJ3tGPF5+nN8WTRJBUy93csgBSfUbxrD0KVy2Hi3XWpmCkTD3tnlvLyab+AStToMjGg==;EndpointSuffix=core.windows.net
AZURE_OPENAI_API_ENDPOINT=https://erasmusbot-simon.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-01
EMBEDDING_MODEL_NAME="erasmusbot-embedding"
CHAT_MODEL_NAME="erasmusbotgpt4"
AZURE_SEARCH_ENDPOINT=https://aisearchsimon.search.windows.net
AZURE_SEARCH_API_KEY=tO2ds3JyF9bF1bPCID3WCvJD2xFxObiXtRV8A7dbDgAzSeDyO9ze
AZURE_SEARCH_INDEX_NAME=erasmusbot
```

## How to Run the Code

### Set Up the Virtual Environment
In the root directory of this repository, open a terminal and activate the virtual environment by running:
```bash
source venv/bin/activate
```

### Prepare data
In the project root, run:
```bash
python3 -m data_prep.chunks
```

### Run the app
In the project root, run:
```bash
python3 -m main
```
