from app import db
from datetime import datetime
import json

class User(db.Model):
    """User model with regional preferences and content direction settings"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    name = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')  # user, admin, premium
    is_active = db.Column(db.Boolean, default=True)
    subscription_tier = db.Column(db.String(50), default='free')
    region = db.Column(db.String(50), default='global')
    language = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(50))
    cultural_preferences = db.Column(db.Text)  # JSON string
    preferred_directions = db.Column(db.Text)  # JSON string
    preferences = db.Column(db.Text)  # JSON string for general preferences
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content = db.relationship('Content', backref='user', lazy=True)
    social_media_accounts = db.relationship('SocialMediaAccount', backref='user', lazy=True)
    
    def __init__(self, username, email, password_hash, first_name=None, last_name=None, name=None, role='user', region='global', language='en'):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.role = role
        self.region = region
        self.language = language
        self.cultural_preferences = json.dumps({})
        self.preferred_directions = json.dumps([])
        self.preferences = json.dumps({})
    
    @property
    def cultural_preferences_dict(self):
        """Get cultural preferences as dictionary"""
        try:
            return json.loads(self.cultural_preferences) if self.cultural_preferences else {}
        except json.JSONDecodeError:
            return {}
    
    @cultural_preferences_dict.setter
    def cultural_preferences_dict(self, value):
        """Set cultural preferences from dictionary"""
        self.cultural_preferences = json.dumps(value)
    
    @property
    def preferred_directions_list(self):
        """Get preferred directions as list"""
        try:
            return json.loads(self.preferred_directions) if self.preferred_directions else []
        except json.JSONDecodeError:
            return []
    
    @preferred_directions_list.setter
    def preferred_directions_list(self, value):
        """Set preferred directions from list"""
        self.preferred_directions = json.dumps(value)
    
    @property
    def preferences_dict(self):
        """Get preferences as dictionary"""
        try:
            return json.loads(self.preferences) if self.preferences else {}
        except json.JSONDecodeError:
            return {}
    
    @preferences_dict.setter
    def preferences_dict(self, value):
        """Set preferences from dictionary"""
        self.preferences = json.dumps(value)
    
    def set_password(self, password):
        """Set password hash"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'name': self.name,
            'role': self.role,
            'is_active': self.is_active,
            'subscription_tier': self.subscription_tier,
            'region': self.region,
            'language': self.language,
            'timezone': self.timezone,
            'cultural_preferences': self.cultural_preferences_dict,
            'preferred_directions': self.preferred_directions_list,
            'preferences': self.preferences_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>' 