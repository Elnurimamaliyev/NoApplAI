# NoApplAI

**AI-Powered University Application Platform**

NoApplAI is a comprehensive web application that helps students discover, track, and manage their university applications using AI-powered recommendations and intelligent document processing.

---

## 🎯 What Does This Project Do?

NoApplAI streamlines the university application process by providing:

- **Smart Program Discovery**: Browse and search through university programs with advanced filtering
- **AI-Powered Recommendations**: Get personalized program suggestions based on your profile
- **Application Tracking**: Manage multiple applications in one centralized dashboard
- **Document Management**: Upload, organize, and validate required application documents
- **Deadline Monitoring**: Never miss an application deadline with automated reminders
- **Progress Analytics**: Track your application journey with detailed statistics and insights
- **Real-time Notifications**: Stay updated on application status changes and important events

---

## 🏗️ Project Architecture

### **Backend** (FastAPI)
- **Framework**: FastAPI 0.109+ with async support
- **Database**: PostgreSQL 16+ with SQLAlchemy ORM
- **Cache**: Redis 7+ for session management
- **Authentication**: JWT-based auth with bcrypt password hashing
- **Storage**: Support for AWS S3/MinIO for document uploads
- **AI Integration**: OpenAI GPT-4 for program matching (configurable)

**Key Features:**
- RESTful API with OpenAPI documentation
- Role-based access control (Student, Admin, Counselor)
- Automated database migrations with Alembic
- Comprehensive endpoint testing
- Docker containerization

### **Frontend** (Vanilla JS + Tailwind CSS)
- Single-page application with client-side routing
- Responsive design with Tailwind CSS
- Real-time updates via REST API integration
- Authentication flow with JWT tokens
- Modern, clean UI with smooth transitions

---

## 🚀 Quick Start

### **Prerequisites**
- Docker Desktop
- Python 3.11+
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/Elnurimamaliyev/NoApplAI.git
cd NoApplAI
```

### **2. Set Up Backend**
```bash
cd backend

# Copy environment configuration
cp .env.example .env

# Edit .env with your settings (optional for local dev)

# Start all services with Docker
docker compose up -d
```

This will start:
- **PostgreSQL** on `localhost:5432`
- **Redis** on `localhost:6379`
- **FastAPI Backend** on `http://localhost:8000`

### **3. Seed Database (First Time Setup)**
```bash
# Run database migrations and seed data
./setup_and_seed.sh

# Or manually:
python -m alembic upgrade head
```

### **4. Access the Application**

- **Frontend**: Open `frontend/full_page_integrated.html` in your browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative Docs**: http://localhost:8000/api/redoc

### **5. Test the Setup**
```bash
# Check backend health
curl http://localhost:8000/health

# Verify programs data
python backend/verify_programs.py

# Test API endpoints
curl http://localhost:8000/api/v1/programs/ | jq
```

---

## 📦 Dependencies & Installation

### **Backend Dependencies**
Core dependencies are listed in `backend/requirements.txt`:

```
fastapi==0.109.0              # Web framework
uvicorn[standard]==0.27.0     # ASGI server
sqlalchemy==2.0.25            # ORM
asyncpg==0.29.0               # Async PostgreSQL driver
alembic==1.13.1               # Database migrations
python-jose[cryptography]     # JWT tokens
passlib[bcrypt]               # Password hashing
redis==5.0.1                  # Caching
boto3==1.34.34                # AWS S3 support
openai==1.10.0                # AI integration
```

Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### **Frontend Dependencies**
The frontend uses CDN-delivered libraries:
- **Tailwind CSS** (via CDN)
- **Google Fonts** (Inter, Montserrat)

No installation required for frontend.

---

## 📂 Folder Structure Explained

```
NoApplAI/
│
├── backend/                    # FastAPI backend application
│   ├── app/                    # Application source code
│   │   ├── api/v1/            # API endpoints grouped by version
│   │   │   └── endpoints/     # Individual endpoint modules
│   │   ├── core/              # Core functionality (config, database, security)
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   └── dependencies/      # Reusable dependencies (auth, pagination)
│   ├── alembic/               # Database migration scripts
│   ├── uploads/               # Document storage (local/development)
│   ├── docker-compose.yml     # Multi-container orchestration
│   ├── Dockerfile             # Backend container definition
│   └── *.sh                   # Utility scripts (start, stop, seed)
│
├── frontend/                   # Frontend application files
│   └── full_page_integrated.html  # Main SPA application
│
├── docs/                       # Project documentation
│   ├── AUTH_IMPLEMENTATION.md      # Authentication system details
│   ├── NAVBAR_AUTH_UPDATE.md       # Navigation updates
│   ├── ROUTING_AUTH_UPDATE.md      # Routing implementation
│   └── backend/                    # Backend-specific guides
│       ├── SETUP.md                # Detailed setup instructions
│       ├── QUICK_REFERENCE.md      # Quick command reference
│       └── SEEDING_GUIDE.md        # Database seeding guide
│
├── archive/                    # Archived/unused files
│   ├── flask-sqlalchemy-project/   # Separate Flask demo project
│   ├── backup/                     # Old page versions
│   └── test_*.{html,py}           # Development test files
│
└── .venv/                      # Python virtual environment (local)
```

### **Key Directories:**

- **`backend/app/api/v1/endpoints/`**: All API endpoints (auth, programs, applications, documents, etc.)
- **`backend/app/models/`**: Database table definitions (User, Program, Application, Document, etc.)
- **`backend/app/schemas/`**: Data validation and serialization schemas
- **`backend/alembic/versions/`**: Database migration history
- **`docs/`**: All project documentation and guides
- **`archive/`**: Old files kept for reference (not required for running the app)

---

## 🛠️ Development

### **Running in Development Mode**
```bash
# Backend with hot reload
cd backend
docker compose up

# Or without Docker:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Database Migrations**
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### **Stopping Services**
```bash
cd backend
docker compose down

# Stop and remove volumes (⚠️ deletes data)
docker compose down -v
```

---

## 📚 Additional Documentation

Detailed documentation is available in the `docs/` folder:

- **[Backend Setup Guide](docs/backend/SETUP.md)**: Complete backend setup and configuration
- **[Quick Reference](docs/backend/QUICK_REFERENCE.md)**: Common commands and troubleshooting
- **[Seeding Guide](docs/backend/SEEDING_GUIDE.md)**: How to populate the database with sample data
- **[Auth Implementation](docs/AUTH_IMPLEMENTATION.md)**: Authentication system details
- **[Routing Updates](docs/ROUTING_AUTH_UPDATE.md)**: Frontend routing implementation

Backend-specific README: [backend/README.md](backend/README.md)

---

## 🔐 Default Test Credentials

After seeding the database, you can use these test accounts:

**Student Account:**
- Email: `student@test.com`
- Password: `password123`

**Admin Account:**
- Email: `admin@test.com`
- Password: `admin123`

---

## 🐛 Troubleshooting

### Docker Issues
```bash
# Check if Docker is running
docker ps

# Check container logs
docker compose logs backend
docker compose logs postgres

# Restart services
docker compose restart
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Access PostgreSQL directly
docker compose exec postgres psql -U noapplai_user -d noapplai_db
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>
```

---

## 🤝 Contributing

This is a completed project. For reference and learning purposes only.

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👨‍💻 Author

**Elnur Imamaliyev**
- GitHub: [@Elnurimamaliyev](https://github.com/Elnurimamaliyev)
- GitHub: [@GurbanaliFeyzullayev](https://github.com/qurbaneliii)

---

## 🙏 Acknowledgments

- FastAPI framework and community
- PostgreSQL database
- Tailwind CSS for UI styling
- OpenAI for AI integration capabilities
