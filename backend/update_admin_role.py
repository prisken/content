#!/usr/bin/env python3
"""
Script to update the admin user with admin role
Run this after adding the role field to the User model
"""

import os
from dotenv import load_dotenv
from app import app, db
from models import User

def update_admin_role():
    with app.app_context():
        # Find the admin user
        admin_user = User.query.get('admin@contentcreator.com')
        
        if admin_user:
            # Update the role to admin
            admin_user.role = 'admin'
            db.session.commit()
            print("✅ Admin user role updated successfully!")
        else:
            print("❌ Admin user not found. Please register the admin user first.")

if __name__ == '__main__':
    load_dotenv()
    update_admin_role() 