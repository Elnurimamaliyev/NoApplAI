"""Tests for post API endpoints."""
import json


class TestPostEndpoints:
    """Test cases for post API endpoints."""
    
    def test_create_post(self, client, db_session, sample_user):
        """Test creating a post via API."""
        response = client.post('/api/v1/posts',
            data=json.dumps({
                'title': 'API Test Post',
                'content': 'This is a test post created via API.',
                'author_id': sample_user.id,
                'published': True
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Post created successfully'
        assert data['post']['title'] == 'API Test Post'
    
    def test_create_post_validation_error(self, client, db_session, sample_user):
        """Test creating a post with invalid data."""
        response = client.post('/api/v1/posts',
            data=json.dumps({
                'title': '',  # Empty title
                'content': 'Content',
                'author_id': sample_user.id
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_post_invalid_author(self, client, db_session):
        """Test creating a post with non-existent author."""
        response = client.post('/api/v1/posts',
            data=json.dumps({
                'title': 'Test',
                'content': 'Content',
                'author_id': 99999
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_get_posts(self, client, db_session, sample_posts):
        """Test getting list of posts."""
        response = client.get('/api/v1/posts')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'posts' in data
        assert 'pagination' in data
        assert len(data['posts']) == 5
    
    def test_get_posts_pagination(self, client, db_session, sample_posts):
        """Test pagination of posts."""
        response = client.get('/api/v1/posts?page=1&page_size=2')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['posts']) == 2
        assert data['pagination']['page_size'] == 2
    
    def test_get_posts_filter_by_author(self, client, db_session, sample_posts, sample_user):
        """Test filtering posts by author."""
        response = client.get(f'/api/v1/posts?author_id={sample_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        for post in data['posts']:
            assert post['author_id'] == sample_user.id
    
    def test_get_posts_filter_by_published(self, client, db_session, sample_posts):
        """Test filtering posts by published status."""
        response = client.get('/api/v1/posts?published=true')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        for post in data['posts']:
            assert post['published'] is True
    
    def test_get_posts_search(self, client, db_session, sample_posts):
        """Test searching posts."""
        response = client.get('/api/v1/posts?search=Post 1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['total'] >= 1
    
    def test_get_post_by_id(self, client, db_session, sample_post):
        """Test getting a specific post."""
        response = client.get(f'/api/v1/posts/{sample_post.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['post']['id'] == sample_post.id
        assert data['post']['title'] == sample_post.title
    
    def test_get_post_with_author(self, client, db_session, sample_post):
        """Test getting post with author information."""
        response = client.get(f'/api/v1/posts/{sample_post.id}?include_author=true')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'author' in data['post']
        assert data['post']['author']['username'] == sample_post.author.username
    
    def test_get_post_not_found(self, client, db_session):
        """Test getting non-existent post."""
        response = client.get('/api/v1/posts/99999')
        
        assert response.status_code == 404
    
    def test_update_post(self, client, db_session, sample_post):
        """Test updating a post."""
        response = client.put(f'/api/v1/posts/{sample_post.id}',
            data=json.dumps({
                'title': 'Updated Title',
                'published': False
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['post']['title'] == 'Updated Title'
        assert data['post']['published'] is False
    
    def test_delete_post(self, client, db_session, sample_post):
        """Test deleting a post."""
        response = client.delete(f'/api/v1/posts/{sample_post.id}')
        
        assert response.status_code == 200
        
        # Verify post is deleted
        response = client.get(f'/api/v1/posts/{sample_post.id}')
        assert response.status_code == 404
    
    def test_publish_post(self, client, db_session, sample_user):
        """Test publishing a post."""
        # Create unpublished post
        from app.services.post_service import PostService
        post = PostService.create_post('Draft', 'Content', sample_user.id, published=False)
        
        response = client.post(f'/api/v1/posts/{post.id}/publish')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['post']['published'] is True
    
    def test_unpublish_post(self, client, db_session, sample_post):
        """Test unpublishing a post."""
        response = client.post(f'/api/v1/posts/{sample_post.id}/unpublish')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['post']['published'] is False
    
    def test_get_user_posts(self, client, db_session, sample_posts, sample_user):
        """Test getting all posts by a user."""
        response = client.get(f'/api/v1/posts/user/{sample_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['total'] == 5
