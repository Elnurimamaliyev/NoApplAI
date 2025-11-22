# NoApplAI Backend

Production-ready FastAPI backend for the NoApplAI university application platform.

## 🏗️ Architecture

### Tech Stack
- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL 16+ with SQLAlchemy (async)
- **Cache**: Redis 7+
- **Storage**: AWS S3 / MinIO (S3-compatible)
- **Task Queue**: Celery with Redis broker
- **AI**: OpenAI GPT-4 for program matching
- **Authentication**: JWT (JSON Web Tokens)
- **Container**: Docker & Docker Compose

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Authentication (register, login, refresh)
│   │       │   ├── users.py         # User management & profile
│   │       │   ├── programs.py      # University programs CRUD
│   │       │   ├── applications.py  # Application management
│   │       │   ├── documents.py     # File upload & document management
│   │       │   ├── notifications.py # Notification system
│   │       │   ├── dashboard.py     # Dashboard stats & AI recommendations
│   │       │   └── websocket.py     # Real-time updates
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py        # Application settings
│   │   ├── database.py      # Database session management
│   │   ├── security.py      # JWT & password hashing
│   │   ├── celery.py        # Celery configuration
│   │   └── cache.py         # Redis cache utilities
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── program.py       # Program model
│   │   ├── application.py   # Application model
│   │   ├── document.py      # Document model
│   │   ├── notification.py  # Notification model
│   │   └── activity.py      # Activity tracking model
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   ├── program.py       # Program schemas
│   │   ├── application.py   # Application schemas
│   │   ├── document.py      # Document schemas
│   │   └── common.py        # Common/shared schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── user_service.py      # User business logic
│   │   ├── program_service.py   # Program management
│   │   ├── file_service.py      # S3 file operations
│   │   ├── ai_service.py        # AI matching algorithm
│   │   ├── notification_service.py  # Notification creation
│   │   └── email_service.py     # Email sending
│   ├── dependencies/
│   │   ├── auth.py          # Authentication dependencies
│   │   └── pagination.py    # Pagination helpers
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── alembic/                 # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start with Docker (Recommended)

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- MinIO (S3) on ports 9000 (API) and 9001 (Console)
- FastAPI Backend on port 8000
- Celery Worker
- Celery Beat (Scheduler)
- Flower (Celery monitoring) on port 5555

### 3. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 4. Create Initial Data (Optional)

```bash
docker-compose exec backend python -m app.scripts.seed_data
```

### 5. Access Services

- **API Documentation**: http://localhost:8000/api/docs
- **Backend API**: http://localhost:8000
- **Flower (Celery)**: http://localhost:5555
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin123)

## 📋 Manual Setup (Without Docker)

### 1. Install PostgreSQL & Redis

```bash
# macOS
brew install postgresql@16 redis

# Start services
brew services start postgresql@16
brew services start redis
```

### 2. Create Database

```bash
createdb noapplai_db
```

### 3. Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Start Celery Worker (Separate Terminal)

```bash
celery -A app.core.celery worker --loglevel=info
```

## 🔐 Authentication Flow

### 1. Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123"
}
```

### 2. Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    ...
  }
}
```

### 3. Use Token in Requests

```http
GET /api/v1/users/me
Authorization: Bearer {access_token}
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/password-reset-request` - Request password reset
- `POST /api/v1/auth/password-reset` - Reset password

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PATCH /api/v1/users/me` - Update user profile
- `POST /api/v1/users/me/avatar` - Upload avatar
- `DELETE /api/v1/users/me` - Delete account

### Programs
- `GET /api/v1/programs` - List programs (with filters)
- `GET /api/v1/programs/{id}` - Get program details
- `GET /api/v1/programs/search` - Search programs
- `GET /api/v1/programs/recommendations` - Get AI-matched programs

### Applications
- `GET /api/v1/applications` - List user applications
- `POST /api/v1/applications` - Create new application
- `GET /api/v1/applications/{id}` - Get application details
- `PATCH /api/v1/applications/{id}` - Update application
- `DELETE /api/v1/applications/{id}` - Delete application
- `POST /api/v1/applications/{id}/submit` - Submit application

### Documents
- `GET /api/v1/documents` - List user documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document
- `GET /api/v1/documents/{id}/download` - Download document

### Notifications
- `GET /api/v1/notifications` - List notifications
- `GET /api/v1/notifications/{id}` - Get notification
- `PATCH /api/v1/notifications/{id}/read` - Mark as read
- `POST /api/v1/notifications/mark-all-read` - Mark all as read
- `DELETE /api/v1/notifications/{id}` - Delete notification

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/dashboard/recent-activity` - Get recent activities
- `GET /api/v1/dashboard/upcoming-deadlines` - Get upcoming deadlines

## 🤖 AI Program Matching

The AI matching system uses OpenAI GPT-4 to analyze:
- User's academic background (degree, GPA, major)
- Career goals and interests
- Test scores (TOEFL, IELTS, etc.)
- Work experience
- Program requirements and characteristics

Match scores are calculated based on:
1. Academic fit (40%)
2. Career alignment (30%)
3. Financial feasibility (15%)
4. Location preferences (10%)
5. Other factors (5%)

## 📁 File Upload System

### Supported Document Types
- CV/Resume (.pdf, .docx)
- Academic Transcripts (.pdf)
- Passport/ID (.jpg, .png, .pdf)
- English Test Certificates (.pdf)
- Recommendation Letters (.pdf, .docx)
- Statement of Purpose (.pdf, .docx)

### Upload Endpoint

```http
POST /api/v1/documents/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: (binary)
document_type: "cv_resume"
name: "My CV"
```

### File Validation
- Max file size: 10MB
- Allowed extensions: .pdf, .jpg, .jpeg, .png, .docx, .doc
- AI validation for document quality

## 📊 Frontend Integration

### API Client Setup

```javascript
// frontend/src/api/client.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

class APIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Token expired, try to refresh
      await this.refreshToken();
      return this.request(endpoint, options);
    }

    return response.json();
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await fetch(`${this.baseURL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    
    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('access_token', data.access_token);
  }

  // Auth methods
  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.token = data.access_token;
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  }

  async logout() {
    await this.request('/auth/logout', { method: 'POST' });
    this.token = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Programs
  async getPrograms(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/programs?${params}`);
  }

  async getProgramRecommendations() {
    return this.request('/programs/recommendations');
  }

  // Applications
  async getApplications() {
    return this.request('/applications');
  }

  async createApplication(programId) {
    return this.request('/applications', {
      method: 'POST',
      body: JSON.stringify({ program_id: programId }),
    });
  }

  // Documents
  async uploadDocument(file, documentType, name) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    formData.append('name', name);

    return fetch(`${this.baseURL}/documents/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
      body: formData,
    }).then(r => r.json());
  }

  // Notifications
  async getNotifications() {
    return this.request('/notifications');
  }

  async markNotificationAsRead(id) {
    return this.request(`/notifications/${id}/read`, { method: 'PATCH' });
  }

  // Dashboard
  async getDashboardStats() {
    return this.request('/dashboard/stats');
  }
}

export default new APIClient();
```

### Update Frontend JavaScript

Replace the frontend's hardcoded data with API calls:

```javascript
// Update version_nointegration.html
// Replace:
const programs = [/* hardcoded data */];

// With:
let programs = [];
let applications = [];
let documents = [];
let notifications = [];

async function loadData() {
  try {
    const [programsData, appsData, docsData, notifsData] = await Promise.all([
      api.getPrograms(),
      api.getApplications(),
      api.getDocuments(),
      api.getNotifications(),
    ]);
    
    programs = programsData.items || [];
    applications = appsData.items || [];
    documents = docsData.items || [];
    notifications = notifsData.items || [];
    
    renderProgramsGrid();
    renderApplicationsList();
    renderDocumentsGrid();
    renderNotifications();
  } catch (error) {
    console.error('Failed to load data:', error);
    showToast('Failed to load data', 'error');
  }
}

// Call on page load
document.addEventListener('DOMContentLoaded', () => {
  loadData();
  // ... rest of initialization
});
```

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/unit -v
```

### Run Integration Tests

```bash
pytest tests/integration -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html tests/
```

## 🔧 Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## 📈 Monitoring

### Celery Tasks (Flower)
Visit: http://localhost:5555

### Application Logs

```bash
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### Database Queries

```bash
docker-compose exec postgres psql -U noapplai_user -d noapplai_db
```

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS for production domains
- [ ] Set up Sentry for error tracking
- [ ] Configure email service (AWS SES recommended)
- [ ] Set up S3 bucket with proper permissions
- [ ] Enable database backups
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure rate limiting
- [ ] Set up CDN for static files

### Deploy with Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key (min 32 characters)
- `OPENAI_API_KEY`: OpenAI API key for AI matching
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: S3 credentials
- `MAIL_*`: Email configuration
- `CORS_ORIGINS`: Allowed frontend origins

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Write tests
4. Run linters and tests
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: support@noapplai.com
- Documentation: [Full API Docs](http://localhost:8000/api/docs)

---

**NoApplAI Backend** - Built with ❤️ using FastAPI
