"""
Copyright Plugin Models

This module defines database models for copyright management functionality.
"""
from app import db
from datetime import datetime

class Copyright(db.Model):
    """Model for copyright records."""
    __tablename__ = 'copyright_records'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    holder_name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_type = db.Column(db.String(50), nullable=False)
    rights_statement = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submission = db.relationship('Submission', backref=db.backref('copyright', uselist=False))
    
    def __repr__(self):
        return f'<Copyright {self.id} for Submission {self.submission_id}>'
        
class LicenseType(db.Model):
    """Model for predefined license types."""
    __tablename__ = 'license_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    short_code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LicenseType {self.name}>'