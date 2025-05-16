# Flask application configuration
import os

# MongoDB configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'gromo')

# API configuration
API_HOST = os.environ.get('API_HOST', '0.0.0.0')
API_PORT = int(os.environ.get('API_PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# CORS settings
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Maximum file upload size (in bytes)
MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB

# Rate limiting
RATE_LIMIT = os.environ.get('RATE_LIMIT', '100 per minute')