"""Application package initialization."""
from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging

logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration name (development, testing, production)
        
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from config import config_by_name
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Configure CORS with restrictions
    cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS(app, 
         origins=cors_origins,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        if not app.config['DEBUG']:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Initialize database
    from app.db import init_db
    init_db(app)
    
    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.posts import posts_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(posts_bp, url_prefix='/api/v1/posts')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Flask SQLAlchemy API',
            'version': '1.0.0',
            'endpoints': {
                'users': '/api/v1/users',
                'posts': '/api/v1/posts',
                'health': '/health'
            }
        }), 200
    
    return app


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {str(error)}', exc_info=True)
        if app.config['DEBUG']:
            return jsonify({'error': 'Internal server error', 'message': str(error)}), 500
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unexpected exceptions."""
        logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        if app.config['DEBUG']:
            return jsonify({'error': 'An unexpected error occurred', 'details': str(error)}), 500
        return jsonify({'error': 'An unexpected error occurred'}), 500
