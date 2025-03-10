"""
Copy Editing Plugin

This plugin adds copy editing functionality to the journal system, 
allowing users to download, upload, and comment on Word documents.
"""

# Plugin metadata
PLUGIN_INFO = {
    'name': 'Copy Editing Plugin',
    'description': 'Adds copy editing functionality to the journal system, allowing editors to assign copyeditors to submissions, and for copyeditors to download, edit, and upload Word documents with comments.',
    'version': '1.0.0',
    'author': 'EasyJournal Team',
    'website': 'https://easyjournal.example.com',
    'documentation': 'https://easyjournal.example.com/docs/plugins/copyediting',
    'min_version': '1.0.0',
    'license': 'MIT',
}
import os
import re
import logging
import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user

from plugin_system import PluginSystem
from app import db
from models import Submission, User
# Use absolute imports to avoid package issues
from plugins.copyedit_plugin.models import CopyEdit, CopyEditComment

logger = logging.getLogger(__name__)

# Create a blueprint for the copy editing routes
copyedit_bp = Blueprint('copyedit', __name__, url_prefix='/copyedit', 
                       template_folder='templates')

# Log output
logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'doc', 'docx', 'rtf', 'txt'}

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_copy_edit_upload_folder():
    """Get the upload folder for copy edited files."""
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'copyedits')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@copyedit_bp.route('/')
@login_required
def index():
    """Render the copy editing dashboard."""
    # Editor or admin can see all copy editing assignments
    if current_user.is_editor() or current_user.is_admin():
        copyedits = CopyEdit.query.all()
    else:
        # Other users only see their own assignments
        copyedits = CopyEdit.query.filter_by(copyeditor_id=current_user.id).all()
    
    return render_template('copyedit/dashboard.html', 
                          title='Copy Editing Dashboard',
                          copyedits=copyedits)

@copyedit_bp.route('/assign/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def assign_copyeditor(submission_id):
    """Assign a copy editor to a submission."""
    # Only editors and admins can assign copy editors
    if not (current_user.is_editor() or current_user.is_admin()):
        flash('You do not have permission to assign copy editors.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    if request.method == 'POST':
        copyeditor_id = request.form.get('copyeditor_id')
        if not copyeditor_id:
            flash('Please select a copy editor.', 'danger')
            return redirect(url_for('copyedit.assign_copyeditor', submission_id=submission_id))
        
        # Create new copy editing record
        copyedit = CopyEdit(
            submission_id=submission_id,
            copyeditor_id=copyeditor_id,
            status='assigned',
            original_file_path=submission.file_path
        )
        
        db.session.add(copyedit)
        db.session.commit()
        
        flash('Copy editor assigned successfully.', 'success')
        return redirect(url_for('copyedit.index'))
    
    # Get all users who could be copy editors (not the author)
    potential_copyeditors = User.query.filter(
        User.id != submission.author_id
    ).order_by(User.name).all()
    
    return render_template('copyedit/assign_copyeditor.html',
                          title='Assign Copy Editor',
                          submission=submission,
                          potential_copyeditors=potential_copyeditors)

@copyedit_bp.route('/view/<int:copyedit_id>')
@login_required
def view_copyedit(copyedit_id):
    """View a copy editing assignment."""
    copyedit = CopyEdit.query.get_or_404(copyedit_id)
    
    # Only the assigned copy editor, editor, admin, or author can view
    if not (current_user.id == copyedit.copyeditor_id or 
            current_user.id == copyedit.submission.author_id or
            current_user.is_editor() or current_user.is_admin()):
        flash('You do not have permission to view this copy editing assignment.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    comments = copyedit.comments.order_by(CopyEditComment.created_at.desc()).all()
    
    return render_template('copyedit/view_copyedit.html',
                          title='Copy Editing Assignment',
                          copyedit=copyedit,
                          comments=comments)

@copyedit_bp.route('/download/<int:copyedit_id>/<string:file_type>')
@login_required
def download_document(copyedit_id, file_type):
    """Download a document (original or edited)."""
    copyedit = CopyEdit.query.get_or_404(copyedit_id)
    
    # Check permissions
    if not (current_user.id == copyedit.copyeditor_id or 
            current_user.id == copyedit.submission.author_id or
            current_user.is_editor() or current_user.is_admin()):
        flash('You do not have permission to download this document.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Determine which file to download
    if file_type == 'original':
        file_path = copyedit.original_file_path
    elif file_type == 'edited':
        file_path = copyedit.edited_file_path
    else:
        flash('Invalid file type specified.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    if not file_path:
        flash(f'No {file_type} document available.', 'warning')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Extract just the filename from the path
    filename = os.path.basename(file_path)
    directory = os.path.dirname(file_path)
    
    return send_from_directory(directory, filename, as_attachment=True)

@copyedit_bp.route('/upload/<int:copyedit_id>', methods=['POST'])
@login_required
def upload_document(copyedit_id):
    """Upload an edited document."""
    copyedit = CopyEdit.query.get_or_404(copyedit_id)
    
    # Only the assigned copy editor can upload the edited document
    if current_user.id != copyedit.copyeditor_id:
        flash('You do not have permission to upload an edited document.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Create secure filename and save path
        filename = secure_filename(file.filename)
        # Add timestamp to filename to prevent conflicts
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Ensure the copyedit upload folder exists
        upload_folder = get_copy_edit_upload_folder()
        
        # Save the file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Update copy edit record
        copyedit.edited_file_path = file_path
        copyedit.status = 'in_progress'
        copyedit.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        flash('Document uploaded successfully.', 'success')
    else:
        flash('Invalid file type. Please upload a Word document, RTF, or text file.', 'danger')
    
    return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))

@copyedit_bp.route('/comment/<int:copyedit_id>', methods=['POST'])
@login_required
def add_comment(copyedit_id):
    """Add a comment to a copy editing assignment."""
    copyedit = CopyEdit.query.get_or_404(copyedit_id)
    
    # Check permissions (copy editor, editor, admin, or author can comment)
    if not (current_user.id == copyedit.copyeditor_id or 
            current_user.id == copyedit.submission.author_id or
            current_user.is_editor() or current_user.is_admin()):
        flash('You do not have permission to comment on this document.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    comment_text = request.form.get('comment')
    page_number = request.form.get('page_number')
    line_number = request.form.get('line_number')
    
    if not comment_text or comment_text.strip() == '':
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Create new comment
    comment = CopyEditComment(
        copyedit_id=copyedit_id,
        user_id=current_user.id,
        comment=comment_text,
        page_number=page_number if page_number else None,
        line_number=line_number if line_number else None
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment added successfully.', 'success')
    return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))

@copyedit_bp.route('/complete/<int:copyedit_id>', methods=['POST'])
@login_required
def complete_copyedit(copyedit_id):
    """Mark a copy editing assignment as complete."""
    copyedit = CopyEdit.query.get_or_404(copyedit_id)
    
    # Only the assigned copy editor can mark as complete
    if current_user.id != copyedit.copyeditor_id:
        flash('You do not have permission to complete this copy editing assignment.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Ensure an edited document has been uploaded
    if not copyedit.edited_file_path:
        flash('You must upload an edited document before marking the assignment as complete.', 'danger')
        return redirect(url_for('copyedit.view_copyedit', copyedit_id=copyedit_id))
    
    # Update status
    copyedit.status = 'completed'
    copyedit.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    
    flash('Copy editing assignment marked as complete.', 'success')
    return redirect(url_for('copyedit.index'))

def add_navigation_items(args):
    """
    Add copy editing navigation items to the main navigation menu.
    """
    if not args.get('current_user') or not args.get('current_user').is_authenticated:
        return args
    
    nav_items = args.get('nav_items', [])
    current_user = args.get('current_user')
    
    # Add copy editing link for editors, admins, and users with copy editing assignments
    if current_user.is_editor() or current_user.is_admin():
        nav_items.append({
            'url': '/copyedit',
            'name': 'Copy Editing',
            'icon': 'bi bi-pencil-square'
        })
    else:
        # Check if the user has any copy editing assignments
        # Use absolute imports to avoid package issues
        from plugins.copyedit_plugin.models import CopyEdit
        copyedit_count = CopyEdit.query.filter_by(copyeditor_id=current_user.id).count()
        if copyedit_count > 0:
            nav_items.append({
                'url': '/copyedit',
                'name': 'Copy Editing',
                'icon': 'bi bi-pencil-square'
            })
    
    args['nav_items'] = nav_items
    return args

def register_plugin():
    """
    Register this plugin with the plugin system.
    This function is called when the plugin is loaded.
    """
    logger.info("Registering Copy Editing Plugin")
    
    # Import models to ensure they're registered with SQLAlchemy
    # Use absolute import to avoid package issues
    import plugins.copyedit_plugin.models
    
    # We'll handle database creation and blueprint registration with Flask's
    # current_app object to avoid circular imports
    from flask import current_app
    
    # Create tables if they don't exist
    with current_app.app_context():
        db.create_all()
    
    # Register the blueprint with the current app
    current_app.register_blueprint(copyedit_bp)
    
    # Register the hook to add navigation items
    PluginSystem.register_hook('getNavItems', add_navigation_items, 10, 'copyedit_plugin')
    
    return True