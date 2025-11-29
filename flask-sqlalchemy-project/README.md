# Flask SQLAlchemy PostgreSQL Project

A complete Flask backend application with PostgreSQL integration using SQLAlchemy (Core + ORM), featuring CRUD operations, pagination, filtering, migrations, and comprehensive testing.

## Features

- ✅ **SQLAlchemy ORM & Core** - Complete database abstraction with both ORM and raw SQL support
- ✅ **Connection Pooling** - Configurable connection pool with SSL support
- ✅ **RESTful API** - Full CRUD endpoints for Users and Posts
- ✅ **Input Validation** - Marshmallow schemas for request/response validation
- ✅ **Pagination & Filtering** - Efficient data retrieval with query parameters
- ✅ **Alembic Migrations** - Database version control and migration management
- ✅ **Transaction Management** - Context managers for atomic operations
- ✅ **Parameterized Queries** - Protection against SQL injection
- ✅ **Testing** - Comprehensive pytest suite with transaction rollback
- ✅ **Docker Support** - Complete containerization with docker-compose
- ✅ **Environment Configuration** - Flexible config for dev/test/production

## Project Structure

```
flask-sqlalchemy-project/
├── app.py                          # Application factory
├── config.py                       # Environment configuration
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose setup
├── alembic.ini                     # Alembic configuration
├── .env.example                    # Environment variables template
├── app/
│   ├── __init__.py
│   ├── db.py                       # Database connection & session management
│   ├── models.py                   # SQLAlchemy models (User, Post)
│   ├── schemas.py                  # Marshmallow validation schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py                # User endpoints
│   │   └── posts.py                # Post endpoints
│   └── services/
│       ├── __init__.py
│       ├── user_service.py         # User business logic
│       └── post_service.py         # Post business logic
├── migrations/
│   ├── env.py                      # Alembic environment
│   ├── script.py.mako              # Migration template
│   ├── seed.py                     # Database seeding script
│   └── versions/
│       └── 001_initial_migration.py
└── tests/
    ├── __init__.py
    ├── conftest.py                 # Pytest fixtures
    ├── test_user_service.py        # User service tests
    ├── test_post_service.py        # Post service tests
    ├── test_user_endpoints.py      # User API tests
    └── test_post_endpoints.py      # Post API tests
```

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

## Quick Start

### Option 1: Docker (Recommended)

1. **Clone and setup**:
   ```bash
   cd flask-sqlalchemy-project
   cp .env.example .env
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Start PostgreSQL container
   - Create development and test databases
   - Run migrations
   - Start Flask application on http://localhost:5000

3. **Verify installation**:
   ```bash
   curl http://localhost:5000/health
   ```

### Option 2: Local Development

1. **Setup environment**:
   ```bash
   cd flask-sqlalchemy-project
   cp .env.example .env
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL** (if not using Docker):
   ```bash
   # Using Docker for PostgreSQL only
   docker run --name flask-postgres \
     -e POSTGRES_USER=flask_user \
     -e POSTGRES_PASSWORD=flask_password \
     -e POSTGRES_DB=flask_app \
     -p 5432:5432 \
     -d postgres:15-alpine
   
   # Create test database
   docker exec flask-postgres psql -U flask_user -d flask_app \
     -c "CREATE DATABASE flask_app_test;"
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Seed database** (optional):
   ```bash
   python migrations/seed.py
   ```

5. **Start application**:
   ```bash
   python app.py
   ```

   Application will be available at http://localhost:5000

## API Endpoints

### Health Check
```http
GET /health
GET /
```

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create a new user |
| GET | `/api/users` | Get paginated list of users |
| GET | `/api/users/:id` | Get user by ID |
| GET | `/api/users/username/:username` | Get user by username |
| PUT/PATCH | `/api/users/:id` | Update user |
| DELETE | `/api/users/:id` | Delete user |

**Query Parameters for GET /api/users**:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)
- `username` - Filter by username (partial match)
- `email` - Filter by email (partial match)
- `is_active` - Filter by active status (true/false)

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts` | Create a new post |
| GET | `/api/posts` | Get paginated list of posts |
| GET | `/api/posts/:id` | Get post by ID |
| GET | `/api/posts/user/:user_id` | Get posts by user |
| PUT/PATCH | `/api/posts/:id` | Update post |
| DELETE | `/api/posts/:id` | Delete post |
| POST | `/api/posts/:id/publish` | Publish post |
| POST | `/api/posts/:id/unpublish` | Unpublish post |

**Query Parameters for GET /api/posts**:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)
- `author_id` - Filter by author ID
- `published` - Filter by published status (true/false)
- `search` - Search in title and content
- `include_author` - Include author details (true/false)

## Example API Usage

### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Get Users with Pagination
```bash
curl "http://localhost:5000/api/users?page=1&page_size=10&is_active=true"
```

### Create a Post
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "author_id": 1,
    "published": true
  }'
```

### Search Posts
```bash
curl "http://localhost:5000/api/posts?search=Flask&published=true"
```

## Database Migrations

### Create a New Migration
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>
```

### View Migration History
```bash
alembic history
alembic current
```

## Database Features

### Connection Pooling

Configured in `config.py`:
- Pool size: 10 connections
- Max overflow: 20 additional connections
- Pool timeout: 30 seconds
- Pool recycle: 3600 seconds (1 hour)
- Pre-ping: Enabled (test connections before use)

### SSL Support

Configure SSL in `.env`:
```env
DB_SSL_MODE=prefer  # Options: disable, allow, prefer, require, verify-ca, verify-full
```

### Raw SQL Queries

Example of executing parameterized raw SQL:
```python
from app.db import execute_raw_sql

result = execute_raw_sql(
    "SELECT * FROM users WHERE email = :email",
    {"email": "user@example.com"}
)
```

### Transaction Management

Example using context manager:
```python
from app.db import get_db_session

with get_db_session() as session:
    # Operations here are in a transaction
    user = User(username='test', email='test@example.com')
    session.add(user)
    # Automatically commits on success, rolls back on exception
```

## Testing

### Run All Tests
```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_user_service.py

# Run specific test
pytest tests/test_user_service.py::TestUserService::test_create_user

# Generate coverage report
pytest --cov=app --cov-report=html
```

### Test Features

The test suite includes:
- **Fixtures**: Database setup with automatic rollback between tests
- **Service Layer Tests**: Business logic validation
- **API Endpoint Tests**: Integration testing of REST APIs
- **Transaction Rollback**: Each test runs in isolation
- **Test Database**: Separate database for testing

### Test Database

Tests use a separate PostgreSQL database (`flask_app_test`) to avoid affecting development data. The `db_session` fixture ensures all changes are rolled back after each test.

## Environment Variables

Create a `.env` file (see `.env.example`):

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://flask_user:flask_password@localhost:5432/flask_app
TEST_DATABASE_URL=postgresql://flask_user:flask_password@localhost:5432/flask_app_test

# Connection Pool Settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# SSL Configuration
DB_SSL_MODE=prefer

# Application Settings
DEBUG=True
TESTING=False
```

## Configuration

The application supports multiple environments:

- **Development**: Debug enabled, verbose logging
- **Testing**: Separate test database, minimal connection pooling
- **Production**: SSL required, debug disabled

Set environment with:
```bash
export FLASK_ENV=production  # or development, testing
```

## Architecture

### Layers

1. **Routes Layer** (`app/routes/`): HTTP request handling and response formatting
2. **Service Layer** (`app/services/`): Business logic and data operations
3. **Models Layer** (`app/models.py`): SQLAlchemy ORM models
4. **Database Layer** (`app/db.py`): Connection management and session handling

### Design Patterns

- **Application Factory**: Flexible app creation for different environments
- **Service Layer**: Separation of business logic from routes
- **Repository Pattern**: Data access abstraction through services
- **Context Managers**: Automatic resource management for database sessions

## Production Deployment

### Environment Configuration

1. Update `.env` for production:
   ```env
   FLASK_ENV=production
   DEBUG=False
   DB_SSL_MODE=require
   SECRET_KEY=<strong-random-key>
   ```

2. Use environment-specific database URLs

### Security Considerations

- ✅ Parameterized queries (SQL injection protection)
- ✅ Password hashing (werkzeug.security)
- ✅ Input validation (Marshmallow schemas)
- ✅ SSL/TLS for database connections
- ✅ Environment-based configuration
- ⚠️ Add authentication/authorization (JWT, OAuth2)
- ⚠️ Enable CORS only for trusted origins
- ⚠️ Use rate limiting for API endpoints
- ⚠️ Add request/response logging

### Performance

- Connection pooling for database efficiency
- Pagination for large datasets
- Indexed database columns for fast queries
- Lazy loading of relationships

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U flask_user -d flask_app

# View logs
docker logs flask-postgres
```

### Migration Issues

```bash
# Reset migrations (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head

# View SQL without executing
alembic upgrade head --sql
```

### Test Failures

```bash
# Run tests with detailed output
pytest -vv --tb=short

# Run specific test with print output
pytest -s tests/test_user_service.py::TestUserService::test_create_user
```

## Contributing

1. Create a feature branch
2. Make changes
3. Add/update tests
4. Ensure tests pass: `pytest`
5. Check code coverage: `pytest --cov=app`
6. Submit pull request

## License

This project is provided as-is for educational purposes.

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
