import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from token_system import TokenSystem
from auth import token_required, authenticate_user, generate_token, ADMIN_USERNAME, ADMIN_PASSWORD
from middleware import init_limiter, validate_token_input, validate_relationship_input
from logger import log_action
from config import CORS_ALLOWED_ORIGINS

# Obtener la ruta absoluta al directorio static
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__)
# Configurar CORS con orígenes permitidos
CORS(app, resources={r"/*": {"origins": CORS_ALLOWED_ORIGINS}})

# Inicializar el rate limiter
limiter = init_limiter(app)

token_system = TokenSystem()

@app.route('/login', methods=['POST'])
@limiter.limit("20 per minute")  # Aumentado a 20 peticiones por minuto
def login():
    data = request.get_json()
    print("Datos recibidos:", data)  # Log para depuración
    username = data.get('username')
    password = data.get('password')
    
    print(f"Username: {username}, Password: {password}")  # Log para depuración
    print(f"Expected: {ADMIN_USERNAME}, {ADMIN_PASSWORD}")  # Log para depuración
    
    if not username or not password:
        log_action('login_error', details={'error': 'Missing credentials'})
        return jsonify({'error': 'Username and password are required'}), 400
        
    if authenticate_user(username, password):
        token = generate_token(username)
        log_action('login_success', user=username)
        return jsonify({'token': token})
    
    log_action('login_failed', details={'username': username})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/tokens', methods=['POST'])
@token_required
@limiter.limit("20 per minute")  # Aumentado a 20 peticiones por minuto
def add_token():
    data = request.get_json()
    errors = validate_token_input(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    token = data.get('token')
    category = data.get('category', 'custom')
    metadata = data.get('metadata', {})
    
    token_system.add_token(token, category, metadata)
    log_action('token_added', user=request.user, details={'token': token, 'category': category})
    return jsonify({'message': f'Token {token} added successfully'})

@app.route('/tokens/relationship', methods=['POST'])
@token_required
@limiter.limit("20 per minute")  # Aumentado a 20 peticiones por minuto
def add_relationship():
    data = request.get_json()
    errors = validate_relationship_input(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    token1 = data.get('token1')
    token2 = data.get('token2')
    relationship_type = data.get('type')
    
    token_system.add_relationship(token1, token2, relationship_type)
    log_action('relationship_added', user=request.user, 
              details={'token1': token1, 'token2': token2, 'type': relationship_type})
    return jsonify({'message': 'Relationship added successfully'})

@app.route('/tokens/search', methods=['GET'])
@token_required
@limiter.limit("20 per minute")  # Aumentado a 20 peticiones por minuto
def search_tokens():
    query = request.args.get('q')
    n_results = int(request.args.get('n', 5))
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    tokens = token_system.search_tokens(query, n_results)
    log_action('tokens_searched', user=request.user, details={'query': query, 'n_results': n_results})
    return jsonify({'tokens': tokens})

@app.route('/tokens/<token>', methods=['GET'])
@token_required
@limiter.limit("30 per minute")
def get_token_info(token):
    info = token_system.get_token_info(token)
    if not info:
        return jsonify({'error': 'Token not found'}), 404
    
    log_action('token_info_retrieved', user=request.user, details={'token': token})
    return jsonify(info)

@app.route('/tokenize', methods=['POST'])
@token_required
@limiter.limit("20 per minute")
def tokenize_text():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    if len(text) > 5000:  # Límite arbitrario para prevenir abuso
        return jsonify({'error': 'Text is too long'}), 400
    
    tokens = token_system.tokenize_text(text)
    log_action('text_tokenized', user=request.user, details={'text_length': len(text)})
    return jsonify({'tokens': tokens})

@app.route('/')
def index():
    return send_from_directory(static_dir, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(static_dir, 'favicon.ico')

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Has excedido el límite de peticiones (20 por minuto). Por favor, espera un momento antes de intentarlo de nuevo.',
        'retry_after': e.description
    }), 429

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)