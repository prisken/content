#!/usr/bin/env python3
"""
Local Backend Test Script
Run this to test your backend locally
"""

import os
import sys

# Set environment variables for local testing
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_APP'] = 'run.py'
os.environ['SECRET_KEY'] = '1e5ff73c70e9d4cccecc9a1a438ceac6c997cd0f05d04906dc6fbd07f1ff441c'
os.environ['CLOUDINARY_CLOUD_NAME'] = 'debyzbnjb'
os.environ['CLOUDINARY_API_KEY'] = '117158686154364'
os.environ['CLOUDINARY_API_SECRET'] = 'QkWKsPdbREy6Ox86kpncl6q4KbI'
os.environ['DEEPSEEK_API_KEY'] = 'sk-9d217f003dd24fd1bc1ce4e5440b11e9'
os.environ['DATABASE_URL'] = 'sqlite:///content_creator_dev.db'
os.environ['ALLOWED_ORIGINS'] = 'http://localhost:3000'

if __name__ == '__main__':
    print("🚀 Starting Content Creator Pro Backend (Local)")
    print("📍 Backend URL: http://localhost:5000")
    print("🔗 Frontend URL: http://localhost:3000")
    print("📊 Health Check: http://localhost:5000/health")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        from run import app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1) 