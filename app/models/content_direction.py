from app import db
from datetime import datetime
import json

class ContentDirection(db.Model):
    """Content direction/niche model for managing industry-specific configurations"""
    
    __tablename__ = 'content_directions'
    
    id = db.Column(db.Integer, primary_key=True)
    direction_key = db.Column(db.String(50), unique=True, nullable=False)
    direction_name = db.Column(db.String(255), nullable=False)
    subcategories = db.Column(db.Text)  # JSON string
    language_style = db.Column(db.Text)
    sources = db.Column(db.Text)  # JSON string
    hashtags = db.Column(db.Text)  # JSON string
    regional_adaptation = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, direction_key, direction_name, language_style=None):
        self.direction_key = direction_key
        self.direction_name = direction_name
        self.language_style = language_style
        self.subcategories = json.dumps([])
        self.sources = json.dumps([])
        self.hashtags = json.dumps([])
        self.regional_adaptation = json.dumps({})
    
    @property
    def subcategories_list(self):
        """Get subcategories as list"""
        try:
            return json.loads(self.subcategories) if self.subcategories else []
        except json.JSONDecodeError:
            return []
    
    @subcategories_list.setter
    def subcategories_list(self, value):
        """Set subcategories from list"""
        self.subcategories = json.dumps(value)
    
    @property
    def sources_list(self):
        """Get sources as list"""
        try:
            return json.loads(self.sources) if self.sources else []
        except json.JSONDecodeError:
            return []
    
    @sources_list.setter
    def sources_list(self, value):
        """Set sources from list"""
        self.sources = json.dumps(value)
    
    @property
    def hashtags_list(self):
        """Get hashtags as list"""
        try:
            return json.loads(self.hashtags) if self.hashtags else []
        except json.JSONDecodeError:
            return []
    
    @hashtags_list.setter
    def hashtags_list(self, value):
        """Set hashtags from list"""
        self.hashtags = json.dumps(value)
    
    @property
    def regional_adaptation_dict(self):
        """Get regional adaptation as dictionary"""
        try:
            return json.loads(self.regional_adaptation) if self.regional_adaptation else {}
        except json.JSONDecodeError:
            return {}
    
    @regional_adaptation_dict.setter
    def regional_adaptation_dict(self, value):
        """Set regional adaptation from dictionary"""
        self.regional_adaptation = json.dumps(value)
    
    def to_dict(self):
        """Convert content direction to dictionary"""
        return {
            'id': self.id,
            'direction_key': self.direction_key,
            'direction_name': self.direction_name,
            'subcategories': self.subcategories_list,
            'language_style': self.language_style,
            'sources': self.sources_list,
            'hashtags': self.hashtags_list,
            'regional_adaptation': self.regional_adaptation_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ContentDirection {self.direction_name}>'


class RegionalData(db.Model):
    """Regional data model for storing region-specific content and cultural context"""
    
    __tablename__ = 'regional_data'
    
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)
    data_content = db.Column(db.Text)  # JSON string
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, region, data_type, data_content=None):
        self.region = region
        self.data_type = data_type
        self.data_content = json.dumps(data_content) if data_content else json.dumps({})
    
    @property
    def data_content_dict(self):
        """Get data content as dictionary"""
        try:
            return json.loads(self.data_content) if self.data_content else {}
        except json.JSONDecodeError:
            return {}
    
    @data_content_dict.setter
    def data_content_dict(self, value):
        """Set data content from dictionary"""
        self.data_content = json.dumps(value)
    
    def to_dict(self):
        """Convert regional data to dictionary"""
        return {
            'id': self.id,
            'region': self.region,
            'data_type': self.data_type,
            'data_content': self.data_content_dict,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<RegionalData {self.region} - {self.data_type}>' 