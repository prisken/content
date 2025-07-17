from flask import Blueprint, request, jsonify, current_app
from app.models.content import Content, ContentVersion
from app.models.user import User
from app.services.content_generator import ContentGenerator
from app.services.direction_manager import DirectionManager
from app import db
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate', methods=['POST'])
def generate_content():
    """Generate content with direction and regional context"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content_direction', 'content_type', 'source_type', 'specific_content', 'tone']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        content_direction = data['content_direction']
        content_type = data['content_type']
        source_type = data['source_type']
        specific_content = data['specific_content']
        tone = data['tone']
        region = data.get('region', 'global')
        language = data.get('language', 'en')
        user_id = data.get('user_id')  # In real app, get from JWT token
        
        # Initialize services
        direction_manager = DirectionManager()
        content_generator = ContentGenerator()
        
        # Get direction context
        direction_context = direction_manager.get_direction_context(content_direction, region)
        
        # Generate content
        generated_content = content_generator.generate_content(
            content_direction=content_direction,
            content_type=content_type,
            source_type=source_type,
            specific_content=specific_content,
            tone=tone,
            region=region,
            language=language,
            direction_context=direction_context
        )
        
        # Save to database if user_id provided
        if user_id:
            content = Content(
                user_id=user_id,
                content_direction=content_direction,
                content_type=content_type,
                source_type=source_type,
                source_data=specific_content,
                generated_content=generated_content['content'],
                tone=tone,
                region=region,
                language=language
            )
            content.cultural_context_dict = generated_content.get('cultural_context', {})
            content.direction_context_dict = direction_context
            
            db.session.add(content)
            db.session.commit()
            
            generated_content['content_id'] = content.id
        
        return jsonify({
            'success': True,
            'data': generated_content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    """Update content with manual edits"""
    try:
        data = request.get_json()
        content = Content.query.get_or_404(content_id)
        
        # Update content
        if 'edited_content' in data:
            content.edited_content = data['edited_content']
        
        if 'media_url' in data:
            content.media_url = data['media_url']
        
        # Create version history
        if 'edited_content' in data and data['edited_content'] != content.generated_content:
            version = ContentVersion(
                content_id=content_id,
                version_number=len(content.versions) + 1,
                content_text=data['edited_content'],
                edited_by=data.get('user_id')
            )
            db.session.add(version)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': content.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/content/<int:content_id>/versions')
def get_content_versions(content_id):
    """Get content version history"""
    try:
        content = Content.query.get_or_404(content_id)
        versions = ContentVersion.query.filter_by(content_id=content_id).order_by(ContentVersion.version_number.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [version.to_dict() for version in versions]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/content/<int:content_id>/revert', methods=['POST'])
def revert_content(content_id):
    """Revert content to previous version"""
    try:
        data = request.get_json()
        version_number = data.get('version_number')
        
        if not version_number:
            return jsonify({
                'success': False,
                'error': 'Version number required'
            }), 400
        
        content = Content.query.get_or_404(content_id)
        version = ContentVersion.query.filter_by(
            content_id=content_id, 
            version_number=version_number
        ).first()
        
        if not version:
            return jsonify({
                'success': False,
                'error': 'Version not found'
            }), 404
        
        # Revert to version
        content.edited_content = version.content_text
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': content.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/content/<int:content_id>/validate', methods=['POST'])
def validate_content(content_id):
    """Validate content for platform compliance and direction appropriateness"""
    try:
        content = Content.query.get_or_404(content_id)
        
        # Basic validation (in real app, use AI service)
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'suggestions': []
        }
        
        # Check content length
        if content.content_type == 'linkedin' and len(content.edited_content or content.generated_content) > 1300:
            validation_result['warnings'].append('Content exceeds LinkedIn character limit')
        
        if content.content_type == 'twitter' and len(content.edited_content or content.generated_content) > 280:
            validation_result['warnings'].append('Content exceeds Twitter character limit')
        
        # Check hashtags
        content_text = content.edited_content or content.generated_content
        hashtag_count = content_text.count('#')
        
        if content.content_type == 'linkedin' and hashtag_count > 2:
            validation_result['suggestions'].append('Consider reducing hashtags for LinkedIn')
        
        if content.content_type == 'instagram' and hashtag_count < 5:
            validation_result['suggestions'].append('Consider adding more hashtags for Instagram')
        
        return jsonify({
            'success': True,
            'data': validation_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 