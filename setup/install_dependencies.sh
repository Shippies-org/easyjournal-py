#!/bin/bash
# Install dependencies for Academic Journal Submission System

# Ensure script is run with bash
if [ -z "$BASH_VERSION" ]; then
    echo "This script requires bash. Please run with: bash install_dependencies.sh"
    exit 1
fi

echo "Installing Python dependencies..."
pip install --no-cache-dir flask==2.3.3
pip install --no-cache-dir flask-login==0.6.2
pip install --no-cache-dir flask-sqlalchemy==3.1.1
pip install --no-cache-dir flask-wtf==1.2.1
pip install --no-cache-dir email-validator==2.1.0
pip install --no-cache-dir gunicorn==23.0.0
pip install --no-cache-dir python-dotenv==1.0.1
pip install --no-cache-dir werkzeug==2.3.7
pip install --no-cache-dir sqlalchemy==2.0.23
pip install --no-cache-dir psycopg2-binary==2.9.9
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir markupsafe==2.1.3

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads uploads/demo data

# Make directories writable
chmod -R 777 uploads

echo "Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration settings."
fi

# Create demo files for uploads
DEMO_FILE1=uploads/demo_paper1.pdf
DEMO_FILE2=uploads/demo_paper2.pdf
DEMO_FILE3=uploads/demo_paper3.pdf

if [ ! -f "$DEMO_FILE1" ]; then
    echo "Creating demo files..."
    echo "Sample paper 1" > $DEMO_FILE1
    echo "Sample paper 2" > $DEMO_FILE2
    echo "Sample paper 3" > $DEMO_FILE3
    chmod 644 $DEMO_FILE1 $DEMO_FILE2 $DEMO_FILE3
fi

echo "Installation complete!"
echo "Next steps:"
echo "1. Configure your .env file"
echo "2. Start the application: python main.py"
echo ""
echo "For Docker deployment:"
echo "1. Build and start containers: docker-compose up -d"
echo "2. Access the application at: http://localhost:5000"