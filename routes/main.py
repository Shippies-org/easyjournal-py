"""
Main routes for the Academic Journal Submission System.

This module handles the main pages and navigation.
"""

from datetime import datetime
import json

from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, jsonify, Response
from flask_login import login_required, current_user
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models import Submission, Issue, Publication, User, ArticleView, Review, Revision

# Create a blueprint for main routes
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the home page."""
    # Get the featured articles (only published submissions)
    try:
        featured_articles = (
            Submission.query
            .join(Publication)
            .filter(Publication.status == 'published')
            .order_by(Publication.published_at.desc())
            .limit(3)
            .all()
        )
    except Exception as e:
        current_app.logger.error(f"Error loading featured articles: {str(e)}")
        featured_articles = []
    
    # Get the latest issues
    try:
        latest_issues = (
            Issue.query
            .filter_by(status='published')
            .order_by(Issue.publication_date.desc())
            .limit(4)
            .all()
        )
    except Exception as e:
        current_app.logger.error(f"Error loading latest issues: {str(e)}")
        latest_issues = []
    
    try:
        return render_template(
            'main/index.html',
            featured_articles=featured_articles,
            latest_issues=latest_issues
        )
    except Exception as e:
        current_app.logger.error(f"Error rendering index template: {str(e)}")
        # Provide a simple fallback
        return "<h1>Academic Journal System</h1><p>We're experiencing technical difficulties. Please try again later.</p>"


@main_bp.route('/about')
def about():
    """Render the about page."""
    # Get content from system settings
    from models import SystemSetting
    
    about_content = SystemSetting.get_value('about_content')
    # Other settings that might be used on the about page
    submission_guidelines = SystemSetting.get_value('submission_guidelines')
    review_policy = SystemSetting.get_value('review_policy')
    ethics_policy = SystemSetting.get_value('ethics_policy')
    
    return render_template(
        'main/about.html',
        about_content=about_content,
        submission_guidelines=submission_guidelines,
        review_policy=review_policy,
        ethics_policy=ethics_policy
    )


@main_bp.route('/contact')
def contact():
    """Render the contact page."""
    # Get content from system settings
    from models import SystemSetting
    
    # Retrieve contact information from settings
    contact_email = SystemSetting.get_value('contact_email')
    contact_phone = SystemSetting.get_value('contact_phone')
    contact_address = SystemSetting.get_value('contact_address')
    
    # Social media links
    twitter_url = SystemSetting.get_value('twitter_url')
    facebook_url = SystemSetting.get_value('facebook_url')
    linkedin_url = SystemSetting.get_value('linkedin_url')
    
    return render_template(
        'main/contact.html',
        contact_email=contact_email,
        contact_phone=contact_phone,
        contact_address=contact_address,
        twitter_url=twitter_url,
        facebook_url=facebook_url,
        linkedin_url=linkedin_url
    )


@main_bp.route('/privacy')
def privacy_policy():
    """Render the privacy policy page."""
    # Get the privacy policy from system settings
    from models import SystemSetting
    
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
    
    privacy_policy = SystemSetting.get_value('gdpr_privacy_policy', default_privacy_policy)
    
    return render_template('main/privacy_policy.html', privacy_policy=privacy_policy)


@main_bp.route('/browse')
def browse():
    """Render the list of published articles."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    try:
        # Base query for published articles
        query = Submission.query.join(Publication).filter(Publication.status == 'published')
        
        # Apply filters
        category = request.args.get('category')
        if category:
            query = query.filter(Submission.category == category)
        
        search = request.args.get('search')
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Submission.title.ilike(search_term)) | 
                (Submission.authors.ilike(search_term)) | 
                (Submission.keywords.ilike(search_term)) | 
                (Submission.abstract.ilike(search_term))
            )
        
        # Apply sorting
        sort = request.args.get('sort', 'date_desc')
        if sort == 'date_desc':
            query = query.order_by(Publication.published_at.desc())
        elif sort == 'date_asc':
            query = query.order_by(Publication.published_at.asc())
        elif sort == 'title_asc':
            query = query.order_by(Submission.title.asc())
        elif sort == 'title_desc':
            query = query.order_by(Submission.title.desc())
        
        # Get paginated results
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        articles = pagination.items
    except (ProgrammingError, Exception):
        # If there's an error (e.g., table doesn't exist yet), return empty results
        articles = []
        pagination = None
    
    # Get popular articles based on view count
    try:
        popular_articles = (
            Submission.query
            .join(Publication)
            .filter(Publication.status == 'published')
            .join(ArticleView, Submission.id == ArticleView.submission_id)
            .group_by(Submission.id)
            .order_by(db.func.count(ArticleView.id).desc())
            .limit(5)
            .all()
        )
    except (ProgrammingError, Exception):
        popular_articles = []
    
    return render_template(
        'main/browse.html',
        articles=articles,
        pagination=pagination,
        popular_articles=popular_articles
    )


@main_bp.route('/issues')
def issues():
    """Render the list of published issues."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    try:
        query = Issue.query.filter_by(status='published').order_by(Issue.publication_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        issues_list = pagination.items
    except (ProgrammingError, Exception):
        issues_list = []
        pagination = None
    
    return render_template(
        'main/issues.html',
        issues=issues_list,
        pagination=pagination
    )


@main_bp.route('/issues/<int:issue_id>')
def issue_detail(issue_id):
    """Render a specific issue with its articles."""
    try:
        issue = Issue.query.get_or_404(issue_id)
        try:
            articles = (
                Submission.query
                .join(Publication)
                .filter(Publication.issue_id == issue_id, Publication.status == 'published')
                .all()
            )
        except (ProgrammingError, Exception):
            articles = []
    except (ProgrammingError, Exception):
        return render_template('errors/404.html'), 404
    
    return render_template(
        'main/issue_detail.html',
        issue=issue,
        articles=articles
    )


@main_bp.route('/articles/<int:submission_id>')
def article_detail(submission_id):
    """Render a specific article."""
    try:
        article = Submission.query.get_or_404(submission_id)
        
        # Check if the article is published or if the user has permission to view it
        is_published = article.publication is not None and article.publication.is_published()
        
        has_permission = (
            is_published or
            (current_user.is_authenticated and (
                current_user.is_admin() or 
                current_user.is_editor() or 
                current_user.id == article.author_id or
                current_user.reviews_given.filter_by(submission_id=submission_id).first() is not None
            ))
        )
        
        if not has_permission:
            return render_template('errors/403.html'), 403
            
        # Track this article view for analytics
        try:
            article_view = ArticleView(
                submission_id=submission_id,
                user_id=current_user.id if current_user.is_authenticated else None,
                ip_address=request.remote_addr
            )
            db.session.add(article_view)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error recording article view: {str(e)}")
            # Continue serving the page even if we couldn't record the view
            
    except (ProgrammingError, Exception):
        return render_template('errors/404.html'), 404
    
    return render_template(
        'main/article_detail.html',
        article=article,
        is_published=is_published
    )


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard."""
    # Redirect to appropriate role-specific dashboard
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_editor():
        return redirect(url_for('review.editor_dashboard'))
    elif current_user.is_reviewer():
        return redirect(url_for('review.reviewer_dashboard'))
    else:  # Author
        return render_template('main/dashboard_author.html')


@main_bp.route('/profile')
@login_required
def profile():
    """Render the user profile page."""
    return render_template('main/profile.html')


@main_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update the user's profile information."""
    name = request.form.get('name')
    email = request.form.get('email')
    institution = request.form.get('institution')
    bio = request.form.get('bio')
    
    if not name or not email:
        flash('Name and email are required.', 'danger')
        return redirect(url_for('main.profile'))
    
    # Check if the email is already in use by another user
    if email != current_user.email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already in use.', 'danger')
            return redirect(url_for('main.profile'))
    
    # Update user information
    current_user.name = name
    current_user.email = email
    current_user.institution = institution
    current_user.bio = bio
    
    db.session.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('main.profile'))


@main_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Change the user's password."""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Validate form inputs
    if not current_password or not new_password or not confirm_password:
        flash('All password fields are required.', 'danger')
        return redirect(url_for('main.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('main.profile'))
    
    if len(new_password) < 8:
        flash('Password must be at least 8 characters long.', 'danger')
        return redirect(url_for('main.profile'))
    
    # Verify current password
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('main.profile'))
    
    # Update password
    current_user.set_password(new_password)
    db.session.commit()
    
    flash('Password changed successfully.', 'success')
    return redirect(url_for('main.profile'))


@main_bp.route('/profile/notification-settings', methods=['POST'])
@login_required
def update_notification_settings():
    """Update the user's notification settings."""
    # This is a placeholder for actual notification settings update
    # In a real implementation, this would update UserSetting records
    
    flash('Notification settings updated successfully.', 'success')
    return redirect(url_for('main.profile'))


@main_bp.route('/set-theme/<theme>')
@login_required
def set_theme(theme):
    """Set the user's theme preference."""
    try:
        current_user.set_theme(theme)
        db.session.commit()
        flash(f'Theme set to {theme.capitalize()}', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error setting theme: {str(e)}")
        flash('Error setting theme', 'danger')
    
    # Redirect back to the referring page
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('main.index'))


@main_bp.route('/profile/export-data')
@login_required
def export_user_data():
    """Export the user's personal data as a JSON file for GDPR compliance."""
    try:
        # Collect user profile data
        user_data = {
            'personal_info': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
                'role': current_user.role,
                'institution': current_user.institution,
                'bio': current_user.bio,
                'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
                'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
                'consent_given': current_user.consent_given,
                'consent_timestamp': current_user.consent_timestamp.isoformat() if current_user.consent_timestamp else None
            },
            'submissions': [],
            'reviews_given': []  # Reviews the user has provided, NOT reviews of their work
        }
        
        # Add user's submissions data
        if current_user.is_author():
            for submission in current_user.submissions:
                submission_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'authors': submission.authors,
                    'abstract': submission.abstract,
                    'keywords': submission.keywords,
                    'category': submission.category,
                    'status': submission.status,
                    'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
                    'updated_at': submission.updated_at.isoformat() if submission.updated_at else None,
                    'revisions': []
                }
                
                # Add revision data if any
                for revision in submission.revisions:
                    try:
                        revision_data = {
                            'id': revision.id,
                            'created_at': revision.created_at.isoformat() if revision.created_at else None
                        }
                        # Only add 'round' if it exists in the model
                        if hasattr(revision, 'round'):
                            revision_data['round'] = revision.round
                        
                        submission_data['revisions'].append(revision_data)
                    except Exception as rev_error:
                        current_app.logger.error(f"Error with revision {revision.id}: {str(rev_error)}")
                        # Continue with other revisions even if this one fails
                
                user_data['submissions'].append(submission_data)
        
        # Add reviews given by the user (not reviews of their work)
        if current_user.is_reviewer():
            for review in current_user.reviews_given:
                # Include only basic information about the submission to respect privacy
                review_data = {
                    'id': review.id,
                    'submission_title': review.submission.title,  # Only include title for reference
                    'status': review.status,
                    'decision': review.decision,
                    'assigned_at': review.assigned_at.isoformat() if review.assigned_at else None,
                    'due_date': review.due_date.isoformat() if review.due_date else None,
                    'completed_at': review.completed_at.isoformat() if review.completed_at else None
                }
                # Only include the reviewer's own review content
                if review.reviewer_id == current_user.id:
                    review_data['content'] = review.content
                
                user_data['reviews_given'].append(review_data)
        
        # Generate the response with the JSON data and proper headers
        response = Response(
            json.dumps(user_data, indent=2),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment; filename=user_data_{current_user.id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.json'
            }
        )
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error exporting user data: {str(e)}")
        flash('An error occurred while exporting your data. Please try again later.', 'danger')
        return redirect(url_for('main.profile'))