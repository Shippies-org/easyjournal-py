# EasyJournal - Installation Guide

This document provides instructions for installing and setting up the EasyJournal Academic Journal Submission System.

## Installation Options

EasyJournal offers two installation methods:
1. **Docker**: Recommended for production and easy deployment
2. **Manual Installation**: For development or customization

## Option 1: Docker Installation (Recommended)

### Prerequisites
- Docker and Docker Compose
- Git (optional)

### Quick Start with Docker

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Shippies-org/easyjournal-py.git
   cd easyjournal-py
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file to set your desired configuration. The default values work for most users.

3. **Build and Start the Application**
   ```bash
   docker-compose up -d
   ```

4. **Access the Application**
   The application will be available at http://localhost:5000

### Docker Notes
- Default admin login: admin@example.com / adminpassword
- Demo mode is enabled by default with pre-populated data
- PostgreSQL data is stored in a Docker volume and persists between container restarts
- You can view logs with `docker-compose logs -f app`
- To stop: `docker-compose down`

## Option 2: Manual Installation

### Prerequisites
- Python 3.10 or higher
- SQLite (default) or PostgreSQL
- Git (optional)

### Step-by-Step Manual Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Shippies-org/easyjournal-py.git
   cd easyjournal-py
   ```

2. **Install Dependencies**
   ```bash
   bash setup/install_dependencies.sh
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file to set your configuration.
   - For SQLite (default): `DATABASE_URL=sqlite:///instance/journal.db`
   - For PostgreSQL: `DATABASE_URL=postgresql://user:password@localhost:5432/journal_db`

4. **Initialize Database**
   For SQLite (this happens automatically on first run):
   ```bash
   mkdir -p instance
   touch instance/journal.db
   ```

   For PostgreSQL, create a database and user first:
   ```bash
   psql -U postgres
   CREATE DATABASE journal_db;
   CREATE USER journal_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE journal_db TO journal_user;
   \q
   ```

5. **Start the Application**
   ```bash
   python main.py
   ```
   The application will be available at http://localhost:5000

## Advanced Configuration

### Demo Mode
Demo mode creates test accounts and sample data. It's enabled by default.
- To disable: Set `DEMO_MODE=False` in `.env`

### Production Deployment
For production, configure these settings in `.env`:
- `SESSION_SECRET`: Set a strong, random secret key
- `DEMO_MODE`: Set to `False`
- `FLASK_DEBUG`: Set to `0`

Use Gunicorn with multiple workers:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

For HTTPS, use a reverse proxy like Nginx.

### Database Selection
- **SQLite**: Best for development or small deployments
- **PostgreSQL**: Recommended for production use
  
The Docker setup uses PostgreSQL by default.

## Plugins & Customization
- Place plugins in the `plugins` directory
- Each plugin should have a `plugin.py` with a `register_plugin()` function
- See the included welcome plugin for an example

## Troubleshooting

### Docker Issues
- Ensure Docker and Docker Compose are properly installed
- Verify ports 5000 and 5432 are not in use by other applications
- Check container logs: `docker-compose logs app` or `docker-compose logs db`
- For permission issues: `sudo chmod -R 777 uploads` in the project directory

### Database Connection Issues
- Verify credentials in `.env` match your database setup
- Check PostgreSQL is running and accessible
- For SQLite, ensure the instance directory exists and is writable

### Permission Problems
- Make sure the uploads directory is writable: `chmod -R 777 uploads`
- For Docker, ensure the user has permission to access Docker volumes

## Support & Contributions
- Report issues on GitHub
- Contributions welcome via pull requests
- Documentation available at easyjournal.org