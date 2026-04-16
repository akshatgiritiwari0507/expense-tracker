import os
from datetime import timedelta


class Config:
    """Configuration class for Flask application"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    db_url = os.environ.get("DATABASE_URL")

    # Render postgres compatibility fix
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///expense.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    WTF_CSRF_TIME_LIMIT = None

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024