import sqlite3
import os
import hashlib
import secrets
from datetime import datetime
import config

# Database setup constants
DB_NAME = "journal.db"

# Define the user roles as constants
ROLE_AUTHOR = "author"
ROLE_REVIEWER = "reviewer"
ROLE_EDITOR = "editor"
ROLE_ADMIN = "admin"

def get_db_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """Initialize the database with required tables"""
    # Check if the database already exists
    if os.path.exists(DB_NAME):
        print(f"Database '{DB_NAME}' already exists.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL,
        institution TEXT,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')
    
    # Create Submissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        abstract TEXT NOT NULL,
        keywords TEXT,
        category TEXT NOT NULL,
        file_path TEXT,
        cover_letter TEXT,
        author_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES users (id)
    )
    ''')
    
    # Create Reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER NOT NULL,
        reviewer_id INTEGER NOT NULL,
        editor_id INTEGER NOT NULL,
        content TEXT,
        decision TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (submission_id) REFERENCES submissions (id),
        FOREIGN KEY (reviewer_id) REFERENCES users (id),
        FOREIGN KEY (editor_id) REFERENCES users (id)
    )
    ''')
    
    # Create Issues table for organizing accepted papers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volume INTEGER NOT NULL,
        issue_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'planned',
        publication_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(volume, issue_number)
    )
    ''')
    
    # Create Publications table to track which submissions are in which issues
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER NOT NULL,
        issue_id INTEGER NOT NULL,
        page_start INTEGER,
        page_end INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (submission_id) REFERENCES submissions (id),
        FOREIGN KEY (issue_id) REFERENCES issues (id),
        UNIQUE(submission_id, issue_id)
    )
    ''')
    
    # Create Editor Decisions table to track editorial decisions on submissions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS editor_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER NOT NULL,
        editor_id INTEGER NOT NULL,
        decision TEXT NOT NULL,
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (submission_id) REFERENCES submissions (id),
        FOREIGN KEY (editor_id) REFERENCES users (id)
    )
    ''')
    
    # Create a Sessions table for authentication management
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Database '{DB_NAME}' initialized with required tables.")

def hash_password(password, salt=None):
    """
    Hash a password using SHA-256 with a salt
    If salt is not provided, a new one will be generated
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Combine password and salt, then hash
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    
    return password_hash, salt

def verify_password(stored_hash, stored_salt, provided_password):
    """Verify a password against a stored hash and salt"""
    calculated_hash, _ = hash_password(provided_password, stored_salt)
    return calculated_hash == stored_hash

def create_user(name, email, password, role, institution=None, bio=None):
    """Create a new user with hashed password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user with this email already exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        conn.close()
        return False, "A user with this email already exists."
    
    # Hash the password
    password_hash, salt = hash_password(password)
    
    # Insert the new user
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, salt, role, institution, bio) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, email, password_hash, salt, role, institution, bio)
    )
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return True, user_id

def validate_login(email, password):
    """Validate user login credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find user by email
    cursor.execute("SELECT id, password_hash, salt FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if user is None:
        conn.close()
        return False, "Invalid email or password."
    
    # Verify password
    if not verify_password(user['password_hash'], user['salt'], password):
        conn.close()
        return False, "Invalid email or password."
    
    # Update last login time
    cursor.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id'])
    )
    
    conn.commit()
    conn.close()
    
    return True, user['id']

def create_session(user_id, expiry_days=1):
    """Create a new session for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate a unique session token
    session_token = secrets.token_hex(32)
    
    # Calculate expiration time
    expires_at = datetime.now()
    expires_at = expires_at.replace(day=expires_at.day + expiry_days)
    
    # Insert the new session
    cursor.execute(
        "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)",
        (user_id, session_token, expires_at.strftime('%Y-%m-%d %H:%M:%S'))
    )
    
    conn.commit()
    conn.close()
    
    return session_token

def validate_session(session_token):
    """Validate a session token and return the user_id if valid"""
    if not session_token:
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Find valid session
    cursor.execute(
        "SELECT user_id FROM sessions WHERE session_token = ? AND expires_at > ?",
        (session_token, current_time)
    )
    
    session = cursor.fetchone()
    conn.close()
    
    if session:
        return session['user_id']
    return None

def get_user_by_id(user_id):
    """Get user details by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, email, role, institution, bio, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def get_user_role(user_id):
    """Get the role of a user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result['role']
    return None

def create_submission(title, authors, abstract, keywords, category, file_path, cover_letter, author_id):
    """Create a new submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO submissions 
        (title, authors, abstract, keywords, category, file_path, cover_letter, author_id, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (title, authors, abstract, keywords, category, file_path, cover_letter, author_id, 'pending')
    )
    
    conn.commit()
    submission_id = cursor.lastrowid
    conn.close()
    
    return submission_id

def get_submissions_by_author(author_id):
    """Get all submissions by an author"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM submissions WHERE author_id = ? ORDER BY created_at DESC", (author_id,))
    submissions = cursor.fetchall()
    
    conn.close()
    return submissions

def get_all_submissions():
    """Get all submissions (for editors)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.*, u.name as author_name 
        FROM submissions s
        JOIN users u ON s.author_id = u.id
        ORDER BY s.created_at DESC
    """)
    submissions = cursor.fetchall()
    
    conn.close()
    return submissions

def get_pending_submissions():
    """Get submissions pending review assignment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.*, u.name as author_name 
        FROM submissions s
        JOIN users u ON s.author_id = u.id
        WHERE s.status = 'pending'
        ORDER BY s.created_at ASC
    """)
    submissions = cursor.fetchall()
    
    conn.close()
    return submissions

def assign_reviewer(submission_id, reviewer_id, editor_id, due_date):
    """Assign a reviewer to a submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if this reviewer is already assigned to this submission
    cursor.execute(
        "SELECT * FROM reviews WHERE submission_id = ? AND reviewer_id = ?",
        (submission_id, reviewer_id)
    )
    
    if cursor.fetchone() is not None:
        conn.close()
        return False, "This reviewer is already assigned to this submission."
    
    # Create the review assignment
    cursor.execute(
        "INSERT INTO reviews (submission_id, reviewer_id, editor_id, due_date) VALUES (?, ?, ?, ?)",
        (submission_id, reviewer_id, editor_id, due_date)
    )
    
    # Update submission status if this is the first reviewer
    cursor.execute(
        "UPDATE submissions SET status = 'in_review' WHERE id = ?",
        (submission_id,)
    )
    
    conn.commit()
    conn.close()
    
    return True, "Reviewer assigned successfully."

def get_reviewer_assignments(reviewer_id):
    """Get all review assignments for a reviewer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, s.title, s.authors, s.abstract
        FROM reviews r
        JOIN submissions s ON r.submission_id = s.id
        WHERE r.reviewer_id = ? AND r.completed_at IS NULL
        ORDER BY r.due_date ASC
    """)
    
    assignments = cursor.fetchall()
    conn.close()
    
    return assignments

def submit_review(review_id, content, decision):
    """Submit a completed review"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        "UPDATE reviews SET content = ?, decision = ?, completed_at = ?, updated_at = ? WHERE id = ?",
        (content, decision, completed_at, completed_at, review_id)
    )
    
    conn.commit()
    
    # Check if all reviews for this submission are complete
    cursor.execute(
        """
        SELECT r.submission_id, COUNT(*) as total, SUM(CASE WHEN r.completed_at IS NOT NULL THEN 1 ELSE 0 END) as completed
        FROM reviews r
        WHERE r.id = ?
        GROUP BY r.submission_id
        """,
        (review_id,)
    )
    
    result = cursor.fetchone()
    if result and result['total'] == result['completed']:
        # All reviews are complete, update submission status
        cursor.execute(
            "UPDATE submissions SET status = 'reviewed', updated_at = ? WHERE id = ?",
            (completed_at, result['submission_id'])
        )
        conn.commit()
    
    conn.close()
    return True

def create_test_accounts():
    """Create default test accounts for each role using configuration from config.py"""
    if not config.DEMO_MODE:
        print("Demo mode is disabled. Test accounts will not be created.")
        return

    # Use the accounts defined in config.py
    accounts_created = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check for existing test accounts first and delete them if they exist
    for role, account in config.TEST_ACCOUNTS.items():
        email = account['email']
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            user_id = existing_user['id']
            try:
                # Delete any related records in other tables
                # First, clean up any reviews this user might have submitted
                cursor.execute("DELETE FROM reviews WHERE reviewer_id = ? OR editor_id = ?", (user_id, user_id))
                
                # For admin and editor test accounts, we need to clean up all related submissions too
                if role in ['admin', 'editor']:
                    # Find all submissions by this user
                    cursor.execute("SELECT id FROM submissions WHERE author_id = ?", (user_id,))
                    submissions = cursor.fetchall()
                    for sub in submissions:
                        # Delete any reviews for these submissions
                        cursor.execute("DELETE FROM reviews WHERE submission_id = ?", (sub['id'],))
                        # Delete the publications linked to these submissions
                        cursor.execute("DELETE FROM publications WHERE submission_id = ?", (sub['id'],))
                        
                    # Now delete the submissions
                    cursor.execute("DELETE FROM submissions WHERE author_id = ?", (user_id,))
                
                # Delete any sessions for this user
                cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
                
                # Finally, delete the user
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            except Exception as e:
                print(f"Warning: Could not fully clean up test account {email}: {str(e)}")
                # Continue anyway, as we'll try to validate login later
    
    conn.commit()
    conn.close()
    
    # Create author test account
    author_info = config.TEST_ACCOUNTS.get('author')
    if author_info:
        author_created, author_id = create_user(
            name="Author Account",
            email=author_info['email'],
            password=author_info['password'],
            role=ROLE_AUTHOR,
            institution="Test University",
            bio="Test author account with basic permissions."
        )
        accounts_created.append(f"Author: {author_info['email']} / password: {author_info['password']}")
    
    # Create reviewer test account
    reviewer_info = config.TEST_ACCOUNTS.get('reviewer')
    if reviewer_info:
        reviewer_created, reviewer_id = create_user(
            name="Reviewer Account",
            email=reviewer_info['email'],
            password=reviewer_info['password'],
            role=ROLE_REVIEWER,
            institution="Test University",
            bio="Test reviewer account with reviewer permissions."
        )
        accounts_created.append(f"Reviewer: {reviewer_info['email']} / password: {reviewer_info['password']}")
    
    # Create editor test account
    editor_info = config.TEST_ACCOUNTS.get('editor')
    if editor_info:
        editor_created, editor_id = create_user(
            name="Editor Account",
            email=editor_info['email'],
            password=editor_info['password'],
            role=ROLE_EDITOR,
            institution="Test University",
            bio="Test editor account with editor permissions."
        )
        accounts_created.append(f"Editor: {editor_info['email']} / password: {editor_info['password']}")
    
    # Create admin test account
    admin_info = config.TEST_ACCOUNTS.get('admin')
    if admin_info:
        admin_created, admin_id = create_user(
            name="Admin Account",
            email=admin_info['email'],
            password=admin_info['password'],
            role=ROLE_ADMIN,
            institution="Test University",
            bio="Test admin account with full administrative permissions."
        )
        accounts_created.append(f"Admin: {admin_info['email']} / password: {admin_info['password']}")
    
    print("Test accounts created successfully:")
    for account in accounts_created:
        print(account)

def seed_demo_data():
    """Seed the database with demo data for testing"""
    # Create admin user
    admin_created, admin_id = create_user(
        name="Admin User",
        email="admin2@example.com",
        password="admin123",
        role=ROLE_ADMIN,
        institution="Journal Administration",
        bio="System administrator for the journal."
    )
    
    # Create editor user
    editor_created, editor_id = create_user(
        name="Editor User",
        email="editor2@example.com",
        password="editor123",
        role=ROLE_EDITOR,
        institution="University of Science",
        bio="Chief editor with expertise in computer science and digital systems."
    )
    
    # Create reviewer users
    reviewer1_created, reviewer1_id = create_user(
        name="Dr. Emily Johnson",
        email="reviewer1@example.com",
        password="reviewer123",
        role=ROLE_REVIEWER,
        institution="Tech University",
        bio="Expert in machine learning and healthcare AI applications."
    )
    
    reviewer2_created, reviewer2_id = create_user(
        name="Prof. Michael Davis",
        email="reviewer2@example.com",
        password="reviewer123",
        role=ROLE_REVIEWER,
        institution="Research Institute",
        bio="Specialist in data science and healthcare informatics."
    )
    
    # Create author users
    author1_created, author1_id = create_user(
        name="John Smith",
        email="author1@example.com",
        password="author123",
        role=ROLE_AUTHOR,
        institution="Innovation Labs",
        bio="Researcher in artificial intelligence and machine learning."
    )
    
    author2_created, author2_id = create_user(
        name="Maria Chen",
        email="author2@example.com",
        password="author123",
        role=ROLE_AUTHOR,
        institution="Environmental Science Center",
        bio="Researcher focused on climate change and ecosystems."
    )
    
    # Create some sample submissions
    if author1_created:
        submission1_id = create_submission(
            title="Advanced Machine Learning in Healthcare Diagnostics",
            authors="John Smith, Sarah Williams",
            abstract="This paper explores the application of advanced machine learning algorithms in healthcare diagnostics, focusing on early disease detection and prevention.",
            keywords="machine learning, healthcare, diagnostics, AI",
            category="Original Research",
            file_path="uploads/sample1.pdf",
            cover_letter="We are pleased to submit our original research on machine learning applications in healthcare.",
            author_id=author1_id
        )
    
    if author2_created:
        submission2_id = create_submission(
            title="Climate Change Effects on Marine Ecosystems",
            authors="Maria Chen, Alex Peterson",
            abstract="This review examines the impact of climate change on marine ecosystems, synthesizing recent findings and identifying research gaps.",
            keywords="climate change, marine ecosystems, environmental science",
            category="Review Article",
            file_path="uploads/sample2.pdf",
            cover_letter="Our review article provides a comprehensive analysis of climate change impacts on marine ecosystems.",
            author_id=author2_id
        )
    
    # Add a few more submissions
    if author1_created:
        submission3_id = create_submission(
            title="Neural Networks for Natural Language Processing",
            authors="John Smith, David Kumar",
            abstract="This paper presents novel approaches to using neural networks for natural language processing tasks.",
            keywords="neural networks, NLP, deep learning",
            category="Original Research",
            file_path="uploads/sample3.pdf",
            cover_letter="We present a novel approach to natural language processing using advanced neural network architectures.",
            author_id=author1_id
        )
    
    print("Demo data seeded successfully.")

if __name__ == "__main__":
    # Initialize the database and seed with demo data
    init_db()
    seed_demo_data()
    
    # Create test accounts for easy login
    try:
        create_test_accounts()
    except Exception as e:
        print(f"Note: Test accounts could not be created: {str(e)}")