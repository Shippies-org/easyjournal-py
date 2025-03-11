"""
Script to clean up legacy theme settings from the database.
"""

from app import create_app, db
from models import SystemSetting

def remove_theme_overrides():
    """Remove theme override settings and custom color settings from database."""
    app = create_app()
    with app.app_context():
        # Get all theme-related settings to remove
        settings_to_remove = [
            'override_theme',
            'primary_color',
            'secondary_color',
            'accent_color',
            'use_navbar_gradient',
            'gradient_direction',
            'gradient_from_color',
            'gradient_to_color'
        ]
        
        # Delete each setting
        for setting_key in settings_to_remove:
            setting = SystemSetting.query.filter_by(setting_key=setting_key).first()
            if setting:
                print(f"Removing setting: {setting_key}")
                db.session.delete(setting)
        
        # Commit changes
        db.session.commit()
        print("Theme override settings removed successfully")

if __name__ == "__main__":
    remove_theme_overrides()