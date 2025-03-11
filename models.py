"""
Database models for the Academic Journal Submission System.

This module defines SQLAlchemy ORM models for all database tables.
"""

from datetime import datetime
import json
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# User role constants
ROLE_AUTHOR = "author"
ROLE_REVIEWER = "reviewer"
ROLE_EDITOR = "editor"
ROLE_ADMIN = "admin"

class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    institution = db.Column(db.String(200))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    # GDPR consent fields
    consent_given = db.Column(db.Boolean, default=False)
    consent_timestamp = db.Column(db.DateTime)
    
    # Relationships
    submissions = db.relationship('Submission', backref='author', lazy='dynamic')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy='dynamic')
    reviews_assigned = db.relationship('Review', foreign_keys='Review.editor_id', backref='editor', lazy='dynamic')
    decisions = db.relationship('EditorDecision', backref='editor', lazy='dynamic')
    
    def __init__(self, name, email, password, role, institution=None, bio=None):
        self.name = name
        self.email = email
        self.set_password(password)
        self.role = role
        self.institution = institution
        self.bio = bio
    
    def set_password(self, password):
        """Set the password hash for this user."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if the user has admin role."""
        return self.role == ROLE_ADMIN
    
    def is_editor(self):
        """Check if the user has editor role."""
        return self.role == ROLE_EDITOR
    
    def is_reviewer(self):
        """Check if the user has reviewer role."""
        return self.role == ROLE_REVIEWER
    
    def is_author(self):
        """Check if the user has author role."""
        return self.role == ROLE_AUTHOR
    
    def get_theme(self):
        """Get the user's preferred theme."""
        theme_setting = self.settings.filter_by(setting_key='theme').first()
        if theme_setting:
            return theme_setting.setting_value
        return 'dark'  # Default theme
    
    def set_theme(self, theme_name):
        """Set the user's preferred theme."""
        valid_themes = ['dark', 'light', 'journal', 'modern', 'elegant', 'high-contrast']
        if theme_name not in valid_themes:
            theme_name = 'dark'  # Default if invalid
            
        theme_setting = self.settings.filter_by(setting_key='theme').first()
        if theme_setting:
            theme_setting.setting_value = theme_name
        else:
            from app import db
            setting = UserSetting(
                user_id=self.id,
                setting_key='theme',
                setting_value=theme_name
            )
            db.session.add(setting)
        
        return theme_name
    
    def set_consent(self, consent=True):
        """Set the user's GDPR consent status."""
        from datetime import datetime
        self.consent_given = consent
        self.consent_timestamp = datetime.utcnow() if consent else None
        from app import db
        db.session.commit()
        return self.consent_given
    
    def has_given_consent(self):
        """Check if the user has given GDPR consent."""
        return self.consent_given
    
    def __repr__(self):
        return f'<User {self.id} {self.name} ({self.role})>'


class Submission(db.Model):
    """Model for article submissions."""
    
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(500), nullable=False)  # Comma-separated list of authors
    abstract = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(200))
    category = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted', nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='submission', lazy='dynamic')
    decisions = db.relationship('EditorDecision', backref='submission', lazy='dynamic')
    revisions = db.relationship('Revision', backref='submission', lazy='dynamic')
    publication = db.relationship('Publication', uselist=False, backref='submission')
    
    def is_accepted(self):
        """Check if the submission has been accepted."""
        return self.status == 'accepted'
    
    def is_published(self):
        """Check if the submission has been published."""
        return self.publication is not None and self.publication.is_published()
    
    def __repr__(self):
        return f'<Submission {self.id} "{self.title}" ({self.status})>'


class Review(db.Model):
    """Model for peer reviews."""
    
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    decision = db.Column(db.String(20))  # accept, reject, revisions
    status = db.Column(db.String(20), default='assigned', nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime)
    
    def is_completed(self):
        """Check if the review is completed."""
        return self.completed_at is not None
    
    def is_overdue(self):
        """Check if the review is overdue."""
        if self.due_date and not self.completed_at:
            from config import now
            return now() > self.due_date
        return False
    
    def __repr__(self):
        return f'<Review {self.id} for Submission {self.submission_id} by Reviewer {self.reviewer_id}>'


class EditorDecision(db.Model):
    """Model for editorial decisions."""
    
    __tablename__ = 'editor_decisions'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # accept, reject, revisions
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EditorDecision {self.id} for Submission {self.submission_id} ({self.decision})>'


class Revision(db.Model):
    """Model for article revisions."""
    
    __tablename__ = 'revisions'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    cover_letter = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Revision {self.id} for Submission {self.submission_id}>'


class Issue(db.Model):
    """Model for journal issues."""
    
    __tablename__ = 'issues'
    
    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer, nullable=False)
    issue_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned', nullable=False)
    publication_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    publications = db.relationship('Publication', backref='issue', lazy='dynamic')
    
    __table_args__ = (
        db.UniqueConstraint('volume', 'issue_number', name='uix_volume_issue'),
    )
    
    def __repr__(self):
        return f'<Issue {self.id} Vol. {self.volume} No. {self.issue_number}>'


class Publication(db.Model):
    """Model linking accepted submissions to issues."""
    
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    page_start = db.Column(db.Integer)
    page_end = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='scheduled', nullable=False)  # scheduled, published, unpublished
    
    __table_args__ = (
        db.UniqueConstraint('submission_id', 'issue_id', name='uix_submission_issue'),
    )
    
    def is_published(self):
        """Check if this article is published."""
        return self.status == 'published' and self.published_at is not None
    
    def publish(self):
        """Publish this article."""
        self.status = 'published'
        self.published_at = datetime.utcnow()
        
    def unpublish(self):
        """Unpublish this article."""
        self.status = 'unpublished'
    
    def __repr__(self):
        return f'<Publication {self.id} Submission {self.submission_id} in Issue {self.issue_id} ({self.status})>'


class Notification(db.Model):
    """Model for user notifications."""
    
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'


class PluginSetting(db.Model):
    """Model for plugin settings."""
    
    __tablename__ = 'plugin_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    plugin_name = db.Column(db.String(100), nullable=False)
    setting_key = db.Column(db.String(100), nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('plugin_name', 'setting_key', name='uix_plugin_setting'),
    )
    
    def __repr__(self):
        return f'<PluginSetting {self.id} {self.plugin_name}.{self.setting_key}>'


class SystemSetting(db.Model):
    """Model for system-wide settings."""

    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), nullable=False, unique=True)
    setting_value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<SystemSetting {self.id} {self.setting_key}>"
        
    @classmethod
    def get_value(cls, key, default=None):
        """Get a system setting value by key."""
        setting = cls.query.filter_by(setting_key=key).first()
        if setting:
            return setting.setting_value
        return default
    
    @classmethod
    def set_value(cls, key, value):
        """Set a system setting value."""
        from flask import current_app
        
        setting = cls.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            setting = cls(setting_key=key, setting_value=value)
            db.session.add(setting)
        db.session.commit()
        
        # Invalidate the system settings cache by setting its time to None
        if hasattr(current_app, '_system_settings_cache_time'):
            current_app._system_settings_cache_time = None
            print(f"Cache invalidated after setting {key} = {value}")
        
        return value


class UserSetting(db.Model):
    """Model for user-specific settings."""
    
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    setting_key = db.Column(db.String(100), nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('settings', lazy='dynamic'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'setting_key', name='uix_user_setting'),
    )
    
    def __repr__(self):
        return f'<UserSetting {self.id} User {self.user_id}.{self.setting_key}>'


class VisitorLog(db.Model):
    """Model for tracking site visits (anonymous and logged-in)."""
    
    __tablename__ = 'visitor_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL for anonymous
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 can be long
    user_agent = db.Column(db.String(255), nullable=True)
    path = db.Column(db.String(255), nullable=False)
    referer = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user (optional)
    user = db.relationship('User', backref=db.backref('visits', lazy='dynamic'))
    
    def __repr__(self):
        return f'<VisitorLog {self.id} {"User "+str(self.user_id) if self.user_id else "Anonymous"} - {self.path}>'


class ArticleView(db.Model):
    """Model for tracking article views."""
    
    __tablename__ = 'article_views'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL for anonymous
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submission = db.relationship('Submission', backref=db.backref('views', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('article_views', lazy='dynamic'))
    
    def __repr__(self):
        return f'<ArticleView {self.id} Submission {self.submission_id}>'


class UserActivity(db.Model):
    """Model for tracking user activity for admin analysis."""
    
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # login, submission, review, etc.
    details = db.Column(db.Text, nullable=True)  # JSON field for additional details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))
    
    def get_details_dict(self):
        """Get the details as a dictionary."""
        if not self.details:
            return {}
        try:
            return json.loads(self.details)
        except json.JSONDecodeError:
            return {}
    
    def set_details_dict(self, details_dict):
        """Set the details from a dictionary."""
        if not details_dict:
            self.details = None
        else:
            self.details = json.dumps(details_dict)
    
    def __repr__(self):
        return f'<UserActivity {self.id} User {self.user_id} {self.activity_type}>'