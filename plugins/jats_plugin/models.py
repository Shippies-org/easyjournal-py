"""
JATS XML Plugin Models

This module defines database models for JATS XML generation functionality.
"""

from datetime import datetime

from flask import current_app
from app import db

class JATSXMLRecord(db.Model):
    """Model for JATS XML records."""
    __tablename__ = 'jats_xml_records'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    xml_file_path = db.Column(db.String(255), nullable=True)  # Path to the generated XML file
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, processing, completed, error
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    generated_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    submission = db.relationship('Submission', backref=db.backref('jats_xml', uselist=False))

    def __repr__(self):
        return f'<JATSXMLRecord {self.id} for submission {self.submission_id}>'
    
    def is_completed(self):
        """Check if the XML generation is completed."""
        return self.status == 'completed'
    
class JATSAPISettings(db.Model):
    """Model for JATS API settings."""
    __tablename__ = 'jats_api_settings'

    id = db.Column(db.Integer, primary_key=True)
    api_url = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=True)
    timeout = db.Column(db.Integer, default=30, nullable=False)  # Timeout in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<JATSAPISettings {self.id}>'
    
    @classmethod
    def get_settings(cls):
        """Get the API settings, creating default ones if they don't exist."""
        settings = cls.query.first()
        if settings is None:
            settings = cls(
                api_url='https://html-api-adam394.replit.app/upload?format=all',
                timeout=30
            )
            db.session.add(settings)
            db.session.commit()
        return settings