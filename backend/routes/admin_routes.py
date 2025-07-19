from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash
from functools import wraps

admin_routes = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For now, check if user email is admin@contentcreator.com
        # In production, you'd want proper role-based authentication
        user_email = request.headers.get('X-User-Email')
        if user_email != 'admin@contentcreator.com':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_routes.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        
        # Build query
        query = User.query
        
        # Apply search filter
        if search:
            query = query.filter(User.email.contains(search))
        
        # Apply role filter (when role column is available)
        # if role:
        #     query = query.filter(User.role == role)
        
        # Get paginated results
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        users = []
        for user in pagination.items:
            users.append({
                'id': user.email,  # Using email as ID for now
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
                'is_active': user.is_active,
                'subscription_tier': user.subscription_tier,
                'content_limit': user.content_limit,
                'image_limit': user.image_limit,
                'storage_limit_mb': user.storage_limit_mb,
                'role': 'admin' if user.email == 'admin@contentcreator.com' else 'user'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'users': users,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'pages': pagination.pages,
                    'total': pagination.total,
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

@admin_routes.route('/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Update user fields
        if 'subscription_tier' in data:
            user.subscription_tier = data['subscription_tier']
        if 'content_limit' in data:
            user.content_limit = data['content_limit']
        if 'image_limit' in data:
            user.image_limit = data['image_limit']
        if 'storage_limit_mb' in data:
            user.storage_limit_mb = data['storage_limit_mb']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_routes.route('/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Prevent deleting admin user
        if user.email == 'admin@contentcreator.com':
            return jsonify({
                'success': False,
                'error': 'Cannot delete admin user'
            }), 400
        
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

@admin_routes.route('/users/<user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Prevent deactivating admin user
        if user.email == 'admin@contentcreator.com':
            return jsonify({
                'success': False,
                'error': 'Cannot deactivate admin user'
            }), 400
        
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        
        return jsonify({
            'success': True,
            'data': {
                'message': f'User {status} successfully'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_routes.route('/users/<user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """Reset user password"""
    try:
        data = request.get_json()
        new_password = data.get('new_password')
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': 'New password is required'
            }), 400
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user.password_hash = generate_password_hash(new_password)
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