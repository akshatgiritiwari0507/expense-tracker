from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Category(db.Model):
    """Category model for custom expense categories"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50))  # Font Awesome icons
    color = db.Column(db.String(7))  # Hex color codes
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Default categories for all users
    DEFAULT_CATEGORIES = [
        {'name': 'Food', 'icon': 'fa-utensils', 'color': '#FF6B6B'},
        {'name': 'Travel', 'icon': 'fa-plane', 'color': '#4ECDC4'},
        {'name': 'Shopping', 'icon': 'fa-shopping-cart', 'color': '#45B7D1'},
        {'name': 'Bills', 'icon': 'fa-file-invoice-dollar', 'color': '#96CEB4'},
        {'name': 'Entertainment', 'icon': 'fa-film', 'color': '#FFEAA7'},
        {'name': 'Others', 'icon': 'fa-ellipsis-h', 'color': '#DDA0DD'}
    ]
    
    def to_dict(self):
        """Convert category to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Expense(db.Model):
    """Expense model for tracking user expenses"""
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Categories (hardcoded as per requirements)
    CATEGORIES = [
        'Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Others'
    ]
    
    def __repr__(self):
        return f'<Expense {self.amount} - {self.category}>'
    
    def to_dict(self):
        """Convert expense to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Income(db.Model):
    """Income model for tracking user income"""
    __tablename__ = 'income'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Income sources (hardcoded)
    SOURCES = [
        'Salary', 'Business', 'Investment', 'Freelance', 'Others'
    ]
    
    def __repr__(self):
        return f'<Income {self.amount} - {self.source}>'
