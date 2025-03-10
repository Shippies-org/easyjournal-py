"""
GDPR-related forms for the Academic Journal Submission System.

This module defines the forms used for GDPR compliance management.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class ConsentSettingsForm(FlaskForm):
    """Form for managing GDPR consent text and settings."""
    consent_text = TextAreaField('Consent Text', validators=[
        DataRequired(),
        Length(min=100, max=2000, message='Consent text should be between 100 and 2000 characters')
    ], description="This text will be shown to users when requesting consent")
    
    privacy_policy = TextAreaField('Privacy Policy', validators=[
        DataRequired(),
        Length(min=200, max=10000, message='Privacy policy should be detailed and between 200 and 10000 characters')
    ], description="Detailed privacy policy")
    
    require_existing_users_consent = BooleanField('Require Existing Users to Give Consent', 
        default=True,
        description="If checked, existing users will be required to give consent on their next login")
    
    submit = SubmitField('Save GDPR Settings')


class DataExportRequestForm(FlaskForm):
    """Form for managing data export requests."""
    email = StringField('User Email', validators=[
        DataRequired(),
        Length(max=100)
    ], description="Email of the user requesting data export")
    
    notes = TextAreaField('Notes', validators=[
        Optional(),
        Length(max=500)
    ], description="Optional administrative notes about this request")
    
    submit = SubmitField('Process Data Export Request')


class DataDeletionRequestForm(FlaskForm):
    """Form for managing data deletion requests."""
    email = StringField('User Email', validators=[
        DataRequired(),
        Length(max=100)
    ], description="Email of the user requesting data deletion")
    
    reason = TextAreaField('Reason for Deletion', validators=[
        Optional(),
        Length(max=500)
    ], description="Optional reason for deletion request")
    
    confirmation = BooleanField('I understand this action cannot be undone', validators=[
        DataRequired()
    ], description="Confirm irreversible data deletion")
    
    submit = SubmitField('Process Data Deletion Request')