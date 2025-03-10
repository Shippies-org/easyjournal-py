FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app:${PATH}"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        libpq-dev \
        sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY setup/install_dependencies.sh .
RUN bash install_dependencies.sh

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p uploads \
    && chmod 777 uploads

# Create volume for persistent data
VOLUME ["/app/uploads", "/app/data"]

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]