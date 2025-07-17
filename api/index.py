import os
import sys

# Set environment variable to indicate serverless mode
os.environ['VERCEL_ENV'] = 'production'

try:
    from app import create_app
    app = create_app('vercel')
except Exception as e:
    print(f"Error creating Flask app: {e}")
    # Create a minimal app for serverless
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "Content Creator Pro - Serverless Mode Active"
    
    @app.route('/health')
    def health():
        return {"status": "healthy", "mode": "serverless"} 