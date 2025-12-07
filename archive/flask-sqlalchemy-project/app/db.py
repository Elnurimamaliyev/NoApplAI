"""Database connection and session management."""
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from flask import g
import logging

logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()

# Global variables for engine and session
engine = None
SessionLocal = None


def get_engine_args(app):
    """
    Get engine arguments including connection pool and SSL configuration.
    
    Args:
        app: Flask application instance
        
    Returns:
        dict: Engine configuration arguments
    """
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    is_sqlite = database_url.startswith('sqlite')
    
    # SQLite uses different connection arguments
    if is_sqlite:
        return {
            'echo': app.config['DEBUG'],
            'connect_args': {'check_same_thread': False}  # Allow multi-threaded access
        }
    
    # PostgreSQL connection pooling and SSL
    engine_args = {
        'poolclass': QueuePool,
        'pool_size': app.config['DB_POOL_SIZE'],
        'max_overflow': app.config['DB_MAX_OVERFLOW'],
        'pool_timeout': app.config['DB_POOL_TIMEOUT'],
        'pool_recycle': app.config['DB_POOL_RECYCLE'],
        'pool_pre_ping': True,  # Test connections before using them
        'echo': app.config['DEBUG'],  # Log SQL statements in debug mode
    }
    
    # Configure SSL if required
    ssl_mode = app.config.get('DB_SSL_MODE')
    if ssl_mode and ssl_mode in ('require', 'verify-ca', 'verify-full'):
        connect_args = {'sslmode': ssl_mode}
        
        # For verify-ca and verify-full, you would add certificate paths here
        # Example:
        # if ssl_mode in ('verify-ca', 'verify-full'):
        #     connect_args['sslrootcert'] = '/path/to/ca-cert.pem'
        #     connect_args['sslcert'] = '/path/to/client-cert.pem'
        #     connect_args['sslkey'] = '/path/to/client-key.pem'
        
        engine_args['connect_args'] = connect_args
    
    return engine_args


def init_db(app):
    """
    Initialize database engine and session factory.
    
    Args:
        app: Flask application instance
    """
    global engine, SessionLocal
    
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    engine_args = get_engine_args(app)
    
    # Create engine
    engine = create_engine(database_url, **engine_args)
    
    # Configure connection pool events for logging
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        """Log new database connections."""
        if app.config['DEBUG']:
            app.logger.info("Database connection established")
    
    @event.listens_for(engine, "close")
    def receive_close(dbapi_conn, connection_record):
        """Log database connection closures."""
        if app.config['DEBUG']:
            app.logger.info("Database connection closed")
    
    # Create session factory
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    SessionLocal = scoped_session(session_factory)
    
    # Store in app context
    app.extensions = getattr(app, 'extensions', {})
    app.extensions['sqlalchemy'] = {'engine': engine, 'session': SessionLocal}
    
    # Register teardown handler
    app.teardown_appcontext(close_session)


def get_db():
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    """
    Get the current request's database session.
    Creates one if it doesn't exist.
    Session is automatically cleaned up at end of request.
    
    Returns:
        SQLAlchemy session for current request
    """
    if 'db_session' not in g:
        g.db_session = SessionLocal()
    return g.db_session


def close_session(exception=None):
    """
    Close database session at end of request.
    Called automatically by Flask teardown_appcontext.
    """
    session = g.pop('db_session', None)
    if session is not None:
        try:
            if exception is None:
                session.commit()
            else:
                session.rollback()
        except Exception as e:
            logger.error(f"Error closing session: {e}")
            session.rollback()
        finally:
            session.close()


@contextmanager
def get_db_session():
    """
    Context manager for standalone database operations.
    Use this for CLI scripts or background jobs.
    For web requests, use get_session() instead.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def execute_raw_sql(query, params=None):
    """
    Execute raw SQL safely using parameterized queries.
    
    Args:
        query: SQL query string with :param placeholders
        params: Dictionary of parameters
        
    Returns:
        Result proxy object
        
    Example:
        result = execute_raw_sql(
            "SELECT * FROM users WHERE email = :email",
            {"email": "user@example.com"}
        )
    """
    with get_db_session() as session:
        result = session.execute(text(query), params or {})
        return result.fetchall()


def transaction_example():
    """
    Example of explicit transaction management using session.begin().
    
    This demonstrates how to use the transaction context manager
    for operations that require atomicity.
    """
    with get_db_session() as session:
        # The session.begin() context manager handles commit/rollback
        with session.begin():
            # All operations here are in a transaction
            # If any operation fails, everything is rolled back
            user = session.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": 1}
            ).fetchone()
            
            if user:
                session.execute(
                    text("UPDATE users SET last_login = NOW() WHERE id = :id"),
                    {"id": user.id}
                )


def create_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine)
