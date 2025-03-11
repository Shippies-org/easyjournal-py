# EasyJournal - Scaling & Performance Guide

This document provides guidance for administrators on scaling EasyJournal for larger deployments, performance tuning, and optimizing resource usage.

## Deployment Architecture

### Single-Server Deployment
Suitable for small to medium journals with low to moderate traffic:

```
[Users] → [Nginx/reverse proxy] → [Gunicorn (multiple workers)] → [EasyJournal] → [PostgreSQL]
```

### Multi-Server Deployment
Recommended for larger journals with higher traffic:

```
[Users] → [Load Balancer] → [Multiple App Servers] → [Shared Database] → [File Storage]
            ↓                    ↓
      [CDN for Static]    [Cache Server]
```

## Database Scaling

### Connection Pooling
EasyJournal uses SQLAlchemy's connection pooling. Configure the pool size in `app.py`:

```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 20,  # Adjust based on your needs
    "max_overflow": 10
}
```

### PostgreSQL Optimization
Key PostgreSQL configuration settings for improved performance:

1. **Memory Configuration**:
   ```
   shared_buffers = 25% of system RAM (up to 8GB)
   work_mem = 64MB
   maintenance_work_mem = 256MB
   effective_cache_size = 75% of system RAM
   ```

2. **Write Performance**:
   ```
   synchronous_commit = off  # Use with caution - improves write performance but can risk data loss
   wal_buffers = 16MB
   ```

3. **Query Performance**:
   ```
   random_page_cost = 1.1  # Lowered value for SSD storage
   effective_io_concurrency = 200  # Higher for SSDs
   ```

4. **Index and Analyze**:
   Regularly run:
   ```
   VACUUM ANALYZE;
   ```

### Read Replicas
For high-traffic journals, configure PostgreSQL read replicas and direct read queries to them.

## Application Scaling

### Gunicorn Configuration
Adjust worker settings based on available CPUs:

```bash
# For CPU-bound applications
gunicorn --bind 0.0.0.0:5000 --workers $(( 2 * $(nproc) + 1 )) main:app

# For I/O-bound applications
gunicorn --bind 0.0.0.0:5000 --workers $(( 4 * $(nproc) )) --threads 2 main:app
```

### Caching Strategies

1. **System-Level Caching**:
   - Configure `_CACHE_DURATION` in `app.py` (default: 600 seconds)
   - Increase for larger sites with infrequent setting changes

2. **Add Redis Cache** for larger deployments:
   ```python
   # Install Flask-Caching and redis
   # pip install Flask-Caching redis
   
   from flask_caching import Cache
   
   cache = Cache(config={
       'CACHE_TYPE': 'redis',
       'CACHE_REDIS_URL': 'redis://localhost:6379/0'
   })
   
   cache.init_app(app)
   
   # Then use:
   @cache.cached(timeout=300)
   def get_data():
       # expensive operation
       return data
   ```

3. **Static Asset Caching**:
   Configure Nginx with aggressive caching for static assets:
   ```nginx
   location /static/ {
       expires 30d;
       add_header Cache-Control "public, max-age=2592000";
   }
   ```

### File Storage
For multi-server deployments, use a shared file system or object storage:

1. **NFS** for simple shared storage
2. **S3-compatible storage** for better scalability
   - Requires code changes to use boto3/S3 clients
   - Supports CDN integration for better performance

## Load Testing & Monitoring

### Load Testing Tools
Before scaling up, benchmark your application:

1. **Locust**: Python-based load testing
   ```bash
   pip install locust
   # Create a locustfile.py with test scenarios
   locust --host=http://localhost:5000
   ```

2. **ApacheBench**: Quick load tests
   ```bash
   ab -n 1000 -c 50 http://localhost:5000/
   ```

### Monitoring

1. **Application Monitoring**:
   - Install and configure Prometheus with Flask exporter
   - Set up Grafana dashboards for visualization

2. **Database Monitoring**:
   - Enable PostgreSQL statistics collector
   - Monitor slow queries with pg_stat_statements

3. **System Monitoring**:
   - Track CPU, memory, disk I/O, and network usage
   - Set up alerts for resource constraints

## Performance Bottlenecks

Common bottlenecks and solutions:

### Database Queries
1. **Problem**: Slow analytics queries
   - **Solution**: Create materialized views or summary tables

2. **Problem**: High database load during peak hours
   - **Solution**: Implement query caching and rate limiting

### File Uploads/Downloads
1. **Problem**: Slow file uploads/downloads
   - **Solution**: Implement direct-to-S3 uploads and CDN for downloads

2. **Problem**: Large file handling
   - **Solution**: Process uploads asynchronously with task queues

### Request Processing
1. **Problem**: High response times
   - **Solution**: Profile with tools like Werkzeug Profiler and optimize slow functions

2. **Problem**: Frequent cache misses
   - **Solution**: Adjust cache strategy and preload common data

## Scaling Checklist

When planning to scale EasyJournal for larger deployments:

1. **Database**:
   - [ ] Optimize PostgreSQL configuration
   - [ ] Set up proper indexes for common queries
   - [ ] Configure appropriate connection pool settings
   - [ ] Consider read replicas for read-heavy workloads

2. **Application**:
   - [ ] Configure proper Gunicorn worker count
   - [ ] Implement Redis cache for frequently accessed data
   - [ ] Review and optimize database queries
   - [ ] Implement asynchronous processing for heavy tasks

3. **Infrastructure**:
   - [ ] Set up load balancer for multiple app servers
   - [ ] Configure CDN for static assets
   - [ ] Implement shared file storage
   - [ ] Set up monitoring and alerting

4. **Testing**:
   - [ ] Perform load testing with realistic scenarios
   - [ ] Identify and address bottlenecks
   - [ ] Verify data integrity under load
   - [ ] Test failure scenarios and recovery

## Production-Ready Configuration

Sample Nginx configuration for production:

```nginx
server {
    listen 80;
    server_name journal.example.com;
    
    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name journal.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Static files
    location /static/ {
        alias /path/to/easyjournal/static/;
        expires 30d;
    }
    
    location /uploads/ {
        alias /path/to/easyjournal/uploads/;
        expires 7d;
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Sample systemd service file:

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

[Install]
WantedBy=multi-user.target
```

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/faq/performance.html)