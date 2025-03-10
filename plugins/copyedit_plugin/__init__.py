"""
Copy Editing Plugin for EasyJournal

This plugin adds copy editing functionality to the journal system,
allowing editors to assign copyeditors to submissions, and for copyeditors
to download, edit, and upload Word documents with comments.
"""

# We don't use relative imports here to avoid package issues
try:
    from plugins.copyedit_plugin.plugin import register_plugin
except ImportError:
    # Fallback for direct plugin loading
    pass