"""
Issue management routes for the Academic Journal Submission System (Editor View).

This module handles issue management for editors.
"""

from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models import Issue, Publication
from forms.admin import IssueForm

# Create a blueprint for issue management routes
issue_bp = Blueprint('issues', __name__, url_prefix='/editor/issues')


@issue_bp.route('/')
@login_required
def editor_issues():
    """Render the issue management page for editors."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to access issue management.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get all issues
    issues = Issue.query.order_by(Issue.volume.desc(), Issue.issue_number.desc()).all()
    
    return render_template(
        'review/editor_issues.html',
        title='Issue Management',
        issues=issues
    )


@issue_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_issue():
    """Create a new journal issue."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to create issues.', 'danger')
        return redirect(url_for('main.dashboard'))
    
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
            return redirect(url_for('issues.editor_issues'))
    
    return render_template('review/issue_form.html', title='New Issue', form=form)


@issue_bp.route('/edit/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def edit_issue(issue_id):
    """Edit an existing journal issue."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to edit issues.', 'danger')
        return redirect(url_for('main.dashboard'))
    
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
            return redirect(url_for('issues.editor_issues'))
    
    return render_template('review/issue_form.html', title='Edit Issue', form=form, issue=issue)


@issue_bp.route('/delete/<int:issue_id>', methods=['POST'])
@login_required
def delete_issue(issue_id):
    """Delete a journal issue."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to delete issues.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    issue = Issue.query.get_or_404(issue_id)
    
    # Check if issue has publications
    if issue.publications.count() > 0:
        # Delete all publications associated with this issue
        for publication in issue.publications:
            # Update submission status for published articles
            if publication.status == 'published':
                submission = publication.submission
                submission.status = 'accepted'
                
            db.session.delete(publication)
    
    db.session.delete(issue)
    db.session.commit()
    
    flash('Issue deleted successfully.', 'success')
    return redirect(url_for('issues.editor_issues'))