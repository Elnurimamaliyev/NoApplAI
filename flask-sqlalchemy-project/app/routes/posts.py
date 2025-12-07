"""Post routes and endpoints with improved error handling."""
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.services.post_service import PostService
from app.schemas import (
    post_schema, posts_schema, post_update_schema, post_filter_schema
)
import logging

logger = logging.getLogger(__name__)
posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['POST'])
def create_post():
    """Create a new post."""
    try:
        data = post_schema.load(request.json)
        post = PostService.create_post(
            title=data['title'],
            content=data['content'],
            author_id=data['author_id'],
            published=data.get('published', False)
        )
        return jsonify({
            'message': 'Post created successfully',
            'post': post_schema.dump(post)
        }), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('', methods=['GET'])
def get_posts():
    """Get paginated list of posts."""
    try:
        filters = post_filter_schema.load(request.args)
        result = PostService.get_posts(
            page=filters['page'],
            page_size=filters['page_size'],
            author_id=filters.get('author_id'),
            published=filters.get('published'),
            search=filters.get('search')
        )
        return jsonify({
            'posts': posts_schema.dump(result['items']),
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
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by ID."""
    try:
        include_author = request.args.get('include_author', 'false').lower() == 'true'
        post = PostService.get_post_by_id(post_id, include_author=include_author)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        if include_author:
            post_data = post.to_dict(include_author=True)
        else:
            post_data = post_schema.dump(post)
        return jsonify({'post': post_data}), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/<int:post_id>', methods=['PUT', 'PATCH'])
def update_post(post_id):
    """Update a post."""
    try:
        data = post_update_schema.load(request.json)
        if not data:
            return jsonify({'error': 'No valid fields provided for update'}), 400
        post = PostService.update_post(post_id, **data)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({
            'message': 'Post updated successfully',
            'post': post_schema.dump(post)
        }), 200
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post."""
    try:
        deleted = PostService.delete_post(post_id)
        if not deleted:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'message': 'Post deleted successfully'}), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/<int:post_id>/publish', methods=['POST'])
def publish_post(post_id):
    """Publish a post."""
    try:
        post = PostService.publish_post(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({
            'message': 'Post published successfully',
            'post': post_schema.dump(post)
        }), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/<int:post_id>/unpublish', methods=['POST'])
def unpublish_post(post_id):
    """Unpublish a post."""
    try:
        post = PostService.unpublish_post(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({
            'message': 'Post unpublished successfully',
            'post': post_schema.dump(post)
        }), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500


@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """Get all posts by a specific user."""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        published = request.args.get('published')
        if published is not None:
            published = published.lower() == 'true'
        result = PostService.get_user_posts(
            user_id=user_id,
            page=page,
            page_size=page_size,
            published=published
        )
        return jsonify({
            'posts': posts_schema.dump(result['items']),
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'page_size': result['page_size'],
                'pages': result['pages']
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid parameter', 'details': str(e)}), 400
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        if current_app.config['DEBUG']:
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred'}), 500
