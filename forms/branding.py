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
    
    # Primary branding colors
    primary_color = StringField('Primary Color', validators=[
        Optional(), 
        Length(max=20)
    ], description="Hex color code (e.g., #007bff)")
    
    secondary_color = StringField('Secondary Color', validators=[
        Optional(), 
        Length(max=20)
    ], description="Hex color code (e.g., #6c757d)")
    
    accent_color = StringField('Accent Color', validators=[
        Optional(), 
        Length(max=20)
    ], description="Hex color code (e.g., #28a745)")
    
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
    
    # Override system theme
    override_theme = BooleanField('Override System Theme with Custom Colors', default=False)
    
    # Navbar gradient options
    use_navbar_gradient = BooleanField('Use Gradient for Navigation Bar', default=False)
    gradient_direction = SelectField('Gradient Direction', choices=[
        ('to right', 'Horizontal'),
        ('to bottom', 'Vertical'),
        ('to bottom right', 'Diagonal'),
        ('radial', 'Radial')
    ], default='to right')
    gradient_from_color = StringField('Gradient Start Color', validators=[
        Optional(), 
        Length(max=20)
    ], description="Starting color for gradient (defaults to primary color)")
    gradient_to_color = StringField('Gradient End Color', validators=[
        Optional(), 
        Length(max=20)
    ], description="Ending color for gradient (defaults to secondary color)")
    
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
    
    submit = SubmitField('Save Content Settings')