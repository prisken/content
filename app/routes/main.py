from flask import Blueprint, render_template, request, jsonify, current_app
from app.models.user import User
from app.models.content import Content
from app.models.content_direction import ContentDirection
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

@main_bp.route('/generator')
def generator():
    """Content generator page"""
    return render_template('generator.html')

@main_bp.route('/library')
def library():
    """Content library page"""
    return render_template('library.html')

@main_bp.route('/settings')
def settings():
    """User settings page"""
    return render_template('settings.html')

@main_bp.route('/api/directions')
def get_directions():
    """Get available content directions"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            # Return static data for serverless deployment
            directions_data = [
                {
                    'id': 1,
                    'direction_key': 'business_finance',
                    'name': 'Business & Finance',
                    'description': 'Content related to business strategies, financial markets, entrepreneurship, and corporate insights.'
                },
                {
                    'id': 2,
                    'direction_key': 'technology',
                    'name': 'Technology',
                    'description': 'Latest tech trends, software development, AI, and digital innovation.'
                },
                {
                    'id': 3,
                    'direction_key': 'health_wellness',
                    'name': 'Health & Wellness',
                    'description': 'Physical health, mental wellness, nutrition, and lifestyle tips.'
                },
                {
                    'id': 4,
                    'direction_key': 'education',
                    'name': 'Education',
                    'description': 'Learning resources, academic insights, and educational content.'
                },
                {
                    'id': 5,
                    'direction_key': 'entertainment',
                    'name': 'Entertainment',
                    'description': 'Movies, music, gaming, and pop culture content.'
                },
                {
                    'id': 6,
                    'direction_key': 'travel_tourism',
                    'name': 'Travel & Tourism',
                    'description': 'Travel guides, destination reviews, and tourism insights.'
                }
            ]
            return jsonify({
                'success': True,
                'directions': directions_data
            })
        
        directions = ContentDirection.query.all()
        return jsonify({
            'success': True,
            'directions': [direction.to_dict() for direction in directions]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/directions/<direction_key>/sources')
def get_direction_sources(direction_key):
    """Get sources for specific direction"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            # Return static data for serverless deployment
            sources_data = {
                'business_finance': ['news', 'research', 'industry_reports', 'expert_insights'],
                'technology': ['news', 'research', 'product_reviews', 'expert_insights'],
                'health_wellness': ['news', 'research', 'expert_insights', 'user_experiences'],
                'education': ['news', 'research', 'academic_papers', 'expert_insights'],
                'entertainment': ['news', 'reviews', 'interviews', 'user_experiences'],
                'travel_tourism': ['news', 'reviews', 'travel_guides', 'user_experiences']
            }
            
            if direction_key not in sources_data:
                return jsonify({
                    'success': False,
                    'error': 'Direction not found'
                }), 404
            
            return jsonify({
                'success': True,
                'sources': sources_data[direction_key]
            })
        
        direction = ContentDirection.query.filter_by(direction_key=direction_key).first()
        if not direction:
            return jsonify({
                'success': False,
                'error': 'Direction not found'
            }), 404
        
        return jsonify({
            'success': True,
            'sources': direction.sources_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/directions/<direction_key>/topics')
def get_direction_topics(direction_key):
    """Get topics for specific direction"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            # Return static data for serverless deployment
            topics_data = {
                'business_finance': ['startup_advice', 'market_analysis', 'investment_tips', 'leadership'],
                'technology': ['ai_ml', 'web_development', 'mobile_apps', 'cybersecurity'],
                'health_wellness': ['nutrition', 'fitness', 'mental_health', 'preventive_care'],
                'education': ['online_learning', 'skill_development', 'academic_research', 'teaching_methods'],
                'entertainment': ['movie_reviews', 'music_news', 'gaming', 'celebrity_news'],
                'travel_tourism': ['destination_guides', 'travel_tips', 'cultural_insights', 'budget_travel']
            }
            
            if direction_key not in topics_data:
                return jsonify({
                    'success': False,
                    'error': 'Direction not found'
                }), 404
            
            return jsonify({
                'success': True,
                'topics': topics_data[direction_key]
            })
        
        direction = ContentDirection.query.filter_by(direction_key=direction_key).first()
        if not direction:
            return jsonify({
                'success': False,
                'error': 'Direction not found'
            }), 404
        
        return jsonify({
            'success': True,
            'topics': direction.subcategories_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 