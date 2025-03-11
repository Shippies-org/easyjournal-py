# EasyJournal - Performance Optimization Guide

This document details the performance optimizations implemented in EasyJournal to ensure efficient operation, especially under heavier loads.

## Recent Performance Optimizations

### Before Request Handlers

The system uses Flask's `before_request` handlers to set up each request. These have been optimized for improved performance:

1. **System Settings Loading**
   - Implemented SQL query optimization with `with_entities` to fetch only needed columns
   - Added expanded path exclusions to skip unnecessary processing for static resources
   - Improved caching mechanism to reduce database queries
   - Added attribute existence checking to prevent attribute errors

2. **GDPR Consent Checking**
   - Restructured with early returns to minimize unnecessary processing
   - Improved path filtering for better performance
   - Added proper authentication state checking before expensive operations
   - Moved large text constants to config.py to reduce handler complexity

3. **Visitor Tracking**
   - Optimized SQL operations with minimal data storage
   - Implemented smarter session-based tracking to reduce database writes
   - Added extended path exclusions for admin routes and health checks
   - Implemented conditional imports to reduce unnecessary module loading
   - Simplified article view detection logic

### Configuration Improvements

1. **Default Text Templates**
   - Moved large text constants (like GDPR consent text) to config.py
   - Reduced memory usage in request handlers
   - Centralized text management for easier updates

## Caching Strategy

### Current Implementation

The system currently uses a 10-minute cache for system settings to balance freshness with performance. This duration can be adjusted in `app.py` by modifying the `_CACHE_DURATION` variable:

```python
_CACHE_DURATION = 600  # Default: 10 minutes in seconds
```

### In-Memory Cache

EasyJournal uses a simple in-memory caching mechanism for system settings:

```python
# Cache storage
_settings_cache = {}
_settings_cache_time = 0

def load_system_settings():
    """Load system settings before handling any request."""
    global _settings_cache, _settings_cache_time
    
    # Skip for static files and certain paths
    if request.path.startswith('/static/') or request.path.startswith('/uploads/'):
        return
    
    # Check if cache is still valid
    current_time = time.time()
    if current_time - _settings_cache_time < _CACHE_DURATION and _settings_cache:
        g.settings = _settings_cache
        return
    
    # If cache expired or empty, fetch from database
    try:
        settings = SystemSetting.query.with_entities(
            SystemSetting.setting_key, 
            SystemSetting.setting_value
        ).all()
        
        # Update cache
        _settings_cache = {s.setting_key: s.setting_value for s in settings}
        _settings_cache_time = current_time
        g.settings = _settings_cache
        
    except Exception as e:
        # Fallback to empty settings if database error occurs
        g.settings = {}
        app.logger.error(f"Error loading system settings: {str(e)}")
```

### Optimization Considerations

1. **Cache Duration Adjustment**:
   - For high-traffic sites: Increase cache duration (e.g., 30-60 minutes)
   - For sites with frequent setting changes: Decrease duration (e.g., 5 minutes)
   - For development: Set to a low value or 0 to see changes immediately

2. **Cache Invalidation**:
   After updating system settings in the admin panel, the cache is explicitly invalidated:
   ```python
   # After successful settings update
   global _settings_cache_time
   _settings_cache_time = 0  # Force cache refresh on next request
   ```

## Database Query Optimization

Several database queries have been optimized:

1. **System Settings**: Using optimized queries with only required columns
2. **Visitor Tracking**: Reduced data collection and storage to essential fields
3. **Session Management**: Implemented smart tracking to avoid duplicate entries

### SQL Query Optimization Techniques

The following techniques are used throughout the codebase to ensure optimal database performance:

1. **Selective Column Retrieval**:
   ```python
   # Instead of fetching entire rows:
   settings = SystemSetting.query.all()
   
   # We fetch only the columns we need:
   settings = SystemSetting.query.with_entities(
       SystemSetting.setting_key, 
       SystemSetting.setting_value
   ).all()
   ```

2. **Strategic Indexing**:
   Key columns are indexed to improve query performance:
   ```python
   class Submission(db.Model):
       # ... column definitions ...
       __table_args__ = (
           db.Index('idx_submission_status', 'status'),
           db.Index('idx_submission_category', 'category'),
       )
   ```

3. **Eager Loading Relationships**:
   We use joined loads to avoid the N+1 query problem:
   ```python
   # Instead of:
   submissions = Submission.query.all()
   # and then later: submission.author.name (which creates additional queries)
   
   # We use:
   submissions = Submission.query.options(
       joinedload(Submission.author)
   ).all()
   ```

4. **Query Optimization for Lists**:
   For listing pages, we use pagination:
   ```python
   page = request.args.get('page', 1, type=int)
   per_page = request.args.get('per_page', 20, type=int)
   
   submissions = Submission.query.order_by(
       Submission.submitted_at.desc()
   ).paginate(page=page, per_page=per_page)
   ```

5. **Count Optimization**:
   For counting records, we use optimized count queries:
   ```python
   # Instead of:
   count = len(Submission.query.all())
   
   # We use:
   count = db.session.query(db.func.count(Submission.id)).scalar()
   ```

## Future Optimization Areas

Areas that could benefit from further optimization:

1. **Analytics Dashboard**: Query optimization for report generation
2. **Admin Routes**: Refactoring large blueprint modules (especially admin.py)
3. **Plugin System**: Lazy loading of plugins as needed
4. **SQL Query Caching**: Implementing query result caching for frequently accessed data

## Performance Monitoring

To monitor EasyJournal's performance:

1. **Server Logs**: Watch for slow database queries or high response times
2. **Database Performance**: Use PostgreSQL's query analyzer for complex queries
3. **Application Profiling**: Use Python profiling tools to identify bottlenecks

## Best Practices

1. **Avoid Heavy Processing in Request Handlers**: Defer processing when possible
2. **Use SQL Query Optimization**: Always fetch only required columns
3. **Implement Path Exclusions**: Skip processing for static files and health checks
4. **Prioritize Early Returns**: Structure code to exit early when possible
5. **Implement Proper Caching**: Use caching for frequently accessed data