from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password required'
            }), 400
        
        email = data['email']
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 401
        
        # Verify password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': 'dummy-token'  # In real app, generate JWT token
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password required'
            }), 400
        
        email = data['email']
        password = data['password']
        username = data.get('username', email.split('@')[0])  # Use email prefix as default username
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        name = data.get('name', f"{first_name} {last_name}".strip())
        region = data.get('region', 'global')
        language = data.get('language', 'en')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User already exists'
            }), 409
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({
                'success': False,
                'error': 'Username already taken'
            }), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash='',  # Will be set by set_password
            first_name=first_name,
            last_name=last_name,
            name=name,
            role='user',
            region=region,
            language=language
        )
        
        # Set password
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': 'dummy-token'  # In real app, generate JWT token
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        # In real app, get user from JWT token
        # For now, use dummy user_id
        user_id = request.args.get('user_id', 1)
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/preferences', methods=['PUT'])
def update_preferences():
    """Update user preferences"""
    try:
        data = request.get_json()
        
        # In real app, get user from JWT token
        # For now, use dummy user_id
        user_id = data.get('user_id', 1)
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Update preferences
        if 'region' in data:
            user.region = data['region']
        
        if 'language' in data:
            user.language = data['language']
        
        if 'timezone' in data:
            user.timezone = data['timezone']
        
        if 'cultural_preferences' in data:
            user.cultural_preferences_dict = data['cultural_preferences']
        
        if 'preferred_directions' in data:
            user.preferred_directions_list = data['preferred_directions']
        
        if 'preferences' in data:
            user.preferences_dict = data['preferences']
        
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