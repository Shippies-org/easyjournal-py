"""
Admin forms for the Academic Journal Submission System.

This module defines the forms used for administrative functions.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError, NumberRange


class UserForm(FlaskForm):
    """Form for creating and editing users."""
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        Optional(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    role = SelectField('Role', validators=[
        DataRequired()
    ], choices=[
        ('admin', 'Administrator'),
        ('editor', 'Editor'),
        ('reviewer', 'Reviewer'),
        ('author', 'Author')
    ])
    institution = StringField('Institution/Organization', validators=[
        Optional(),
        Length(max=200)
    ])
    bio = TextAreaField('Bio/Research Interests', validators=[
        Optional(),
        Length(max=1000)
    ])


class IssueForm(FlaskForm):
    """Form for creating and editing journal issues."""
    volume = IntegerField('Volume', validators=[
        DataRequired(),
        NumberRange(min=1, message='Volume must be a positive integer')
    ])
    issue_number = IntegerField('Issue Number', validators=[
        DataRequired(),
        NumberRange(min=1, message='Issue number must be a positive integer')
    ])
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=2000)
    ])
    status = SelectField('Status', validators=[
        DataRequired()
    ], choices=[
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('published', 'Published')
    ])
    publication_date = DateField('Publication Date', validators=[
        Optional()
    ], format='%Y-%m-%d')


class PublicationForm(FlaskForm):
    """Form for adding publications to an issue."""
    submission_id = SelectField('Article', validators=[
        DataRequired()
    ], coerce=int)
    page_start = IntegerField('Starting Page', validators=[
        Optional(),
        NumberRange(min=1, message='Page number must be positive')
    ])
    page_end = IntegerField('Ending Page', validators=[
        Optional(),
        NumberRange(min=1, message='Page number must be positive')
    ])
    
    def validate_page_end(form, field):
        """Validate that end page is greater than or equal to start page."""
        if form.page_start.data and field.data and field.data < form.page_start.data:
            raise ValidationError('End page must be greater than or equal to start page')


class PluginSettingForm(FlaskForm):
    """Form for editing plugin settings."""
    setting_value = TextAreaField('Value', validators=[
        DataRequired()
    ])