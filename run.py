#!/usr/bin/env python3
"""
Content Creator Pro - Main Application Entry Point
"""

import os
from app import create_app, db
from app.models.user import User
from app.models.content import Content, ContentVersion
from app.models.social_media import SocialMediaAccount, SocialMediaPost
from app.models.content_direction import ContentDirection, RegionalData

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add database models to Flask shell context"""
    return {
        'db': db,
        'User': User,
        'Content': Content,
        'ContentVersion': ContentVersion,
        'SocialMediaAccount': SocialMediaAccount,
        'SocialMediaPost': SocialMediaPost,
        'ContentDirection': ContentDirection,
        'RegionalData': RegionalData
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Add sample content directions
        add_sample_directions()
        print("Sample content directions added!")
        
        # Add sample user
        add_sample_user()
        print("Sample user added!")

def add_sample_directions():
    """Add sample content directions to the database"""
    directions = [
        {
            'direction_key': 'business_finance',
            'direction_name': 'Business & Finance',
            'subcategories': ['entrepreneurship', 'investing', 'corporate', 'market_analysis'],
            'language_style': 'professional, authoritative',
            'sources': ['bloomberg', 'cnbc', 'wsj', 'forbes'],
            'hashtags': ['business', 'finance', 'entrepreneurship', 'investing'],
            'regional_adaptation': 'local_markets, regional_business_trends'
        },
        {
            'direction_key': 'technology',
            'direction_name': 'Technology',
            'subcategories': ['tech_news', 'software', 'ai', 'digital_transformation'],
            'language_style': 'innovative, technical',
            'sources': ['techcrunch', 'the_verge', 'wired', 'ars_technica'],
            'hashtags': ['tech', 'innovation', 'ai', 'digital'],
            'regional_adaptation': 'local_tech_scene, regional_innovation'
        },
        {
            'direction_key': 'health_wellness',
            'direction_name': 'Health & Wellness',
            'subcategories': ['fitness', 'nutrition', 'mental_health', 'lifestyle'],
            'language_style': 'supportive, informative',
            'sources': ['health_news', 'nutrition_sources', 'fitness_experts'],
            'hashtags': ['health', 'wellness', 'fitness', 'nutrition'],
            'regional_adaptation': 'local_health_trends, regional_wellness'
        },
        {
            'direction_key': 'education',
            'direction_name': 'Education',
            'subcategories': ['learning', 'skills_development', 'academic_insights', 'online_courses'],
            'language_style': 'informative, educational',
            'sources': ['education_news', 'academic_journals', 'learning_platforms'],
            'hashtags': ['education', 'learning', 'skills', 'academic'],
            'regional_adaptation': 'local_education_trends, regional_learning'
        },
        {
            'direction_key': 'entertainment',
            'direction_name': 'Entertainment',
            'subcategories': ['movies', 'music', 'gaming', 'pop_culture'],
            'language_style': 'engaging, trend_aware',
            'sources': ['entertainment_news', 'music_platforms', 'gaming_sites'],
            'hashtags': ['entertainment', 'movies', 'music', 'gaming'],
            'regional_adaptation': 'local_entertainment, regional_pop_culture'
        },
        {
            'direction_key': 'travel_tourism',
            'direction_name': 'Travel & Tourism',
            'subcategories': ['destinations', 'travel_tips', 'cultural_experiences', 'hospitality'],
            'language_style': 'inspirational, destination_focused',
            'sources': ['travel_guides', 'tourism_news', 'destination_sites'],
            'hashtags': ['travel', 'tourism', 'destinations', 'adventure'],
            'regional_adaptation': 'local_travel_trends, regional_destinations'
        }
    ]
    
    for direction_data in directions:
        # Check if direction already exists
        existing = ContentDirection.query.filter_by(direction_key=direction_data['direction_key']).first()
        if not existing:
            direction = ContentDirection(
                direction_key=direction_data['direction_key'],
                direction_name=direction_data['direction_name'],
                language_style=direction_data['language_style']
            )
            # Set the JSON fields using the property setters
            direction.subcategories_list = direction_data['subcategories']
            direction.sources_list = direction_data['sources']
            direction.hashtags_list = direction_data['hashtags']
            direction.regional_adaptation_dict = direction_data['regional_adaptation']
            db.session.add(direction)
    
    db.session.commit()

def add_sample_user():
    """Add a sample user to the database"""
    # Check if sample user already exists
    existing_user = User.query.filter_by(email='demo@contentcreator.com').first()
    if not existing_user:
        user = User(
            email='demo@contentcreator.com',
            name='Demo User',
            region='global',
            language='en'
        )
        user.subscription_tier = 'premium'  # Set after creation
        db.session.add(user)
        db.session.commit()
        print(f"Sample user created: {user.email}")

@app.cli.command()
def test():
    """Run the application tests"""
    import pytest
    pytest.main(['tests'])

if __name__ == '__main__':
    # Run the Flask development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    ) 