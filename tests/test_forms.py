"""
Tests for form validation.

This module contains tests for form validation to ensure forms work correctly.
"""

import unittest
from io import BytesIO
from datetime import datetime, timedelta

from app import create_app
from forms.auth import LoginForm, RegistrationForm
from forms.submission import SubmissionForm, RevisionForm
from forms.review import ReviewForm, AssignReviewerForm, EditorDecisionForm
from forms.admin import UserForm, IssueForm, PublicationForm


class TestForms(unittest.TestCase):
    """Test cases for form validation."""

    def setUp(self):
        """Set up test case."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after test case."""
        self.app_context.pop()

    def test_login_form(self):
        """Test LoginForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = LoginForm(email='user@example.com', password='password')
            self.assertTrue(form.validate())

            # Test missing email
            form = LoginForm(email='', password='password')
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.email.errors)

            # Test invalid email format
            form = LoginForm(email='invalid-email', password='password')
            self.assertFalse(form.validate())
            self.assertIn('Invalid email address', form.email.errors)

            # Test missing password
            form = LoginForm(email='user@example.com', password='')
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.password.errors)

    def test_registration_form(self):
        """Test RegistrationForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = RegistrationForm(
                name='Test User',
                email='user@example.com',
                password='password123',
                confirm_password='password123',
                institution='Test University',
                bio='Test bio'
            )
            self.assertTrue(form.validate())

            # Test password mismatch
            form = RegistrationForm(
                name='Test User',
                email='user@example.com',
                password='password123',
                confirm_password='different',
                institution='Test University',
                bio='Test bio'
            )
            self.assertFalse(form.validate())
            self.assertIn('Passwords must match', form.confirm_password.errors)

            # Test short password
            form = RegistrationForm(
                name='Test User',
                email='user@example.com',
                password='short',
                confirm_password='short',
                institution='Test University',
                bio='Test bio'
            )
            self.assertFalse(form.validate())
            self.assertIn('Password must be at least 8 characters long', form.password.errors)

            # Test missing name
            form = RegistrationForm(
                name='',
                email='user@example.com',
                password='password123',
                confirm_password='password123'
            )
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.name.errors)

    def test_submission_form(self):
        """Test SubmissionForm validation."""
        with self.app.test_request_context():
            # Create a mock file
            test_file = (BytesIO(b'test file content'), 'test.pdf')
            
            # Test valid form
            form = SubmissionForm(
                title='Test Submission',
                authors='Author One, Author Two',
                abstract='This is a detailed abstract with sufficient length for testing purposes.',
                keywords='test, submission, form',
                category='computer_science',
                file=test_file,
                cover_letter='This is a cover letter'
            )
            self.assertTrue(form.validate())

            # Test missing title
            form = SubmissionForm(
                title='',
                authors='Author One, Author Two',
                abstract='This is a detailed abstract with sufficient length for testing purposes.',
                category='computer_science',
                file=test_file
            )
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.title.errors)

            # Test short abstract
            form = SubmissionForm(
                title='Test Submission',
                authors='Author One, Author Two',
                abstract='Too short',
                category='computer_science',
                file=test_file
            )
            self.assertFalse(form.validate())
            self.assertIn('least 100 characters', form.abstract.errors)

            # Test invalid file type
            invalid_file = (BytesIO(b'test file content'), 'test.exe')
            form = SubmissionForm(
                title='Test Submission',
                authors='Author One, Author Two',
                abstract='This is a detailed abstract with sufficient length for testing purposes.',
                category='computer_science',
                file=invalid_file
            )
            self.assertFalse(form.validate())
            self.assertIn('Only PDF, DOC, DOCX, TXT, and RTF files are allowed', form.file.errors)

    def test_review_form(self):
        """Test ReviewForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = ReviewForm(
                content='This is a detailed review with sufficient length to meet the minimum requirements. It discusses the paper in depth and provides constructive feedback to the authors. The review addresses the methodology, results, and conclusions of the paper.',
                decision='accept'
            )
            self.assertTrue(form.validate())

            # Test short review content
            form = ReviewForm(
                content='Too short',
                decision='accept'
            )
            self.assertFalse(form.validate())
            self.assertIn('Please provide a detailed review of at least 200 characters', form.content.errors)

            # Test missing decision
            form = ReviewForm(
                content='This is a detailed review with sufficient length to meet the minimum requirements. It discusses the paper in depth and provides constructive feedback to the authors. The review addresses the methodology, results, and conclusions of the paper.',
                decision=''
            )
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.decision.errors)

    def test_editor_decision_form(self):
        """Test EditorDecisionForm validation."""
        with self.app.test_request_context():
            # Test valid form
            form = EditorDecisionForm(
                decision='accept',
                comments='This paper is accepted for publication. The research is sound and the presentation is clear. The authors have addressed all reviewer concerns adequately.'
            )
            self.assertTrue(form.validate())

            # Test short comments
            form = EditorDecisionForm(
                decision='accept',
                comments='Too short'
            )
            self.assertFalse(form.validate())
            self.assertIn('Please provide comments of at least 50 characters', form.comments.errors)

            # Test missing decision
            form = EditorDecisionForm(
                decision='',
                comments='This paper is accepted for publication. The research is sound and the presentation is clear. The authors have addressed all reviewer concerns adequately.'
            )
            self.assertFalse(form.validate())
            self.assertIn('This field is required', form.decision.errors)


if __name__ == '__main__':
    unittest.main()