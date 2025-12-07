"""Pytest configuration and fixtures."""
import pytest
from app import create_app
from app.db import Base
from app.models import User, Post
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash
import os


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def _db(app):
    """
    Create database tables for testing.
    This fixture runs once per test session.
    """
    # Get the engine from the app's extensions
    db_engine = app.extensions['sqlalchemy']['engine']
    
    # Create all tables
    Base.metadata.create_all(bind=db_engine)
    
    yield db_engine
    
    # Drop all tables after tests
    Base.metadata.drop_all(bind=db_engine)


@pytest.fixture(scope='function')
def db_session(app, _db):
    """
    Create a new database session for each test.
    Rolls back all changes after each test to ensure test isolation.
    """
    # Get SessionLocal from app extensions
    SessionLocal = app.extensions['sqlalchemy']['session']
    
    # Create a new session
    connection = _db.connect()
    transaction = connection.begin()
    
    session = scoped_session(
        sessionmaker(bind=connection, expire_on_commit=False)
    )
    
    # Patch the SessionLocal to use our test session
    import app.db as db_module
    old_session = db_module.SessionLocal
    db_module.SessionLocal = session
    
    yield session
    
    # Rollback transaction to undo all changes
    session.close()
    transaction.rollback()
    connection.close()
    
    # Restore original session
    db_module.SessionLocal = old_session


@pytest.fixture(scope='function')
def client(app, db_session):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('testpassword'),
        first_name='Test',
        last_name='User',
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_users(db_session):
    """Create multiple sample users for testing."""
    users = [
        User(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password_hash=generate_password_hash('password123'),
            first_name=f'User{i}',
            last_name='Test',
            is_active=True
        )
        for i in range(1, 6)
    ]
    db_session.add_all(users)
    db_session.commit()
    for user in users:
        db_session.refresh(user)
    return users


@pytest.fixture
def sample_post(db_session, sample_user):
    """Create a sample post for testing."""
    post = Post(
        title='Test Post',
        content='This is a test post content.',
        published=True,
        author_id=sample_user.id
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


@pytest.fixture
def sample_posts(db_session, sample_user):
    """Create multiple sample posts for testing."""
    posts = [
        Post(
            title=f'Test Post {i}',
            content=f'This is test post content {i}.',
            published=i % 2 == 0,  # Alternate published status
            author_id=sample_user.id
        )
        for i in range(1, 6)
    ]
    db_session.add_all(posts)
    db_session.commit()
    for post in posts:
        db_session.refresh(post)
    return posts
