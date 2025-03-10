"""
Welcome Plugin

This plugin adds a welcome banner to the top of the home page.
"""
import os
import re
import logging
from plugin_system import PluginSystem

logger = logging.getLogger(__name__)

# Plugin metadata
PLUGIN_INFO = {
    'name': 'Welcome Banner Plugin',
    'version': '1.0.0',
    'description': 'Adds a welcome banner to the home page',
    'author': 'Replit AI'
}

def modify_home_content(args):
    """
    This hook function modifies the home page content by adding a welcome banner.
    """
    template_path = args.get('template_path', '')
    page = args.get('page', '')
    
    # Only modify the home page content
    if not (template_path.endswith('home.php') or page.endswith('index.php')):
        return
    
    # Get the content
    content = args.get('content', '')
    
    # Create a welcome banner
    welcome_banner = """
    <div class="alert alert-info text-center mb-4">
        <h4 class="alert-heading">🎉 Welcome to the Academic Journal Submission System!</h4>
        <p>This plugin-enhanced message demonstrates the plugin system's capability to modify content.</p>
        <hr>
        <p class="mb-0">Explore our modular submission workflow designed for researchers and reviewers.</p>
    </div>
    """
    
    # Find the first div in the content (typically the main container)
    # and add the welcome banner after it
    div_pattern = r'<div class="container.*?>'
    if re.search(div_pattern, content):
        modified_content = re.sub(div_pattern, lambda m: m.group(0) + welcome_banner, content, count=1)
        args['content'] = modified_content
        
        # Log the modification
        logger.info("Welcome banner added to home page")
    
    return args

def register_plugin():
    """
    Register this plugin with the plugin system.
    This function is called when the plugin is loaded.
    """
    logger.info("Registering Welcome Banner Plugin")
    
    # Register the hook to modify the home page content
    PluginSystem.register_hook('beforeContentRender', modify_home_content, 10, 'welcome_plugin')
    
    return True