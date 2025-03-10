# Academic Journal Submission System - Installation Guide

This document provides instructions for installing and setting up the Academic Journal Submission System.

## Prerequisites

- Python 3.7 or higher
- SQLite3 (default) or PostgreSQL/MySQL (optional)
- PHP 7.4 or higher (optional, for PHP plugins)

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/academic-journal-system.git
cd academic-journal-system
```

## 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configuration

Copy the example environment file and modify it as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to configure the application settings:

- `APP_ENV`: Set to `production` for production environments
- `SECRET_KEY`: Change to a secure random string for production
- `DEMO_MODE`: Set to `False` in production
- `DB_TYPE`: Choose your database type (`sqlite`, `postgresql`, or `mysql`)
- Configure database connection settings if using PostgreSQL or MySQL
- Configure email settings for notifications

## 4. Database Setup

### SQLite (Default)

For SQLite, the system will create the database file automatically. To initialize the schema:

```bash
sqlite3 journal.db < setup/database_schema.sql
```

### PostgreSQL

For PostgreSQL, first create a database and user:

```bash
psql -U postgres
CREATE DATABASE journal;
CREATE USER journal_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE journal TO journal_user;
\q

# Then import the schema
psql -U journal_user -d journal -f setup/database_schema.sql
```

## 5. Create Admin User

```bash
python setup/create_admin.py
```

You'll be prompted to enter an admin name, email, and password. Alternatively, you can provide these as command-line arguments:

```bash
python setup/create_admin.py --name "Admin User" --email "admin@example.com" --password "secure_password"
```

## 6. (Optional) Seed Demo Data

For development or testing environments, you can seed the database with sample data:

```bash
python setup/seed_demo_data.py
```

To reset the database before seeding:

```bash
python setup/seed_demo_data.py --reset
```

## 7. Start the Application

### Development

```bash
python main.py
```

The application will be available at http://localhost:5000

### Production

For production deployment, we recommend using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

Use a reverse proxy like Nginx or Apache to handle HTTPS and static files.

## 8. (Optional) Set Up Plugins

Place PHP or Python plugins in the `plugins` directory following the structure outlined in `plugins/README.md`.

## Troubleshooting

### Database Connection Issues

- Verify database connection settings in `.env`
- Check database user permissions
- For PostgreSQL or MySQL, verify the database server is running

### Application Startup Errors

- Check Python version (`python --version`)
- Verify all dependencies are installed (`pip list`)
- Check log files for error messages

### Permission Issues

- Ensure the upload directory is writable by the application
- Check file permissions for the database file

## Upgrading

To upgrade to a new version:

1. Back up your database and configuration
2. Pull the latest code
3. Update dependencies: `pip install -r requirements.txt`
4. Run database migrations if provided
5. Restart the application