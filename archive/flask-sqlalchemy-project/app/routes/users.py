"""User routes and endpoints with improved error handling."""
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.services.user_service import UserService
from app.schemas import (
    user_schema, users_schema, user_update_schema, user_filter_schema
)
import logging

logger = logging.getLogger(__name__)
users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['POST'])
def create_user():
    """
    Create a new user.
    
    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "first_name": "string" (optional),
            "last_name": "string" (optional)
        }
    
    Returns:
        201: User created successfully
        400: Validation error or user already exists
        500: Server error
    """
    try:
        # Validate request data
        data = user_schema.load(request.json)
        
        # Create user
        user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        return jsonify({
            'message': 'User created successfully',
            'user': user_schema.dump(user)
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error creating user: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route('', methods=['GET'])
def get_users():
    """
    Get paginated list of users with optional filtering.
    
    Query Parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 20, max: 100)
        - username: Filter by username (partial match)
        - email: Filter by email (partial match)
        - is_active: Filter by active status (true/false)
    
    Returns:
        200: List of users with pagination info
        400: Validation error
    """
    try:
        # Validate query parameters
        filters = user_filter_schema.load(request.args)
        
        # Get users
        result = UserService.get_users(
            page=filters['page'],
            page_size=filters['page_size'],
            username=filters.get('username'),
            email=filters.get('email'),
            is_active=filters.get('is_active')
        )
        
        return jsonify({
            'users': users_schema.dump(result['items']),
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'page_size': result['page_size'],
                'pages': result['pages']
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching users: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error fetching users: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID.
    
    Path Parameters:
        user_id: User ID
    
    Returns:
        200: User found
        404: User not found
    """
    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user_schema.dump(user)}), 200
        
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error fetching user {user_id}: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    """
    Update a user.
    
    Path Parameters:
        user_id: User ID
    
    Request Body (all fields optional):
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "first_name": "string",
            "last_name": "string"
        }
    
    Returns:
        200: User updated successfully
        400: Validation error
        404: User not found
    """
    try:
        # Validate request data
        data = user_update_schema.load(request.json)
        
        if not data:
            return jsonify({'error': 'No valid fields provided for update'}), 400
        
        # Update user
        user = UserService.update_user(user_id, **data)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user_schema.dump(user)
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error updating user {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error updating user {user_id}: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user.
    
    Path Parameters:
        user_id: User ID
    
    Returns:
        200: User deleted successfully
        404: User not found
    """
    try:
        deleted = UserService.delete_user(user_id)
        
        if not deleted:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting user {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error deleting user {user_id}: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route('/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    """
    Get a user by username.
    
    Path Parameters:
        username: Username
    
    Returns:
        200: User found
        404: User not found
    """
    try:
        user = UserService.get_user_by_username(username)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user_schema.dump(user)}), 200
        
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user by username {username}: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error fetching user by username {username}: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500
