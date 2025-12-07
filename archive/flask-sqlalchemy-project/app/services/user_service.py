"""User service layer for business logic."""
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.db import get_session
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(username, email, password, first_name=None, last_name=None, session=None):
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Plain text password
            first_name: Optional first name
            last_name: Optional last name
            session: Optional SQLAlchemy session (uses request session if None)
            
        Returns:
            User object
            
        Raises:
            ValueError: If user already exists or validation fails
            SQLAlchemyError: Database errors
        """
        if session is None:
            session = get_session()
        
        try:
            # Validate username length (database has VARCHAR(50))
            if len(username) > 50:
                raise ValueError("Username must not exceed 50 characters")
            
            # Validate for null bytes
            if '\x00' in username or '\x00' in email:
                raise ValueError("Null bytes are not allowed in username or email")
            
            # Check if user exists
            existing_user = session.execute(
                select(User).where(
                    or_(User.username == username, User.email == email)
                )
            ).scalar_one_or_none()
            
            if existing_user:
                if existing_user.username == username:
                    raise ValueError("Username already exists")
                else:
                    raise ValueError("Email already exists")
            
            # Validate password strength
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
                first_name=first_name,
                last_name=last_name
            )
            
            session.add(user)
            session.flush()  # Get the ID before commit
            session.refresh(user)
            
            return user
        except SQLAlchemyError as e:
            logger.error(f"Database error creating user: {e}")
            raise
    
    @staticmethod
    def get_user_by_id(user_id, session=None):
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            session: Optional SQLAlchemy session
            
        Returns:
            User object or None
        """
        if session is None:
            session = get_session()
        
        return session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()
    
    @staticmethod
    def get_user_by_username(username, session=None):
        """
        Get user by username.
        
        Args:
            username: Username
            session: Optional SQLAlchemy session
            
        Returns:
            User object or None
        """
        if session is None:
            session = get_session()
        
        return session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
    
    @staticmethod
    def get_user_by_email(email, session=None):
        """
        Get user by email.
        
        Args:
            email: Email address
            session: Optional SQLAlchemy session
            
        Returns:
            User object or None
        """
        if session is None:
            session = get_session()
        
        return session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
    
    @staticmethod
    def get_users(page=1, page_size=20, username=None, email=None, is_active=None, session=None):
        """
        Get paginated list of users with optional filtering.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            username: Filter by username (partial match)
            email: Filter by email (partial match)
            is_active: Filter by active status
            session: Optional SQLAlchemy session
            
        Returns:
            dict with 'items', 'total', 'page', 'page_size', 'pages'
        """
        if session is None:
            session = get_session()
        
        # Build base query
        query = select(User)
        
        # Apply filters
        if username:
            # Use parameterized query instead of f-string
            query = query.where(User.username.ilike(f'%{username}%'))
        if email:
            query = query.where(User.email.ilike(f'%{email}%'))
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        # Optimized count query - count ID directly
        count_query = select(func.count(User.id))
        if username:
            count_query = count_query.where(User.username.ilike(f'%{username}%'))
        if email:
            count_query = count_query.where(User.email.ilike(f'%{email}%'))
        if is_active is not None:
            count_query = count_query.where(User.is_active == is_active)
        
        total = session.execute(count_query).scalar()
        
        # Apply pagination with bounds checking
        offset = max(0, (page - 1) * page_size)
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        users = session.execute(query).scalars().all()
        
        return {
            'items': users,
            'total': total,
            'page': page,
            'page_size': page_size,
            'pages': max(1, (total + page_size - 1) // page_size)
        }
    
    @staticmethod
    def update_user(user_id, session=None, **kwargs):
        """
        Update user information.
        
        Args:
            user_id: User ID
            session: Optional SQLAlchemy session
            **kwargs: Fields to update (username, email, password, first_name, last_name)
            
        Returns:
            Updated User object or None if not found
            
        Raises:
            ValueError: If username or email already exists
        """
        if session is None:
            session = get_session()
        
        user = session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()
        
        if not user:
            return None
        
        # Check for uniqueness if username or email is being updated
        if 'username' in kwargs and kwargs['username'] != user.username:
            existing = session.execute(
                select(User).where(User.username == kwargs['username'])
            ).scalar_one_or_none()
            if existing:
                raise ValueError("Username already exists")
        
        if 'email' in kwargs and kwargs['email'] != user.email:
            existing = session.execute(
                select(User).where(User.email == kwargs['email'])
            ).scalar_one_or_none()
            if existing:
                raise ValueError("Email already exists")
        
        # Update fields
        for key, value in kwargs.items():
            if key == 'password':
                if len(value) < 8:
                    raise ValueError("Password must be at least 8 characters long")
                user.password_hash = generate_password_hash(value, method='pbkdf2:sha256')
            elif hasattr(user, key) and key not in ('id', 'password_hash', 'created_at'):
                setattr(user, key, value)
        
        session.flush()
        session.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(user_id, session=None):
        """
        Delete a user.
        
        Args:
            user_id: User ID
            session: Optional SQLAlchemy session
            
        Returns:
            True if deleted, False if not found
        """
        if session is None:
            session = get_session()
        
        user = session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()
        
        if not user:
            return False
        
        session.delete(user)
        return True
    
    @staticmethod
    def verify_password(user, password):
        """
        Verify user password.
        
        Args:
            user: User object
            password: Plain text password
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(user.password_hash, password)
