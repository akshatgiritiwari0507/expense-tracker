#!/bin/bash
# Render deployment script for database migrations

echo "Starting database migration..."

# Run the migration script
python migrate_categories.py

echo "Migration completed successfully!"

# Start the application
python run.py
