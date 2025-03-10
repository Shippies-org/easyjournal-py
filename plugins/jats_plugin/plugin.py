"""
JATS XML Generation Plugin

This plugin adds JATS XML generation functionality to the journal system,
allowing editors to generate JATS XML for articles after they've been accepted.
The plugin uses a configurable API endpoint to process DOCX files.
"""

import os
import json
import requests
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import Submission, Publication
from plugin_system import PluginSystem
from .models import JATSXMLRecord, JATSAPISettings

# Create a blueprint for JATS XML routes
jats_bp = Blueprint('jats', __name__, url_prefix='/jats',
                    template_folder='templates')


def get_jats_upload_folder():
    """Get the upload folder for JATS XML files."""
    # Create the folder if it doesn't exist
    uploads_folder = os.path.join(current_app.root_path, 'uploads', 'jats')
    os.makedirs(uploads_folder, exist_ok=True)
    return uploads_folder


@jats_bp.route('/dashboard')
@login_required
def index():
    """Render the JATS XML dashboard."""
    # Ensure user is an editor or admin
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to access the JATS XML dashboard.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get all submissions with JATS XML records
    xml_records = JATSXMLRecord.query.join(Submission).order_by(JATSXMLRecord.updated_at.desc()).all()
    
    # Get API settings
    api_settings = JATSAPISettings.get_settings()
    
    return render_template(
        'jats/dashboard.html',
        title='JATS XML Dashboard',
        xml_records=xml_records,
        api_settings=api_settings
    )


@jats_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Manage JATS API settings."""
    # Ensure user is an admin
    if not current_user.is_admin():
        flash('You do not have permission to access the JATS API settings.', 'danger')
        return redirect(url_for('jats.index'))
    
    api_settings = JATSAPISettings.get_settings()
    
    if request.method == 'POST':
        api_settings.api_url = request.form.get('api_url')
        api_settings.api_key = request.form.get('api_key')
        api_settings.timeout = int(request.form.get('timeout', 30))
        
        db.session.commit()
        flash('JATS API settings updated successfully.', 'success')
        return redirect(url_for('jats.index'))
    
    return render_template(
        'jats/settings.html',
        title='JATS API Settings',
        api_settings=api_settings
    )


@jats_bp.route('/generate/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def generate_xml(submission_id):
    """Generate JATS XML for a submission."""
    # Ensure user is an editor or admin
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to generate JATS XML.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get the submission
    submission = Submission.query.get_or_404(submission_id)
    
    # Check if the submission is accepted or published
    if submission.status not in ['accepted', 'published']:
        flash('JATS XML can only be generated for accepted or published submissions.', 'warning')
        return redirect(url_for('review.publishing_dashboard'))
    
    # Check if a record already exists
    xml_record = JATSXMLRecord.query.filter_by(submission_id=submission_id).first()
    
    if xml_record is None:
        xml_record = JATSXMLRecord(submission_id=submission_id)
        db.session.add(xml_record)
        db.session.commit()
    
    if request.method == 'POST':
        # Get API settings
        api_settings = JATSAPISettings.get_settings()
        
        # Update the status to processing
        xml_record.status = 'processing'
        db.session.commit()
        
        try:
            # Get the file path
            file_path = os.path.join(current_app.root_path, submission.file_path)
            
            # Prepare metadata
            metadata = {
                'title': submission.title,
                'authors': submission.authors,
                'abstract': submission.abstract,
                'keywords': submission.keywords,
                'category': submission.category,
                'submission_date': submission.submitted_at.isoformat(),
            }
            
            # Add publication info if available
            publication = Publication.query.filter_by(submission_id=submission_id).first()
            if publication and publication.is_published():
                metadata['publication_date'] = publication.published_at.isoformat()
                metadata['volume'] = publication.issue.volume
                metadata['issue'] = publication.issue.issue_number
                metadata['page_start'] = publication.page_start
                metadata['page_end'] = publication.page_end
                metadata['issue_title'] = publication.issue.title
            
            # Prepare files for upload
            files = {
                'document': (os.path.basename(file_path), open(file_path, 'rb')),
                'metadata': ('metadata.json', json.dumps(metadata))
            }
            
            # Prepare headers
            headers = {}
            if api_settings.api_key:
                headers['Authorization'] = f'Bearer {api_settings.api_key}'
            
            # Send request to the API
            response = requests.post(
                api_settings.api_url,
                files=files,
                headers=headers,
                timeout=api_settings.timeout
            )
            
            # Check response
            if response.status_code == 200:
                # Save the XML content
                xml_content = response.content
                xml_filename = f'jats_xml_{submission_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xml'
                xml_path = os.path.join(get_jats_upload_folder(), xml_filename)
                
                with open(xml_path, 'wb') as f:
                    f.write(xml_content)
                
                # Update the record
                xml_record.xml_file_path = os.path.join('uploads', 'jats', xml_filename)
                xml_record.status = 'completed'
                xml_record.generated_at = datetime.utcnow()
                db.session.commit()
                
                flash('JATS XML generated successfully.', 'success')
                return redirect(url_for('jats.view_xml', record_id=xml_record.id))
            else:
                # Update the record with error
                xml_record.status = 'error'
                xml_record.error_message = f'API Error: {response.status_code} - {response.text}'
                db.session.commit()
                
                flash(f'Error generating JATS XML: {response.text}', 'danger')
                
        except Exception as e:
            # Update the record with error
            xml_record.status = 'error'
            xml_record.error_message = str(e)
            db.session.commit()
            
            flash(f'Error generating JATS XML: {str(e)}', 'danger')
        
        return redirect(url_for('jats.index'))
    
    return render_template(
        'jats/generate.html',
        title='Generate JATS XML',
        submission=submission,
        xml_record=xml_record
    )


@jats_bp.route('/view/<int:record_id>')
@login_required
def view_xml(record_id):
    """View a JATS XML record."""
    # Ensure user is an editor or admin
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to view JATS XML records.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get the record
    xml_record = JATSXMLRecord.query.get_or_404(record_id)
    
    # Check if the XML file exists
    xml_path = None
    xml_content = None
    if xml_record.xml_file_path:
        xml_path = os.path.join(current_app.root_path, xml_record.xml_file_path)
        if os.path.exists(xml_path):
            with open(xml_path, 'r') as f:
                xml_content = f.read()
    
    return render_template(
        'jats/view.html',
        title='View JATS XML',
        xml_record=xml_record,
        xml_content=xml_content
    )


@jats_bp.route('/download/<int:record_id>')
@login_required
def download_xml(record_id):
    """Download a JATS XML file."""
    # Ensure user is an editor or admin
    if not current_user.is_editor() and not current_user.is_admin():
        flash('You do not have permission to download JATS XML files.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get the record
    xml_record = JATSXMLRecord.query.get_or_404(record_id)
    
    # Check if the XML file exists
    if not xml_record.xml_file_path:
        flash('XML file not found.', 'danger')
        return redirect(url_for('jats.view_xml', record_id=record_id))
    
    xml_path = os.path.join(current_app.root_path, xml_record.xml_file_path)
    if not os.path.exists(xml_path):
        flash('XML file not found.', 'danger')
        return redirect(url_for('jats.view_xml', record_id=record_id))
    
    # Get the filename
    filename = os.path.basename(xml_path)
    
    return send_file(
        xml_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/xml'
    )


# Add "Generate JATS XML" button to the publishing dashboard
def add_publication_actions(args):
    """
    Add JATS XML actions to the publication workflow.
    This hook adds a "Generate JATS XML" button to the submission view page.
    """
    if not args or 'submission' not in args:
        return ''
    
    submission = args['submission']
    
    # Check if the submission is accepted or published
    if submission.status not in ['accepted', 'published']:
        return ''
    
    # Check if JATS XML has already been generated
    xml_record = JATSXMLRecord.query.filter_by(submission_id=submission.id).first()
    
    if xml_record:
        # XML already exists, provide a button to view it
        if xml_record.status == 'completed':
            # Link to view the XML
            return f'''
            <a href="{url_for('jats.view_xml', record_id=xml_record.id)}" 
               class="btn btn-sm btn-primary">
                <i class="bi bi-file-earmark-code"></i> View JATS XML
            </a>
            '''
        elif xml_record.status == 'error':
            # Link to retry generation
            return f'''
            <a href="{url_for('jats.generate_xml', submission_id=submission.id)}" 
               class="btn btn-sm btn-warning">
                <i class="bi bi-arrow-repeat"></i> Retry JATS XML Generation
            </a>
            '''
        elif xml_record.status == 'processing':
            # Show processing status
            return '''
            <button class="btn btn-sm btn-secondary" disabled>
                <i class="bi bi-hourglass-split"></i> JATS XML Processing...
            </button>
            '''
        else:
            # Link to generate
            return f'''
            <a href="{url_for('jats.generate_xml', submission_id=submission.id)}" 
               class="btn btn-sm btn-outline-primary">
                <i class="bi bi-file-earmark-code"></i> Generate JATS XML
            </a>
            '''
    else:
        # No XML yet, provide a button to generate it
        return f'''
        <a href="{url_for('jats.generate_xml', submission_id=submission.id)}" 
           class="btn btn-sm btn-outline-primary">
            <i class="bi bi-file-earmark-code"></i> Generate JATS XML
        </a>
        '''


# Add navigation items to the main menu
def add_navigation_items(args):
    """
    Add JATS XML navigation items to the main navigation menu.
    """
    if not args:
        return ''
    
    # Only add the menu item if the user is an editor or admin
    user = args.get('user')
    if not user or (not user.is_editor() and not user.is_admin()):
        return ''
    
    return '''
    <li class="nav-item">
        <a class="nav-link" href="/jats/dashboard">
            <i class="bi bi-file-earmark-code"></i> JATS XML
        </a>
    </li>
    '''


def register_plugin():
    """
    Register this plugin with the plugin system.
    This function is called when the plugin is loaded.
    """
    # Register the blueprint
    PluginSystem.register_hook('before_request', lambda app: app.register_blueprint(jats_bp), plugin_name='jats_plugin')
    
    # Register the hooks
    PluginSystem.register_hook('submission_view_actions', add_publication_actions, plugin_name='jats_plugin')
    PluginSystem.register_hook('navigation_items', add_navigation_items, plugin_name='jats_plugin')