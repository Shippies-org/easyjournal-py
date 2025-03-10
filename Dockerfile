FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DEMO_MODE=True

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libpq-dev \
        sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p uploads uploads/demo data \
    && chmod -R 777 uploads

# Create volume for persistent data
VOLUME ["/app/uploads", "/app/data"]

# Expose port
EXPOSE 5000

# Set up wait-for-it script to ensure database is available
COPY setup/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]