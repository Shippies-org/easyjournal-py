#!/bin/bash
set -e

# Install netcat if not present
if ! command -v nc &> /dev/null; then
  echo "Installing netcat for database connection checks..."
  apt-get update && apt-get install -y netcat-openbsd && apt-get clean
fi

# Handle database connection
echo "Checking database connection..."

# Use environment variables directly if available
if [ -n "$DB_HOST" ]; then
  HOST=$DB_HOST
  PORT=${DB_PORT:-5432}
  echo "Using provided DB_HOST: $HOST and port: $PORT"
# Extract from DATABASE_URL if those aren't set
elif [[ $DATABASE_URL == postgresql://* || $DATABASE_URL == mysql://* ]]; then
  echo "Extracting database info from DATABASE_URL: $DATABASE_URL"
  if [[ $DATABASE_URL == postgresql://* ]]; then
    HOST=$(echo $DATABASE_URL | sed -E 's/.*\@([^:]+):[0-9]+\/.*/\1/')
    PORT=$(echo $DATABASE_URL | sed -E 's/.*\@[^:]+:([0-9]+)\/.*/\1/')
    PORT=${PORT:-5432}
    echo "PostgreSQL host: $HOST, port: $PORT"
  elif [[ $DATABASE_URL == mysql://* ]]; then
    HOST=$(echo $DATABASE_URL | sed -E 's/.*\@([^:]+):[0-9]+\/.*/\1/')
    PORT=$(echo $DATABASE_URL | sed -E 's/.*\@[^:]+:([0-9]+)\/.*/\1/')
    PORT=${PORT:-3306}
    echo "MySQL host: $HOST, port: $PORT"
  fi
else
  echo "No database connection information found in environment"
  HOST=""
fi

# Wait for DB to become available if host is defined
if [ -n "$HOST" ]; then
  echo "Waiting for database at $HOST:$PORT..."
  for i in {1..30}; do
    if nc -z -w5 $HOST $PORT; then
      echo "✓ Database is up and running!"
      break
    fi
    echo "Waiting for database connection... (attempt $i/30)"
    sleep 2
    if [ $i -eq 30 ]; then
      echo "⚠️ Warning: Could not connect to database after 30 attempts"
      echo "⚠️ The application will still try to start, but may fail if database is required"
    fi
  done
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