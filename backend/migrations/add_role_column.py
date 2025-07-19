#!/usr/bin/env python3
"""
Migration script to add role column to users table
Run this to update the database schema
"""

import os
from dotenv import load_dotenv
from app import app, db

def add_role_column():
    with app.app_context():
        try:
            # Add role column to users table
            db.engine.execute("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(20) DEFAULT 'user'
            """)
            
            # Update existing admin user
            db.engine.execute("""
                UPDATE users 
                SET role = 'admin' 
                WHERE email = 'admin@contentcreator.com'
            """)
            
            print("✅ Role column added successfully!")
            print("✅ Admin user role updated!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Column might already exist, continuing...")

if __name__ == '__main__':
    load_dotenv()
    add_role_column() 