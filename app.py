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
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 15,
        "echo": False,
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
    
    # Add custom filter for converting hex color to RGB values
    @app.template_filter('int_to_rgb')
    def int_to_rgb_filter(i):
        """Convert an integer color value to comma-separated RGB values."""
        if not isinstance(i, int):
            return "0, 0, 0"
        r = (i >> 16) & 255
        g = (i >> 8) & 255
        b = i & 255
        return f"{r}, {g}, {b}"
    
    # Add regex replace filter
    @app.template_filter('regex_replace')
    def regex_replace_filter(s, pattern, replacement):
        """Perform a regex replacement on a string."""
        if s is None:
            return ""
        import re
        return re.sub(pattern, replacement, s)
    
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
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    
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
        
        # Skip for static files and certain paths
        if (request.path.startswith('/static') or 
            request.path.startswith('/css') or 
            request.path == '/favicon.ico'):
            return
            
        # Check if we need to refresh the cache
        current_time = time.time()
        refresh_cache = (_system_settings_cache_time is None or 
                         current_time - _system_settings_cache_time > _CACHE_DURATION)
        
        if refresh_cache:
            try:
                # Get all system settings in a single query
                all_settings = SystemSetting.query.all()
                # Update the cache
                app._system_settings_cache = {s.setting_key: s.setting_value for s in all_settings}
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
        g.primary_color = get_setting('primary_color')
        g.secondary_color = get_setting('secondary_color')
        g.accent_color = get_setting('accent_color')
        g.logo_url = get_setting('logo_url')
        g.use_logo_text = get_setting('use_logo_text')
        g.logo_text = get_setting('logo_text')
        g.banner_url = get_setting('banner_url')
        g.banner_title = get_setting('banner_title')
        g.banner_subtitle = get_setting('banner_subtitle')
        g.override_theme = get_setting('override_theme') == 'true'
        
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
    
    @app.before_request
    def check_gdpr_consent():
        """Check if the user has given GDPR consent."""
        from flask_login import current_user
        from flask import render_template, make_response, redirect, url_for
        
        # Skip for static files, auth routes, and certain paths
        if (request.path.startswith('/static') or 
            request.path.startswith('/css') or 
            request.path == '/favicon.ico' or
            request.path.startswith('/auth') or  # Allow all auth routes
            request.endpoint == 'main.index'):  # Allow access to home page
            return
        
        # Only check authenticated users
        if current_user.is_authenticated:
            # Helper function to get settings with default values - reusing the one from load_system_settings
            def get_setting(key, default=None):
                return app._system_settings_cache.get(key, default) if hasattr(app, '_system_settings_cache') else default
                
            # Get GDPR settings
            require_consent = get_setting('gdpr_require_existing_consent', 'true') == 'true'
            
            # Check if user has consented or consent is not required
            if not current_user.has_given_consent() and require_consent:
                # Skip for the consent endpoint itself
                if request.endpoint == 'auth.provide_consent':
                    return
                
                # Get consent text and privacy policy from settings
                default_consent_text = """We value your privacy.
EasyJournal collects and processes your personal data (name, email, affiliation) to manage your submissions, peer review process, and publish your articles. By continuing, you consent to our storage and use of your data as described in our Privacy Policy. You can withdraw consent or request data removal at any time."""
                
                default_privacy_policy = """# Privacy Policy

## What data we collect
EasyJournal collects and stores the following information:
- Name, email address, and institutional affiliation
- Submission content and metadata
- Review comments and decisions
- User activity for system functionality

## How we use your data
Your data is used exclusively for:
- Managing the journal submission and review process
- Publishing accepted articles
- Providing personalized user experience
- Improving our services

## Your rights
Under GDPR, you have the right to:
- Access your personal data
- Request correction of inaccurate data
- Request deletion of your data
- Object to processing of your data
- Request restriction of processing
- Data portability
- Lodge complaints with supervisory authorities

## Data retention
We keep your data for as long as necessary to provide our services and comply with legal obligations.

## Contact
For any privacy-related inquiries, please contact the journal administration."""
                
                consent_text = get_setting('gdpr_consent_text', default_consent_text)
                privacy_policy = get_setting('gdpr_privacy_policy', default_privacy_policy)
                
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
        from models import VisitorLog, ArticleView
        from flask_login import current_user
        from flask import session
        import re
        import time
        
        # Skip tracking for static files and certain paths
        if (request.path.startswith('/static') or 
            request.path.startswith('/css') or 
            request.path == '/favicon.ico'):
            return
            
        # Limit tracking frequency to reduce database load
        # Only track once per session, or once every 10 minutes for the same path
        session_key = f'tracked_{request.path}'
        
        # Initialize tracking session data if not present
        if 'last_tracked_time' not in session:
            session['last_tracked_time'] = {}

        current_time = time.time()
        should_track = False
        
        # Check if this path was tracked in this session
        if session_key not in session or current_time - session.get('last_tracked_time', {}).get(request.path, 0) > 600:
            should_track = True
            session[session_key] = True
            session['last_tracked_time'][request.path] = current_time
            session.modified = True
        
        if should_track:
            # Create visitor log entry
            visitor_log = VisitorLog(
                user_id=current_user.id if current_user.is_authenticated else None,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string if request.user_agent else None,
                path=request.path,
                referer=request.referrer
            )
            
            # Check if this is an article view
            article_match = re.match(r'/articles/(\d+)', request.path)
            if article_match:
                submission_id = int(article_match.group(1))
                article_view = ArticleView(
                    submission_id=submission_id,
                    user_id=current_user.id if current_user.is_authenticated else None,
                    ip_address=request.remote_addr
                )
                db.session.add(article_view)
            
            db.session.add(visitor_log)
            try:
                db.session.commit()
            except:
                # Don't let tracking errors affect the user experience
                db.session.rollback()
    
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