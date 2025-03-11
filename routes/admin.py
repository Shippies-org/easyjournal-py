"""
Admin routes for the Academic Journal Submission System.

This module handles administrative functions such as user management and system settings.
"""

from datetime import datetime, timedelta
import json
from collections import Counter
from sqlalchemy import func, desc

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, g, current_app
from flask_login import login_required, current_user

from app import db
from models import User, Submission, Review, Issue, Publication, PluginSetting, SystemSetting, VisitorLog, ArticleView, UserActivity
from forms.admin import UserForm, IssueForm, PublicationForm, PluginSettingForm
from forms.doi import DOIHealthCheckForm
from forms.branding import BrandingForm, ContentSettingsForm
from forms.gdpr import ConsentSettingsForm, DataExportRequestForm, DataDeletionRequestForm
from services.doi_service import DOIService

# Create a blueprint for admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Admin access decorator
def admin_required(func):
    """Decorator to require admin role."""
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            flash('You must be an administrator to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    
    # Preserve the function's metadata
    decorated_view.__name__ = func.__name__
    decorated_view.__doc__ = func.__doc__
    
    return decorated_view


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Render the admin dashboard."""
    # Get counts for dashboard statistics
    user_count = User.query.count()
    submission_count = Submission.query.count()
    review_count = Review.query.count()
    issue_count = Issue.query.count()
    
    # Get user counts by role
    admin_count = User.query.filter_by(role='admin').count()
    editor_count = User.query.filter_by(role='editor').count()
    reviewer_count = User.query.filter_by(role='reviewer').count()
    author_count = User.query.filter_by(role='author').count()
    
    # Get submission counts by status
    submitted_count = Submission.query.filter_by(status='submitted').count()
    in_review_count = Submission.query.filter_by(status='in_review').count()
    accepted_count = Submission.query.filter_by(status='accepted').count()
    rejected_count = Submission.query.filter_by(status='rejected').count()
    
    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        user_count=user_count,
        submission_count=submission_count,
        review_count=review_count,
        issue_count=issue_count,
        admin_count=admin_count,
        editor_count=editor_count,
        reviewer_count=reviewer_count,
        author_count=author_count,
        submitted_count=submitted_count,
        in_review_count=in_review_count,
        accepted_count=accepted_count,
        rejected_count=rejected_count
    )


@admin_bp.route('/users')
@admin_required
def users():
    """Render the user management page."""
    users = User.query.order_by(User.name).all()
    return render_template('admin/users.html', title='User Management', users=users)


@admin_bp.route('/user/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    """Create a new user."""
    form = UserForm()
    
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already in use.', 'danger')
        else:
            # Create new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                role=form.role.data,
                institution=form.institution.data,
                bio=form.bio.data
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('User created successfully.', 'success')
            return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', title='New User', form=form)


@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit an existing user."""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        # Check if email already exists and it's not this user's email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.id != user_id:
            flash('Email address already in use.', 'danger')
        else:
            # Update user data
            user.name = form.name.data
            user.email = form.email.data
            user.role = form.role.data
            user.institution = form.institution.data
            user.bio = form.bio.data
            
            # Only update password if provided
            if form.password.data:
                user.set_password(form.password.data)
            
            db.session.commit()
            
            flash('User updated successfully.', 'success')
            return redirect(url_for('admin.users'))
    
    # Don't fill in the password field for security
    form.password.data = ''
    
    return render_template('admin/user_form.html', title='Edit User', form=form, user=user)


@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    # Consider adding more checks here to handle user data cleanup
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/issues')
@admin_required
def issues():
    """Render the issue management page."""
    issues = Issue.query.order_by(Issue.volume.desc(), Issue.issue_number.desc()).all()
    return render_template('admin/issues.html', title='Issue Management', issues=issues)


@admin_bp.route('/issue/new', methods=['GET', 'POST'])
@admin_required
def new_issue():
    """Create a new journal issue."""
    form = IssueForm()
    
    if form.validate_on_submit():
        # Check if volume/issue combination already exists
        existing_issue = Issue.query.filter_by(
            volume=form.volume.data,
            issue_number=form.issue_number.data
        ).first()
        
        if existing_issue:
            flash('An issue with this volume and number already exists.', 'danger')
        else:
            # Create new issue
            issue = Issue(
                volume=form.volume.data,
                issue_number=form.issue_number.data,
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                publication_date=form.publication_date.data
            )
            
            db.session.add(issue)
            db.session.commit()
            
            flash('Issue created successfully.', 'success')
            return redirect(url_for('admin.issues'))
    
    return render_template('admin/issue_form.html', title='New Issue', form=form)


@admin_bp.route('/issue/edit/<int:issue_id>', methods=['GET', 'POST'])
@admin_required
def edit_issue(issue_id):
    """Edit an existing journal issue."""
    issue = Issue.query.get_or_404(issue_id)
    form = IssueForm(obj=issue)
    
    if form.validate_on_submit():
        # Check if volume/issue combination already exists and it's not this issue
        existing_issue = Issue.query.filter_by(
            volume=form.volume.data,
            issue_number=form.issue_number.data
        ).first()
        
        if existing_issue and existing_issue.id != issue_id:
            flash('An issue with this volume and number already exists.', 'danger')
        else:
            # Update issue data
            issue.volume = form.volume.data
            issue.issue_number = form.issue_number.data
            issue.title = form.title.data
            issue.description = form.description.data
            issue.status = form.status.data
            issue.publication_date = form.publication_date.data
            
            db.session.commit()
            
            flash('Issue updated successfully.', 'success')
            return redirect(url_for('admin.issues'))
    
    return render_template('admin/issue_form.html', title='Edit Issue', form=form, issue=issue)


@admin_bp.route('/issue/delete/<int:issue_id>', methods=['POST'])
@admin_required
def delete_issue(issue_id):
    """Delete a journal issue."""
    issue = Issue.query.get_or_404(issue_id)
    
    # Check if there are publications in this issue
    has_publications = Publication.query.filter_by(issue_id=issue_id).first() is not None
    
    if has_publications:
        flash('Cannot delete an issue that contains publications.', 'danger')
    else:
        db.session.delete(issue)
        db.session.commit()
        flash('Issue deleted successfully.', 'success')
    
    return redirect(url_for('admin.issues'))


@admin_bp.route('/issue/<int:issue_id>/publications')
@admin_required
def issue_publications(issue_id):
    """Manage publications in an issue."""
    issue = Issue.query.get_or_404(issue_id)
    publications = Publication.query.filter_by(issue_id=issue_id).all()
    
    # Get accepted submissions that aren't published in any issue
    published_submission_ids = [p.submission_id for p in Publication.query.all()]
    available_submissions = Submission.query.filter_by(status='accepted').filter(
        ~Submission.id.in_(published_submission_ids) if published_submission_ids else True
    ).all()
    
    return render_template(
        'admin/issue_publications.html',
        title=f'Publications in Volume {issue.volume}, Issue {issue.issue_number}',
        issue=issue,
        publications=publications,
        available_submissions=available_submissions
    )


@admin_bp.route('/issue/<int:issue_id>/publication/add', methods=['GET', 'POST'])
@admin_required
def add_publication(issue_id):
    """Add a publication to an issue."""
    issue = Issue.query.get_or_404(issue_id)
    form = PublicationForm()
    
    # Get accepted submissions that aren't published in any issue
    published_submission_ids = [p.submission_id for p in Publication.query.all()]
    available_submissions = Submission.query.filter_by(status='accepted').filter(
        ~Submission.id.in_(published_submission_ids) if published_submission_ids else True
    ).all()
    
    form.submission_id.choices = [(s.id, s.title) for s in available_submissions]
    
    if form.validate_on_submit():
        # Create new publication
        publication = Publication(
            submission_id=form.submission_id.data,
            issue_id=issue_id,
            page_start=form.page_start.data,
            page_end=form.page_end.data
        )
        
        # Update submission status
        submission = Submission.query.get(form.submission_id.data)
        submission.status = 'published'
        
        db.session.add(publication)
        db.session.commit()
        
        flash('Publication added successfully.', 'success')
        return redirect(url_for('admin.issue_publications', issue_id=issue_id))
    
    return render_template(
        'admin/publication_form.html',
        title='Add Publication',
        form=form,
        issue=issue
    )


@admin_bp.route('/plugins')
@admin_required
def plugins():
    """Render the plugin management page."""
    # Get all plugin settings from database
    plugin_settings = PluginSetting.query.order_by(PluginSetting.plugin_name, PluginSetting.setting_key).all()
    
    # Get all loaded plugins from the plugin system
    from plugin_system import PluginSystem
    loaded_plugins_info = PluginSystem.get_plugin_info()
    
    # Group settings by plugin
    plugins_data = {}
    
    # First add all loaded plugins (even if they have no settings)
    for plugin_name, plugin_info in loaded_plugins_info.items():
        plugins_data[plugin_name] = {
            'info': plugin_info,
            'settings': []
        }
    
    # Then add any settings for plugins
    for setting in plugin_settings:
        if setting.plugin_name not in plugins_data:
            # Create entry for plugins with settings but not loaded
            plugins_data[setting.plugin_name] = {
                'info': {'name': setting.plugin_name, 'path': '', 'hooks': []},
                'settings': []
            }
        
        # Add this setting to the plugin
        plugins_data[setting.plugin_name]['settings'].append(setting)
    
    return render_template('admin/plugins.html', title='Plugin Management', plugins=plugins_data)


@admin_bp.route('/plugin/setting/edit/<int:setting_id>', methods=['GET', 'POST'])
@admin_required
def edit_plugin_setting(setting_id):
    """Edit a plugin setting."""
    setting = PluginSetting.query.get_or_404(setting_id)
    form = PluginSettingForm(obj=setting)
    
    if form.validate_on_submit():
        # Update setting
        setting.setting_value = form.setting_value.data
        db.session.commit()
        
        flash('Plugin setting updated successfully.', 'success')
        return redirect(url_for('admin.plugins'))
    
    return render_template(
        'admin/plugin_setting_form.html',
        title=f'Edit {setting.plugin_name} Setting',
        form=form,
        setting=setting
    )


@admin_bp.route('/set-system-theme/<theme>')
@admin_required
def set_system_theme(theme):
    """Set the system-wide theme."""
    valid_themes = ['dark', 'light', 'journal', 'modern', 'elegant', 'high-contrast']
    
    if theme not in valid_themes:
        flash('Invalid theme selected.', 'danger')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    try:
        # Update or create the system theme setting
        SystemSetting.set_value('theme', theme)
        flash(f'System theme set to {theme.capitalize()}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error setting system theme: {str(e)}', 'danger')
    
    # Redirect back to the referring page
    return redirect(request.referrer or url_for('admin.dashboard'))


@admin_bp.route('/doi-health-check', methods=['GET', 'POST'])
@admin_required
def doi_health_check():
    """DOI health check tool for CrossRef and DataCite integration."""
    form = DOIHealthCheckForm()
    report = None
    
    if form.validate_on_submit():
        try:
            organization_id = form.organization_id.data
            service = form.service.data
            
            # Get the health report from the DOI service
            report = DOIService.get_health_report(organization_id, service)
            
            if report.get('error'):
                flash(f"Error: {report['error']}", 'danger')
            else:
                flash('Health check completed successfully.', 'success')
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error performing DOI health check: {str(e)}', 'danger')
    
    return render_template(
        'admin/doi_health.html',
        title='DOI Health Check',
        form=form,
        report=report
    )


@admin_bp.route('/branding', methods=['GET', 'POST'])
@admin_required
def branding_settings():
    """Manage journal branding settings."""
    # Initialize branding form with current settings
    branding_form = BrandingForm()
    content_form = ContentSettingsForm()
    
    # Get current logo and banner URLs if they exist
    logo_url = SystemSetting.get_value('logo_url')
    banner_url = SystemSetting.get_value('banner_url')
    print(f"Current banner_url from database: {banner_url}")
    
    # Fill form with existing values
    if request.method == 'GET':
        branding_form.site_name.data = SystemSetting.get_value('site_name', 'Academic Journal')
        branding_form.site_description.data = SystemSetting.get_value('site_description', 'A peer-reviewed academic journal')
        branding_form.primary_color.data = SystemSetting.get_value('primary_color')
        branding_form.secondary_color.data = SystemSetting.get_value('secondary_color')
        branding_form.accent_color.data = SystemSetting.get_value('accent_color')
        branding_form.use_logo_text.data = SystemSetting.get_value('use_logo_text') == 'true'
        branding_form.logo_text.data = SystemSetting.get_value('logo_text')
        branding_form.banner_title.data = SystemSetting.get_value('banner_title')
        branding_form.banner_subtitle.data = SystemSetting.get_value('banner_subtitle')
        branding_form.override_theme.data = SystemSetting.get_value('override_theme') == 'true'
        # Get gradient options
        branding_form.use_navbar_gradient.data = SystemSetting.get_value('use_navbar_gradient') == 'true'
        branding_form.gradient_direction.data = SystemSetting.get_value('gradient_direction', 'to right')
        branding_form.gradient_from_color.data = SystemSetting.get_value('gradient_from_color')
        branding_form.gradient_to_color.data = SystemSetting.get_value('gradient_to_color')
    
    # Process branding form submission
    if request.method == 'POST' and branding_form.validate_on_submit():
        try:
            # Update text-based settings
            SystemSetting.set_value('site_name', branding_form.site_name.data)
            SystemSetting.set_value('site_description', branding_form.site_description.data)
            SystemSetting.set_value('primary_color', branding_form.primary_color.data)
            SystemSetting.set_value('secondary_color', branding_form.secondary_color.data)
            SystemSetting.set_value('accent_color', branding_form.accent_color.data)
            SystemSetting.set_value('use_logo_text', 'true' if branding_form.use_logo_text.data else 'false')
            SystemSetting.set_value('logo_text', branding_form.logo_text.data)
            SystemSetting.set_value('banner_title', branding_form.banner_title.data)
            SystemSetting.set_value('banner_subtitle', branding_form.banner_subtitle.data)
            SystemSetting.set_value('override_theme', 'true' if branding_form.override_theme.data else 'false')
            
            # Save gradient settings
            SystemSetting.set_value('use_navbar_gradient', 'true' if branding_form.use_navbar_gradient.data else 'false')
            SystemSetting.set_value('gradient_direction', branding_form.gradient_direction.data)
            SystemSetting.set_value('gradient_from_color', branding_form.gradient_from_color.data)
            SystemSetting.set_value('gradient_to_color', branding_form.gradient_to_color.data)
            
            # Handle logo upload if provided
            logo_file = branding_form.custom_logo.data
            if logo_file and logo_file.filename:
                # Print debug information
                print(f"Logo file received: {logo_file.filename}")
                
                filename = secure_filename(logo_file.filename)
                # Create timestamp to prevent browser caching
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # Ensure uploads directory exists
                upload_dir = os.path.join('uploads', 'branding')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Define the file path
                filepath = os.path.join(upload_dir, filename)
                save_path = filepath  # Actual path to save the file
                
                # Create a URL path that's properly accessible in templates
                url_path = f"/uploads/branding/{filename}"
                
                try:
                    # Save file
                    logo_file.save(save_path)
                    print(f"Logo file saved to: {save_path}")
                    
                    # Update database with URL path (not file system path)
                    SystemSetting.set_value('logo_url', url_path)
                    # Update logo_url for template rendering
                    logo_url = url_path
                    print(f"Logo URL set to: {url_path}")
                except Exception as e:
                    print(f"Error saving logo file: {str(e)}")
                    flash(f"Error saving logo image: {str(e)}", "danger")
            
            # Handle banner upload if provided
            banner_file = branding_form.banner_image.data
            if banner_file and banner_file.filename:
                # Print debug information
                print(f"Banner file received: {banner_file.filename}")
                
                filename = secure_filename(banner_file.filename)
                # Create timestamp to prevent browser caching
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # Ensure uploads directory exists
                upload_dir = os.path.join('uploads', 'branding')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Define the file path
                filepath = os.path.join(upload_dir, filename)
                save_path = filepath  # Actual path to save the file
                
                # Create a URL path that's properly accessible in templates
                url_path = f"/uploads/branding/{filename}"
                
                try:
                    # Save file
                    banner_file.save(save_path)
                    print(f"Banner file saved to: {save_path}")
                    
                    # Update database with URL path (not file system path)
                    SystemSetting.set_value('banner_url', url_path)
                    # Update banner_url for template rendering
                    banner_url = url_path
                    print(f"Banner URL set to: {url_path}")
                except Exception as e:
                    print(f"Error saving banner file: {str(e)}")
                    flash(f"Error saving banner image: {str(e)}", "danger")
            
            flash('Branding settings updated successfully.', 'success')
            return redirect(url_for('admin.branding_settings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating branding settings: {str(e)}', 'danger')
    
    return render_template(
        'admin/branding.html',
        title='Branding Settings',
        branding_form=branding_form,
        content_form=content_form,
        logo_url=logo_url,
        banner_url=banner_url
    )


@admin_bp.route('/content', methods=['GET', 'POST'])
@admin_required
def content_settings():
    """Manage journal content and policies."""
    form = ContentSettingsForm()
    
    # Fill form with existing values
    if request.method == 'GET':
        form.about_content.data = SystemSetting.get_value('about_content', 'About our journal...')
        form.submission_guidelines.data = SystemSetting.get_value('submission_guidelines', 'Guidelines for submission...')
        form.review_policy.data = SystemSetting.get_value('review_policy', 'Our review policy...')
        form.ethics_policy.data = SystemSetting.get_value('ethics_policy', 'Our ethics policy...')
        form.author_guidelines.data = SystemSetting.get_value('author_guidelines', 'Guidelines for authors...')
        form.contact_email.data = SystemSetting.get_value('contact_email', 'contact@example.com')
        form.contact_phone.data = SystemSetting.get_value('contact_phone')
        form.contact_address.data = SystemSetting.get_value('contact_address')
        form.twitter_url.data = SystemSetting.get_value('twitter_url')
        form.facebook_url.data = SystemSetting.get_value('facebook_url')
        form.linkedin_url.data = SystemSetting.get_value('linkedin_url')
    
    if form.validate_on_submit():
        try:
            # Update content settings
            SystemSetting.set_value('about_content', form.about_content.data)
            SystemSetting.set_value('submission_guidelines', form.submission_guidelines.data)
            SystemSetting.set_value('review_policy', form.review_policy.data)
            SystemSetting.set_value('ethics_policy', form.ethics_policy.data)
            SystemSetting.set_value('author_guidelines', form.author_guidelines.data)
            SystemSetting.set_value('contact_email', form.contact_email.data)
            SystemSetting.set_value('contact_phone', form.contact_phone.data)
            SystemSetting.set_value('contact_address', form.contact_address.data)
            SystemSetting.set_value('twitter_url', form.twitter_url.data)
            SystemSetting.set_value('facebook_url', form.facebook_url.data)
            SystemSetting.set_value('linkedin_url', form.linkedin_url.data)
            
            flash('Content settings updated successfully.', 'success')
            return redirect(url_for('admin.branding_settings', _anchor='content'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating content settings: {str(e)}', 'danger')
    
    # Redirect to the branding page with content tab active
    return redirect(url_for('admin.branding_settings', _anchor='content'))


@admin_bp.route('/analytics')
@admin_required
def analytics_default():
    """Redirect to default analytics period."""
    return redirect(url_for('admin.analytics', period='week'))


@admin_bp.route('/gdpr', methods=['GET', 'POST'])
@admin_required
def gdpr_settings():
    """Manage GDPR consent settings."""
    # Initialize the consent settings form
    form = ConsentSettingsForm()
    
    # Get current consent message
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
    
    # Fill form with existing values on GET
    if request.method == 'GET':
        form.consent_text.data = SystemSetting.get_value('gdpr_consent_text', default_consent_text)
        form.privacy_policy.data = SystemSetting.get_value('gdpr_privacy_policy', default_privacy_policy)
        form.require_existing_users_consent.data = SystemSetting.get_value('gdpr_require_existing_consent', 'true') == 'true'
    
    # Handle form submission
    if form.validate_on_submit():
        try:
            # Save settings
            SystemSetting.set_value('gdpr_consent_text', form.consent_text.data)
            SystemSetting.set_value('gdpr_privacy_policy', form.privacy_policy.data)
            SystemSetting.set_value('gdpr_require_existing_consent', 
                                   'true' if form.require_existing_users_consent.data else 'false')
            
            flash('GDPR settings updated successfully.', 'success')
            return redirect(url_for('admin.gdpr_settings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating GDPR settings: {str(e)}', 'danger')
    
    # Get user consent statistics
    total_users = User.query.count()
    consented_users = User.query.filter_by(consent_given=True).count()
    consent_percentage = round((consented_users / total_users) * 100) if total_users > 0 else 0
    
    # Prepare data for the template
    data_export_form = DataExportRequestForm()
    data_deletion_form = DataDeletionRequestForm()
    
    return render_template(
        'admin/gdpr_settings.html',
        title='GDPR Compliance Settings',
        form=form,
        data_export_form=data_export_form,
        data_deletion_form=data_deletion_form,
        total_users=total_users,
        consented_users=consented_users,
        consent_percentage=consent_percentage
    )


@admin_bp.route('/gdpr/export', methods=['POST'])
@admin_required
def export_user_data():
    """Handle user data export requests."""
    form = DataExportRequestForm()
    
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash(f'No user found with email: {email}', 'danger')
            return redirect(url_for('admin.gdpr_settings'))
        
        try:
            # Prepare user data export (basic info for demo)
            data = {
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'institution': user.institution,
                    'bio': user.bio,
                    'created_at': user.created_at.isoformat() if user.created_at else None,
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'consent_given': user.consent_given,
                    'consent_timestamp': user.consent_timestamp.isoformat() if user.consent_timestamp else None
                },
                'submissions': [],
                'reviews': [],
                'activities': []
            }
            
            # Add submission data
            for submission in user.submissions:
                data['submissions'].append({
                    'id': submission.id,
                    'title': submission.title,
                    'status': submission.status,
                    'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None
                })
            
            # Add review data
            for review in user.reviews_given:
                data['reviews'].append({
                    'id': review.id,
                    'submission_id': review.submission_id,
                    'status': review.status,
                    'assigned_at': review.assigned_at.isoformat() if review.assigned_at else None,
                    'completed_at': review.completed_at.isoformat() if review.completed_at else None
                })
            
            # Add activity data
            for activity in user.activities:
                data['activities'].append({
                    'id': activity.id,
                    'activity_type': activity.activity_type,
                    'timestamp': activity.timestamp.isoformat() if activity.timestamp else None
                })
            
            # Log this action
            activity = UserActivity(
                user_id=current_user.id,
                activity_type='data_export',
                details=json.dumps({'target_user_id': user.id, 'target_email': user.email})
            )
            db.session.add(activity)
            db.session.commit()
            
            # In a real implementation, you would:
            # 1. Generate a more comprehensive data export
            # 2. Create a downloadable file (CSV, JSON, etc.)
            # 3. Potentially email the file to the user or admin
            
            flash(f'Data export for {user.name} ({user.email}) has been processed.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error exporting user data: {str(e)}', 'danger')
    
    return redirect(url_for('admin.gdpr_settings'))


@admin_bp.route('/gdpr/delete', methods=['POST'])
@admin_required
def delete_user_data():
    """Handle user data deletion requests."""
    form = DataDeletionRequestForm()
    
    if form.validate_on_submit():
        if not form.confirmation.data:
            flash('You must confirm the deletion action.', 'danger')
            return redirect(url_for('admin.gdpr_settings'))
        
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash(f'No user found with email: {email}', 'danger')
            return redirect(url_for('admin.gdpr_settings'))
        
        if user.id == current_user.id:
            flash('You cannot delete your own account data through this interface.', 'danger')
            return redirect(url_for('admin.gdpr_settings'))
        
        try:
            # Log this action before deleting the user
            activity = UserActivity(
                user_id=current_user.id,
                activity_type='data_deletion',
                details=json.dumps({
                    'target_user_id': user.id,
                    'target_email': user.email,
                    'reason': form.reason.data
                })
            )
            db.session.add(activity)
            
            # In a real implementation, you would need to:
            # 1. Handle cascading deletes or anonymization
            # 2. Consider legal requirements for retention
            # 3. Possibly implement a soft-delete instead
            
            # For this example, we'll just anonymize the user data
            user.name = f"Deleted User {user.id}"
            user.email = f"deleted_{user.id}@example.com"
            user.password_hash = "deleted"
            user.institution = None
            user.bio = None
            user.consent_given = False
            user.consent_timestamp = None
            
            db.session.commit()
            flash(f'User data for {email} has been anonymized.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting user data: {str(e)}', 'danger')
    
    return redirect(url_for('admin.gdpr_settings'))


@admin_bp.route('/analytics/<period>')
@admin_required
def analytics(period='week'):
    """Display site analytics dashboard."""
    # Validate period parameter
    valid_periods = ['today', 'week', 'month', 'year', 'all']
    if period not in valid_periods:
        period = 'week'  # Default to week if invalid
    
    # Calculate date ranges based on period
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if period == 'today':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    elif period == 'year':
        start_date = today - timedelta(days=365)
    else:  # 'all'
        start_date = datetime(2000, 1, 1)  # Far in the past
    
    # Get visitor statistics
    visitor_query = VisitorLog.query
    if period != 'all':
        visitor_query = visitor_query.filter(VisitorLog.timestamp >= start_date)
    
    total_visitors = visitor_query.count()
    anonymous_visitors = visitor_query.filter(VisitorLog.user_id == None).count()
    logged_in_visitors = total_visitors - anonymous_visitors
    unique_ips = visitor_query.with_entities(VisitorLog.ip_address).distinct().count()
    
    # Get article view statistics
    article_query = ArticleView.query
    if period != 'all':
        article_query = article_query.filter(ArticleView.timestamp >= start_date)
    
    total_article_views = article_query.count()
    anonymous_article_views = article_query.filter(ArticleView.user_id == None).count()
    logged_in_article_views = total_article_views - anonymous_article_views
    
    # Most viewed article
    most_viewed_submission = None
    if total_article_views > 0:
        most_viewed_id = db.session.query(
            ArticleView.submission_id, 
            func.count(ArticleView.id).label('view_count')
        ).group_by(ArticleView.submission_id).order_by(desc('view_count')).first()
        
        if most_viewed_id:
            most_viewed_submission = Submission.query.get(most_viewed_id[0])
    
    # User activity statistics
    activity_query = UserActivity.query
    if period != 'all':
        activity_query = activity_query.filter(UserActivity.timestamp >= start_date)
    
    total_activities = activity_query.count()
    login_activities = activity_query.filter(UserActivity.activity_type == 'login').count()
    submission_activities = activity_query.filter(UserActivity.activity_type == 'submission').count()
    review_activities = activity_query.filter(UserActivity.activity_type == 'review').count()
    
    # Get popular pages
    popular_pages = db.session.query(
        VisitorLog.path, 
        func.count(VisitorLog.id).label('count')
    ).filter(
        VisitorLog.timestamp >= start_date if period != 'all' else True
    ).group_by(VisitorLog.path).order_by(desc('count')).limit(10).all()
    
    # Get popular articles with view counts
    popular_articles_query = db.session.query(
        Submission,
        func.count(ArticleView.id).label('view_count'),
        func.max(ArticleView.timestamp).label('last_viewed')
    ).join(
        ArticleView, ArticleView.submission_id == Submission.id
    ).filter(
        ArticleView.timestamp >= start_date if period != 'all' else True
    ).group_by(Submission.id).order_by(desc('view_count')).limit(10)
    
    popular_articles = []
    for article, view_count, last_viewed in popular_articles_query:
        article.view_count = view_count
        article.last_viewed = last_viewed
        popular_articles.append(article)
    
    # Get recent visitor logs
    recent_logs = VisitorLog.query.order_by(desc(VisitorLog.timestamp)).limit(50).all()
    
    # Prepare chart data
    if period == 'today':
        # Hourly data for today
        labels = [f'{hour}:00' for hour in range(24)]
        date_format = '%H'
        delta = timedelta(hours=1)
        iterations = 24
    elif period == 'week':
        # Daily data for the past week
        labels = [(today - timedelta(days=i)).strftime('%a') for i in range(7, 0, -1)]
        date_format = '%a'
        delta = timedelta(days=1)
        iterations = 7
    elif period == 'month':
        # Weekly data for the past month
        labels = [f'Week {i+1}' for i in range(4)]
        date_format = '%W'
        delta = timedelta(days=7)
        iterations = 4
    elif period == 'year':
        # Monthly data for the past year
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        date_format = '%b'
        delta = timedelta(days=30)
        iterations = 12
    else:  # 'all'
        # Yearly data
        current_year = today.year
        labels = [str(year) for year in range(current_year - 4, current_year + 1)]
        date_format = '%Y'
        delta = timedelta(days=365)
        iterations = 5
    
    # Initialize empty data arrays
    visitor_data = [0] * len(labels)
    article_data = [0] * len(labels)
    
    # This is a simplified approach; in a real app, you'd want more precise SQL aggregations
    # For demonstration purposes, we'll just populate with some basic counts
    if period == 'today':
        # Group by hour
        for i, hour in enumerate(range(24)):
            start = today.replace(hour=hour, minute=0, second=0)
            end = start + timedelta(hours=1)
            visitor_data[i] = VisitorLog.query.filter(VisitorLog.timestamp >= start, VisitorLog.timestamp < end).count()
            article_data[i] = ArticleView.query.filter(ArticleView.timestamp >= start, ArticleView.timestamp < end).count()
    elif period == 'week':
        # Group by day
        for i in range(7):
            day = today - timedelta(days=7-i)
            next_day = day + timedelta(days=1)
            visitor_data[i] = VisitorLog.query.filter(VisitorLog.timestamp >= day, VisitorLog.timestamp < next_day).count()
            article_data[i] = ArticleView.query.filter(ArticleView.timestamp >= day, ArticleView.timestamp < next_day).count()
    elif period == 'month':
        # Group by week
        for i in range(4):
            week_start = today - timedelta(days=30-i*7)
            week_end = week_start + timedelta(days=7)
            visitor_data[i] = VisitorLog.query.filter(VisitorLog.timestamp >= week_start, VisitorLog.timestamp < week_end).count()
            article_data[i] = ArticleView.query.filter(ArticleView.timestamp >= week_start, ArticleView.timestamp < week_end).count()
    elif period == 'year':
        # Group by month
        for i in range(12):
            month = today.replace(month=i+1 if i+1 <= 12 else 1, day=1)
            next_month = month.replace(month=month.month+1 if month.month < 12 else 1, 
                                      year=month.year if month.month < 12 else month.year+1)
            visitor_data[i] = VisitorLog.query.filter(VisitorLog.timestamp >= month, VisitorLog.timestamp < next_month).count()
            article_data[i] = ArticleView.query.filter(ArticleView.timestamp >= month, ArticleView.timestamp < next_month).count()
    else:  # 'all'
        # Group by year
        current_year = today.year
        for i, year in enumerate(range(current_year - 4, current_year + 1)):
            year_start = datetime(year, 1, 1)
            year_end = datetime(year+1, 1, 1)
            visitor_data[i] = VisitorLog.query.filter(VisitorLog.timestamp >= year_start, VisitorLog.timestamp < year_end).count()
            article_data[i] = ArticleView.query.filter(ArticleView.timestamp >= year_start, ArticleView.timestamp < year_end).count()
    
    # Prepare statistics dictionaries
    visitor_stats = {
        'total': total_visitors,
        'anonymous': anonymous_visitors,
        'logged_in': logged_in_visitors,
        'unique_ips': unique_ips
    }
    
    article_stats = {
        'total': total_article_views,
        'anonymous': anonymous_article_views,
        'logged_in': logged_in_article_views,
        'most_viewed_title': most_viewed_submission.title if most_viewed_submission else 'N/A'
    }
    
    activity_stats = {
        'total': total_activities,
        'logins': login_activities,
        'submissions': submission_activities,
        'reviews': review_activities
    }
    
    return render_template(
        'admin/analytics.html',
        title='Site Analytics',
        period=period,
        visitor_stats=visitor_stats,
        article_stats=article_stats,
        activity_stats=activity_stats,
        popular_pages=popular_pages,
        popular_articles=popular_articles,
        recent_logs=recent_logs,
        date_labels=json.dumps(labels),
        visitor_data=json.dumps(visitor_data),
        article_data=json.dumps(article_data)
    )