# EasyJournal - Developer Guide

This document provides detailed information for developers working with the EasyJournal codebase, including architectural patterns, code organization, performance considerations, and best practices.

## Architecture Overview

EasyJournal follows a modular architecture based on Flask blueprints:

```
easyjournal/
├── app.py            # Main application factory and initialization
├── config.py         # Configuration and environment settings
├── main.py           # Entry point for the application
├── models.py         # Database models (SQLAlchemy ORM)
├── forms/            # Form definitions for data validation
├── routes/           # Route handlers organized by blueprints
├── plugins/          # Plugin system for extending functionality
├── services/         # Service modules for external integrations
├── static/           # Static assets (CSS, JS, images)
├── templates/        # Jinja2 templates
└── uploads/          # User-uploaded files
```

### Key Components

1. **Blueprint-based Routing**: 
   - All routes are organized into feature-specific blueprints (auth, admin, submission, review)
   - Each blueprint handles a specific aspect of the application
   - Blueprints are registered in `app.py`

2. **SQLAlchemy ORM**:
   - Models defined in `models.py`
   - Database configuration in `app.py` and `config.py`
   - Connection pooling configured for production use

3. **Plugin System**:
   - Located in `plugin_system.py`
   - Allows extending functionality without modifying core code
   - Plugins live in the `plugins/` directory
   - Each plugin should implement a `register_plugin()` function

4. **Authentication and Authorization**:
   - Flask-Login for session management
   - Role-based access control in route handlers
   - User model with password hashing and role checking methods

## Performance Optimization

### Request Handlers

Flask's `before_request` handlers are used for common tasks but can impact performance. The system employs these optimization techniques:

1. **Early Returns**:
   - Path filtering to skip processing for static assets
   - Authentication checks before expensive operations
   - Conditional processing based on request properties
   
2. **Caching System Settings**:
   - System settings are cached for 10 minutes to reduce database queries
   - Cache refreshed only when needed
   - Optimized data retrieval with targeted SQL queries

3. **Visitor Tracking**:
   - Session-based frequency limiting to reduce database writes
   - Optimized data collection for analytics
   - Expanded path exclusions for admin and health check routes

### Query Optimization

Database query patterns to follow:

1. **Selective Column Retrieval**:
   ```python
   # Instead of this:
   all_users = User.query.all()
   
   # Use this when only specific fields are needed:
   user_names = User.query.with_entities(User.id, User.name).all()
   ```

2. **Pagination**:
   ```python
   # For large result sets:
   users_page = User.query.paginate(page=page_num, per_page=20)
   ```

3. **Eager Loading for Relationships**:
   ```python
   # Instead of this (causes N+1 query problem):
   submissions = Submission.query.all()
   # and then later: submission.author.name
   
   # Use this:
   submissions = Submission.query.options(joinedload(Submission.author)).all()
   ```

4. **Indexing for Performance**:
   ```python
   # In models.py:
   __table_args__ = (
       db.Index('idx_submission_status', 'status'),
       db.Index('idx_user_role', 'role'),
   )
   ```

## Best Practices

### Coding Standards

1. **Flask Route Organization**:
   - Group related routes in blueprints
   - Use clear route naming
   - Implement proper error handling and status codes

2. **Database Operations**:
   - Wrap database operations in try/except blocks
   - Properly commit or rollback transactions
   - Don't leave sessions open longer than necessary

3. **Authentication & Security**:
   - Use decorator patterns for access control
   - Validate all user input
   - Never store raw passwords
   - Implement proper CSRF protection

### Performance Best Practices

1. **Request Handlers**:
   - Keep `before_request` handlers lightweight
   - Cache expensive operations
   - Use early returns for optimization

2. **Database Access**:
   - Minimize database queries
   - Optimize with appropriate indexes
   - Use SQLAlchemy's query optimization features

3. **Caching Strategy**:
   - Cache system settings and slow-changing data
   - Use sensible cache durations
   - Implement cache invalidation properly

4. **Template Rendering**:
   - Minimize complex logic in templates
   - Use template inheritance and includes
   - Cache rendered templates when appropriate

## Testing

1. **Unit Tests**:
   - Located in the `tests/` directory
   - Run with `python run_tests.py`
   - Test coverage includes models, forms, and routes

2. **Test Database**:
   - Tests use SQLite in-memory database
   - Fixtures are defined in test modules
   - Use the `app.test_client()` for route testing

## Common Pitfalls

1. **Session Management**:
   - Always check user authentication before accessing current_user attributes
   - Handle session expiration gracefully
   - Be careful with session data size

2. **File Uploads**:
   - Always validate file types and sizes
   - Store uploaded files securely
   - Handle file IO errors gracefully

3. **Performance Issues**:
   - Watch for N+1 query problems in relationships
   - Avoid complex queries in templates
   - Profile slow endpoints with the Flask debug toolbar

## Contribution Workflow

1. **Setting up for Development**:
   - Fork the repository
   - Create a feature branch
   - Follow coding standards

2. **Testing Changes**:
   - Run existing tests
   - Add new tests for your features
   - Ensure all tests pass

3. **Pull Requests**:
   - Provide descriptive PR titles and descriptions
   - Reference issues being addressed
   - Ensure CI checks pass

## Deployment

See [INSTALL.md](INSTALL.md) for detailed deployment instructions.

For performance optimization details, see [PERFORMANCE.md](PERFORMANCE.md).