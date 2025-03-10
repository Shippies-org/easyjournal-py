"""
Tests for database models.

This module contains tests for the database models to ensure they work correctly.
"""

import unittest
from datetime import datetime, timedelta

from app import create_app, db
from models import User, Submission, Review, EditorDecision


class TestModels(unittest.TestCase):
    """Test cases for database models."""

    def setUp(self):
        """Set up test case with a test app and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after test case."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        """Test User model creation and methods."""
        # Create test user
        user = User(
            name='Test User',
            email='test@example.com',
            password='password',
            role='author',
            institution='Test University',
            bio='Test researcher bio'
        )
        db.session.add(user)
        db.session.commit()

        # Test retrieval
        retrieved_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, 'Test User')
        self.assertEqual(retrieved_user.role, 'author')
        self.assertEqual(retrieved_user.institution, 'Test University')

        # Test password hashing
        self.assertTrue(retrieved_user.check_password('password'))
        self.assertFalse(retrieved_user.check_password('wrong_password'))

        # Test role methods
        self.assertTrue(retrieved_user.is_author())
        self.assertFalse(retrieved_user.is_editor())
        self.assertFalse(retrieved_user.is_reviewer())
        self.assertFalse(retrieved_user.is_admin())

    def test_submission_model(self):
        """Test Submission model creation and relationships."""
        # Create test user
        user = User(
            name='Test Author',
            email='author@example.com',
            password='password',
            role='author'
        )
        db.session.add(user)
        db.session.commit()

        # Create test submission
        submission = Submission(
            title='Test Submission',
            authors='Test Author, Another Author',
            abstract='This is a test abstract for the submission.',
            keywords='test, submission, model',
            category='computer_science',
            file_path='/uploads/test.pdf',
            cover_letter='Test cover letter',
            author_id=user.id
        )
        db.session.add(submission)
        db.session.commit()

        # Test retrieval
        retrieved_submission = Submission.query.filter_by(title='Test Submission').first()
        self.assertIsNotNone(retrieved_submission)
        self.assertEqual(retrieved_submission.authors, 'Test Author, Another Author')
        self.assertEqual(retrieved_submission.status, 'submitted')  # Default status
        self.assertIsInstance(retrieved_submission.submitted_at, datetime)

        # Test author relationship
        self.assertEqual(retrieved_submission.author.name, 'Test Author')
        self.assertEqual(user.submissions.count(), 1)
        self.assertEqual(user.submissions.first().title, 'Test Submission')

    def test_review_model(self):
        """Test Review model creation and relationships."""
        # Create test users
        author = User(name='Test Author', email='author@example.com', password='password', role='author')
        reviewer = User(name='Test Reviewer', email='reviewer@example.com', password='password', role='reviewer')
        editor = User(name='Test Editor', email='editor@example.com', password='password', role='editor')
        db.session.add_all([author, reviewer, editor])
        db.session.commit()

        # Create test submission
        submission = Submission(
            title='Test Submission',
            authors='Test Author',
            abstract='Test abstract',
            category='computer_science',
            file_path='/uploads/test.pdf',
            author_id=author.id
        )
        db.session.add(submission)
        db.session.commit()

        # Create test review
        due_date = datetime.now() + timedelta(days=14)
        review = Review(
            submission_id=submission.id,
            reviewer_id=reviewer.id,
            editor_id=editor.id,
            due_date=due_date
        )
        db.session.add(review)
        db.session.commit()

        # Test retrieval
        retrieved_review = Review.query.first()
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review.status, 'assigned')  # Default status
        self.assertIsNone(retrieved_review.content)
        self.assertIsNone(retrieved_review.decision)

        # Test relationships
        self.assertEqual(retrieved_review.submission.title, 'Test Submission')
        self.assertEqual(retrieved_review.reviewer.name, 'Test Reviewer')
        self.assertEqual(retrieved_review.editor.name, 'Test Editor')
        self.assertEqual(reviewer.reviews_given.count(), 1)
        self.assertEqual(editor.reviews_assigned.count(), 1)

        # Test completion
        self.assertFalse(retrieved_review.is_completed())
        retrieved_review.content = 'This is a review.'
        retrieved_review.decision = 'accept'
        retrieved_review.status = 'completed'
        retrieved_review.completed_at = datetime.now()
        db.session.commit()
        self.assertTrue(retrieved_review.is_completed())

        # Test overdue
        self.assertFalse(retrieved_review.is_overdue())
        retrieved_review.due_date = datetime.now() - timedelta(days=1)
        db.session.commit()
        self.assertTrue(retrieved_review.is_overdue())


if __name__ == '__main__':
    unittest.main()