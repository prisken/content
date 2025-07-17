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