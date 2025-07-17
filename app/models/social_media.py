from app import db
from datetime import datetime
import json

class SocialMediaAccount(db.Model):
    """Social media account model for platform connections"""
    
    __tablename__ = 'social_media_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(255))
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, platform, account_name=None):
        self.user_id = user_id
        self.platform = platform
        self.account_name = account_name
    
    def to_dict(self):
        """Convert social media account to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'platform': self.platform,
            'account_name': self.account_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SocialMediaAccount {self.platform} - {self.account_name}>'


class SocialMediaPost(db.Model):
    """Social media post model for tracking published content"""
    
    __tablename__ = 'social_media_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    platform_post_id = db.Column(db.String(255))
    post_status = db.Column(db.String(50), default='pending')
    scheduled_time = db.Column(db.DateTime)
    posted_time = db.Column(db.DateTime)
    engagement_metrics = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, content_id, platform, scheduled_time=None):
        self.content_id = content_id
        self.platform = platform
        self.scheduled_time = scheduled_time
    
    @property
    def engagement_metrics_dict(self):
        """Get engagement metrics as dictionary"""
        try:
            return json.loads(self.engagement_metrics) if self.engagement_metrics else {}
        except json.JSONDecodeError:
            return {}
    
    @engagement_metrics_dict.setter
    def engagement_metrics_dict(self, value):
        """Set engagement metrics from dictionary"""
        self.engagement_metrics = json.dumps(value)
    
    def to_dict(self):
        """Convert social media post to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'platform': self.platform,
            'platform_post_id': self.platform_post_id,
            'post_status': self.post_status,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'posted_time': self.posted_time.isoformat() if self.posted_time else None,
            'engagement_metrics': self.engagement_metrics_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SocialMediaPost {self.platform} - {self.post_status}>'


class ContentLibrary(db.Model):
    """Content library model for organizing saved content"""
    
    __tablename__ = 'content_library'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    title = db.Column(db.String(255))
    tags = db.Column(db.Text)  # JSON string
    regional_tags = db.Column(db.Text)  # JSON string
    direction_tags = db.Column(db.Text)  # JSON string
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, content_id, title=None):
        self.user_id = user_id
        self.content_id = content_id
        self.title = title
        self.tags = json.dumps([])
        self.regional_tags = json.dumps([])
        self.direction_tags = json.dumps([])
    
    @property
    def tags_list(self):
        """Get tags as list"""
        try:
            return json.loads(self.tags) if self.tags else []
        except json.JSONDecodeError:
            return []
    
    @tags_list.setter
    def tags_list(self, value):
        """Set tags from list"""
        self.tags = json.dumps(value)
    
    @property
    def regional_tags_list(self):
        """Get regional tags as list"""
        try:
            return json.loads(self.regional_tags) if self.regional_tags else []
        except json.JSONDecodeError:
            return []
    
    @regional_tags_list.setter
    def regional_tags_list(self, value):
        """Set regional tags from list"""
        self.regional_tags = json.dumps(value)
    
    @property
    def direction_tags_list(self):
        """Get direction tags as list"""
        try:
            return json.loads(self.direction_tags) if self.direction_tags else []
        except json.JSONDecodeError:
            return []
    
    @direction_tags_list.setter
    def direction_tags_list(self, value):
        """Set direction tags from list"""
        self.direction_tags = json.dumps(value)
    
    def to_dict(self):
        """Convert content library item to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id,
            'title': self.title,
            'tags': self.tags_list,
            'regional_tags': self.regional_tags_list,
            'direction_tags': self.direction_tags_list,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ContentLibrary {self.title}>' 