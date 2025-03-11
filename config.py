"""
Configuration settings for the Academic Journal Submission System

This module provides a centralized configuration system that reads from environment
variables with sensible defaults. This allows for easy configuration changes
without modifying code.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Helper function to get current datetime (for templates)
def now():
    return datetime.now()

# Load environment variables from .env file if it exists
load_dotenv()

# Application configuration
APP_NAME = "EasyJournal"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A comprehensive platform for academic publishing workflow management"
DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

# Database settings
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///instance/journal.db")

# Security settings
SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-key-for-journal-application")

# GDPR default text settings - moved from app.py for better performance
DEFAULT_CONSENT_TEXT = """We value your privacy.
EasyJournal collects and processes your personal data (name, email, affiliation) to manage your submissions, peer review process, and publish your articles. By continuing, you consent to our storage and use of your data as described in our Privacy Policy. You can withdraw consent or request data removal at any time."""

DEFAULT_PRIVACY_POLICY = """# Privacy Policy

## What data we collect
EasyJournal collects and stores the following information:
- Name, email address, and institutional affiliation
- Submission content and metadata
- Review comments and decisions
- User activity for system functionality

## How we use your data
Your data is used exclusively for:
- Managing the journal submission and review process
- Publishing accepted articles
- Providing personalized user experience
- Improving our services

## Your rights
Under GDPR, you have the right to:
- Access your personal data
- Request correction of inaccurate data
- Request deletion of your data
- Object to processing of your data
- Request restriction of processing
- Data portability
- Lodge complaints with supervisory authorities

## Data retention
We keep your data for as long as necessary to provide our services and comply with legal obligations.

## Contact
For any privacy-related inquiries, please contact the journal administration."""
SESSION_LIFETIME = timedelta(days=1)
PASSWORD_MIN_LENGTH = 8

# File upload settings
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

# Demo mode configuration
DEMO_MODE = os.environ.get("DEMO_MODE", "True").lower() == "true"

# Test account configuration (used when seeding demo data)
TEST_ACCOUNTS = {
    "admin": {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": os.environ.get("ADMIN_PASSWORD", "adminpassword"),
        "role": "admin"
    },
    "editor": {
        "name": "Editor User",
        "email": "editor@example.com",
        "password": os.environ.get("EDITOR_PASSWORD", "editorpassword"),
        "role": "editor"
    },
    "reviewer": {
        "name": "Reviewer User",
        "email": "reviewer@example.com",
        "password": os.environ.get("REVIEWER_PASSWORD", "reviewerpassword"),
        "role": "reviewer"
    },
    "author": {
        "name": "Author User",
        "email": "author@example.com",
        "password": os.environ.get("AUTHOR_PASSWORD", "authorpassword"),
        "role": "author"
    }
}