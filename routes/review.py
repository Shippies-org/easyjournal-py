"""
Review routes for the Academic Journal Submission System.

This module handles review assignments and peer review processes.
"""

from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models import Submission, Review, EditorDecision, User
from forms.review import ReviewForm, AssignReviewerForm, EditorDecisionForm

# Create a blueprint for review routes
review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('/editor/dashboard')
@login_required
def editor_dashboard():
    """Render the editor dashboard."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to access the editor dashboard.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get submissions in various states
    new_submissions = Submission.query.filter_by(status='submitted').order_by(Submission.submitted_at).all()
    in_review_submissions = Submission.query.filter_by(status='under_review').order_by(Submission.submitted_at).all()
    ready_for_decision = Submission.query.filter_by(status='reviewed').order_by(Submission.updated_at).all()
    recently_revised = Submission.query.filter_by(status='revision_submitted').order_by(Submission.updated_at).all()
    
    return render_template(
        'review/editor_dashboard.html',
        title='Editor Dashboard',
        new_submissions=new_submissions,
        in_review_submissions=in_review_submissions,
        ready_for_decision=ready_for_decision,
        recently_revised=recently_revised
    )


@review_bp.route('/reviewer/dashboard')
@login_required
def reviewer_dashboard():
    """Render the reviewer dashboard."""
    # Ensure user is a reviewer
    if not current_user.is_reviewer() and not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to access the reviewer dashboard.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get review assignments for this reviewer
    pending_reviews = Review.query.filter_by(reviewer_id=current_user.id, status='assigned').order_by(Review.due_date).all()
    completed_reviews = Review.query.filter_by(reviewer_id=current_user.id, status='completed').order_by(Review.completed_at.desc()).all()
    
    return render_template(
        'review/reviewer_dashboard.html',
        title='Reviewer Dashboard',
        pending_reviews=pending_reviews,
        completed_reviews=completed_reviews
    )


@review_bp.route('/assign/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def assign_reviewer(submission_id):
    """Assign a reviewer to a submission."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to assign reviewers.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    form = AssignReviewerForm()
    
    if form.validate_on_submit():
        # Calculate due date (default 30 days from now)
        due_date = datetime.utcnow() + timedelta(days=30)
        if form.due_date.data:
            due_date = form.due_date.data
        
        # Find or create user based on email
        reviewer_email = form.reviewer_email.data.lower().strip()
        
        # Check if user already exists
        reviewer = User.query.filter_by(email=reviewer_email).first()
        
        if not reviewer:
            # Create a new user with reviewer role
            import secrets
            import string
            import hashlib
            
            # Generate a random password
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(12))
            
            reviewer = User(
                name=reviewer_email.split('@')[0],  # Use email prefix as name initially
                email=reviewer_email,
                password=password,  # This will be hashed by the User model
                role='reviewer',
                institution=''
            )
            db.session.add(reviewer)
            db.session.commit()
            
            # TODO: Send invitation email with account details
            
            flash(f'Created new reviewer account for {reviewer_email}.', 'info')
        
        # Don't allow assigning the author as a reviewer
        if reviewer.id == submission.author_id:
            flash('The author cannot review their own submission.', 'danger')
            return render_template(
                'review/assign.html',
                title='Assign Reviewer',
                submission=submission,
                form=form,
                existing_reviewers=Review.query.filter_by(submission_id=submission_id).all()
            )
        
        # Check if this reviewer is already assigned
        existing_review = Review.query.filter_by(
            submission_id=submission_id,
            reviewer_id=reviewer.id
        ).first()
        
        if existing_review:
            flash('This reviewer is already assigned to this submission.', 'danger')
        else:
            # Create new review assignment
            review = Review(
                submission_id=submission_id,
                reviewer_id=reviewer.id,
                editor_id=current_user.id,
                due_date=due_date,
                status='assigned'
            )
            
            # Update submission status
            submission.status = 'under_review'
            submission.updated_at = datetime.utcnow()
            
            db.session.add(review)
            db.session.commit()
            
            flash('Reviewer successfully assigned.', 'success')
            return redirect(url_for('review.editor_dashboard'))
    
    # Get existing reviewers for this submission
    existing_reviewers = Review.query.filter_by(submission_id=submission_id).all()
    
    return render_template(
        'review/assign.html',
        title='Assign Reviewer',
        submission=submission,
        form=form,
        existing_reviewers=existing_reviewers
    )


@review_bp.route('/submission/<int:submission_id>')
@login_required
def view_submission_for_review(submission_id):
    """View a submission as a reviewer or editor."""
    submission = Submission.query.get_or_404(submission_id)
    
    # Check if user is allowed to view this submission
    is_editor = current_user.is_editor() or current_user.is_admin()
    is_assigned_reviewer = Review.query.filter_by(
        submission_id=submission_id,
        reviewer_id=current_user.id
    ).first() is not None
    
    if not (is_editor or is_assigned_reviewer):
        flash('You do not have permission to view this submission.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get reviews for this submission
    reviews = Review.query.filter_by(submission_id=submission_id).all()
    
    # Get editor decisions
    decisions = EditorDecision.query.filter_by(submission_id=submission_id).order_by(EditorDecision.created_at.desc()).all()
    
    return render_template(
        'review/view_submission.html',
        title=submission.title,
        submission=submission,
        reviews=reviews,
        decisions=decisions
    )


@review_bp.route('/complete/<int:review_id>', methods=['GET', 'POST'])
@login_required
def complete_review(review_id):
    """Complete a review assignment."""
    review = Review.query.get_or_404(review_id)
    
    # Ensure user is the assigned reviewer
    if current_user.id != review.reviewer_id:
        flash('You are not authorized to complete this review.', 'danger')
        return redirect(url_for('review.reviewer_dashboard'))
    
    # Ensure review is not already completed
    if review.status == 'completed':
        flash('This review has already been completed.', 'danger')
        return redirect(url_for('review.reviewer_dashboard'))
    
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Update the review
        review.content = form.content.data
        review.decision = form.decision.data
        review.status = 'completed'
        review.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Check if this submission has ANY completed reviews
        # (We want editors to see it immediately after the first review is completed)
        submission = Submission.query.get(review.submission_id)
        submission.status = 'reviewed'
        submission.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Your review has been submitted successfully.', 'success')
        return redirect(url_for('review.reviewer_dashboard'))
    
    # Pre-populate form if review was started previously
    if review.content:
        form.content.data = review.content
    if review.decision:
        form.decision.data = review.decision
    
    submission = Submission.query.get(review.submission_id)
    
    return render_template(
        'review/complete.html',
        title='Complete Review',
        form=form,
        review=review,
        submission=submission
    )


@review_bp.route('/decision/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def make_decision(submission_id):
    """Make an editorial decision on a submission."""
    # Ensure user is an editor
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to make editorial decisions.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    # Ensure submission has been reviewed or is a revision submission
    if submission.status != 'reviewed' and submission.status != 'revision_submitted':
        flash('This submission is not ready for a decision.', 'danger')
        return redirect(url_for('review.editor_dashboard'))
    
    form = EditorDecisionForm()
    
    if form.validate_on_submit():
        # Create new decision
        decision = EditorDecision(
            submission_id=submission_id,
            editor_id=current_user.id,
            decision=form.decision.data,
            comments=form.comments.data
        )
        
        # Update submission status based on decision
        if form.decision.data == 'accept':
            submission.status = 'accepted'
        elif form.decision.data == 'reject':
            submission.status = 'rejected'
        else:  # revisions
            submission.status = 'revisions'  # Changed from 'revisions_requested' to match what the revise_submission route expects
        
        submission.updated_at = datetime.utcnow()
        
        db.session.add(decision)
        db.session.commit()
        
        flash('Your decision has been recorded.', 'success')
        return redirect(url_for('review.editor_dashboard'))
    
    # Get reviews for this submission
    reviews = Review.query.filter_by(submission_id=submission_id).all()
    
    # Get only completed reviews for the template
    completed_reviews = [r for r in reviews if r.status == 'completed']
    
    return render_template(
        'review/make_decision.html',
        title='Make Decision',
        form=form,
        submission=submission,
        reviews=reviews,
        completed_reviews=completed_reviews
    )