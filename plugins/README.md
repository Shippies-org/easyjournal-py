# EasyJournal Plugin System

The EasyJournal platform features a robust plugin architecture that allows you to extend the functionality of the journal system without modifying the core code.

## How Plugins Work

Plugins in EasyJournal are self-contained modules that can:

1. **Add new features** - Routes, pages, database tables, and functionality
2. **Modify existing features** - Through the hook system
3. **Override templates** - Customize the look and feel
4. **Integrate with the navigation** - Add menu items based on user roles

## Plugin Structure

A basic plugin consists of:

```
plugins/
└── my_plugin/
    ├── __init__.py       # Package initialization
    ├── plugin.py         # Main plugin file with register_plugin() function
    ├── models.py         # Database models (optional)
    └── templates/        # Template overrides (optional)
        └── my_plugin/    # Plugin-specific templates
```

## Creating a Plugin

1. Create a new directory in the `plugins/` folder with your plugin name
2. Create a `plugin.py` file with at least a `register_plugin()` function
3. Import any required modules and define your functionality
4. Register hooks, routes, and templates as needed

## The Hook System

Plugins interact with the core application through hooks. Hooks are predefined points in the application where plugins can inject or modify content.

Common hooks include:
- `getNavItems` - Modify navigation menu items
- `modifyHomeContent` - Change content on the home page
- `beforeRenderTemplate` - Modify template variables before rendering
- `afterUserRegistration` - Perform actions after a user registers

## Registering Hooks

```python
from plugin_system import PluginSystem

def my_hook_function(args):
    # Modify args or perform actions
    return args

def register_plugin():
    PluginSystem.register_hook('hookName', my_hook_function, 10, 'my_plugin')
```

The parameters for `register_hook` are:
- `hook_name`: The name of the hook to register for
- `callback`: The function to call when the hook is triggered
- `priority`: Optional priority (lower numbers run first, default 10)
- `plugin_name`: Name of the plugin registering the hook

## Adding Routes

Plugins can add their own routes using Flask Blueprints:

```python
from flask import Blueprint, render_template

# Create a blueprint
bp = Blueprint('my_plugin', __name__, url_prefix='/my-plugin')

@bp.route('/')
def index():
    return render_template('my_plugin/index.html')

def register_plugin():
    # Import app here to avoid circular imports
    from app import app
    app.register_blueprint(bp)
```

## Access Control

Plugins should implement appropriate access controls using Flask-Login decorators and role checks:

```python
from flask_login import login_required, current_user

@bp.route('/admin-only')
@login_required
def admin_only():
    if not current_user.is_admin():
        abort(403)
    return render_template('my_plugin/admin.html')
```

## Examples

See the existing plugins in the `plugins/` directory for examples:
- `welcome_plugin` - A simple plugin that adds content to the home page
- `copyedit_plugin` - A comprehensive plugin that adds copy editing functionality

## Troubleshooting

If your plugin isn't working as expected:

1. Check the application logs for error messages
2. Verify that your plugin's `register_plugin()` function is being called
3. Ensure that the hooks you're using exist in the core application
4. Check for circular imports or other Python errors