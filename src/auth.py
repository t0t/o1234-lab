import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta
import bcrypt
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, ADMIN_USERNAME, ADMIN_PASSWORD
from logger import log_action

def generate_token(username):
    """Genera un token JWT para el usuario."""
    expiration = datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)
    token = jwt.encode(
        {'user': username, 'exp': expiration},
        JWT_SECRET_KEY,
        algorithm='HS256'
    )
    return token

def verify_password(password, hashed):
    """Verifica si la contraseña coincide con el hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def hash_password(password):
    """Genera un hash de la contraseña."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def token_required(f):
    """Decorador para proteger rutas que requieren autenticación."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            log_action('auth_error', details={'error': 'Token missing'})
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = token.split('Bearer ')[1]
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            request.user = data['user']
        except Exception as e:
            log_action('auth_error', details={'error': str(e)})
            return jsonify({'error': 'Token is invalid'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

def authenticate_user(username, password):
    """Autentica un usuario."""
    if username != ADMIN_USERNAME:
        return False
    
    return password == ADMIN_PASSWORD
