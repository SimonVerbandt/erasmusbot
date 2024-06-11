from flask import Flask, request, jsonify
from flask_cors import CORS
from data_prep.generate_embedding import generate_embedding
from search.ai_search import generate_response, search_documents

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.json.get('question')
        print(f"User input: {user_input}")
        
        query_vector = generate_embedding(user_input)
        
        documents = search_documents(user_input, query_vector)
        print(f"Documents found: {documents}")
        
        context = '\n'.join([doc['content_text'] for doc in documents if 'content_text' in doc])
        print(f"Context: {context}")
        
        response_text = generate_response(f"Context: {context}\nQuestion: {user_input}")
        print(f"Response: {response_text}")
        
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
