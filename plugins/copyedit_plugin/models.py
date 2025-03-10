"""
Copy Editing Plugin Models

This module defines database models for copy editing functionality.
"""

from datetime import datetime
from app import db
from models import Submission, User

class CopyEdit(db.Model):
    """Model for copy editing records."""
    
    __tablename__ = 'copyedit_records'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    copyeditor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='assigned', nullable=False)  # assigned, in_progress, completed
    original_file_path = db.Column(db.String(255))  # Path to the original document
    edited_file_path = db.Column(db.String(255))  # Path to the edited document
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    submission = db.relationship('Submission', backref=db.backref('copyedits', lazy='dynamic'))
    copyeditor = db.relationship('User', backref=db.backref('copyedits_assigned', lazy='dynamic'))
    comments = db.relationship('CopyEditComment', backref='copyedit', lazy='dynamic',
                             cascade="all, delete-orphan")
    
    def is_completed(self):
        """Check if the copy editing is completed."""
        return self.status == 'completed'
    
    def __repr__(self):
        return f"<CopyEdit {self.id} for Submission {self.submission_id}>"

class CopyEditComment(db.Model):
    """Model for copy editing comments."""
    
    __tablename__ = 'copyedit_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    copyedit_id = db.Column(db.Integer, db.ForeignKey('copyedit_records.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    page_number = db.Column(db.Integer)  # Optional page number for the comment
    line_number = db.Column(db.Integer)  # Optional line number for the comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('copyedit_comments', lazy='dynamic'))
    
    def __repr__(self):
        return f"<CopyEditComment {self.id} by User {self.user_id}>"