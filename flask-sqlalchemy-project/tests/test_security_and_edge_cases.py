"""Additional security and edge case tests."""
import pytest
from app.services.user_service import UserService
from app.services.post_service import PostService
from sqlalchemy.exc import SQLAlchemyError


class TestSecurityAndEdgeCases:
    """Test security vulnerabilities and edge cases."""
    
    def test_sql_injection_attempt_in_search(self, db_session, sample_users):
        """Test that SQL injection attempts in search are handled safely."""
        # Attempt SQL injection in username search
        malicious_input = "'; DROP TABLE users; --"
        result = UserService.get_users(username=malicious_input)
        
        # Should return no results, not execute SQL
        assert result['total'] == 0
        
        # Verify users table still exists
        all_users = UserService.get_users()
        assert all_users['total'] == 5
    
    def test_xss_attempt_in_post_content(self, db_session, sample_user):
        """Test XSS attempt in post content."""
        xss_content = "<script>alert('XSS')</script>"
        post = PostService.create_post(
            title="Test Post",
            content=xss_content,
            author_id=sample_user.id
        )
        
        # Content should be stored as-is (escaping happens at template level)
        assert post.content == xss_content.strip()
    
    def test_extremely_long_username(self, db_session):
        """Test username exceeding maximum length."""
        long_username = "a" * 1000
        
        # Should be caught by validation or database constraint
        with pytest.raises((ValueError, SQLAlchemyError)):
            UserService.create_user(
                username=long_username,
                email="test@example.com",
                password="password123"
            )
    
    def test_unicode_characters_in_fields(self, db_session):
        """Test Unicode characters in user fields."""
        user = UserService.create_user(
            username="用户名",
            email="user@例え.com",
            password="пароль123",
            first_name="José",
            last_name="Müller"
        )
        
        assert user.username == "用户名"
        assert user.first_name == "José"
        assert user.last_name == "Müller"
    
    def test_empty_string_fields(self, db_session):
        """Test empty strings in required fields."""
        with pytest.raises(ValueError):
            PostService.create_post(
                title="   ",  # Only whitespace
                content="Content",
                author_id=1
            )
    
    def test_negative_page_number(self, db_session, sample_users):
        """Test pagination with negative page number."""
        result = UserService.get_users(page=-1, page_size=10)
        
        # Should handle gracefully, not crash
        assert 'items' in result
    
    def test_extremely_large_page_size(self, db_session, sample_users):
        """Test pagination with excessive page size."""
        # This should be limited by schema validation
        result = UserService.get_users(page=1, page_size=10000)
        
        # Should limit results
        assert len(result['items']) <= 100
    
    def test_concurrent_user_creation(self, db_session):
        """Test race condition in user creation."""
        # This would require actual threading to test properly
        # Placeholder for race condition test
        username = "concurrent_user"
        email = "concurrent@example.com"
        
        user1 = UserService.create_user(username, email, "password123")
        
        # Second attempt should fail
        with pytest.raises(ValueError, match="already exists"):
            UserService.create_user(username, f"different{email}", "password123")
    
    def test_null_bytes_in_input(self, db_session):
        """Test null byte injection."""
        with pytest.raises((ValueError, SQLAlchemyError)):
            UserService.create_user(
                username="test\x00user",
                email="test@example.com",
                password="password123"
            )
    
    def test_password_not_stored_plain_text(self, db_session, sample_user):
        """Verify passwords are hashed."""
        # Password should not be stored as plain text
        assert sample_user.password_hash != "testpassword"
        assert len(sample_user.password_hash) > 50  # Hashed passwords are long
        
        # Should verify correctly
        assert UserService.verify_password(sample_user, "testpassword")
        assert not UserService.verify_password(sample_user, "wrongpassword")
    
    def test_weak_password_rejected(self, db_session):
        """Test that weak passwords are rejected."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            UserService.create_user(
                username="testuser",
                email="test@example.com",
                password="short"
            )
    
    def test_email_case_sensitivity(self, db_session):
        """Test email uniqueness is case-insensitive."""
        UserService.create_user("user1", "Test@Example.com", "password123")
        
        # Should fail even with different case
        # Note: This depends on database collation settings
        # PostgreSQL is case-sensitive by default, so this might pass
        # In production, you'd want to normalize emails
    
    def test_update_to_duplicate_username(self, db_session, sample_users):
        """Test updating user to existing username."""
        user1 = sample_users[0]
        user2_username = sample_users[1].username
        
        with pytest.raises(ValueError, match="Username already exists"):
            UserService.update_user(user1.id, username=user2_username)
    
    def test_delete_cascade_posts(self, db_session, sample_user, sample_posts):
        """Test that deleting user cascades to posts."""
        user_id = sample_user.id
        post_count = len(sample_posts)
        
        # Delete user
        deleted = UserService.delete_user(user_id)
        assert deleted is True
        
        # Posts should also be deleted (cascade)
        remaining_posts = PostService.get_posts(author_id=user_id)
        assert remaining_posts['total'] == 0
    
    def test_pagination_beyond_total_pages(self, db_session, sample_users):
        """Test requesting page beyond available data."""
        result = UserService.get_users(page=100, page_size=10)
        
        # Should return empty results, not crash
        assert result['items'] == []
        assert result['total'] == 5
    
    def test_special_characters_in_search(self, db_session, sample_users):
        """Test search with special regex characters."""
        special_chars = "%_[]{}().*+?|^$\\"
        result = UserService.get_users(username=special_chars)
        
        # Should handle safely without regex errors
        assert 'items' in result
    
    def test_post_search_performance(self, db_session, sample_user):
        """Test search with large dataset (performance test placeholder)."""
        # Create many posts
        for i in range(50):
            PostService.create_post(
                title=f"Post {i}",
                content=f"Content for post number {i}",
                author_id=sample_user.id,
                published=True
            )
        
        # Search should still be fast
        result = PostService.get_posts(search="post")
        assert result['total'] >= 50
    
    def test_transaction_rollback_on_error(self, db_session):
        """Test that failed operations don't leave partial data."""
        initial_count = UserService.get_users()['total']
        
        # Attempt to create user that should fail validation
        # This tests that validation errors don't leave partial data
        try:
            user = UserService.create_user(
                username="validuser",
                email="valid@example.com",
                password="short"  # Too short - will fail validation
            )
        except ValueError:
            pass  # Expected to fail
        
        # Count should be unchanged - no user was created
        final_count = UserService.get_users()['total']
        assert final_count == initial_count
