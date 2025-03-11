"""
Flask application initialization for the Academic Journal Submission System.

This module initializes the Flask application with necessary extensions.
"""

import os
import re
from flask import Flask, g, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from markupsafe import Markup, escape

import config


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


# Initialize extensions without app context
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure the application
    app.config['DEBUG'] = config.DEBUG
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    # Enhanced database connection handling for better reliability in deployment
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,  # Recycle connections every 5 minutes
        "pool_pre_ping": True,  # Verify connections before use
        "pool_size": 10,  # Number of connections to keep open
        "max_overflow": 15,  # Max number of connections to create beyond pool_size
        "echo": config.DEBUG,  # Log SQL in debug mode
        "connect_args": {
            "connect_timeout": 10  # Connection timeout in seconds
        }
    }
    
    # Add custom filter for converting newlines to <br>
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s is None:
            return ""
        # First escape any HTML to prevent XSS attacks
        s = escape(s)
        # Then convert newlines to <br>
        return Markup(re.sub(r'\r\n|\r|\n', '<br>', s))
    
    # Legacy color filter removed - no longer needed with simplified theme system
    
    # Add regex replace filter
    @app.template_filter('regex_replace')
    def regex_replace_filter(s, pattern, replacement):
        """Perform a regex replacement on a string."""
        if s is None:
            return ""
        import re
        return re.sub(pattern, replacement, s)
    
    # Add markdown filter for rendering markdown text
    @app.template_filter('markdown')
    def markdown_filter(s):
        """Convert Markdown text to HTML."""
        if s is None:
            return ""
        import markdown
        # Convert markdown to HTML and mark as safe
        return Markup(markdown.markdown(s))
    
    # Add custom context processor for templates
    @app.context_processor
    def utility_processor():
        return {
            'now': config.now,
            'DEMO_MODE': config.DEMO_MODE
        }
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.submission import submission_bp
    from routes.review import review_bp
    from routes.admin import admin_bp
    from routes.review_issues import issue_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(issue_bp)
    
    # User loader for flask-login
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load a user by ID for Flask-Login."""
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            app.logger.error(f"Error loading user: {str(e)}")
            db.session.rollback()
            return None
    
    # Cache for system settings (10 minute expiry)
    _system_settings_cache = {}
    _system_settings_cache_time = None
    _CACHE_DURATION = 600  # 10 minutes in seconds
    
    # Register a before_request handler to load system settings
    @app.before_request
    def load_system_settings():
        """Load system settings before handling any request."""
        from models import SystemSetting
        import time
        
        # Skip for static files and certain paths - expanded for improved performance
        if (request.path.startswith('/static') or 
            request.path.startswith('/css') or 
            request.path.startswith('/uploads') or
            request.path.startswith('/favicon') or
            request.path == '/favicon.ico'):
            return
            
        # Check if we need to refresh the cache
        # Move the expensive operations inside the refresh_cache condition
        if not hasattr(app, '_system_settings_cache_time') or not hasattr(app, '_system_settings_cache'):
            app._system_settings_cache_time = None
            app._system_settings_cache = {}
            
        current_time = time.time()
        refresh_cache = (app._system_settings_cache_time is None or 
                         current_time - app._system_settings_cache_time > _CACHE_DURATION)
        
        if refresh_cache:
            try:
                # Get all system settings in a single query - add optimization
                all_settings = SystemSetting.query.with_entities(
                    SystemSetting.setting_key, SystemSetting.setting_value
                ).all()
                # Update the cache - simplified
                app._system_settings_cache = dict(all_settings)
                app._system_settings_cache_time = current_time
            except Exception as e:
                app.logger.error(f"Error loading system settings: {str(e)}")
                db.session.rollback()
                # Create an empty cache if there's an error
                app._system_settings_cache = {}
                app._system_settings_cache_time = current_time
        
        # Helper function to get settings with default values
        def get_setting(key, default=None):
            return app._system_settings_cache.get(key, default)
        
        # Set default system theme
        g.system_theme = get_setting('theme', 'dark')
        
        # Load branding settings
        g.site_name = get_setting('site_name', 'EasyJournal')
        g.site_description = get_setting('site_description', 'A peer-reviewed academic journal')
        g.logo_url = get_setting('logo_url')
        g.use_logo_text = get_setting('use_logo_text')
        g.logo_text = get_setting('logo_text')
        # Fix banner URL path by ensuring it starts with a slash
        banner_url = get_setting('banner_url')
        if banner_url and not banner_url.startswith('/'):
            banner_url = '/' + banner_url
        g.banner_url = banner_url
        g.banner_title = get_setting('banner_title')
        g.banner_subtitle = get_setting('banner_subtitle')
        
        # Load content settings
        g.about_content = get_setting('about_content')
        g.submission_guidelines = get_setting('submission_guidelines')
        g.review_policy = get_setting('review_policy')
        g.ethics_policy = get_setting('ethics_policy')
        g.author_guidelines = get_setting('author_guidelines')
        g.contact_email = get_setting('contact_email')
        g.contact_phone = get_setting('contact_phone')
        g.contact_address = get_setting('contact_address')
        g.twitter_url = get_setting('twitter_url')
        g.facebook_url = get_setting('facebook_url')
        g.linkedin_url = get_setting('linkedin_url')
        
        # Load support hours
        g.support_hours_weekday = get_setting('support_hours_weekday', '9:00 AM - 6:00 PM (EST)')
        g.support_hours_saturday = get_setting('support_hours_saturday', '10:00 AM - 2:00 PM (EST)')
        g.support_hours_sunday = get_setting('support_hours_sunday', 'Closed')
        g.urgent_email = get_setting('urgent_email', 'urgent@easyjournal.org')
    
    @app.before_request
    def check_gdpr_consent():
        """Check if the user has given GDPR consent."""
        from flask_login import current_user
        from flask import render_template, make_response, redirect, url_for
        
        # Skip for static files, auth routes, and certain paths
        if (request.path.startswith('/static') or 
            request.path.startswith('/css') or 
            request.path.startswith('/uploads') or
            request.path.startswith('/favicon') or
            request.path == '/favicon.ico' or
            request.path.startswith('/auth') or  # Allow all auth routes
            request.endpoint == 'main.index'):  # Allow access to home page
            return
        
        # Only check authenticated users - early return if not authenticated
        if not current_user.is_authenticated:
            return
            
        # Early return if user has already given consent (checked first to avoid 
        # the more expensive operations below)
        if hasattr(current_user, 'has_given_consent') and current_user.has_given_consent():
            return
            
        # Helper function to get settings with default values - reusing the one from load_system_settings
        def get_setting(key, default=None):
            return app._system_settings_cache.get(key, default) if hasattr(app, '_system_settings_cache') else default
            
        # Get GDPR settings
        require_consent = get_setting('gdpr_require_existing_consent', 'true') == 'true'
        
        # Early return if consent is not required
        if not require_consent:
            return
            
        # Skip for the consent endpoint itself
        if request.endpoint == 'auth.provide_consent':
            return
        
        # Get consent text and privacy policy from settings
        # Use the default values from config.py (moved there to improve this function's performance)
        consent_text = get_setting('gdpr_consent_text', config.DEFAULT_CONSENT_TEXT)
        privacy_policy = get_setting('gdpr_privacy_policy', config.DEFAULT_PRIVACY_POLICY)
        
        # If it's an AJAX request, return a 403 status with a message
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'error': 'GDPR consent required'}, 403
        
        # Render consent template and show
        g.show_consent_modal = True
        g.consent_text = Markup(consent_text.replace('\n', '<br>'))
        g.privacy_policy = privacy_policy
    
    @app.before_request
    def track_visitor():
        """Track visitor information for analytics."""
        # Skip visitor tracking in deployment if there are issues with it
        # This makes sure login still works even if tracking doesn't
        try:
            # Skip tracking for static files and certain paths - expanded list for better performance
            if (request.path.startswith('/static') or 
                request.path.startswith('/css') or 
                request.path.startswith('/uploads') or
                request.path.startswith('/favicon') or
                request.path == '/favicon.ico' or
                # Don't track admin routes to reduce database load
                request.path.startswith('/admin') or
                # Don't track health check or ping endpoints
                request.path == '/ping' or
                request.path == '/health'):
                return
                
            # Import only if needed (after path exclusion check)
            from models import VisitorLog, ArticleView
            from flask_login import current_user
            from flask import session
            import re
            import time
            
            # Limit tracking frequency to reduce database load
            # Only track once per session, or once every 10 minutes for the same path
            session_key = f'tracked_{request.path}'
            
            # Initialize tracking session data if not present
            if 'last_tracked_time' not in session:
                session['last_tracked_time'] = {}

            current_time = time.time()
            
            # Check if this path was tracked in this session - avoid tracking duplicates
            if session_key in session and current_time - session.get('last_tracked_time', {}).get(request.path, 0) <= 600:
                return  # Skip tracking for this request
                
            # Update session tracking info
            session[session_key] = True
            if 'last_tracked_time' not in session:
                session['last_tracked_time'] = {}
            session['last_tracked_time'][request.path] = current_time
            session.modified = True
            
            # Use a separate thread or deferred task for tracking to avoid slowing down the response
            # For now, we'll optimize the DB operations
            
            # Check if this is an article view - only do this check once
            is_article_view = bool(re.match(r'/articles/(\d+)', request.path))
            submission_id = None
            if is_article_view:
                submission_id = int(re.match(r'/articles/(\d+)', request.path).group(1))
            
            # Create visitor log entry - only store essential data
            visitor_log = VisitorLog(
                user_id=current_user.id if current_user.is_authenticated else None,
                ip_address=request.remote_addr,
                user_agent=None,  # Omit user agent to reduce data storage
                path=request.path,
                referer=None  # Omit referer to reduce data storage
            )
            
            # If it's an article view, create that record too
            if is_article_view and submission_id:
                article_view = ArticleView(
                    submission_id=submission_id,
                    user_id=current_user.id if current_user.is_authenticated else None,
                    ip_address=request.remote_addr
                )
                db.session.add(article_view)
            
            db.session.add(visitor_log)
            
            # Commit but don't let errors block the request
            try:
                db.session.commit()
            except Exception as tracking_error:
                # Log the error but don't let it affect user experience
                app.logger.error(f"Visitor tracking error: {str(tracking_error)}")
                db.session.rollback()
                
        except Exception as e:
            # If any error occurs in the whole visitor tracking process, 
            # log it but don't interrupt the request
            app.logger.error(f"Failed to initialize visitor tracking: {str(e)}")
            # We don't need to rollback as we're catching at function level
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
        # Seed test accounts if in demo mode
        if config.DEMO_MODE:
            seed_test_accounts(app)
            
        # Initialize system settings if needed
        from models import SystemSetting
        if not SystemSetting.query.filter_by(setting_key='theme').first():
            SystemSetting.set_value('theme', 'dark')
            
        # Initialize and load plugins
        from plugin_system import init_plugin_system
        loaded_plugins = init_plugin_system()
        app.logger.info(f"Loaded plugins: {', '.join(loaded_plugins) if loaded_plugins else 'None'}")
    
    return app


def seed_test_accounts(app):
    """Seed test accounts if they don't exist."""
    from models import User, ROLE_ADMIN, ROLE_EDITOR, ROLE_REVIEWER, ROLE_AUTHOR
    
    with app.app_context():
        # Create test accounts if they don't exist
        for role, account in config.TEST_ACCOUNTS.items():
            email = account['email']
            user = User.query.filter_by(email=email).first()
            
            if not user:
                if role == 'admin':
                    role_type = ROLE_ADMIN
                elif role == 'editor':
                    role_type = ROLE_EDITOR
                elif role == 'reviewer':
                    role_type = ROLE_REVIEWER
                else:
                    role_type = ROLE_AUTHOR
                
                user = User(
                    name=account['name'],
                    email=email,
                    password=account['password'],
                    role=role_type,
                    institution=f"{role.capitalize()} Institution",
                    bio=f"This is a test {role} account."
                )
                db.session.add(user)
                db.session.commit()
                
                app.logger.info(f"Created test {role} account: {email}")
            else:
                app.logger.info(f"Test {role} account already exists: {email}")


# Create the global application instance
app = create_app()