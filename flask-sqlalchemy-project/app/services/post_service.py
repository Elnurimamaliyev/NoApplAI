"""Post service layer for business logic."""
from sqlalchemy import select, func, or_
from sqlalchemy.exc import SQLAlchemyError
from app.models import Post, User
from app.db import get_session
import logging

logger = logging.getLogger(__name__)


class PostService:
    """Service class for post operations."""
    
    @staticmethod
    def create_post(title, content, author_id, published=False, session=None):
        """
        Create a new post.
        
        Args:
            title: Post title
            content: Post content
            author_id: ID of the author (user)
            published: Whether the post is published
            session: Optional SQLAlchemy session
            
        Returns:
            Post object
            
        Raises:
            ValueError: If author doesn't exist or validation fails
            SQLAlchemyError: Database errors
        """
        if session is None:
            session = get_session()
        
        try:
            # Verify author exists
            author = session.execute(
                select(User).where(User.id == author_id)
            ).scalar_one_or_none()
            
            if not author:
                raise ValueError("Author does not exist")
            
            # Validate inputs
            if not title or len(title.strip()) == 0:
                raise ValueError("Title cannot be empty")
            if not content or len(content.strip()) == 0:
                raise ValueError("Content cannot be empty")
            
            # Create new post
            post = Post(
                title=title.strip(),
                content=content.strip(),
                author_id=author_id,
                published=published
            )
            
            session.add(post)
            session.flush()
            session.refresh(post)
            
            return post
        except SQLAlchemyError as e:
            logger.error(f"Database error creating post: {e}")
            raise
    
    @staticmethod
    def get_post_by_id(post_id, include_author=False, session=None):
        """
        Get post by ID.
        
        Args:
            post_id: Post ID
            include_author: Whether to eagerly load author
            session: Optional SQLAlchemy session
            
        Returns:
            Post object or None
        """
        if session is None:
            session = get_session()
        
        query = select(Post).where(Post.id == post_id)
        
        # Eagerly load author if requested
        if include_author:
            from sqlalchemy.orm import joinedload
            query = query.options(joinedload(Post.author))
        
        return session.execute(query).scalar_one_or_none()
    
    @staticmethod
    def get_posts(page=1, page_size=20, author_id=None, published=None, search=None, session=None):
        """
        Get paginated list of posts with optional filtering.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            author_id: Filter by author ID
            published: Filter by published status
            search: Search in title and content
            session: Optional SQLAlchemy session
            
        Returns:
            dict with 'items', 'total', 'page', 'page_size', 'pages'
        """
        if session is None:
            session = get_session()
        
        # Build query
        query = select(Post)
        
        # Apply filters
        if author_id is not None:
            query = query.where(Post.author_id == author_id)
        if published is not None:
            query = query.where(Post.published == published)
        if search:
            search_pattern = f'%{search}%'
            query = query.where(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern)
                )
            )
        
        # Optimized count query
        count_query = select(func.count(Post.id))
        if author_id is not None:
            count_query = count_query.where(Post.author_id == author_id)
        if published is not None:
            count_query = count_query.where(Post.published == published)
        if search:
            search_pattern = f'%{search}%'
            count_query = count_query.where(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern)
                )
            )
        
        total = session.execute(count_query).scalar()
        
        # Apply pagination and ordering
        offset = max(0, (page - 1) * page_size)
        query = query.order_by(Post.created_at.desc())
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        posts = session.execute(query).scalars().all()
        
        return {
            'items': posts,
            'total': total,
            'page': page,
            'page_size': page_size,
            'pages': max(1, (total + page_size - 1) // page_size)
        }
    
    @staticmethod
    def update_post(post_id, session=None, **kwargs):
        """
        Update post information.
        
        Args:
            post_id: Post ID
            session: Optional SQLAlchemy session
            **kwargs: Fields to update (title, content, published)
            
        Returns:
            Updated Post object or None if not found
        """
        if session is None:
            session = get_session()
        
        post = session.execute(
            select(Post).where(Post.id == post_id)
        ).scalar_one_or_none()
        
        if not post:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(post, key) and key not in ('id', 'author_id', 'created_at'):
                if key in ('title', 'content') and isinstance(value, str):
                    value = value.strip()
                setattr(post, key, value)
        
        session.flush()
        session.refresh(post)
        
        return post
    
    @staticmethod
    def delete_post(post_id, session=None):
        """
        Delete a post.
        
        Args:
            post_id: Post ID
            session: Optional SQLAlchemy session
            
        Returns:
            True if deleted, False if not found
        """
        if session is None:
            session = get_session()
        
        post = session.execute(
            select(Post).where(Post.id == post_id)
        ).scalar_one_or_none()
        
        if not post:
            return False
        
        session.delete(post)
        return True
    
    @staticmethod
    def get_user_posts(user_id, page=1, page_size=20, published=None):
        """
        Get all posts by a specific user.
        
        Args:
            user_id: User ID
            page: Page number
            page_size: Items per page
            published: Filter by published status
            
        Returns:
            dict with pagination info and post items
        """
        return PostService.get_posts(
            page=page,
            page_size=page_size,
            author_id=user_id,
            published=published
        )
    
    @staticmethod
    def publish_post(post_id):
        """
        Publish a post.
        
        Args:
            post_id: Post ID
            
        Returns:
            Updated Post object or None
        """
        return PostService.update_post(post_id, published=True)
    
    @staticmethod
    def unpublish_post(post_id):
        """
        Unpublish a post.
        
        Args:
            post_id: Post ID
            
        Returns:
            Updated Post object or None
        """
        return PostService.update_post(post_id, published=False)
