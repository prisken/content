import os
from datetime import timedelta

class TestingConfig:
    """Testing configuration"""
    
    # Flask Configuration
    SECRET_KEY = 'test-secret-key'
    DEBUG = True
    TESTING = True
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    
    # AI Services Configuration
    DEEPSEEK_API_KEY = 'test-api-key'
    DEEPSEEK_API_BASE = 'https://api.deepseek.com'
    
    # Social Media APIs
    LINKEDIN_CLIENT_ID = 'test-client-id'
    LINKEDIN_CLIENT_SECRET = 'test-client-secret'
    
    FACEBOOK_APP_ID = 'test-app-id'
    FACEBOOK_APP_SECRET = 'test-app-secret'
    
    TWITTER_API_KEY = 'test-api-key'
    TWITTER_API_SECRET = 'test-api-secret'
    TWITTER_ACCESS_TOKEN = 'test-access-token'
    TWITTER_ACCESS_TOKEN_SECRET = 'test-access-token-secret'
    
    INSTAGRAM_APP_ID = 'test-app-id'
    INSTAGRAM_APP_SECRET = 'test-app-secret'
    
    YOUTUBE_API_KEY = 'test-api-key'
    
    # Content Sources
    NEWS_API_KEY = 'test-api-key'
    GOOGLE_BOOKS_API_KEY = 'test-api-key'
    
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