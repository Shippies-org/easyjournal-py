"""
Tests for application routes.

This module contains tests for route handlers to ensure they function correctly.
"""

import unittest
import flask
from io import BytesIO

from app import create_app, db
from models import User, Submission


class TestRoutes(unittest.TestCase):
    """Test cases for application routes."""

    def setUp(self):
        """Set up test case with a test app and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after test case."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self, role='author'):
        """Create a test user with the specified role."""
        user = User(
            name=f'Test {role.capitalize()}',
            email=f'{role}@example.com',
            password='password',
            role=role,
            institution='Test University'
        )
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, email, password):
        """Log in a user through the login route."""
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_index_route(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EasyJournal', response.data)

    def test_about_route(self):
        """Test the about route."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_contact_route(self):
        """Test the contact route."""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact', response.data)

    def test_login_route(self):
        """Test the login route."""
        # Test GET request
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        # Create a test user
        user = self.create_user()

        # Test successful login
        response = self.login(user.email, 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

        # Test failed login
        response = self.login(user.email, 'wrong_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

    def test_register_route(self):
        """Test the register route."""
        # Test GET request
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

        # Test successful registration
        response = self.client.post('/register', data=dict(
            name='New User',
            email='new@example.com',
            password='password',
            confirm_password='password',
            institution='New University',
            bio='New researcher'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

        # Verify the user was created
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'New User')
        self.assertEqual(user.role, 'author')  # Default role

    def test_logout_route(self):
        """Test the logout route."""
        # Create and login a user
        user = self.create_user()
        self.login(user.email, 'password')

        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_protected_routes(self):
        """Test that protected routes require authentication."""
        # Test author dashboard without login
        response = self.client.get('/author/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        # Test reviewer dashboard without login
        response = self.client.get('/reviewer/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        # Test editor dashboard without login
        response = self.client.get('/editor/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        # Test admin dashboard without login
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_role_protected_routes(self):
        """Test that role-protected routes require appropriate roles."""
        # Create and login an author
        author = self.create_user('author')
        self.login(author.email, 'password')

        # Try to access reviewer dashboard as author
        response = self.client.get('/reviewer/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Try to access editor dashboard as author
        response = self.client.get('/editor/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Try to access admin dashboard as author
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Logout
        self.client.get('/logout')

        # Create and login an editor
        editor = self.create_user('editor')
        self.login(editor.email, 'password')

        # Try to access admin dashboard as editor
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 403)  # Forbidden


if __name__ == '__main__':
    unittest.main()