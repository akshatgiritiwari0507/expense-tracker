import os
from datetime import timedelta

class Config:
    """Configuration class for Flask application"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Use DATABASE_URL if available (for production/PostgreSQL), otherwise use SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'expense.db')
    
    # Disable SQLAlchemy modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # CSRF configuration
    WTF_CSRF_TIME_LIMIT = None
    
    # Upload configuration (if needed in future)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
