from app import db
from datetime import datetime
import json

class Content(db.Model):
    """Content model with regional, direction, and social media context"""
    
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_direction = db.Column(db.String(50), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    source_data = db.Column(db.Text)
    generated_content = db.Column(db.Text, nullable=False)
    edited_content = db.Column(db.Text)
    media_url = db.Column(db.String(500))
    tone = db.Column(db.String(50))
    region = db.Column(db.String(50))
    language = db.Column(db.String(10))
    cultural_context = db.Column(db.Text)  # JSON string
    direction_context = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    versions = db.relationship('ContentVersion', backref='content', lazy=True)
    social_media_posts = db.relationship('SocialMediaPost', backref='content', lazy=True)
    
    def __init__(self, user_id, content_direction, content_type, source_type, 
                 generated_content, tone=None, region=None, language=None):
        self.user_id = user_id
        self.content_direction = content_direction
        self.content_type = content_type
        self.source_type = source_type
        self.generated_content = generated_content
        self.tone = tone
        self.region = region
        self.language = language
        self.cultural_context = json.dumps({})
        self.direction_context = json.dumps({})
    
    @property
    def cultural_context_dict(self):
        """Get cultural context as dictionary"""
        try:
            return json.loads(self.cultural_context) if self.cultural_context else {}
        except json.JSONDecodeError:
            return {}
    
    @cultural_context_dict.setter
    def cultural_context_dict(self, value):
        """Set cultural context from dictionary"""
        self.cultural_context = json.dumps(value)
    
    @property
    def direction_context_dict(self):
        """Get direction context as dictionary"""
        try:
            return json.loads(self.direction_context) if self.direction_context else {}
        except json.JSONDecodeError:
            return {}
    
    @direction_context_dict.setter
    def direction_context_dict(self, value):
        """Set direction context from dictionary"""
        self.direction_context = json.dumps(value)
    
    def to_dict(self):
        """Convert content to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_direction': self.content_direction,
            'content_type': self.content_type,
            'source_type': self.source_type,
            'source_data': self.source_data,
            'generated_content': self.generated_content,
            'edited_content': self.edited_content,
            'media_url': self.media_url,
            'tone': self.tone,
            'region': self.region,
            'language': self.language,
            'cultural_context': self.cultural_context_dict,
            'direction_context': self.direction_context_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Content {self.content_type} - {self.content_direction}>'


class ContentVersion(db.Model):
    """Content version history model"""
    
    __tablename__ = 'content_versions'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content_text = db.Column(db.Text, nullable=False)
    edited_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, content_id, version_number, content_text, edited_by=None):
        self.content_id = content_id
        self.version_number = version_number
        self.content_text = content_text
        self.edited_by = edited_by
    
    def to_dict(self):
        """Convert content version to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'version_number': self.version_number,
            'content_text': self.content_text,
            'edited_by': self.edited_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ContentVersion {self.content_id} v{self.version_number}>' 