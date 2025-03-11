# EasyJournal - Security Guide

This document provides security best practices and guidelines for securing your EasyJournal installation.

## Table of Contents
1. [Security Overview](#security-overview)
2. [Server Security](#server-security)
3. [Application Security](#application-security)
4. [Database Security](#database-security)
5. [User Authentication](#user-authentication)
6. [Data Protection](#data-protection)
7. [File Upload Security](#file-upload-security)
8. [API and Integration Security](#api-and-integration-security)
9. [Docker Security](#docker-security)
10. [GDPR Compliance](#gdpr-compliance)
11. [Security Monitoring](#security-monitoring)
12. [Security Checklist](#security-checklist)

## Security Overview

EasyJournal is designed with security in mind, but proper configuration and deployment practices are essential to maintain a secure installation. This guide outlines recommended security measures for production deployments.

## Server Security

### Operating System Hardening

1. **Keep Systems Updated**:
   ```bash
   # For Ubuntu/Debian
   apt update && apt upgrade -y
   
   # For CentOS/RHEL
   yum update -y
   ```

2. **Limit SSH Access**:
   ```bash
   # Edit SSH configuration
   vim /etc/ssh/sshd_config
   
   # Disable root login
   PermitRootLogin no
   
   # Use key-based authentication
   PasswordAuthentication no
   
   # Restart SSH
   systemctl restart sshd
   ```

3. **Use a Firewall**:
   ```bash
   # Allow only necessary ports
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw allow 22/tcp
   ufw enable
   ```

4. **Install Security Updates Automatically**:
   ```bash
   # On Ubuntu
   apt install unattended-upgrades
   dpkg-reconfigure unattended-upgrades
   ```

### Web Server Configuration

1. **Use HTTPS Only**: Configure your web server to redirect all HTTP traffic to HTTPS:
   ```nginx
   server {
       listen 80;
       server_name your-journal.com;
       return 301 https://$host$request_uri;
   }
   ```

2. **Implement Strong SSL/TLS Configuration**:
   ```nginx
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_prefer_server_ciphers on;
   ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
   ssl_session_cache shared:SSL:10m;
   ssl_session_timeout 10m;
   ```

3. **Set Security Headers**:
   ```nginx
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
   add_header X-Content-Type-Options nosniff;
   add_header X-Frame-Options SAMEORIGIN;
   add_header X-XSS-Protection "1; mode=block";
   add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data:; font-src 'self' https://cdn.jsdelivr.net; connect-src 'self';";
   ```

4. **Disable Server Tokens**:
   ```nginx
   server_tokens off;
   ```

## Application Security

### Environment Configuration

1. **Secure Environment Variables**:
   - Never commit `.env` files to version control
   - Use strong, random values for secrets
   - Use different secrets for development and production
   
   Example `.env` file for production:
   ```
   SESSION_SECRET=<generated-long-random-string>
   FLASK_DEBUG=0
   DEMO_MODE=False
   ```

2. **Generate Secure Random Values**:
   ```bash
   # Generate a secure random value for SESSION_SECRET
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Secure Application Settings

1. **Disable Debug Mode in Production**:
   ```python
   app.debug = False
   ```

2. **Configure Session Security**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
   app.config['SESSION_COOKIE_HTTPONLY'] = True  # Not accessible via JavaScript
   app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout (in seconds)
   ```

3. **Enable CSRF Protection**:
   EasyJournal already uses Flask-WTF's CSRF protection. Ensure all forms include:
   ```html
   <form method="post">
       {{ form.csrf_token }}
       <!-- form fields -->
   </form>
   ```

## Database Security

### Secure Database Configuration

1. **Use Strong Database Passwords**:
   - Generate a strong, random password for the database user
   - Store the password securely in environment variables
   
   ```bash
   # Generate a strong database password
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Limit Database User Permissions**:
   ```sql
   -- Create a user with only necessary permissions
   CREATE USER journal_user WITH PASSWORD 'strong-password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO journal_user;
   GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO journal_user;
   ```

3. **Use Connection Pooling Securely**:
   ```python
   app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
       "pool_recycle": 300,  # Recycle connections after 5 minutes
       "pool_pre_ping": True,  # Check connection validity before use
   }
   ```

4. **Configure PostgreSQL Security**:
   Edit `pg_hba.conf` to restrict access:
   ```
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   local   journal_db      journal_user                            scram-sha-256
   host    journal_db      journal_user    127.0.0.1/32            scram-sha-256
   host    journal_db      journal_user    ::1/128                 scram-sha-256
   ```

### Database Backups

1. **Encrypt Database Backups**:
   ```bash
   # Create an encrypted backup
   pg_dump -U postgres journal_db | gpg -c > journal_backup_$(date +%Y-%m-%d).sql.gpg
   
   # To restore
   gpg -d journal_backup.sql.gpg | psql -U postgres journal_db
   ```

2. **Regular Backup Schedule**:
   ```bash
   # Add to crontab
   0 2 * * * /path/to/backup-script.sh
   ```

## User Authentication

### Password Policies

1. **Enforce Strong Password Requirements**:
   EasyJournal should validate passwords to ensure they:
   - Are at least 8 characters long
   - Contain a mix of uppercase, lowercase, numbers, and special characters
   - Are not commonly used passwords

2. **Secure Password Storage**:
   EasyJournal uses Werkzeug's security functions for password hashing. Always use:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   
   # To hash
   password_hash = generate_password_hash(password)
   
   # To verify
   check_password_hash(password_hash, provided_password)
   ```

3. **Implement Account Lockout**:
   Add logic to temporarily lock accounts after multiple failed login attempts.

### Two-Factor Authentication

Consider implementing two-factor authentication for user accounts:
```python
# Using a library like Flask-2FA
from flask_2fa import setup_2fa

setup_2fa(app)
```

## Data Protection

### Sensitive Data Handling

1. **Minimize Data Collection**:
   - Only collect data necessary for the journal's operation
   - Provide clear purposes for all collected data

2. **Classify Data Sensitivity**:
   - Identify personally identifiable information (PII)
   - Apply stricter controls to sensitive data

3. **Data Encryption**:
   - Use TLS for data in transit
   - Consider field-level encryption for highly sensitive data:
     ```python
     from cryptography.fernet import Fernet
     
     key = Fernet.generate_key()  # Store securely
     f = Fernet(key)
     
     # To encrypt
     encrypted_data = f.encrypt(data.encode())
     
     # To decrypt
     decrypted_data = f.decrypt(encrypted_data).decode()
     ```

### Data Retention Policies

1. **Implement Data Lifecycle Management**:
   - Define retention periods for different data types
   - Automate removal of outdated data
   - Provide data export and deletion functionality for users

## File Upload Security

### Secure File Upload Configuration

1. **Restrict File Types**:
   ```python
   ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
   
   def allowed_file(filename):
       return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   ```

2. **Validate File Content**:
   ```python
   # Check file content matches its extension
   import magic
   
   def validate_file_content(file):
       mime = magic.Magic(mime=True)
       file_type = mime.from_buffer(file.read())
       file.seek(0)  # Reset file pointer
       
       allowed_mimes = {
           'application/pdf': 'pdf',
           'application/msword': 'doc',
           'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
           'text/plain': 'txt',
           'application/rtf': 'rtf'
       }
       
       return file_type in allowed_mimes
   ```

3. **Use Secure File Names**:
   ```python
   import uuid
   import os
   
   def secure_filename(filename):
       ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
       return f"{uuid.uuid4().hex}.{ext}"
   ```

4. **Store Files Securely**:
   - Use a directory outside the web root
   - Set proper permissions (e.g., 755 for directories, 644 for files)
   - Consider using a separate file storage service for large deployments

## API and Integration Security

### Secure External API Usage

1. **API Key Management**:
   - Store API keys in environment variables, not code
   - Use different API keys for development and production
   - Implement key rotation policies

2. **Validate API Responses**:
   ```python
   import requests
   
   def call_external_api(endpoint, params):
       try:
           response = requests.get(endpoint, params=params, timeout=10)
           response.raise_for_status()  # Raise exception for 4XX/5XX responses
           
           # Validate response structure before using
           data = response.json()
           if 'required_field' not in data:
               raise ValueError("Invalid API response format")
               
           return data
       except (requests.exceptions.RequestException, ValueError) as e:
           # Log error and handle gracefully
           app.logger.error(f"API error: {str(e)}")
           return None
   ```

3. **Rate Limiting and Timeouts**:
   ```python
   # Implement rate limiting for external API calls
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=get_remote_address)
   
   @app.route('/api/endpoint')
   @limiter.limit("10 per minute")
   def api_endpoint():
       # Implementation
       pass
   ```

## Docker Security

### Docker Deployment Security

1. **Use Official Images**:
   ```dockerfile
   FROM python:3.10-slim
   ```

2. **Run Containers as Non-Root**:
   ```dockerfile
   # Create a non-root user
   RUN useradd -m appuser
   
   # Change to non-root user
   USER appuser
   
   # Switch to the appropriate user
   WORKDIR /home/appuser/app
   ```

3. **Scan Docker Images for Vulnerabilities**:
   ```bash
   # Using tools like Trivy
   trivy image easyjournal:latest
   ```

4. **Limit Container Resources**:
   ```yaml
   # In docker-compose.yml
   services:
     app:
       # ... other configuration
       deploy:
         resources:
           limits:
             cpus: '0.50'
             memory: 512M
   ```

5. **Secure Docker Networking**:
   ```yaml
   # Use internal networks for container communication
   networks:
     internal:
       internal: true
     web:
       internal: false
   
   services:
     app:
       networks:
         - internal
         - web
     db:
       networks:
         - internal
   ```

## GDPR Compliance

### Compliance Features

1. **Consent Management**:
   - Implement clear consent mechanism
   - Record consent timestamps
   - Allow users to withdraw consent

2. **Data Subject Rights**:
   - Provide data export functionality
   - Implement account deletion with complete data removal
   - Support right to be forgotten

3. **Privacy Policy**:
   - Maintain a clear, accessible privacy policy
   - Document all data processing activities
   - Keep data processing records

## Security Monitoring

### Logging and Monitoring

1. **Configure Comprehensive Logging**:
   ```python
   import logging
   
   # Set up logging
   logging.basicConfig(
       filename='journal.log',
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   
   # Log security events
   app.logger.warning('Security event: Failed login attempt for %s', user_email)
   ```

2. **Monitor Failed Login Attempts**:
   ```python
   # In login route
   failed_attempts = get_failed_attempts(user_email)
   if failed_attempts > 5:
       app.logger.warning('Account locked: Too many failed attempts for %s', user_email)
       # Lock account logic
   ```

3. **Regular Log Analysis**:
   - Review logs for suspicious patterns
   - Monitor for unusual access patterns
   - Set up alerts for security events

### Security Updates

1. **Keep Dependencies Updated**:
   ```bash
   # Update requirements
   pip install --upgrade -r requirements.txt
   
   # Check for security vulnerabilities
   pip install safety
   safety check
   ```

2. **Subscribe to Security Notifications**:
   - Monitor security mailing lists for Flask and dependencies
   - Set up automated security scanning for your codebase

## Security Checklist

Use this checklist for your EasyJournal deployment:

### Pre-Deployment Security Checklist

- [ ] Debug mode disabled
- [ ] Strong SESSION_SECRET configured
- [ ] HTTPS configured with valid certificate
- [ ] Database using strong, unique password
- [ ] All default credentials changed
- [ ] File upload validation implemented
- [ ] Input validation on all forms
- [ ] CSRF protection enabled
- [ ] Security headers configured in web server
- [ ] Firewall and network security configured
- [ ] Regular backup process established
- [ ] Privacy policy and terms of service published
- [ ] Security logging enabled
- [ ] Dependencies checked for vulnerabilities

### Regular Security Maintenance

- [ ] Weekly: Check for system updates
- [ ] Weekly: Review application logs for suspicious activity
- [ ] Monthly: Review user accounts and access
- [ ] Monthly: Test backup restoration
- [ ] Quarterly: Review security policies and procedures
- [ ] Quarterly: Update SSL certificates if needed
- [ ] Annually: Conduct security assessment

## Reporting Security Issues

If you discover a security vulnerability in EasyJournal:

1. Do NOT disclose it publicly on GitHub issues, forums, or mailing lists
2. Send an email to security@easyjournal.org with details
3. Allow time for the issue to be addressed before any public disclosure

## Security Resources

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)