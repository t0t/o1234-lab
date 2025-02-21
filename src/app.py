import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from token_system import TokenSystem

# Obtener la ruta absoluta al directorio static
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__)
CORS(app)
token_system = TokenSystem()

@app.route('/tokens', methods=['POST'])
def add_token():
    data = request.get_json()
    token = data.get('token')
    category = data.get('category', 'custom')
    metadata = data.get('metadata', {})
    
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    token_system.add_token(token, category, metadata)
    return jsonify({'message': f'Token {token} added successfully'})

@app.route('/tokens/relationship', methods=['POST'])
def add_relationship():
    data = request.get_json()
    token1 = data.get('token1')
    token2 = data.get('token2')
    relationship_type = data.get('type')
    
    if not all([token1, token2, relationship_type]):
        return jsonify({'error': 'All fields are required'}), 400
    
    token_system.add_relationship(token1, token2, relationship_type)
    return jsonify({'message': 'Relationship added successfully'})

@app.route('/tokens/search', methods=['GET'])
def search_tokens():
    query = request.args.get('q')
    n_results = int(request.args.get('n', 5))
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    tokens = token_system.search_tokens(query, n_results)
    return jsonify({'tokens': tokens})

@app.route('/tokens/<token>', methods=['GET'])
def get_token_info(token):
    info = token_system.get_token_info(token)
    if not info:
        return jsonify({'error': 'Token not found'}), 404
    return jsonify(info)

@app.route('/tokenize', methods=['POST'])
def tokenize_text():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    tokens = token_system.tokenize_text(text)
    return jsonify({'tokens': tokens})

@app.route('/')
def index():
    return send_from_directory(static_dir, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(static_dir, 'favicon.ico')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)