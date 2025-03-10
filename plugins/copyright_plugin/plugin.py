"""
Copyright Plugin

This plugin adds copyright management functionality to the journal system,
allowing administrators to set and display copyright notices, licensing information,
and manage rights for published articles.
"""
from datetime import datetime
import os

from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user

from flask import current_app
from plugin_system import PluginSystem

# Create a blueprint for the copyright plugin
bp = Blueprint('copyright', __name__, url_prefix='/copyright')

# Plugin metadata
__plugin_name__ = "Copyright Management"
__plugin_version__ = "1.0.0"
__plugin_author__ = "EasyJournal Team"
__plugin_description__ = "Adds copyright management functionality to the journal system"

@bp.route('/')
@login_required
def index():
    """Render the copyright management dashboard."""
    # Check if user has admin or editor role
    if not (current_user.is_admin() or current_user.is_editor()):
        abort(403)
    
    # Get license types and recent copyright records
    from plugins.copyright_plugin.models import Copyright, LicenseType
    licenses = LicenseType.query.all()
    recent_records = Copyright.query.order_by(Copyright.updated_at.desc()).limit(5).all()
    
    return render_template('copyright/dashboard.html',
                          licenses=licenses,
                          recent_records=recent_records)

@bp.route('/licenses/new', methods=['GET', 'POST'])
@login_required
def new_license():
    """Create a new license type."""
    if not current_user.is_admin():
        abort(403)
    
    # Form handling would go here
    return render_template('copyright/new_license.html')

@bp.route('/licenses/edit/<int:license_id>', methods=['GET', 'POST'])
@login_required
def edit_license(license_id):
    """Edit an existing license type."""
    if not current_user.is_admin():
        abort(403)
    
    from plugins.copyright_plugin.models import LicenseType
    license_type = LicenseType.query.get_or_404(license_id)
    # Form handling would go here
    return render_template('copyright/edit_license.html', license=license_type)

@bp.route('/records/<int:record_id>')
@login_required
def view_record(record_id):
    """View a copyright record."""
    if not (current_user.is_admin() or current_user.is_editor()):
        abort(403)
    
    from plugins.copyright_plugin.models import Copyright
    record = Copyright.query.get_or_404(record_id)
    return render_template('copyright/view_record.html', record=record)

@bp.route('/assign/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def assign_copyright(submission_id):
    """Assign copyright information to a submission."""
    if not (current_user.is_admin() or current_user.is_editor()):
        abort(403)
    
    from models import Submission
    submission = Submission.query.get_or_404(submission_id)
    # Form handling would go here
    return render_template('copyright/assign_copyright.html', submission=submission)

def add_footer_content(args):
    """
    Add copyright information to the footer.
    """
    content = args.get('content', '')
    
    # Get the current year
    current_year = datetime.now().year
    
    # Add copyright statement to the footer
    copyright_html = f"""
    <div class="copyright-notice text-center mt-3">
        <hr>
        <p class="text-muted">
            © {current_year} EasyJournal. All rights reserved.
            <br>
            <small>Powered by the EasyJournal Copyright Management Plugin</small>
        </p>
    </div>
    """
    
    args['content'] = content + copyright_html
    return args

def add_article_copyright_info(args):
    """
    Add copyright information to article detail pages.
    """
    if not args.get('submission'):
        return args
    
    from plugins.copyright_plugin.models import Copyright
    
    submission = args.get('submission')
    content = args.get('content', '')
    
    # Look up copyright record for this submission
    copyright_record = Copyright.query.filter_by(submission_id=submission.id).first()
    
    if copyright_record:
        copyright_html = f"""
        <div class="card mt-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h6 class="mb-0">Copyright Information</h6>
            </div>
            <div class="card-body">
                <p class="mb-1">© {copyright_record.year} {copyright_record.holder_name}</p>
                <p class="mb-1">Licensed under {copyright_record.license_type}</p>
                {copyright_record.rights_statement if copyright_record.rights_statement else ''}
            </div>
        </div>
        """
    else:
        copyright_html = f"""
        <div class="card mt-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h6 class="mb-0">Copyright Information</h6>
            </div>
            <div class="card-body">
                <p class="mb-0">© {datetime.now().year} All rights reserved.</p>
            </div>
        </div>
        """
    
    args['content'] = content + copyright_html
    return args

def add_navigation_items(args):
    """
    Add copyright management navigation items to the main navigation menu.
    """
    if not args.get('current_user') or not args.get('current_user').is_authenticated:
        return args
    
    nav_items = args.get('nav_items', [])
    current_user = args.get('current_user')
    
    # Add copyright management link for editors and admins
    if current_user.is_editor() or current_user.is_admin():
        nav_items.append({
            'url': '/copyright',
            'name': 'Copyright',
            'icon': 'bi bi-file-earmark-text'
        })
    
    args['nav_items'] = nav_items
    return args

def seed_license_types():
    """Seed database with common license types if they don't exist."""
    from flask import current_app
    from app import db
    from plugins.copyright_plugin.models import LicenseType
    
    licenses = [
        {
            'name': 'Creative Commons Attribution 4.0',
            'short_code': 'CC-BY-4.0',
            'description': 'This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator.',
            'url': 'https://creativecommons.org/licenses/by/4.0/'
        },
        {
            'name': 'Creative Commons Attribution-ShareAlike 4.0',
            'short_code': 'CC-BY-SA-4.0',
            'description': 'This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license requires that adaptations be shared under the same terms.',
            'url': 'https://creativecommons.org/licenses/by-sa/4.0/'
        },
        {
            'name': 'Creative Commons Attribution-NonCommercial 4.0',
            'short_code': 'CC-BY-NC-4.0',
            'description': 'This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format for noncommercial purposes only, and only so long as attribution is given to the creator.',
            'url': 'https://creativecommons.org/licenses/by-nc/4.0/'
        },
        {
            'name': 'All Rights Reserved',
            'short_code': 'ARR',
            'description': 'Traditional copyright protection. All rights reserved by the copyright holder.',
            'url': ''
        }
    ]
    
    # Add license types if they don't exist
    for license_data in licenses:
        existing = LicenseType.query.filter_by(short_code=license_data['short_code']).first()
        if not existing:
            new_license = LicenseType(
                name=license_data['name'],
                short_code=license_data['short_code'],
                description=license_data['description'],
                url=license_data['url']
            )
            db.session.add(new_license)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to seed license types: {str(e)}")

def register_plugin():
    """
    Register this plugin with the plugin system.
    This function is called when the plugin is loaded.
    """
    # Import current_app instead of app to avoid circular imports
    from flask import current_app
    from app import db
    
    # Register the blueprint
    current_app.register_blueprint(bp)
    
    # Register hooks
    PluginSystem.register_hook('getFooterContent', add_footer_content, 10, 'copyright_plugin')
    PluginSystem.register_hook('getArticleDetailContent', add_article_copyright_info, 10, 'copyright_plugin')
    PluginSystem.register_hook('getNavItems', add_navigation_items, 10, 'copyright_plugin')
    
    # Create database tables
    with current_app.app_context():
        db.create_all()
        seed_license_types()
    
    # Log that the plugin has been registered
    current_app.logger.info("Copyright plugin registered")