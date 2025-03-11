# EasyJournal - Plugin System Guide

This document provides detailed information about EasyJournal's plugin system, including how to develop, install, and manage plugins.

## Plugin System Overview

EasyJournal features an extensible plugin architecture that allows developers to add new functionality without modifying the core codebase. The plugin system is designed around a hook-based approach, where plugins can register callbacks for specific application events.

## Plugin Directory Structure

Plugins are stored in the `plugins/` directory with the following structure:

```
plugins/
├── plugin_name/
│   ├── __init__.py        # Package initialization 
│   ├── plugin.py          # Main plugin file with register_plugin()
│   ├── models.py          # Optional database models
│   ├── routes.py          # Optional route handlers
│   ├── static/            # Optional static assets
│   └── templates/         # Optional template overrides
```

## Creating a Plugin

### 1. Basic Plugin Structure

Create a new directory in the `plugins/` folder with your plugin name:

```bash
mkdir -p plugins/my_plugin
touch plugins/my_plugin/__init__.py
touch plugins/my_plugin/plugin.py
```

### 2. Plugin Registration

In `plugin.py`, implement the `register_plugin()` function that will be called when the plugin is loaded:

```python
from plugin_system import PluginSystem

def register_plugin():
    """
    Register this plugin with the plugin system.
    This function is called when the plugin is loaded.
    """
    # Register hooks
    PluginSystem.register_hook('after_submission_create', on_submission_created, priority=10)
    PluginSystem.register_hook('modify_home_content', modify_home_content, priority=20)
    
    # Register any routes
    from flask import Blueprint
    bp = Blueprint('my_plugin', __name__, url_prefix='/my-plugin')
    
    @bp.route('/')
    def index():
        return "My Plugin Index Page"
    
    # Return the blueprint to be registered with the application
    return bp

def on_submission_created(args):
    """
    Hook called after a submission is created.
    """
    submission = args.get('submission')
    print(f"New submission created: {submission.title}")
    
def modify_home_content(args):
    """
    Hook to modify the home page content.
    """
    content = args.get('content', '')
    
    # Add custom content to the home page
    custom_content = """
    <div class="alert alert-info">
        This is added by my_plugin!
    </div>
    """
    
    # Return the modified content
    return content + custom_content
```

### 3. Adding Database Models

If your plugin needs database tables, create a `models.py` file:

```python
from app import db
from datetime import datetime

class PluginModel(db.Model):
    """Model for plugin-specific data."""
    __tablename__ = 'my_plugin_data'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PluginModel {self.name}>'
```

### 4. Adding Templates

You can override core templates or add plugin-specific templates:

```
plugins/my_plugin/templates/
├── my_plugin/              # Plugin-specific templates
│   ├── index.html
│   └── dashboard.html
└── home.html               # Override for core template
```

Templates in the plugin directory take precedence over core templates with the same name.

## Available Hooks

The EasyJournal plugin system provides these hooks for plugins to integrate with:

| Hook Name | Description | Arguments |
|-----------|-------------|-----------|
| `after_user_register` | Called after a user is registered | `user`: User object |
| `after_submission_create` | Called after a submission is created | `submission`: Submission object |
| `after_review_submit` | Called after a review is submitted | `review`: Review object |
| `modify_home_content` | Modify home page content | `content`: HTML content string |
| `modify_dashboard` | Modify dashboard content | `dashboard_type`: string, `content`: HTML content |
| `add_navigation_items` | Add items to navigation menus | `items`: list of nav items |
| `before_submission_display` | Called before displaying a submission | `submission`: Submission object |
| `after_editor_decision` | Called after editor makes a decision | `decision`: EditorDecision object |
| `after_issue_publish` | Called after an issue is published | `issue`: Issue object |

## Plugin Settings

Plugins can store settings in the database using the `PluginSetting` model:

```python
from models import PluginSetting

# Store a setting
def save_setting(key, value):
    setting = PluginSetting.query.filter_by(
        plugin_name='my_plugin',
        setting_key=key
    ).first()
    
    if setting:
        setting.setting_value = value
        db.session.commit()
    else:
        new_setting = PluginSetting(
            plugin_name='my_plugin',
            setting_key=key,
            setting_value=value
        )
        db.session.add(new_setting)
        db.session.commit()

# Retrieve a setting
def get_setting(key, default=None):
    setting = PluginSetting.query.filter_by(
        plugin_name='my_plugin',
        setting_key=key
    ).first()
    
    if setting:
        return setting.setting_value
    return default
```

## Example Plugins

### 1. Welcome Banner Plugin

This simple plugin adds a welcome banner to the top of the home page:

```python
def modify_home_content(args):
    """
    This hook function modifies the home page content by adding a welcome banner.
    """
    content = args.get('content', '')
    
    banner = """
    <div class="alert alert-success mb-4">
        <h4 class="alert-heading">Welcome to our Journal!</h4>
        <p>Thank you for visiting. We publish cutting-edge research in multiple disciplines.</p>
        <hr>
        <p class="mb-0">Interested in submitting your work? <a href="/submit" class="alert-link">Click here</a>.</p>
    </div>
    """
    
    # Insert the banner at the beginning of the content
    return banner + content
```

### 2. Copyright Management Plugin

A more complex plugin that adds copyright management functionality:

```python
def register_plugin():
    """
    Register this plugin with the plugin system.
    """
    # Register hooks
    PluginSystem.register_hook('add_footer_content', add_footer_content)
    PluginSystem.register_hook('add_article_copyright_info', add_article_copyright_info)
    PluginSystem.register_hook('add_navigation_items', add_navigation_items)
    
    # Create blueprint for routes
    from flask import Blueprint
    bp = Blueprint('copyright', __name__, url_prefix='/copyright')
    
    @bp.route('/')
    def index():
        """Render the copyright management dashboard."""
        # Implementation...
    
    @bp.route('/new-license', methods=['GET', 'POST'])
    def new_license():
        """Create a new license type."""
        # Implementation...
    
    @bp.route('/edit-license/<int:license_id>', methods=['GET', 'POST'])
    def edit_license(license_id):
        """Edit an existing license type."""
        # Implementation...
    
    # Seed initial data
    seed_license_types()
    
    return bp
```

## Installing and Managing Plugins

### Installing a Plugin

1. Place the plugin directory in the `plugins/` folder
2. Restart the application
3. The plugin will be automatically loaded

### Disabling a Plugin

Currently, to disable a plugin:

1. Rename the plugin directory to add a `.disabled` suffix:
   ```bash
   mv plugins/my_plugin plugins/my_plugin.disabled
   ```
2. Restart the application

### Plugin Management Interface

Administrators can manage plugins through the admin interface at `/admin/plugins`, which provides:

- List of installed plugins
- Plugin status (active/inactive)
- Plugin settings management
- Links to plugin-specific administration pages

## Performance Considerations

### Plugin Loading

Plugins are loaded at application startup, which can affect startup time with many plugins. Optimize by:

- Keeping plugin initialization code lightweight
- Deferring resource-intensive operations until needed
- Using lazy loading patterns for blueprint routes

### Hook Execution

When many plugins register for the same hook, performance may be affected. Best practices:

- Use appropriate priorities (lower numbers execute first)
- Keep hook callbacks efficient
- Avoid expensive database operations in frequently called hooks

## Debugging Plugins

When developing plugins, use these debugging techniques:

1. Enable debug mode in the application
2. Check the application logs for plugin-related messages
3. Add explicit logging in your plugin:

```python
from flask import current_app

def my_hook_function(args):
    try:
        # Plugin logic
        result = do_something()
        current_app.logger.debug(f"Plugin executed with result: {result}")
        return result
    except Exception as e:
        current_app.logger.error(f"Plugin error: {str(e)}")
        # Graceful fallback
        return None
```

## Security Best Practices

When developing plugins, follow these security guidelines:

1. **Input Validation**: Always validate user input
2. **SQL Injection Prevention**: Use SQLAlchemy's parameter binding
3. **XSS Prevention**: Escape user-generated content in templates
4. **Access Control**: Check user permissions before operations
5. **Error Handling**: Catch exceptions and fail gracefully

## Plugin Distribution

Distribute your plugins as Git repositories or zip archives with clear installation instructions.

Include in your documentation:

- Plugin purpose and features
- Installation instructions
- Configuration options
- Required EasyJournal version
- License information

## Troubleshooting

### Common Issues

1. **Plugin Not Loading**
   - Check that it has a `register_plugin()` function
   - Verify there are no syntax errors
   - Check application logs for errors

2. **Database Errors**
   - Make sure your models are properly defined
   - Avoid table name conflicts with core application

3. **Template Not Found**
   - Check template path and hierarchy
   - Verify template exists in the correct location

4. **Hook Not Firing**
   - Verify hook name is correct
   - Check hook registration code
   - Add debug logging to confirm registration