"""
Branding forms for the Academic Journal Submission System.

This module defines the forms used for customizing the journal branding,
appearance, and content.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, URL
from flask_wtf.file import FileAllowed

class BrandingForm(FlaskForm):
    """Form for customizing journal branding settings."""
    site_name = StringField('Journal/Site Name', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    
    site_description = TextAreaField('Journal Description', validators=[
        DataRequired(), 
        Length(max=500)
    ])
    
    # Theme selection
    theme = SelectField('System Theme', choices=[
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('journal', 'Journal'),
        ('modern', 'Modern'),
        ('elegant', 'Elegant'),
        ('high-contrast', 'High Contrast')
    ], default='dark')
    
    # Logo settings
    custom_logo = FileField('Upload Logo', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'svg'], 'Only images (JPG, PNG, SVG) are allowed')
    ])
    
    use_logo_text = BooleanField('Use Text Instead of Logo', default=False)
    logo_text = StringField('Logo Text', validators=[Optional(), Length(max=50)])
    
    # Banner settings
    banner_image = FileField('Banner Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Only images (JPG, PNG) are allowed')
    ])
    
    banner_title = StringField('Banner Title', validators=[Optional(), Length(max=100)])
    banner_subtitle = StringField('Banner Subtitle', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Save Branding Settings')


class ContentSettingsForm(FlaskForm):
    """Form for customizing journal content and policies."""
    
    # About content
    about_content = TextAreaField('About Page Content', validators=[
        DataRequired(),
        Length(max=10000)
    ])
    
    # Policies and guidelines
    submission_guidelines = TextAreaField('Submission Guidelines', validators=[
        DataRequired(),
        Length(max=10000)
    ])
    
    review_policy = TextAreaField('Review Policy', validators=[
        DataRequired(),
        Length(max=5000)
    ])
    
    ethics_policy = TextAreaField('Ethics Policy', validators=[
        DataRequired(),
        Length(max=5000)
    ])
    
    author_guidelines = TextAreaField('Author Guidelines', validators=[
        DataRequired(),
        Length(max=5000)
    ])
    
    # Contact information
    contact_email = StringField('Contact Email', validators=[
        DataRequired(),
        Length(max=100)
    ])
    
    contact_phone = StringField('Contact Phone', validators=[
        Optional(),
        Length(max=30)
    ])
    
    contact_address = TextAreaField('Physical Address', validators=[
        Optional(),
        Length(max=300)
    ])
    
    # Social media links
    twitter_url = StringField('Twitter URL', validators=[
        Optional(),
        URL(),
        Length(max=200)
    ])
    
    facebook_url = StringField('Facebook URL', validators=[
        Optional(),
        URL(),
        Length(max=200)
    ])
    
    linkedin_url = StringField('LinkedIn URL', validators=[
        Optional(),
        URL(),
        Length(max=200)
    ])
    
    # Journal Information
    journal_established = StringField('Established Year', validators=[
        Optional(),
        Length(max=10)
    ])
    
    journal_frequency = StringField('Publication Frequency', validators=[
        Optional(),
        Length(max=50)
    ])
    
    journal_open_access = StringField('Open Access Status', validators=[
        Optional(),
        Length(max=10)
    ])
    
    journal_indexing = StringField('Indexing Services', validators=[
        Optional(),
        Length(max=200)
    ])
    
    journal_issn = StringField('ISSN Number', validators=[
        Optional(),
        Length(max=20)
    ])
    
    # Editorial Board
    editorial_board = TextAreaField('Editorial Board', validators=[
        Optional(),
        Length(max=5000)
    ], description="HTML formatting is supported")
    
    # Support Hours
    support_hours_weekday = StringField('Weekday Support Hours', validators=[
        Optional(),
        Length(max=50)
    ], description="e.g. 9:00 AM - 6:00 PM (EST)")
    
    support_hours_saturday = StringField('Saturday Support Hours', validators=[
        Optional(),
        Length(max=50)
    ], description="e.g. 10:00 AM - 2:00 PM (EST)")
    
    support_hours_sunday = StringField('Sunday Support Hours', validators=[
        Optional(),
        Length(max=50)
    ], description="e.g. Closed")
    
    urgent_email = StringField('Urgent Support Email', validators=[
        Optional(),
        Length(max=100)
    ], description="Email for urgent matters outside support hours")
    
    submit = SubmitField('Save Content Settings')