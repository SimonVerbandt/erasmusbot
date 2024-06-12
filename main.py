from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import webbrowser
import threading

from ai_search import generate_response

app = Flask(__name__, static_folder='') 
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.json.get('question')
        print(f"User input: {user_input}")
                
        response_text = generate_response(user_input)
        print(f"Response: {response_text}")
        
        return jsonify(response_text)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html') 

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Start Flask server in a separate thread
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    # Open the default web browser
    open_browser()
