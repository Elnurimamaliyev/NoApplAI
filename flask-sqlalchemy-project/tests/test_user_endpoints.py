"""Tests for user API endpoints."""
import json


class TestUserEndpoints:
    """Test cases for user API endpoints."""
    
    def test_create_user(self, client, db_session):
        """Test creating a user via API."""
        response = client.post('/api/v1/users', 
            data=json.dumps({
                'username': 'apiuser',
                'email': 'api@example.com',
                'password': 'password123',
                'first_name': 'API',
                'last_name': 'User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
        assert data['user']['username'] == 'apiuser'
    
    def test_create_user_validation_error(self, client, db_session):
        """Test creating a user with invalid data."""
        response = client.post('/api/v1/users',
            data=json.dumps({
                'username': 'ab',  # Too short
                'email': 'invalid-email',
                'password': 'short'  # Too short
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_users(self, client, db_session, sample_users):
        """Test getting list of users."""
        response = client.get('/api/v1/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert 'pagination' in data
        assert len(data['users']) == 5
    
    def test_get_users_pagination(self, client, db_session, sample_users):
        """Test pagination of users."""
        response = client.get('/api/v1/users?page=1&page_size=2')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['users']) == 2
        assert data['pagination']['page'] == 1
        assert data['pagination']['page_size'] == 2
    
    def test_get_user_by_id(self, client, db_session, sample_user):
        """Test getting a specific user."""
        response = client.get(f'/api/v1/users/{sample_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['id'] == sample_user.id
        assert data['user']['username'] == sample_user.username
    
    def test_get_user_not_found(self, client, db_session):
        """Test getting non-existent user."""
        response = client.get('/api/v1/users/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_user(self, client, db_session, sample_user):
        """Test updating a user."""
        response = client.put(f'/api/v1/users/{sample_user.id}',
            data=json.dumps({
                'first_name': 'Updated',
                'last_name': 'Name'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['first_name'] == 'Updated'
        assert data['user']['last_name'] == 'Name'
    
    def test_delete_user(self, client, db_session, sample_user):
        """Test deleting a user."""
        response = client.delete(f'/api/v1/users/{sample_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'User deleted successfully'
        
        # Verify user is deleted
        response = client.get(f'/api/v1/users/{sample_user.id}')
        assert response.status_code == 404
    
    def test_get_user_by_username(self, client, db_session, sample_user):
        """Test getting user by username."""
        response = client.get(f'/api/v1/users/username/{sample_user.username}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['username'] == sample_user.username
