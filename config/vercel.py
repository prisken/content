import os
from datetime import timedelta

class VercelConfig:
    """Vercel serverless configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # Database Configuration - Disabled for serverless
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # AI Services Configuration
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
    DEEPSEEK_API_BASE = os.environ.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    
    # Social Media APIs
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
    
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
    
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    INSTAGRAM_APP_ID = os.environ.get('INSTAGRAM_APP_ID')
    INSTAGRAM_APP_SECRET = os.environ.get('INSTAGRAM_APP_SECRET')
    
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    
    # Content Sources
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'app/static/uploads'
    
    # Regional Configuration
    DEFAULT_REGION = 'global'
    DEFAULT_LANGUAGE = 'en'
    
    # Content Direction Configuration
    CONTENT_DIRECTIONS = [
        'business_finance', 'technology', 'health_wellness', 'education',
        'entertainment', 'travel_tourism', 'food_cooking', 'fashion_beauty',
        'sports_fitness', 'science_research', 'politics_current_events',
        'environment_sustainability', 'personal_development', 'parenting_family',
        'art_creativity', 'real_estate', 'automotive', 'pet_care'
    ] 