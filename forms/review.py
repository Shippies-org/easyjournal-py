"""
Review forms for the Academic Journal Submission System.

This module defines the forms used for peer reviews and editorial decisions.
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, DateField, StringField
from wtforms.validators import DataRequired, Length, Optional, Email


class ReviewForm(FlaskForm):
    """Form for completing a peer review."""
    content = TextAreaField('Review Content', validators=[
        DataRequired(),
        Length(min=200, max=10000, message='Please provide a detailed review of at least 200 characters')
    ])
    decision = SelectField('Recommendation', validators=[
        DataRequired()
    ], choices=[
        ('', 'Select Recommendation'),
        ('accept', 'Accept as is'),
        ('minor_revisions', 'Accept with minor revisions'),
        ('major_revisions', 'Major revisions required'),
        ('reject', 'Reject')
    ])


class AssignReviewerForm(FlaskForm):
    """Form for assigning a reviewer to a submission."""
    reviewer_email = StringField('Reviewer Email', validators=[
        DataRequired(),
        Email()
    ])
    due_date = DateField('Due Date', validators=[
        Optional()
    ], format='%Y-%m-%d')


class EditorDecisionForm(FlaskForm):
    """Form for making editorial decisions."""
    decision = SelectField('Decision', validators=[
        DataRequired()
    ], choices=[
        ('', 'Select Decision'),
        ('accept', 'Accept for publication'),
        ('reject', 'Reject'),
        ('revisions', 'Request revisions')
    ])
    comments = TextAreaField('Comments', validators=[
        DataRequired(),
        Length(min=50, max=5000, message='Please provide comments of at least 50 characters')
    ])