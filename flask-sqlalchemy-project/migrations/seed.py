"""Seed database with sample data."""
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Post
import os
from config import config_by_name


def seed_database():
    """Seed the database with sample data."""
    # Get database URL from config
    app_config = config_by_name[os.getenv('FLASK_ENV', 'development')]
    database_url = app_config.SQLALCHEMY_DATABASE_URI
    
    # Create engine and session
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if data already exists
        existing_users = session.query(User).count()
        if existing_users > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding database...")
        
        # Create sample users
        users = [
            User(
                username='johndoe',
                email='john@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='John',
                last_name='Doe',
                is_active=True
            ),
            User(
                username='janedoe',
                email='jane@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Jane',
                last_name='Doe',
                is_active=True
            ),
            User(
                username='bobsmith',
                email='bob@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Bob',
                last_name='Smith',
                is_active=True
            )
        ]
        
        session.add_all(users)
        session.flush()  # Get IDs for users
        
        # Create sample posts
        posts = [
            Post(
                title='Getting Started with Flask',
                content='Flask is a lightweight WSGI web application framework...',
                published=True,
                author_id=users[0].id
            ),
            Post(
                title='Introduction to SQLAlchemy',
                content='SQLAlchemy is the Python SQL toolkit and Object Relational Mapper...',
                published=True,
                author_id=users[0].id
            ),
            Post(
                title='Database Design Best Practices',
                content='When designing a database, there are several best practices to follow...',
                published=True,
                author_id=users[1].id
            ),
            Post(
                title='Draft Post',
                content='This is a draft post that is not yet published...',
                published=False,
                author_id=users[1].id
            ),
            Post(
                title='REST API Design Principles',
                content='REST APIs should be designed with clear conventions...',
                published=True,
                author_id=users[2].id
            )
        ]
        
        session.add_all(posts)
        session.commit()
        
        print(f"Successfully seeded database with {len(users)} users and {len(posts)} posts.")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    seed_database()
