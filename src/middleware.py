from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import RATE_LIMIT_STORAGE_URL, DEFAULT_RATE_LIMIT, STRICT_RATE_LIMIT
from logger import log_action

def init_limiter(app):
    """Inicializa el rate limiter."""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=RATE_LIMIT_STORAGE_URL,
        default_limits=[DEFAULT_RATE_LIMIT],
        strategy="fixed-window"
    )
    return limiter

def validate_token_input(token_data):
    """Valida los datos de entrada para tokens."""
    errors = []
    
    # Validar token
    if not token_data.get('token'):
        errors.append('Token is required')
    elif len(token_data['token']) > 100:  # límite arbitrario
        errors.append('Token is too long')
    
    # Validar categoría
    category = token_data.get('category', 'custom')
    if len(category) > 50:  # límite arbitrario
        errors.append('Category name is too long')
    
    # Validar metadatos
    metadata = token_data.get('metadata', {})
    if not isinstance(metadata, dict):
        errors.append('Metadata must be a dictionary')
    elif len(str(metadata)) > 1000:  # límite arbitrario
        errors.append('Metadata is too large')
    
    if errors:
        log_action('validation_error', details={'errors': errors})
        
    return errors

def validate_relationship_input(relationship_data):
    """Valida los datos de entrada para relaciones."""
    errors = []
    
    # Validar tokens
    if not relationship_data.get('token1'):
        errors.append('First token is required')
    if not relationship_data.get('token2'):
        errors.append('Second token is required')
    
    # Validar tipo de relación
    relationship_type = relationship_data.get('type')
    if not relationship_type:
        errors.append('Relationship type is required')
    elif len(relationship_type) > 50:  # límite arbitrario
        errors.append('Relationship type is too long')
    
    if errors:
        log_action('validation_error', details={'errors': errors})
        
    return errors
