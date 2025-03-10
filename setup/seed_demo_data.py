#!/usr/bin/env python3
"""
Seed Demo Data Script for Academic Journal Submission System

This script seeds the database with demo data for testing the system.
Usage: python seed_demo_data.py [--reset]
"""

import os
import sys
import argparse
import sqlite3
import hashlib
import random
import string
import time
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def generate_salt(length=16):
    """Generate a random salt for password hashing"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def hash_password(password, salt):
    """Hash a password using SHA-256 with a salt"""
    hash_obj = hashlib.sha256((password + salt).encode())
    return hash_obj.hexdigest()


def reset_database(db_path):
    """Reset the database by deleting all data from tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Delete all data from each table except sqlite_sequence
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"DELETE FROM {table_name};")
        
        # Reset autoincrement counters
        cursor.execute("DELETE FROM sqlite_sequence;")
        
        # Commit the transaction
        conn.commit()
        print("Database reset completed successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"Database error during reset: {e}")
        return False
    
    finally:
        conn.close()


def create_test_accounts(db_path):
    """Create test accounts for each role using configuration from config.py"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create test accounts for each role
        for role, account in config.TEST_ACCOUNTS.items():
            # Generate a salt and hash the password
            salt = generate_salt()
            password_hash = hash_password(account['password'], salt)
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (account['email'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update existing user
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = ?, password_salt = ?
                    WHERE email = ?
                """, (password_hash, salt, account['email']))
            else:
                # Create new user
                cursor.execute("""
                    INSERT INTO users (name, email, password_hash, password_salt, role, institution, bio)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"Test {role.capitalize()}", 
                    account['email'], 
                    password_hash, 
                    salt, 
                    role,
                    f"Test Institution for {role.capitalize()}",
                    f"This is a test account for the {role} role."
                ))
        
        # Commit the transaction
        conn.commit()
        print("Test accounts created successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"Database error creating test accounts: {e}")
        return False
    
    finally:
        conn.close()


def create_demo_submissions(db_path):
    """Create demo article submissions"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get the author ID
        cursor.execute("SELECT id FROM users WHERE role = 'author' LIMIT 1")
        author = cursor.fetchone()
        
        if not author:
            print("No author account found. Please create test accounts first.")
            return False
        
        author_id = author[0]
        
        # Create demo submissions
        demo_submissions = [
            {
                "title": "Advances in Machine Learning for Healthcare",
                "authors": "John Smith, Sarah Johnson",
                "abstract": "This paper presents novel machine learning techniques for healthcare applications...",
                "keywords": "machine learning, healthcare, artificial intelligence",
                "category": "Computer Science",
                "file_path": "uploads/demo_paper1.pdf",
                "cover_letter": "Dear Editor, I am pleased to submit our manuscript for consideration...",
                "status": "submitted"
            },
            {
                "title": "Climate Change Effects on Biodiversity",
                "authors": "Emily Chen, David Williams",
                "abstract": "This study examines the impact of climate change on global biodiversity patterns...",
                "keywords": "climate change, biodiversity, ecology",
                "category": "Environmental Science",
                "file_path": "uploads/demo_paper2.pdf",
                "cover_letter": "Dear Editor, We believe our research on climate change is timely...",
                "status": "in_review"
            },
            {
                "title": "Novel Approach to Quantum Computing",
                "authors": "Michael Brown, Lisa Garcia",
                "abstract": "We present a new approach to quantum computing that enhances qubit stability...",
                "keywords": "quantum computing, qubits, quantum physics",
                "category": "Physics",
                "file_path": "uploads/demo_paper3.pdf",
                "cover_letter": "Dear Editor, Our breakthrough in quantum computing represents...",
                "status": "accepted"
            }
        ]
        
        # Insert the demo submissions
        for submission in demo_submissions:
            cursor.execute("""
                INSERT INTO submissions (
                    title, authors, abstract, keywords, category, 
                    file_path, cover_letter, status, author_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                submission["title"],
                submission["authors"],
                submission["abstract"],
                submission["keywords"],
                submission["category"],
                submission["file_path"],
                submission["cover_letter"],
                submission["status"],
                author_id
            ))
        
        # Commit the transaction
        conn.commit()
        print("Demo submissions created successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"Database error creating demo submissions: {e}")
        return False
    
    finally:
        conn.close()


def create_demo_reviews(db_path):
    """Create demo review assignments and reviews"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get the reviewer ID
        cursor.execute("SELECT id FROM users WHERE role = 'reviewer' LIMIT 1")
        reviewer = cursor.fetchone()
        
        if not reviewer:
            print("No reviewer account found. Please create test accounts first.")
            return False
        
        reviewer_id = reviewer[0]
        
        # Get the editor ID
        cursor.execute("SELECT id FROM users WHERE role = 'editor' LIMIT 1")
        editor = cursor.fetchone()
        
        if not editor:
            print("No editor account found. Please create test accounts first.")
            return False
        
        editor_id = editor[0]
        
        # Get in_review submission ID
        cursor.execute("SELECT id FROM submissions WHERE status = 'in_review' LIMIT 1")
        submission = cursor.fetchone()
        
        if not submission:
            print("No in_review submission found. Please create demo submissions first.")
            return False
        
        submission_id = submission[0]
        
        # Create a review assignment
        due_date = datetime.now() + timedelta(days=14)
        due_date_str = due_date.strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            INSERT INTO review_assignments (
                submission_id, reviewer_id, editor_id, due_date, status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            submission_id,
            reviewer_id,
            editor_id,
            due_date_str,
            'pending'
        ))
        
        # Get the assignment ID
        assignment_id = cursor.lastrowid
        
        # Create a completed review for another submission
        cursor.execute("SELECT id FROM submissions WHERE status = 'accepted' LIMIT 1")
        completed_submission = cursor.fetchone()
        
        if completed_submission:
            completed_submission_id = completed_submission[0]
            
            # Create an assignment
            cursor.execute("""
                INSERT INTO review_assignments (
                    submission_id, reviewer_id, editor_id, due_date, status, completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                completed_submission_id,
                reviewer_id,
                editor_id,
                due_date_str,
                'completed',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            completed_assignment_id = cursor.lastrowid
            
            # Create a review
            cursor.execute("""
                INSERT INTO reviews (
                    assignment_id, content, decision
                )
                VALUES (?, ?, ?)
            """, (
                completed_assignment_id,
                "This is a high-quality paper with significant contributions. The methodology is sound and the results are compelling. I recommend acceptance with minor revisions.",
                "accept"
            ))
        
        # Commit the transaction
        conn.commit()
        print("Demo reviews created successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"Database error creating demo reviews: {e}")
        return False
    
    finally:
        conn.close()


def main():
    """Main function to parse arguments and seed demo data"""
    parser = argparse.ArgumentParser(description='Seed demo data for the Academic Journal Submission System')
    parser.add_argument('--reset', action='store_true', help='Reset the database before seeding')
    
    args = parser.parse_args()
    
    # Get database path from config
    db_path = config.DB_NAME
    
    # Reset the database if requested
    if args.reset:
        if not reset_database(db_path):
            print("Failed to reset database.")
            sys.exit(1)
    
    # Create test accounts
    if not create_test_accounts(db_path):
        print("Failed to create test accounts.")
        sys.exit(1)
    
    # Create demo submissions
    if not create_demo_submissions(db_path):
        print("Failed to create demo submissions.")
        sys.exit(1)
    
    # Create demo reviews
    if not create_demo_reviews(db_path):
        print("Failed to create demo reviews.")
        sys.exit(1)
    
    print("Demo data seeding completed successfully!")


if __name__ == "__main__":
    main()