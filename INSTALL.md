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

#### Environment Configuration
For production, configure these settings in `.env`:
- `SESSION_SECRET`: Set a strong, random secret key
- `DEMO_MODE`: Set to `False`
- `FLASK_DEBUG`: Set to `0`
- `UPLOAD_FOLDER`: Configure a path with sufficient storage

#### Web Server Configuration
Use Gunicorn with multiple workers for improved performance:
```bash
# Formula for CPU-bound applications
gunicorn --bind 0.0.0.0:5000 --workers $(( 2 * $(nproc) + 1 )) main:app

# For I/O-bound applications (like EasyJournal)
gunicorn --bind 0.0.0.0:5000 --workers $(( 4 * $(nproc) )) --threads 2 main:app
```

#### Recommended: HTTPS with Nginx Reverse Proxy
Create an Nginx configuration file in `/etc/nginx/sites-available/easyjournal.conf`:

```nginx
server {
    listen 80;
    server_name your-journal-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-journal-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    
    # Static files with caching
    location /static/ {
        alias /path/to/easyjournal/static/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # File uploads - shorter cache time
    location /uploads/ {
        alias /path/to/easyjournal/uploads/;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large file uploads
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

Enable the site and restart Nginx:
```bash
ln -s /etc/nginx/sites-available/easyjournal.conf /etc/nginx/sites-enabled/
nginx -t  # Test configuration
systemctl restart nginx
```

#### Systemd Service for Auto-start
Create a systemd service file at `/etc/systemd/system/easyjournal.service`:

```ini
[Unit]
Description=EasyJournal Gunicorn Service
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/easyjournal
ExecStart=/path/to/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 60 main:app
Restart=on-failure
Environment="DATABASE_URL=postgresql://user:password@localhost:5432/journal_db"
Environment="SESSION_SECRET=your-secure-secret-key"
Environment="FLASK_DEBUG=0"
Environment="DEMO_MODE=False"
Environment="UPLOAD_FOLDER=/path/to/uploads"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
systemctl enable easyjournal
systemctl start easyjournal
systemctl status easyjournal  # Check status
```

#### SSL Certificate with Let's Encrypt
For free HTTPS certificates:
```bash
apt-get install certbot python3-certbot-nginx
certbot --nginx -d your-journal-domain.com
```

### Performance Considerations
EasyJournal includes several performance optimizations for efficient operation:

- System settings are cached for 10 minutes to reduce database load
- Request handlers are optimized with early returns and path exclusions
- Visitor tracking includes frequency limiting to prevent database overload

For detailed information on performance optimizations, see the `PERFORMANCE.md` file.

If deploying for a large journal with many users, consider:
- Increasing the PostgreSQL connection pool size
- Using a more powerful database server
- Implementing a Redis cache for session data
- Adjusting the cache duration in app.py if needed

### Scaling for Larger Deployments

For journals with high traffic or many users, consider these scaling options:

#### Multi-Server Deployment
1. **Load Balancer**: Distribute traffic across multiple application servers
   ```
   [Users] → [Load Balancer] → [Multiple EasyJournal Servers] → [Shared PostgreSQL]
   ```

2. **PostgreSQL Configuration**: For high traffic scenarios
   ```
   max_connections = 200
   shared_buffers = 2GB
   work_mem = 64MB
   maintenance_work_mem = 256MB
   ```

3. **Redis Cache Implementation**:
   ```bash
   pip install Flask-Caching redis
   ```
   Then modify `app.py` to use Redis cache:
   ```python
   from flask_caching import Cache
   
   cache = Cache(config={
       'CACHE_TYPE': 'redis',
       'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
   })
   
   # Initialize in create_app()
   cache.init_app(app)
   ```

#### Backup and Disaster Recovery

1. **Database Backups**:
   ```bash
   # Set up daily PostgreSQL backups
   pg_dump -U journal_user journal_db | gzip > /backup/journal_db_$(date +%Y-%m-%d).sql.gz
   
   # Keep the last 30 days of backups
   find /backup/ -name "journal_db_*.sql.gz" -mtime +30 -delete
   ```

2. **File Uploads Backup**:
   ```bash
   # Backup uploaded files
   rsync -av /path/to/easyjournal/uploads/ /backup/uploads/
   ```

3. **Automated Backup Script** (save as `/etc/cron.daily/backup-easyjournal`):
   ```bash
   #!/bin/bash
   
   # PostgreSQL backup
   pg_dump -U journal_user journal_db | gzip > /backup/journal_db_$(date +%Y-%m-%d).sql.gz
   
   # Uploads backup
   rsync -av /path/to/easyjournal/uploads/ /backup/uploads/
   
   # Cleanup old backups
   find /backup/ -name "journal_db_*.sql.gz" -mtime +30 -delete
   
   # Optional: Copy to remote storage
   rsync -avz /backup/ user@remote-server:/remote-backup/easyjournal/
   ```
   
   Make executable and test:
   ```bash
   chmod +x /etc/cron.daily/backup-easyjournal
   /etc/cron.daily/backup-easyjournal
   ```

For comprehensive scaling guidance, see the [SCALING.md](SCALING.md) document.

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