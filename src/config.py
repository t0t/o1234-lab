import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret-key-change-in-production')
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora

# Configuración Rate Limiting
RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')
DEFAULT_RATE_LIMIT = "100 per day"
STRICT_RATE_LIMIT = "3 per minute"

# Configuración CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8080').split(',')

# Configuración Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configuración ChromaDB
CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')

# Configuración Admin
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-password')
