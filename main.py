"""
Main entry point for the Academic Journal Submission System Flask application.

This module initializes the application and defines routes for serving
static files and handling compatibility with the existing PHP system.
"""

from app import app
import os
import config
from flask import send_from_directory

# Configure app to serve uploaded files
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve uploaded files."""
    # If the path starts with 'branding', use the uploads directory directly
    if filename.startswith('branding/'):
        return send_from_directory('uploads', filename)
    # Otherwise use the config.UPLOAD_FOLDER
    return send_from_directory(config.UPLOAD_FOLDER, filename)

# Configure app to serve CSS files
@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files."""
    return send_from_directory('css', filename)

# Ensure upload directories exist with proper error handling
for folder in [config.UPLOAD_FOLDER, os.path.join(config.UPLOAD_FOLDER, 'demo')]:
    if not os.path.exists(folder):
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Created directory: {folder}")
        except Exception as dir_error:
            print(f"Warning: Could not create directory {folder}: {str(dir_error)}")
            # This is non-fatal - continue with application startup
        
# Create sample demo PDF files - but make it optional
try:
    demo_files = [
        (os.path.join(config.UPLOAD_FOLDER, 'demo_paper1.pdf'), 'Sample paper 1'),
        (os.path.join(config.UPLOAD_FOLDER, 'demo_paper2.pdf'), 'Sample paper 2'),
        (os.path.join(config.UPLOAD_FOLDER, 'demo_paper3.pdf'), 'Sample paper 3')
    ]

    for file_path, content in demo_files:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"Created demo file: {file_path}")
            except Exception as e:
                print(f"Warning: Could not create demo file {file_path}: {str(e)}")
                # This is non-fatal - demo files are optional
except Exception as demo_file_error:
    print(f"Warning: Skipping demo file creation: {str(demo_file_error)}")

# Ensure demo data is loaded when the app starts
with app.app_context():
    from models import db, User, Submission, Review, EditorDecision
    from datetime import datetime, timedelta
    
    # Create database tables if they don't exist
    db.create_all()
    
    # Check if we need to seed demo data (if no users exist)
    if config.DEMO_MODE and User.query.count() == 0:
        print("Seeding demo data...")
        try:
            # Create test accounts from config
            for role, account in config.TEST_ACCOUNTS.items():
                user = User(
                    name=account['name'],
                    email=account['email'],
                    password=account['password'],
                    role=role,
                    institution=account.get('institution', 'Test University'),
                    bio=account.get('bio', f'This is a test {role} account.')
                )
                db.session.add(user)
            
            db.session.commit()
            
            # Get user IDs for demo data
            author = User.query.filter_by(role='author').first()
            editor = User.query.filter_by(role='editor').first()
            reviewer = User.query.filter_by(role='reviewer').first()
            
            if author and editor and reviewer:
                # Create demo submissions
                submissions = [
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
                
                # Add submissions
                for sub_data in submissions:
                    submission = Submission(
                        title=sub_data["title"],
                        authors=sub_data["authors"],
                        abstract=sub_data["abstract"],
                        keywords=sub_data["keywords"],
                        category=sub_data["category"],
                        file_path=sub_data["file_path"],
                        cover_letter=sub_data["cover_letter"],
                        status=sub_data["status"],
                        author_id=author.id
                    )
                    db.session.add(submission)
                
                db.session.commit()
                
                # Add a review for the in_review submission
                in_review_submission = Submission.query.filter_by(status='in_review').first()
                if in_review_submission:
                    review = Review(
                        submission_id=in_review_submission.id,
                        reviewer_id=reviewer.id,
                        editor_id=editor.id,
                        status='assigned',
                        due_date=datetime.utcnow() + timedelta(days=14)
                    )
                    db.session.add(review)
                    
                    # Add some completed reviews and editorial decisions
                    accepted_submission = Submission.query.filter_by(status='accepted').first()
                    if accepted_submission:
                        completed_review = Review(
                            submission_id=accepted_submission.id,
                            reviewer_id=reviewer.id,
                            editor_id=editor.id,
                            content="This paper presents excellent research with strong methodology.",
                            decision="accept",
                            status="completed",
                            assigned_at=datetime.utcnow() - timedelta(days=30),
                            due_date=datetime.utcnow() - timedelta(days=15),
                            completed_at=datetime.utcnow() - timedelta(days=20)
                        )
                        db.session.add(completed_review)
                        
                        # Add editorial decision
                        decision = EditorDecision(
                            submission_id=accepted_submission.id,
                            editor_id=editor.id,
                            decision="accept",
                            comments="This paper is accepted based on positive peer reviews."
                        )
                        db.session.add(decision)
                
                db.session.commit()
            
            print("Demo data seeded successfully!")
        except Exception as e:
            print(f"Error seeding demo data: {str(e)}")

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)