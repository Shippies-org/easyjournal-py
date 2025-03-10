#!/bin/bash
# Install dependencies for Academic Journal Submission System

# Ensure script is run with bash
if [ -z "$BASH_VERSION" ]; then
    echo "This script requires bash. Please run with: bash install_dependencies.sh"
    exit 1
fi

echo "Installing Python dependencies..."
pip install flask==2.3.3
pip install flask-login==0.6.2
pip install flask-sqlalchemy==3.1.1
pip install flask-wtf==1.2.1
pip install email-validator==2.1.0
pip install gunicorn==23.0.0
pip install python-dotenv==1.0.1
pip install werkzeug==2.3.7
pip install sqlalchemy==2.0.23
pip install psycopg2-binary==2.9.9  # For PostgreSQL support
pip install pymysql==1.1.0  # For MySQL support

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads

# Make uploads directory writable
chmod 777 uploads

echo "Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration settings."
fi

echo "Installation complete!"
echo "Next steps:"
echo "1. Configure your .env file"
echo "2. Initialize the database: sqlite3 journal.db < setup/database_schema.sql"
echo "3. Create an admin user: python setup/create_admin.py"
echo "4. Start the application: python main.py"