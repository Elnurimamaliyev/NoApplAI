"""Tests for post service layer."""
import pytest
from app.services.post_service import PostService
from app.models import Post


class TestPostService:
    """Test cases for PostService."""
    
    def test_create_post(self, db_session, sample_user):
        """Test creating a new post."""
        post = PostService.create_post(
            title='New Post',
            content='This is a new post.',
            author_id=sample_user.id,
            published=True
        )
        
        assert post is not None
        assert post.id is not None
        assert post.title == 'New Post'
        assert post.content == 'This is a new post.'
        assert post.author_id == sample_user.id
        assert post.published is True
    
    def test_create_post_invalid_author(self, db_session):
        """Test creating a post with non-existent author."""
        with pytest.raises(ValueError, match="Author does not exist"):
            PostService.create_post(
                title='Test',
                content='Test content',
                author_id=99999
            )
    
    def test_get_post_by_id(self, db_session, sample_post):
        """Test getting a post by ID."""
        post = PostService.get_post_by_id(sample_post.id)
        
        assert post is not None
        assert post.id == sample_post.id
        assert post.title == sample_post.title
    
    def test_get_post_by_id_with_author(self, db_session, sample_post):
        """Test getting a post with author information."""
        post = PostService.get_post_by_id(sample_post.id, include_author=True)
        
        assert post is not None
        assert post.author is not None
        assert post.author.username == sample_post.author.username
    
    def test_get_post_not_found(self, db_session):
        """Test getting a non-existent post."""
        post = PostService.get_post_by_id(99999)
        assert post is None
    
    def test_get_posts_pagination(self, db_session, sample_posts):
        """Test getting paginated list of posts."""
        result = PostService.get_posts(page=1, page_size=3)
        
        assert len(result['items']) == 3
        assert result['total'] == 5
        assert result['page'] == 1
        assert result['page_size'] == 3
        assert result['pages'] == 2
    
    def test_get_posts_by_author(self, db_session, sample_posts, sample_user):
        """Test filtering posts by author."""
        result = PostService.get_posts(author_id=sample_user.id)
        
        assert len(result['items']) == 5
        for post in result['items']:
            assert post.author_id == sample_user.id
    
    def test_get_posts_by_published_status(self, db_session, sample_posts):
        """Test filtering posts by published status."""
        result = PostService.get_posts(published=True)
        
        # sample_posts creates posts where i % 2 == 0 are published
        # Posts 2 and 4 are published
        assert result['total'] == 2
        for post in result['items']:
            assert post.published is True
    
    def test_get_posts_search(self, db_session, sample_posts):
        """Test searching posts by content."""
        result = PostService.get_posts(search='Post 1')
        
        assert result['total'] == 1
        assert 'Post 1' in result['items'][0].title
    
    def test_update_post(self, db_session, sample_post):
        """Test updating a post."""
        updated_post = PostService.update_post(
            sample_post.id,
            title='Updated Title',
            published=False
        )
        
        assert updated_post is not None
        assert updated_post.title == 'Updated Title'
        assert updated_post.published is False
        assert updated_post.content == sample_post.content  # Unchanged
    
    def test_update_post_not_found(self, db_session):
        """Test updating non-existent post."""
        result = PostService.update_post(99999, title='Test')
        assert result is None
    
    def test_delete_post(self, db_session, sample_post):
        """Test deleting a post."""
        result = PostService.delete_post(sample_post.id)
        
        assert result is True
        
        # Verify post is deleted
        post = PostService.get_post_by_id(sample_post.id)
        assert post is None
    
    def test_delete_post_not_found(self, db_session):
        """Test deleting non-existent post."""
        result = PostService.delete_post(99999)
        assert result is False
    
    def test_get_user_posts(self, db_session, sample_posts, sample_user):
        """Test getting all posts by a user."""
        result = PostService.get_user_posts(sample_user.id)
        
        assert result['total'] == 5
        for post in result['items']:
            assert post.author_id == sample_user.id
    
    def test_publish_post(self, db_session):
        """Test publishing a post."""
        from app.services.user_service import UserService
        
        # Create user and unpublished post
        user = UserService.create_user('author', 'author@test.com', 'password123')
        post = PostService.create_post('Draft', 'Content', user.id, published=False)
        
        assert post.published is False
        
        # Publish the post
        published_post = PostService.publish_post(post.id)
        
        assert published_post is not None
        assert published_post.published is True
    
    def test_unpublish_post(self, db_session, sample_post):
        """Test unpublishing a post."""
        assert sample_post.published is True
        
        unpublished_post = PostService.unpublish_post(sample_post.id)
        
        assert unpublished_post is not None
        assert unpublished_post.published is False
