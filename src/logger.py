import logging
from pythonjsonlogger import jsonlogger
from config import LOG_LEVEL, LOG_FORMAT

# Configurar el logger
logger = logging.getLogger('token_system')
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(LOG_FORMAT)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(LOG_LEVEL)

def log_action(action_type, user=None, details=None):
    """
    Registra una acción en el sistema
    
    Args:
        action_type (str): Tipo de acción (e.g., 'token_added', 'login_attempt')
        user (str, optional): Usuario que realiza la acción
        details (dict, optional): Detalles adicionales de la acción
    """
    log_data = {
        'action': action_type,
        'user': user or 'anonymous',
        'details': details or {}
    }
    
    logger.info('Action logged', extra=log_data)
