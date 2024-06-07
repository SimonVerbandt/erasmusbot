import os
import openai 
import numpy as np
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def load_filenames(data_path):
    return [f for f in os.listdir(data_path) if f.endswith('.html')]

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model='text-embedding-ada-002'
    )
    return response['data'][0]['embedding']

def save_vector(vector, filename, output_dir):
    vector_filename = os.path.splitext(filename)[0] + '_vector.npy'
    np.save(os.path.join(output_dir, vector_filename), vector)


def main():
    data_path = './erasmus-bot/erasmus-site-parsed'
    output_dir = './chunks/data'
    os.makedirs(output_dir, exist_ok=True)
    filenames = load_filenames(data_path)
    for item in filenames:
        with open(os.path.join(data_path, item), 'r', encoding='utf-8') as f:
            html = f.read()
            text = extract_text(html)
            vector = generate_embedding(text)
            save_vector(vector, item, output_dir)
             
if __name__ == '__main__':
    main()