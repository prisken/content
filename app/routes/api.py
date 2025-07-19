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
        
        # Save to database if user_id provided and database is available
        if user_id and current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            try:
                content = Content(
                    user_id=user_id,
                    content_direction=content_direction,
                    content_type=content_type,
                    source_type=source_type,
                    generated_content=generated_content['content'],
                    tone=tone,
                    region=region,
                    language=language
                )
                content.source_data = specific_content
                content.cultural_context_dict = generated_content.get('cultural_context', {})
                content.direction_context_dict = direction_context
                
                db.session.add(content)
                db.session.commit()
                
                generated_content['content_id'] = content.id
            except Exception as e:
                print(f"Database save error: {e}")
                # Continue without saving to database
        
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
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        data = request.get_json()
        content = Content.query.get_or_404(content_id)
        
        # Update content
        if 'edited_content' in data:
            content.edited_content = data['edited_content']
        
        if 'media_url' in data:
            content.media_url = data['media_url']
        
        # Create version history
        if 'edited_content' in data and data['edited_content'] != content.generated_content:
            try:
                version = ContentVersion(
                    content_id=content_id,
                    version_number=len(content.versions) + 1,
                    content_text=data['edited_content'],
                    edited_by=data.get('user_id')
                )
                db.session.add(version)
            except Exception as e:
                print(f"Version creation error: {e}")
                # Continue without version history
        
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

# Admin User Management Routes
@api_bp.route('/admin/users', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        # Get query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        
        # Build query
        query = User.query
        
        # Apply search filter
        if search:
            query = query.filter(
                (User.username.contains(search)) |
                (User.email.contains(search)) |
                (User.first_name.contains(search)) |
                (User.last_name.contains(search))
            )
        
        # Apply role filter
        if role:
            query = query.filter(User.role == role)
        
        # Paginate results
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        users = pagination.items
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in users],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/admin/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user details (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        user = User.query.get_or_404(user_id)
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user details (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        
        # Update user fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'preferences' in data:
            user.preferences = data['preferences']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        user = User.query.get_or_404(user_id)
        
        # Don't allow admin to delete themselves
        # In real app, get current user from JWT token
        # if user.id == current_user.id:
        #     return jsonify({
        #         'success': False,
        #         'error': 'Cannot delete your own account'
        #     }), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
def toggle_user_status(user_id):
    """Toggle user active/inactive status (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        user = User.query.get_or_404(user_id)
        user.is_active = not user.is_active
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user.id,
                'is_active': user.is_active,
                'message': f'User {"activated" if user.is_active else "deactivated"} successfully'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
def reset_user_password(user_id):
    """Reset user password (admin only)"""
    try:
        # Check if database is available
        if not current_app.config.get('SQLALCHEMY_DATABASE_URI'):
            return jsonify({
                'success': False,
                'error': 'Database not available in serverless mode'
            }), 503
        
        data = request.get_json()
        new_password = data.get('new_password')
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': 'New password is required'
            }), 400
        
        user = User.query.get_or_404(user_id)
        user.set_password(new_password)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 