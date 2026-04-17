from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

csrf = CSRFProtect()

def create_app(config_name='development'):
    """Application factory pattern"""
    # Get the parent directory of the app folder (project root)
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Import config
    from app.config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register routes
    from app.routes import main
    app.register_blueprint(main)
    
    # Add custom Jinja filters
    @app.template_filter('dateformat')
    def dateformat(date, format='%d/%m/%Y'):
        if isinstance(date, str):
            from datetime import datetime
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except:
                return date
        return date.strftime(format)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
