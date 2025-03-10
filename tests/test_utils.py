"""
Tests for utility functions.

This module contains tests for utility functions used throughout the application.
"""

import unittest
import os
from datetime import datetime

import config
from app import create_app, db


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def setUp(self):
        """Set up test case."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after test case."""
        self.app_context.pop()

    def test_now_function(self):
        """Test the now function in config."""
        # Test that now() returns a datetime object
        now = config.now()
        self.assertIsInstance(now, datetime)
        
        # Test that now() returns the current time
        current_time = datetime.now()
        self.assertLess((current_time - now).total_seconds(), 1.0)  # Within 1 second

    def test_upload_folder_exists(self):
        """Test that the upload folder exists."""
        self.assertTrue(os.path.exists(config.UPLOAD_FOLDER))
        self.assertTrue(os.path.isdir(config.UPLOAD_FOLDER))

    def test_app_config(self):
        """Test that app configuration is properly loaded."""
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], config.DATABASE_URL)
        self.assertEqual(self.app.config['SECRET_KEY'], config.SECRET_KEY)
        self.assertEqual(self.app.config['MAX_CONTENT_LENGTH'], config.MAX_CONTENT_LENGTH)
        self.assertEqual(self.app.config['UPLOAD_FOLDER'], config.UPLOAD_FOLDER)

    def test_app_context_processor(self):
        """Test that the context processor works correctly."""
        with self.app.test_request_context():
            context = self.app.jinja_env.globals
            self.assertIn('now', context)
            self.assertIn('DEMO_MODE', context)

            # Test that now() is callable
            now_result = context['now']()
            self.assertIsInstance(now_result, datetime)


if __name__ == '__main__':
    unittest.main()