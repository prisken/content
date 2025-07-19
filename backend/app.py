import os
from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# Optional imports for production features
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("Warning: Cloudinary not available. Image features will be limited.")

try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    print("Warning: Celery not available. Background jobs will be disabled.")

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///content_creator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Import models first to get the db instance
from models import db, User, Content, Image

# Initialize extensions with the db instance from models
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, origins=[
    'https://content-gray-nu.vercel.app',
    'https://content-priskens-projects-61a29b86.vercel.app',
    'http://localhost:3000'
], supports_credentials=True)

# Cloudinary configuration
if CLOUDINARY_AVAILABLE:
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET')
    )
else:
    print("Cloudinary not configured - image features disabled")

# Celery configuration
if CELERY_AVAILABLE:
    celery = Celery('content_creator', broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
    celery.conf.update(app.config)
else:
    celery = None
    print("Celery not configured - background jobs disabled")

# Import routes
from routes import auth_routes, content_routes, image_routes, api_routes, admin_routes

# Register blueprints
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(content_routes, url_prefix='/api/content')
app.register_blueprint(image_routes, url_prefix='/api/images')
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(admin_routes, url_prefix='/api/admin')

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 