#!/usr/bin/env python3
"""
Create Admin User Script for Academic Journal Submission System

This script creates an initial admin user for the system.
Usage: python create_admin.py [--name NAME] [--email EMAIL] [--password PASSWORD]
"""

import os
import sys
import argparse
import sqlite3
import hashlib
import random
import string

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def generate_salt(length=16):
    """Generate a random salt for password hashing"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def hash_password(password, salt):
    """Hash a password using SHA-256 with a salt"""
    hash_obj = hashlib.sha256((password + salt).encode())
    return hash_obj.hexdigest()


def create_admin_user(name, email, password, db_path):
    """Create an admin user in the database"""
    # Generate a salt and hash the password
    salt = generate_salt()
    password_hash = hash_password(password, salt)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"User with email {email} already exists.")
            conn.close()
            return False
        
        # Create the admin user
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, password_salt, role)
            VALUES (?, ?, ?, ?, 'admin')
        """, (name, email, password_hash, salt))
        
        # Commit the transaction
        conn.commit()
        print(f"Admin user '{name}' with email '{email}' created successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    finally:
        conn.close()


def main():
    """Main function to parse arguments and create the admin user"""
    parser = argparse.ArgumentParser(description='Create an admin user for the Academic Journal Submission System')
    parser.add_argument('--name', dest='name', help='Admin user name')
    parser.add_argument('--email', dest='email', help='Admin user email')
    parser.add_argument('--password', dest='password', help='Admin user password')
    
    args = parser.parse_args()
    
    # Get admin details from arguments or prompt
    name = args.name if args.name else input("Enter admin name: ")
    email = args.email if args.email else input("Enter admin email: ")
    password = args.password if args.password else input("Enter admin password: ")
    
    # Validate inputs
    if not name or not email or not password:
        print("Error: Name, email, and password are required.")
        sys.exit(1)
    
    # Get database path from config
    db_path = config.DB_NAME
    
    # Create the admin user
    if create_admin_user(name, email, password, db_path):
        print("Admin user creation complete!")
    else:
        print("Failed to create admin user.")
        sys.exit(1)


if __name__ == "__main__":
    main()