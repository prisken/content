from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if we're in serverless mode
IS_SERVERLESS = os.environ.get('VERCEL_ENV') == 'production'

# Initialize extensions conditionally
if not IS_SERVERLESS:
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_jwt_extended import JWTManager
    from flask_cors import CORS
    
    db = SQLAlchemy()
    migrate = Migrate()
    jwt = JWTManager()
    cors = CORS
else:
    # Dummy objects for serverless mode
    class DummyDB:
        def init_app(self, app): pass
        def create_all(self): pass
        def session(self): return None
    
    class DummyMigrate:
        def init_app(self, app, db): pass
    
    class DummyJWT:
        def init_app(self, app): pass
    
    class DummyCORS:
        def __init__(self, app): pass
    
    db = DummyDB()
    migrate = DummyMigrate()
    jwt = DummyJWT()
    cors = DummyCORS

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    if config_name == 'development':
        app.config.from_object('config.development.DevelopmentConfig')
    elif config_name == 'production':
        app.config.from_object('config.production.ProductionConfig')
    elif config_name == 'vercel':
        app.config.from_object('config.vercel.VercelConfig')
    else:
        app.config.from_object('config.testing.TestingConfig')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Create database tables only if database is configured
    if app.config.get('SQLALCHEMY_DATABASE_URI'):
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"Database initialization error: {e}")
    
    return app 