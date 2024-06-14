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
