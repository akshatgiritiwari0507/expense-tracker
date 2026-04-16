"""
WSGI entry point for Basic Expense Tracker application.

This file serves as the main entry point for both development and production.
It creates the Flask app instance using the application factory pattern.

Usage:
- Development: python run.py
- Production: gunicorn run:app
"""

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run in development mode
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
