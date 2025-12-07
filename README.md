# 🎓 NoApplAI - AI-Powered University Application Platform

An intelligent platform that helps students discover, organize, and manage university applications with AI-powered recommendations.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)

## ✨ Features

### For Students
- 🔍 **Program Discovery**: Browse 32+ university programs from top institutions (TUM, DAAD, ETH Zurich, University of Zurich, EPFL)
- 🎯 **Smart Search**: Filter by country, degree type, deadline, and search across program names, universities, and descriptions
- 📝 **Application Tracking**: Manage multiple applications with status tracking and deadline monitoring
- 📄 **Document Management**: Upload and organize CVs, transcripts, and language certificates
- 🔔 **Notifications**: Get deadline reminders and status updates
- 📊 **Dashboard**: View application statistics, recent activities, and progress tracking

### Technical Features
- 🤖 **AI Recommendations**: GPT-4 powered program matching (coming soon)
- 🔐 **Secure Authentication**: JWT-based authentication with refresh tokens
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Async Python backend with Redis caching
- 🐳 **Easy Deployment**: Docker Compose for one-command setup

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### 1. Clone Repository
```bash
git clone https://github.com/Elnurimamaliyev/NoApplAI.git
cd NoApplAI
```

### 2. Start Backend Services
```bash
cd backend
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- FastAPI backend (port 8000)

### 3. Run Database Migrations & Seed Data
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed database with 32 university programs
docker-compose exec backend python seed_programs.py
```

### 4. Start Frontend
```bash
# From project root, in a new terminal
python3 -m http.server 3000
# Or use any static file server
```

### 5. Access Application
- **Frontend**: http://localhost:3000 (open `full_page_integrated.html`)
- **API Documentation**: http://localhost:8000/api/docs
- **API Health Check**: http://localhost:8000/health

### Test Credentials
```
Email: demo@noapplai.com
Password: Demo123!@#
```

## 📁 Project Structure

```
NoApplAI/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/        # API endpoints
│   │   │   ├── auth.py              # Authentication (register, login, profile)
│   │   │   ├── programs.py          # Program CRUD & search
│   │   │   ├── applications.py      # Application management
│   │   │   ├── documents.py         # Document upload/download
│   │   │   ├── dashboard.py         # Dashboard stats
│   │   │   └── notifications.py     # Notifications
│   │   ├── core/                    # Core configuration
│   │   │   ├── config.py            # Settings & environment
│   │   │   ├── database.py          # Database connection
│   │   │   └── security.py          # JWT & password hashing
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── user.py              # User model
│   │   │   ├── program.py           # Program model
│   │   │   ├── application.py       # Application model
│   │   │   ├── document.py          # Document model
│   │   │   ├── notification.py      # Notification model
│   │   │   └── activity.py          # Activity tracking
│   │   ├── schemas/                 # Pydantic schemas
│   │   └── dependencies/            # FastAPI dependencies
│   ├── alembic/                     # Database migrations
│   ├── seed_programs.py             # Seed script
│   └── docker-compose.yml           # Docker services
├── full_page_integrated.html        # Frontend SPA (3,752 lines)
├── test_api.html                    # API testing page
└── README.md                        # This file
```

## 🛠️ Development

### Backend Development

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend locally (without Docker)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Create new database migration
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Frontend Development

The frontend is currently a single HTML file (`full_page_integrated.html`) with inline JavaScript and Tailwind CSS.

**Key Features:**
- Real-time search with 300ms debouncing
- Instant filter updates (country, degree type)
- Route persistence (stays on current page after reload)
- JWT token management in localStorage
- Toast notifications for user feedback

### Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://noapplai:noapplai123@localhost:5432/noapplai_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-min-32-chars-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Future: AWS S3 (for file storage)
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_S3_BUCKET=noapplai-documents

# Future: OpenAI (for AI features)
# OPENAI_API_KEY=your-openai-api-key
```

## 📖 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login with email/password |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user info |
| PATCH | `/api/v1/auth/profile` | Update user profile |
| POST | `/api/v1/auth/logout` | Logout user |

### Programs Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/programs/` | List all programs (with filters) |
| GET | `/api/v1/programs/{id}` | Get program by ID |
| GET | `/api/v1/programs/recommendations` | Get AI recommendations (coming soon) |

**Filter Parameters:**
- `country`: Filter by country (e.g., "Germany", "Switzerland")
- `degree_type`: Filter by degree (e.g., "Master", "PhD")
- `search`: Search in name, university, location, description
- `skip`: Pagination offset (default: 0)
- `limit`: Results per page (default: 100)

### Applications Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/applications/` | List user's applications |
| POST | `/api/v1/applications/` | Create new application |
| GET | `/api/v1/applications/{id}` | Get application details |
| PATCH | `/api/v1/applications/{id}` | Update application |
| POST | `/api/v1/applications/{id}/submit` | Submit application |
| DELETE | `/api/v1/applications/{id}` | Delete application |

### Documents Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/documents/` | List user's documents |
| POST | `/api/v1/documents/upload/cv` | Upload CV/Resume |
| POST | `/api/v1/documents/upload/transcript` | Upload transcript |
| POST | `/api/v1/documents/upload/language-certificate` | Upload language cert |
| GET | `/api/v1/documents/{id}` | Get document metadata |
| GET | `/api/v1/documents/{id}/download` | Download document |
| DELETE | `/api/v1/documents/{id}` | Delete document |

### Dashboard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/` | Get full dashboard data |
| GET | `/api/v1/dashboard/stats` | Get statistics only |

### Notifications Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notifications/` | List notifications |
| GET | `/api/v1/notifications/unread-count` | Get unread count |
| PATCH | `/api/v1/notifications/{id}/read` | Mark as read |
| POST | `/api/v1/notifications/mark-all-read` | Mark all as read |

**Interactive API Docs**: Visit http://localhost:8000/api/docs for full Swagger documentation with try-it-out functionality.

## 🗄️ Database Schema

### Core Models

**User**
- Authentication & profile information
- Fields: email, password_hash, full_name, role, profile_picture, etc.

**Program**
- University program details
- Fields: name, university_name, country, city, degree_type, deadline, etc.
- 32 programs seeded from TUM, DAAD, ETH Zurich, UZH, EPFL

**Application**
- User applications to programs
- Fields: program_id, user_id, status, submitted_at, notes
- Status: draft, submitted, under_review, accepted, rejected, withdrawn

**Document**
- Uploaded documents
- Fields: filename, file_path, document_type, file_size, mime_type
- Types: CV_RESUME, TRANSCRIPT, ENGLISH_TEST, RECOMMENDATION_LETTER, etc.

**Notification**
- System notifications
- Fields: user_id, title, message, type, read, created_at
- Types: application_submitted, document_uploaded, deadline_reminder, status_update

**Activity**
- Activity tracking log
- Fields: user_id, activity_type, description, metadata, created_at

## 🧪 Testing

```bash
# Run test script (Python)
cd backend
python test_programs_api.py

# Test API with web interface
# Open test_api.html in browser
```

**Future**: Full pytest test suite planned (see `CODE_QUALITY_ANALYSIS.md`)

## 🚢 Deployment

### Using Docker Compose (Recommended)

```bash
# Production deployment
cd backend
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Deployment

1. Set up PostgreSQL 16 database
2. Set up Redis 7 cache
3. Configure environment variables
4. Run migrations: `alembic upgrade head`
5. Seed database: `python seed_programs.py`
6. Start backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
7. Serve frontend with Nginx or any static file server

## 📚 Documentation

- **Setup Guide**: `backend/SETUP.md`
- **Quick Reference**: `backend/SIMPLIFIED_GUIDE.md`
- **Seeding Guide**: `backend/SEEDING_GUIDE.md`
- **Code Quality Analysis**: `CODE_QUALITY_ANALYSIS.md`
- **API Docs**: http://localhost:8000/api/docs (when running)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ES6+ features, consistent naming
- Write clear commit messages
- Add comments for complex logic

## 🐛 Known Issues & TODOs

See `CODE_QUALITY_ANALYSIS.md` for comprehensive list.

**High Priority:**
- [ ] Implement S3/MinIO file storage (documents currently in memory)
- [ ] Add AI program matching with OpenAI
- [ ] Write test suite (pytest)
- [ ] Split frontend into modular structure

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **University Programs**: Data sourced from TUM, DAAD, ETH Zurich, University of Zurich, EPFL
- **Framework**: Built with FastAPI, PostgreSQL, and Redis
- **UI**: Styled with Tailwind CSS

## 📞 Contact

- **Repository**: [github.com/Elnurimamaliyev/NoApplAI](https://github.com/Elnurimamaliyev/NoApplAI)
- **Issues**: [GitHub Issues](https://github.com/Elnurimamaliyev/NoApplAI/issues)

---

**Built with ❤️ for students worldwide**