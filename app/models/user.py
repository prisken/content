from app import db
from datetime import datetime
import json

class User(db.Model):
    """User model with regional preferences and content direction settings"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    subscription_tier = db.Column(db.String(50), default='free')
    region = db.Column(db.String(50), default='global')
    language = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(50))
    cultural_preferences = db.Column(db.Text)  # JSON string
    preferred_directions = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content = db.relationship('Content', backref='user', lazy=True)
    social_media_accounts = db.relationship('SocialMediaAccount', backref='user', lazy=True)
    
    def __init__(self, email, name=None, region='global', language='en'):
        self.email = email
        self.name = name
        self.region = region
        self.language = language
        self.cultural_preferences = json.dumps({})
        self.preferred_directions = json.dumps([])
    
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
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'subscription_tier': self.subscription_tier,
            'region': self.region,
            'language': self.language,
            'timezone': self.timezone,
            'cultural_preferences': self.cultural_preferences_dict,
            'preferred_directions': self.preferred_directions_list,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>' 