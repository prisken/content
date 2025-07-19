from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # User role and permissions
    # role = db.Column(db.String(20), default='user')  # user, admin - TEMPORARILY DISABLED
    
    # User limits and subscription info
    subscription_tier = db.Column(db.String(20), default='free')  # free, pro, enterprise
    content_limit = db.Column(db.Integer, default=50)
    image_limit = db.Column(db.Integer, default=10)
    storage_limit_mb = db.Column(db.Integer, default=100)
    
    # Relationships
    contents = db.relationship('Content', backref='user', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('Image', backref='user', lazy=True, cascade='all, delete-orphan')

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.String(20), primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    tone = db.Column(db.String(20), nullable=False)
    content_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status and scheduling
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, published, failed
    scheduled_time = db.Column(db.DateTime, nullable=True)
    published_time = db.Column(db.DateTime, nullable=True)
    
    # Performance metrics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    
    # Language and regional info
    language = db.Column(db.String(10), default='en')
    region = db.Column(db.String(50), nullable=True)
    
    # Relationships
    images = db.relationship('Image', backref='content', lazy=True, cascade='all, delete-orphan')

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.String(20), primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)
    content_id = db.Column(db.String(20), db.ForeignKey('contents.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    mime_type = db.Column(db.String(100), nullable=False)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Image metadata
    alt_text = db.Column(db.String(500), nullable=True)
    caption = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # JSON string of tags 