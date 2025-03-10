"""
Form package initialization for the Academic Journal Submission System.

This package contains all form definitions used throughout the application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

# Import all form modules to make them available when importing the package
from forms import auth, submission, review, admin

# Define role constants to be used throughout the application
ROLE_CHOICES = [
    ('admin', 'Administrator'),
    ('editor', 'Editor'),
    ('reviewer', 'Reviewer'),
    ('author', 'Author')
]

# Define submission status choices
SUBMISSION_STATUS_CHOICES = [
    ('submitted', 'Submitted'),
    ('in_review', 'In Review'),
    ('reviewed', 'Review Complete'),
    ('revisions_requested', 'Revisions Requested'),
    ('resubmitted', 'Resubmitted'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('published', 'Published'),
    ('withdrawn', 'Withdrawn')
]

# Define category choices for submissions
CATEGORY_CHOICES = [
    ('', 'Select Category'),
    ('biology', 'Biology'),
    ('chemistry', 'Chemistry'),
    ('physics', 'Physics'),
    ('mathematics', 'Mathematics'),
    ('computer_science', 'Computer Science'),
    ('engineering', 'Engineering'),
    ('medicine', 'Medicine'),
    ('social_sciences', 'Social Sciences'),
    ('humanities', 'Humanities'),
    ('other', 'Other')
]

# Define review decision choices
REVIEW_DECISION_CHOICES = [
    ('', 'Select Recommendation'),
    ('accept', 'Accept as is'),
    ('minor_revisions', 'Accept with minor revisions'),
    ('major_revisions', 'Major revisions required'),
    ('reject', 'Reject')
]

# Define editor decision choices
EDITOR_DECISION_CHOICES = [
    ('', 'Select Decision'),
    ('accept', 'Accept for publication'),
    ('reject', 'Reject'),
    ('revisions', 'Request revisions')
]

# Define issue status choices
ISSUE_STATUS_CHOICES = [
    ('planned', 'Planned'),
    ('in_progress', 'In Progress'),
    ('published', 'Published')
]