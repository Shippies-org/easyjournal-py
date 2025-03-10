"""
Submission forms for the Academic Journal Submission System.

This module defines the forms used for article submissions and revisions.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class SubmissionForm(FlaskForm):
    """Form for new article submissions."""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=200)
    ])
    authors = StringField('Authors (comma separated)', validators=[
        DataRequired(),
        Length(max=500)
    ])
    abstract = TextAreaField('Abstract', validators=[
        DataRequired(),
        Length(min=100, max=2000)
    ])
    keywords = StringField('Keywords (comma separated)', validators=[
        Optional(),
        Length(max=200)
    ])
    category = SelectField('Category', validators=[
        DataRequired()
    ], choices=[
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
    ])
    file = FileField('Manuscript File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'rtf'], 'Only PDF, DOC, DOCX, TXT, and RTF files are allowed')
    ])
    cover_letter = TextAreaField('Cover Letter', validators=[
        Optional(),
        Length(max=5000)
    ])


class RevisionForm(FlaskForm):
    """Form for article revisions."""
    file = FileField('Revised Manuscript File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'rtf'], 'Only PDF, DOC, DOCX, TXT, and RTF files are allowed')
    ])
    cover_letter = TextAreaField('Cover Letter / Response to Reviewers', validators=[
        DataRequired(),
        Length(min=100, max=5000, message='Please provide a detailed response to the reviewers\' comments')
    ])
    revision_note = TextAreaField('Revision Notes (For Editorial Record)', validators=[
        Optional(),
        Length(max=1000, message='Revision notes should be less than 1000 characters')
    ])