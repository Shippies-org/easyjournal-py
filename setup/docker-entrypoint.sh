#!/bin/bash
set -e

# Wait for the database to be ready if using PostgreSQL or MySQL
if [[ $DATABASE_URL == postgresql://* || $DATABASE_URL == mysql://* ]]; then
  echo "Waiting for database to be ready..."
  # Extract host and port from DATABASE_URL
  if [[ $DATABASE_URL == postgresql://* ]]; then
    DB_HOST=$(echo $DATABASE_URL | awk -F[@//] '{print $4}' | awk -F[:] '{print $1}')
    DB_PORT=$(echo $DATABASE_URL | awk -F[@//] '{print $4}' | awk -F[:] '{print $2}' | awk -F[/] '{print $1}')
    DB_PORT=${DB_PORT:-5432}
    echo "PostgreSQL host: $DB_HOST, port: $DB_PORT"
  elif [[ $DATABASE_URL == mysql://* ]]; then
    DB_HOST=$(echo $DATABASE_URL | awk -F[@//] '{print $4}' | awk -F[:] '{print $1}')
    DB_PORT=$(echo $DATABASE_URL | awk -F[@//] '{print $4}' | awk -F[:] '{print $2}' | awk -F[/] '{print $1}')
    DB_PORT=${DB_PORT:-3306}
    echo "MySQL host: $DB_HOST, port: $DB_PORT"
  fi

  # Wait for DB to become available
  until nc -z -v -w30 $DB_HOST $DB_PORT; do
    echo "Waiting for database connection..."
    sleep 2
  done
  
  echo "Database is up and running!"
fi

# Create necessary directories
mkdir -p uploads/demo data
chmod -R 777 uploads

# If .env doesn't exist, create from example
if [ ! -f ".env" ]; then
  echo "Creating .env file from example..."
  cp .env.example .env
  echo "Please update .env file with your configuration."
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

# Execute the command
echo "Starting application: $@"
exec "$@"