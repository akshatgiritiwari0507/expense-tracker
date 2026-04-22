#!/usr/bin/env python
"""
Migration script to add Category table and default categories
"""
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category

def migrate_categories():
    """Create Category table and add default categories for existing users"""
    app = create_app()
    
    with app.app_context():
        # Create the Category table
        Category.__table__.create(db.engine, checkfirst=True)
        print("Category table created successfully!")
        
        # Add default categories for existing users
        users = User.query.all()
        
        for user in users:
            # Check if user already has categories
            existing_categories = Category.query.filter_by(user_id=user.id).count()
            
            if existing_categories == 0:
                # Add default categories
                for category_data in Category.DEFAULT_CATEGORIES:
                    category = Category(
                        name=category_data['name'],
                        icon=category_data['icon'],
                        color=category_data['color'],
                        user_id=user.id
                    )
                    db.session.add(category)
                
                print(f"Added default categories for user: {user.name}")
        
        try:
            db.session.commit()
            print("Migration completed successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {e}")
            return False
    
    return True

if __name__ == '__main__':
    migrate_categories()
