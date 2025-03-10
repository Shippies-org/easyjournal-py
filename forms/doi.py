"""
DOI-related forms for the Academic Journal Submission System.

This module defines the forms used for DOI management and health checks.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class DOIHealthCheckForm(FlaskForm):
    """Form for DOI health check requests."""
    organization_id = StringField('Organization Identifier', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Organization ID must be between 2 and 100 characters')
    ])
    
    service = SelectField('DOI Service', validators=[
        DataRequired()
    ], choices=[
        ('crossref', 'CrossRef'),
        ('datacite', 'DataCite')
    ])
    
    submit = SubmitField('Run Health Check')