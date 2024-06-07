import os
import openai 
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

def save_text(text, filename, output_dir):
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    data_path = './chunks/erasmus-bot/erasmus-site-parsed'
    output_dir = './chunks/data'
    os.makedirs(output_dir, exist_ok=True)
    filenames = load_filenames(data_path)
    for item in filenames:
        with open(os.path.join(data_path, item), 'r', encoding='utf-8') as f:
            html = f.read()
            text = extract_text(html)
            text_filename = os.path.splitext(item)[0] + '.txt'
            save_text(text, text_filename, output_dir)
             
if __name__ == '__main__':
    main()