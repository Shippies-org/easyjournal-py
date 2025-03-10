"""
Authentication routes for the Academic Journal Submission System.

This module handles user registration, login, and logout.
"""

from datetime import datetime
import json

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from markupsafe import Markup

import config
from app import db
from models import User, ROLE_AUTHOR, UserActivity, SystemSetting
from forms.auth import LoginForm, RegistrationForm

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_editor():
            return redirect(url_for('review.editor_dashboard'))
        elif current_user.is_reviewer():
            return redirect(url_for('review.reviewer_dashboard'))
        elif current_user.is_author():
            return redirect(url_for('submission.author_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Log in the user
            login_user(user, remember=form.remember_me.data)
            
            # Update user's last login time
            user.last_login = datetime.utcnow()
            
            # Log this activity for analytics, but make it fault-tolerant
            try:
                login_activity = UserActivity(
                    user_id=user.id,
                    activity_type='login',
                    details=json.dumps({
                        'user_agent': request.user_agent.string,
                        'ip': request.remote_addr
                    })
                )
                db.session.add(login_activity)
            except Exception as activity_error:
                # If activity tracking fails, log it but continue with login
                current_app.logger.error(f"Failed to create activity log: {str(activity_error)}")
                # Make sure we don't have any partial transaction
                db.session.rollback()
            
            try:
                db.session.commit()
                flash('Login successful!', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error logging login activity: {str(e)}")
                # Add more detailed logging for debugging
                import traceback
                current_app.logger.error(f"Traceback: {traceback.format_exc()}")
                # Still show success even if activity logging fails
                flash('Login successful!', 'success')
            
            # Redirect to the role-specific dashboard or the page they were trying to access
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                # Redirect based on user role
                if user.is_admin():
                    next_page = url_for('admin.dashboard')
                elif user.is_editor():
                    next_page = url_for('review.editor_dashboard')
                elif user.is_reviewer():
                    next_page = url_for('review.reviewer_dashboard')
                elif user.is_author():
                    next_page = url_for('submission.author_dashboard')
                else:
                    next_page = url_for('main.dashboard')
            return redirect(next_page)
        
        flash('Invalid email or password. Please try again.', 'danger')
    
    # Get demo account information if in demo mode
    demo_accounts = None
    if config.DEMO_MODE:
        demo_accounts = config.TEST_ACCOUNTS
    
    return render_template('auth/login.html', form=form, title='Login', demo_accounts=demo_accounts)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_editor():
            return redirect(url_for('review.editor_dashboard'))
        elif current_user.is_reviewer():
            return redirect(url_for('review.reviewer_dashboard'))
        elif current_user.is_author():
            return redirect(url_for('submission.author_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        
        if existing_user:
            flash('This email address is already registered. Please use a different email or login instead.', 'danger')
            return render_template('auth/register.html', form=form, title='Register')
            
        try:
            # Create new user with Author role by default
            user = User(
                name=form.name.data,
                email=form.email.data.lower().strip(),
                institution=form.institution.data,
                bio=form.bio.data,
                role=ROLE_AUTHOR,
                password=form.password.data
            )
            
            # Add user to database
            db.session.add(user)
            
            # Log registration activity for analytics
            registration_activity = UserActivity(
                user_id=user.id,
                activity_type='registration',
                details=json.dumps({
                    'user_agent': request.user_agent.string,
                    'ip': request.remote_addr,
                    'institution': form.institution.data or ''
                })
            )
            db.session.add(registration_activity)
            
            db.session.commit()
            
            flash('Registration successful! You have been logged in.', 'success')
            # Log the user in after registration
            login_user(user)
            
            # Set last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            return redirect(url_for('submission.author_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration. Please try again.', 'danger')
            current_app.logger.error(f"Registration error: {str(e)}")
    
    return render_template('auth/register.html', form=form, title='Register')


@auth_bp.route('/consent', methods=['POST'])
@login_required
def provide_consent():
    """Handle user GDPR consent."""
    # Check if consent checkbox was checked
    if 'gdprConsent' in request.form:
        try:
            # Update user's consent status
            current_user.set_consent(True)
            db.session.commit()
            
            # Log this activity
            consent_activity = UserActivity(
                user_id=current_user.id,
                activity_type='gdpr_consent',
                details=json.dumps({
                    'user_agent': request.user_agent.string,
                    'ip': request.remote_addr,
                    'timestamp': datetime.utcnow().isoformat()
                })
            )
            db.session.add(consent_activity)
            db.session.commit()
            
            flash('Thank you for providing your consent.', 'success')
            
            # Redirect to appropriate dashboard
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif current_user.is_editor():
                return redirect(url_for('review.editor_dashboard'))
            elif current_user.is_reviewer():
                return redirect(url_for('review.reviewer_dashboard'))
            elif current_user.is_author():
                return redirect(url_for('submission.author_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
                
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error recording consent: {str(e)}")
            flash('An error occurred while recording your consent. Please try again.', 'danger')
    else:
        flash('You must provide consent to continue using the system.', 'warning')
    
    # If we get here, something went wrong; send back to referring page or home
    return redirect(request.referrer or url_for('main.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))