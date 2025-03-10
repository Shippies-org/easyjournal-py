"""
Submission routes for the Academic Journal Submission System.

This module handles article submissions and management.
"""

import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

import config
from app import db
from models import Submission, Revision, EditorDecision, ROLE_AUTHOR
from forms.submission import SubmissionForm, RevisionForm

# Create a blueprint for submission routes
submission_bp = Blueprint('submission', __name__, url_prefix='/submissions')


def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@submission_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_submission():
    """Handle new article submissions."""
    # Only authors can submit articles
    if not current_user.is_author():
        flash('Only authors can submit articles.', 'warning')
        return redirect(url_for('main.index'))
    
    form = SubmissionForm()
    
    if form.validate_on_submit():
        # Save uploaded file
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_filename = f"{timestamp}_{current_user.id}_{filename}"
            file_path = os.path.join(config.UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # Create new submission
            submission = Submission(
                title=form.title.data,
                authors=form.authors.data,
                abstract=form.abstract.data,
                keywords=form.keywords.data,
                category=form.category.data,
                file_path=unique_filename,
                cover_letter=form.cover_letter.data,
                author_id=current_user.id
            )
            
            db.session.add(submission)
            db.session.commit()
            
            flash('Your submission has been received successfully!', 'success')
            return redirect(url_for('submission.author_dashboard'))
        else:
            flash('Invalid file type. Please upload a PDF, DOC, DOCX, TXT, or RTF file.', 'danger')
    
    return render_template('submission/new.html', form=form, title='New Submission')


@submission_bp.route('/dashboard')
@login_required
def author_dashboard():
    """Render the author dashboard with their submissions."""
    # Only authors can access this page
    if not current_user.is_author():
        flash('Only authors can access this page.', 'warning')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Base query for author's submissions
    query = Submission.query.filter_by(author_id=current_user.id)
    
    # Apply filters
    status_filter = request.args.getlist('status')
    if status_filter:
        query = query.filter(Submission.status.in_(status_filter))
    
    category = request.args.get('category')
    if category:
        query = query.filter(Submission.category == category)
    
    # Apply sorting
    sort = request.args.get('sort', 'submitted_desc')
    if sort == 'submitted_desc':
        query = query.order_by(Submission.submitted_at.desc())
    elif sort == 'submitted_asc':
        query = query.order_by(Submission.submitted_at.asc())
    elif sort == 'title_asc':
        query = query.order_by(Submission.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Submission.title.desc())
    
    # Get paginated results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    submissions = pagination.items
    
    return render_template('submission/dashboard.html', 
                          title='My Submissions', 
                          submissions=submissions,
                          Revision=Revision)


@submission_bp.route('/<int:submission_id>')
@login_required
def view_submission(submission_id):
    """View a specific submission."""
    submission = Submission.query.get_or_404(submission_id)
    
    # Check if user has permission to view this submission
    has_permission = (
        current_user.is_admin() or 
        current_user.is_editor() or 
        current_user.id == submission.author_id or
        current_user.reviews_given.filter_by(submission_id=submission_id).first() is not None
    )
    
    if not has_permission:
        flash('You do not have permission to view this submission.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('submission/view.html', submission=submission, title='View Submission')


@submission_bp.route('/<int:submission_id>/revise', methods=['GET', 'POST'])
@login_required
def revise_submission(submission_id):
    """Submit a revision for an existing submission."""
    submission = Submission.query.get_or_404(submission_id)
    
    # Check if user has permission to revise this submission
    if current_user.id != submission.author_id:
        flash('You do not have permission to revise this submission.', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if submission is in a state that allows revisions
    if submission.status != 'revisions':
        flash('This submission is not currently open for revisions.', 'warning')
        return redirect(url_for('submission.view_submission', submission_id=submission_id))
    
    form = RevisionForm()
    
    # Get the latest editor decision that requested revisions
    latest_decision = EditorDecision.query.filter_by(
        submission_id=submission_id,
        decision='revisions'
    ).order_by(EditorDecision.created_at.desc()).first()
    
    # Determine the current revision round
    current_round = 1
    if submission.revisions.count() > 0:
        current_round = submission.revisions.order_by(Revision.round.desc()).first().round + 1
    
    if form.validate_on_submit():
        # Save uploaded file
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Add the revision round to the filename
            unique_filename = f"{timestamp}_{current_user.id}_r{current_round}_{filename}"
            file_path = os.path.join(config.UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # Create new revision
            revision = Revision(
                submission_id=submission_id,
                file_path=unique_filename,
                cover_letter=form.cover_letter.data,
                round=current_round,
                decision_id=latest_decision.id if latest_decision else None
            )
            
            # Add revision note if provided
            if hasattr(form, 'revision_note') and form.revision_note.data:
                # Store the revision note in a field or metadata
                # Since we don't have a dedicated field for this in the model yet,
                # we could add it to the cover letter with a clear divider
                if form.revision_note.data.strip():
                    revision.cover_letter += f"\n\n--- EDITORIAL NOTES ---\n{form.revision_note.data}"
            
            # Update submission status to indicate a revision has been submitted
            submission.status = 'revision_submitted'
            submission.updated_at = datetime.utcnow()
            
            db.session.add(revision)
            db.session.commit()
            
            flash(f'Your revision (Round {current_round}) has been submitted successfully!', 'success')
            return redirect(url_for('submission.view_submission', submission_id=submission_id))
        else:
            flash('Invalid file type. Please upload a PDF, DOC, DOCX, TXT, or RTF file.', 'danger')
    
    return render_template(
        'submission/revise.html',
        form=form,
        submission=submission,
        current_round=current_round,
        latest_decision=latest_decision,
        title=f'Submit Revision (Round {current_round})'
    )


@submission_bp.route('/<int:submission_id>/withdraw')
@login_required
def withdraw_submission(submission_id):
    """Withdraw a submission from consideration."""
    submission = Submission.query.get_or_404(submission_id)
    
    # Check if user has permission to withdraw this submission
    if current_user.id != submission.author_id and not current_user.is_admin():
        flash('You do not have permission to withdraw this submission.', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if submission can be withdrawn
    if submission.status not in ['submitted', 'under_review', 'revision_submitted']:
        flash('This submission cannot be withdrawn at its current stage.', 'warning')
        return redirect(url_for('submission.view_submission', submission_id=submission_id))
    
    # Update submission status
    submission.status = 'withdrawn'
    db.session.commit()
    
    flash('Your submission has been withdrawn.', 'success')
    return redirect(url_for('submission.author_dashboard'))