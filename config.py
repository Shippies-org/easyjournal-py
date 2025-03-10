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