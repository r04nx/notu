"""
Script to create an admin user and associate existing notes with this user.
Run this script after migrating the database to add authentication.
"""
from app import create_app, db
from app.models import User, Note
from flask import current_app

def create_admin_user():
    """Create an admin user and associate all existing notes with this user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists.")
        else:
            # Create admin user
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('adminpassword')
            db.session.add(admin)
            db.session.commit()
            print(f"Created admin user with username: 'admin' and password: 'adminpassword'")
        
        # Associate existing notes with admin user
        orphan_notes = Note.query.filter_by(user_id=None).all()
        if orphan_notes:
            for note in orphan_notes:
                note.user_id = admin.id
            db.session.commit()
            print(f"Associated {len(orphan_notes)} existing notes with admin user.")
        else:
            print("No orphaned notes found.")

if __name__ == '__main__':
    create_admin_user()
