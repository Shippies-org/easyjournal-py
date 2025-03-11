# EasyJournal - Troubleshooting Guide

This document provides solutions to common issues that may occur when running EasyJournal.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Database Problems](#database-problems)
3. [Authentication Issues](#authentication-issues)
4. [File Upload Issues](#file-upload-issues)
5. [Email Configuration Problems](#email-configuration-problems)
6. [Performance Issues](#performance-issues)
7. [Plugin Problems](#plugin-problems)
8. [Docker-Related Issues](#docker-related-issues)
9. [HTTPS and Certificate Issues](#https-and-certificate-issues)
10. [Common Error Messages](#common-error-messages)

## Installation Issues

### Python Version Compatibility

**Issue**: Application fails to start with Python version errors.

**Solution**:
- EasyJournal requires Python 3.10 or higher
- Check your Python version with `python --version`
- Install a compatible version if needed

### Dependency Installation Failures

**Issue**: `pip install` fails for some dependencies.

**Solutions**:
- Make sure you have necessary build tools:
  ```bash
  # Ubuntu/Debian
  apt-get install python3-dev build-essential libpq-dev
  
  # CentOS/RHEL
  yum install python3-devel gcc postgresql-devel
  
  # macOS
  xcode-select --install
  brew install postgresql
  ```
- Try creating a fresh virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Module Not Found Errors

**Issue**: `ModuleNotFoundError` when starting the application.

**Solutions**:
- Make sure you've installed all dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Check that you're running in the correct virtual environment
- For Docker, ensure the image is built correctly:
  ```bash
  docker-compose build --no-cache
  ```

## Database Problems

### Connection Errors

**Issue**: "Unable to connect to database" errors.

**Solutions**:
- Verify PostgreSQL is running:
  ```bash
  sudo systemctl status postgresql
  # or for Docker
  docker-compose ps
  ```
- Check connection string in `.env` file:
  ```
  DATABASE_URL=postgresql://user:password@host:port/dbname
  ```
- Ensure the database exists and is accessible:
  ```bash
  psql -U postgres -c "CREATE DATABASE journal_db;"
  psql -U postgres -c "CREATE USER journal_user WITH PASSWORD 'password';"
  psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE journal_db TO journal_user;"
  ```

### Migration Issues

**Issue**: Database tables not created or schema mismatch errors.

**Solutions**:
- For new installations, verify the database initialization:
  ```bash
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade
  ```
- For existing installations with schema changes:
  ```bash
  flask db stamp head  # Mark the current state
  flask db migrate -m "Update schema"
  flask db upgrade
  ```
- If migrations are broken, you may need to recreate the database (data loss warning):
  ```bash
  # Drop and recreate the database
  dropdb -U postgres journal_db
  createdb -U postgres journal_db
  # Then reinitialize
  flask db init
  flask db migrate
  flask db upgrade
  ```

### Foreign Key Violations

**Issue**: "Foreign key violation" errors when modifying data.

**Solutions**:
- Check relationships between related objects
- Ensure you're not deleting a parent record with existing children
- Look for missing or incorrect join conditions in queries
- Verify the database schema is correctly synchronized

## Authentication Issues

### Login Failures

**Issue**: Unable to log in with correct credentials.

**Solutions**:
- Reset the admin password:
  ```bash
  python setup/create_admin.py --name "Admin User" --email "admin@example.com" --password "new_password"
  ```
- Check if the user exists in the database:
  ```sql
  SELECT id, email, role FROM users WHERE email = 'user@example.com';
  ```
- Verify that sessions are being stored correctly (check browser cookies)

### Session Expiration

**Issue**: Users are frequently logged out or sessions expire quickly.

**Solutions**:
- Check the session configuration in `app.py`:
  ```python
  app.permanent_session_lifetime = timedelta(days=1)  # Increase as needed
  ```
- Ensure `SESSION_SECRET` is set in the environment
- Check for cookie issues in the browser (third-party cookies, etc.)

### Role-Based Access Issues

**Issue**: Users can't access pages they should have permission for.

**Solutions**:
- Verify user roles in the database:
  ```sql
  UPDATE users SET role = 'admin' WHERE email = 'user@example.com';
  ```
- Check route decorators for incorrect role requirements
- Clear browser cache and cookies, then log in again

## File Upload Issues

### Permission Denied

**Issue**: "Permission denied" when uploading files.

**Solutions**:
- Check ownership and permissions on the upload directory:
  ```bash
  sudo chown -R www-data:www-data uploads/
  sudo chmod -R 755 uploads/
  ```
- For Docker, ensure volumes are mounted correctly:
  ```yaml
  volumes:
    - ./uploads:/app/uploads
  ```

### File Size Limitations

**Issue**: Large file uploads fail.

**Solutions**:
- Check Nginx/Apache configuration for upload limits:
  ```nginx
  # In nginx.conf
  client_max_body_size 20M;
  ```
- Verify Flask configuration:
  ```python
  app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB
  ```
- Check for timeouts in proxy settings

### Missing Uploaded Files

**Issue**: Files appear to upload successfully but are missing.

**Solutions**:
- Verify the `UPLOAD_FOLDER` path in configuration
- Check disk space (`df -h`)
- Look for symbolic link issues or path mismatches
- Check for file cleanup routines that might be deleting files

## Email Configuration Problems

### Email Not Sending

**Issue**: System doesn't send notification emails.

**Solutions**:
- Verify SMTP configuration in `.env`:
  ```
  MAIL_SERVER=smtp.your-provider.com
  MAIL_PORT=587
  MAIL_USERNAME=your_username
  MAIL_PASSWORD=your_password
  MAIL_USE_TLS=True
  ```
- Check network connectivity to the mail server:
  ```bash
  telnet smtp.your-provider.com 587
  ```
- Look for SMTP server errors in application logs
- Test with a service like SendGrid or Mailgun instead of SMTP

### Email Delivery Problems

**Issue**: Emails are sent but not delivered to recipients.

**Solutions**:
- Check spam/junk folders
- Verify sender domain has proper SPF and DKIM records
- Ensure the sender address is valid and verified with your email provider
- Check if your IP is blacklisted (use a blacklist checker tool)

## Performance Issues

### Slow Page Loads

**Issue**: Pages take a long time to load.

**Solutions**:
- Check database query performance:
  ```sql
  EXPLAIN ANALYZE SELECT * FROM submissions ORDER BY created_at DESC;
  ```
- Review application logs for slow query warnings
- Verify server resources (CPU, memory, disk I/O)
- Implement database indexes on frequently queried columns:
  ```sql
  CREATE INDEX idx_submissions_status ON submissions(status);
  ```
- Optimize SQLAlchemy queries as described in [PERFORMANCE.md](PERFORMANCE.md)

### High Server Load

**Issue**: Server has high CPU/memory usage.

**Solutions**:
- Adjust Gunicorn worker count based on available CPUs:
  ```bash
  gunicorn --workers $(( 2 * $(nproc) + 1 )) main:app
  ```
- Check for runaway database queries or connections
- Look for memory leaks in application code
- Consider implementing caching as described in [SCALING.md](SCALING.md)
- Use a tool like `top` or `htop` to identify resource-intensive processes

### Database Connection Exhaustion

**Issue**: "Too many database connections" error.

**Solutions**:
- Adjust PostgreSQL's `max_connections` parameter:
  ```
  # In postgresql.conf
  max_connections = 100  # Increase as needed
  ```
- Configure SQLAlchemy connection pooling:
  ```python
  app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
      "pool_recycle": 300,
      "pool_size": 10,
      "max_overflow": 20
  }
  ```
- Ensure connections are properly closed after use

## Plugin Problems

### Plugin Not Loading

**Issue**: Installed plugin doesn't appear or function correctly.

**Solutions**:
- Check plugin structure (must include `register_plugin()` function)
- Look for errors in application logs related to plugin loading
- Try disabling other plugins to check for conflicts
- Verify plugin compatibility with your EasyJournal version

### Plugin Errors

**Issue**: Application errors after installing a plugin.

**Solutions**:
- Check the application logs for detailed error messages
- Disable the problematic plugin by renaming its directory:
  ```bash
  mv plugins/problem_plugin plugins/problem_plugin.disabled
  ```
- Contact the plugin developer for assistance
- Verify that all plugin dependencies are installed

## Docker-Related Issues

### Container Won't Start

**Issue**: Docker container fails to start.

**Solutions**:
- Check container logs:
  ```bash
  docker-compose logs app
  ```
- Verify that ports aren't already in use:
  ```bash
  sudo lsof -i :5000
  ```
- Ensure volumes are properly defined and accessible
- Rebuild the container from scratch:
  ```bash
  docker-compose down -v
  docker-compose build --no-cache
  docker-compose up -d
  ```

### Database Connection Issues in Docker

**Issue**: Application can't connect to the database in Docker.

**Solutions**:
- Make sure the database container is running:
  ```bash
  docker-compose ps
  ```
- Check networking between containers:
  ```bash
  docker network ls
  docker network inspect easyjournal_default
  ```
- Verify the database connection string in docker-compose.yml:
  ```yaml
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@db:5432/journal_db
  ```
- Wait for the database to fully initialize before starting the app

## HTTPS and Certificate Issues

### Invalid Certificate

**Issue**: Browser shows certificate warning.

**Solutions**:
- Renew Let's Encrypt certificate:
  ```bash
  certbot renew
  ```
- Check certificate expiration:
  ```bash
  openssl x509 -dates -in /path/to/cert.pem
  ```
- Verify that the certificate matches the domain name
- For development, generate a self-signed certificate:
  ```bash
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
  ```

### Mixed Content Warnings

**Issue**: Browser shows mixed content warnings (HTTP/HTTPS).

**Solutions**:
- Check for hardcoded HTTP URLs in templates and scripts
- Use relative or protocol-relative URLs:
  ```html
  <!-- Instead of http://... -->
  <script src="//cdn.example.com/script.js"></script>
  <img src="/static/images/logo.png">
  ```
- Set up proper redirects from HTTP to HTTPS
- Implement Content Security Policy headers

## Common Error Messages

### "SQLAlchemy.exc.OperationalError: could not connect to server"

**Causes**:
- PostgreSQL not running
- Incorrect connection string
- Network/firewall issues

**Solutions**:
- Start PostgreSQL: `sudo systemctl start postgresql`
- Check connection parameters in `.env`
- Verify PostgreSQL is listening on the expected port:
  ```bash
  sudo netstat -plunt | grep postgres
  ```

### "werkzeug.routing.BuildError: Could not build url for endpoint"

**Causes**:
- Route not defined correctly
- Missing required parameters
- Blueprint registration issues

**Solutions**:
- Check route definitions in view functions
- Verify blueprint registration in `app.py`
- Debug route parameters being passed to `url_for()`

### "jinja2.exceptions.TemplateNotFound"

**Causes**:
- Template file missing
- Incorrect template path
- Blueprint template folder not registered

**Solutions**:
- Verify template exists in the correct location
- Check template folder registration:
  ```python
  bp = Blueprint('name', __name__, template_folder='templates')
  ```
- Debug template loading with absolute paths

### "RuntimeError: Working outside of application context"

**Causes**:
- Accessing Flask objects outside of a request
- Missing app context in scripts or tasks

**Solutions**:
- Wrap operations in an application context:
  ```python
  with app.app_context():
      # Your code here
  ```
- Initialize extensions properly with `init_app()`
- Use application factories correctly

### "sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation)"

**Causes**:
- Duplicate key in unique column
- Violated unique constraint

**Solutions**:
- Check for existing records before insertion
- Handle duplicate key errors gracefully
- Implement proper upsert logic for data imports

## Getting Help

If you're still experiencing issues after trying the solutions above:

1. Check the **GitHub repository** for open and closed issues that might match your problem
2. Search the **community forum** for similar problems and solutions
3. **Create a detailed issue** on GitHub with:
   - Exact error messages
   - Steps to reproduce the problem
   - Environment details (OS, Python version, PostgreSQL version)
   - Relevant log output
   - What you've already tried

For urgent production issues, consider getting professional support from the EasyJournal community or contributors.