#!/bin/bash
# Exit on unset variables instead of continuing
set -eu

echo "🚀 Initializing EasyJournal Academic Submission System..."

# Function to log with timestamp
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors
handle_error() {
  log "❌ ERROR: $1"
  # Continue despite errors 
  return 0
}

# Install netcat if not present (for database connection checks)
if ! command -v nc &> /dev/null; then
  log "Installing netcat for database connection checks..."
  apt-get update && apt-get install -y netcat-openbsd && apt-get clean || handle_error "Failed to install netcat"
fi

# Handle database connection
log "📊 Checking database connection..."

# Use environment variables directly if available
if [ -n "${DB_HOST:-}" ]; then
  HOST="$DB_HOST"
  PORT="${DB_PORT:-5432}"
  log "Using provided DB_HOST: $HOST and port: $PORT"
# Extract from DATABASE_URL if DB_HOST isn't set
elif [ -n "${DATABASE_URL:-}" ] && [[ "${DATABASE_URL:-}" == postgresql://* || "${DATABASE_URL:-}" == mysql://* ]]; then
  log "Extracting database info from DATABASE_URL: $DATABASE_URL"
  if [[ "${DATABASE_URL:-}" == postgresql://* ]]; then
    HOST=$(echo "$DATABASE_URL" | sed -E 's/.*\@([^:]+):[0-9]+\/.*/\1/')
    PORT=$(echo "$DATABASE_URL" | sed -E 's/.*\@[^:]+:([0-9]+)\/.*/\1/')
    PORT=${PORT:-5432}
    log "PostgreSQL host: $HOST, port: $PORT"
  elif [[ "${DATABASE_URL:-}" == mysql://* ]]; then
    HOST=$(echo "$DATABASE_URL" | sed -E 's/.*\@([^:]+):[0-9]+\/.*/\1/')
    PORT=$(echo "$DATABASE_URL" | sed -E 's/.*\@[^:]+:([0-9]+)\/.*/\1/')
    PORT=${PORT:-3306}
    log "MySQL host: $HOST, port: $PORT"
  fi
else
  log "⚠️ No database connection information found in environment"
  HOST=""
fi

# Wait for DB to become available if host is defined
if [ -n "${HOST:-}" ]; then
  MAX_RETRIES=45
  RETRY_INTERVAL=2
  log "🔄 Waiting for database at $HOST:$PORT..."
  
  for ((i=1; i<=MAX_RETRIES; i++)); do
    if nc -z -w5 "$HOST" "$PORT" 2>/dev/null; then
      log "✅ Database is up and running!"
      break
    fi
    log "⏳ Waiting for database connection... (attempt $i/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
    
    if [ $i -eq $MAX_RETRIES ]; then
      log "⚠️ Warning: Could not connect to database after $MAX_RETRIES attempts"
      log "⚠️ The application will still try to start, but may fail if database is required"
    fi
  done
fi

# Create and ensure permissions on necessary directories
log "📁 Setting up directory structure..."
mkdir -p /app/uploads /app/uploads/demo /app/data || handle_error "Failed to create directories"
chmod -R 777 /app/uploads /app/data || handle_error "Failed to set directory permissions"

# If .env doesn't exist, create from example
if [ ! -f "/app/.env" ] && [ -f "/app/.env.example" ]; then
  log "📝 Creating .env file from example..."
  cp /app/.env.example /app/.env || handle_error "Failed to create .env file"
  log "⚠️ Please update .env file with your configuration."
fi

# Create demo files for uploads if DEMO_MODE is enabled
if [ "${DEMO_MODE:-false}" = "True" ] || [ "${DEMO_MODE:-false}" = "true" ]; then
  log "🧪 DEMO MODE enabled - Creating sample files..."
  
  DEMO_FILE1="/app/uploads/demo_paper1.pdf"
  DEMO_FILE2="/app/uploads/demo_paper2.pdf"
  DEMO_FILE3="/app/uploads/demo_paper3.pdf"
  
  if [ ! -f "$DEMO_FILE1" ]; then
    echo "Sample paper 1" > "$DEMO_FILE1" || handle_error "Failed to create demo file 1"
    echo "Sample paper 2" > "$DEMO_FILE2" || handle_error "Failed to create demo file 2"
    echo "Sample paper 3" > "$DEMO_FILE3" || handle_error "Failed to create demo file 3"
    chmod 644 "$DEMO_FILE1" "$DEMO_FILE2" "$DEMO_FILE3" || handle_error "Failed to set demo file permissions"
    log "📄 Demo files created successfully"
  else
    log "📄 Demo files already exist"
  fi
fi

# Execute the command
log "🚀 Starting application: $*"
exec "$@"