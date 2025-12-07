"""Tests for user service layer."""
import pytest
from app.services.user_service import UserService
from app.models import User


class TestUserService:
    """Test cases for UserService."""
    
    def test_create_user(self, db_session):
        """Test creating a new user."""
        user = UserService.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123',
            first_name='New',
            last_name='User'
        )
        
        assert user is not None
        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.is_active is True
    
    def test_create_duplicate_username(self, db_session, sample_user):
        """Test that creating a user with duplicate username raises error."""
        with pytest.raises(ValueError, match="Username already exists"):
            UserService.create_user(
                username=sample_user.username,
                email='different@example.com',
                password='password123'
            )
    
    def test_create_duplicate_email(self, db_session, sample_user):
        """Test that creating a user with duplicate email raises error."""
        with pytest.raises(ValueError, match="Email already exists"):
            UserService.create_user(
                username='differentuser',
                email=sample_user.email,
                password='password123'
            )
    
    def test_get_user_by_id(self, db_session, sample_user):
        """Test getting a user by ID."""
        user = UserService.get_user_by_id(sample_user.id)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.username == sample_user.username
    
    def test_get_user_by_id_not_found(self, db_session):
        """Test getting a user by non-existent ID."""
        user = UserService.get_user_by_id(99999)
        assert user is None
    
    def test_get_user_by_username(self, db_session, sample_user):
        """Test getting a user by username."""
        user = UserService.get_user_by_username(sample_user.username)
        
        assert user is not None
        assert user.username == sample_user.username
    
    def test_get_user_by_email(self, db_session, sample_user):
        """Test getting a user by email."""
        user = UserService.get_user_by_email(sample_user.email)
        
        assert user is not None
        assert user.email == sample_user.email
    
    def test_get_users_pagination(self, db_session, sample_users):
        """Test getting paginated list of users."""
        result = UserService.get_users(page=1, page_size=3)
        
        assert len(result['items']) == 3
        assert result['total'] == 5
        assert result['page'] == 1
        assert result['page_size'] == 3
        assert result['pages'] == 2
    
    def test_get_users_with_username_filter(self, db_session, sample_users):
        """Test filtering users by username."""
        result = UserService.get_users(username='user1')
        
        assert len(result['items']) == 1
        assert result['items'][0].username == 'user1'
    
    def test_update_user(self, db_session, sample_user):
        """Test updating user information."""
        updated_user = UserService.update_user(
            sample_user.id,
            first_name='Updated',
            last_name='Name'
        )
        
        assert updated_user is not None
        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'Name'
        assert updated_user.username == sample_user.username  # Unchanged
    
    def test_update_user_not_found(self, db_session):
        """Test updating non-existent user."""
        result = UserService.update_user(99999, first_name='Test')
        assert result is None
    
    def test_delete_user(self, db_session, sample_user):
        """Test deleting a user."""
        result = UserService.delete_user(sample_user.id)
        
        assert result is True
        
        # Verify user is deleted
        user = UserService.get_user_by_id(sample_user.id)
        assert user is None
    
    def test_delete_user_not_found(self, db_session):
        """Test deleting non-existent user."""
        result = UserService.delete_user(99999)
        assert result is False
    
    def test_verify_password(self, db_session, sample_user):
        """Test password verification."""
        # Correct password
        assert UserService.verify_password(sample_user, 'testpassword') is True
        
        # Incorrect password
        assert UserService.verify_password(sample_user, 'wrongpassword') is False
    
    def test_transaction_rollback(self, db_session):
        """Test that transactions are properly rolled back between tests."""
        # This test verifies that the fixture properly rolls back changes
        users = UserService.get_users()
        initial_count = users['total']
        
        # Create a user
        UserService.create_user(
            username='rollbacktest',
            email='rollback@example.com',
            password='password123'
        )
        
        users_after = UserService.get_users()
        assert users_after['total'] == initial_count + 1
        
        # After this test completes, the db_session fixture will rollback
        # and the next test should not see this user
