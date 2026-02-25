import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_URI = os.environ.get('DATABASE_URI', f'sqlite:///{BASE_DIR}/app.db')

# Secret key for JWT tokens
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Token expiration (in seconds)
TOKEN_EXPIRATION = 86400  # 24 hours

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Max content length (16MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024