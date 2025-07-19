from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Check if user already exists
        if User.query.get(email):
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Set role based on email
        role = 'admin' if email == 'admin@contentcreator.com' else 'user'
        
        # Create new user
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            subscription_tier='free',
            content_limit=50,
            image_limit=10,
            storage_limit_mb=100
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_routes.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Verify user credentials
        user = User.query.get(email)
        if user and check_password_hash(user.password_hash, password):
            session['user'] = email
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'email': user.email,
                    'subscription_tier': user.subscription_tier,
                    'content_limit': user.content_limit,
                    'image_limit': user.image_limit,
                    'storage_limit_mb': user.storage_limit_mb
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_routes.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('user', None)
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })

@auth_routes.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    if 'user' not in session:
        return jsonify({
            'success': False,
            'error': 'User not logged in'
        }), 401
    
    user = User.query.get(session['user'])
    if not user:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'user': {
            'email': user.email,
            'subscription_tier': user.subscription_tier,
            'content_limit': user.content_limit,
            'image_limit': user.image_limit,
            'storage_limit_mb': user.storage_limit_mb,
            'created_at': user.created_at.isoformat()
        }
    }) 