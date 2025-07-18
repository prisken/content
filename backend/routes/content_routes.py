from flask import Blueprint, request, jsonify, session
from models import db, Content, User
from datetime import datetime
import uuid

content_routes = Blueprint('content', __name__)

def generate_content_id():
    """Generate unique content ID"""
    return f"CC{uuid.uuid4().hex[:8].upper()}"

@content_routes.route('/save', methods=['POST'])
def save_content():
    """Save generated content"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        user_email = session['user']
        
        # Check user content limits
        user = User.query.get(user_email)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        current_content_count = Content.query.filter_by(user_email=user_email).count()
        if current_content_count >= user.content_limit:
            return jsonify({
                'success': False,
                'error': f'Content limit reached ({user.content_limit}). Upgrade your subscription for more content.'
            }), 403
        
        # Create content record
        content = Content(
            id=generate_content_id(),
            user_email=user_email,
            direction=data.get('direction'),
            platform=data.get('platform'),
            source=data.get('source'),
            topic=data.get('topic'),
            tone=data.get('tone'),
            content_text=data.get('content'),
            language=data.get('language', 'en'),
            region=data.get('region')
        )
        
        db.session.add(content)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'content_id': content.id,
            'message': 'Content saved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@content_routes.route('/list', methods=['GET'])
def list_content():
    """Get user's content"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        user_email = session['user']
        limit = request.args.get('limit', 10, type=int)
        
        contents = Content.query.filter_by(user_email=user_email)\
                               .order_by(Content.created_at.desc())\
                               .limit(limit).all()
        
        content_list = []
        for content in contents:
            content_list.append({
                'id': content.id,
                'direction': content.direction,
                'platform': content.platform,
                'source': content.source,
                'topic': content.topic,
                'tone': content.tone,
                'content_text': content.content_text,
                'status': content.status,
                'created_at': content.created_at.isoformat(),
                'views': content.views,
                'likes': content.likes,
                'shares': content.shares,
                'comments': content.comments
            })
        
        return jsonify({
            'success': True,
            'contents': content_list,
            'total': len(content_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@content_routes.route('/<content_id>', methods=['GET'])
def get_content(content_id):
    """Get specific content"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        user_email = session['user']
        content = Content.query.filter_by(id=content_id, user_email=user_email).first()
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content not found'
            }), 404
        
        return jsonify({
            'success': True,
            'content': {
                'id': content.id,
                'direction': content.direction,
                'platform': content.platform,
                'source': content.source,
                'topic': content.topic,
                'tone': content.tone,
                'content_text': content.content_text,
                'status': content.status,
                'created_at': content.created_at.isoformat(),
                'views': content.views,
                'likes': content.likes,
                'shares': content.shares,
                'comments': content.comments
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@content_routes.route('/<content_id>', methods=['DELETE'])
def delete_content(content_id):
    """Delete content"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        user_email = session['user']
        content = Content.query.filter_by(id=content_id, user_email=user_email).first()
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content not found'
            }), 404
        
        db.session.delete(content)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Content deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 