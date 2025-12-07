# Quick Reference: Programs Seeding

## One-Command Setup ⚡
```bash
cd /Users/elnurimamaliyev/NoApplAI/backend && ./setup_and_seed.sh
```

## Manual Steps 📝

### 1. Start Docker Desktop
Open Docker Desktop app, wait for whale icon to be steady

### 2. Start Services
```bash
cd /Users/elnurimamaliyev/NoApplAI/backend
docker compose up -d
```

### 3. Seed Programs
```bash
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

### 4. Verify
```bash
./verify_programs.py
```

## Test API 🧪
```bash
# Check if running
curl http://localhost:8000/api/v1/programs/ | jq 'length'

# Get first program
curl http://localhost:8000/api/v1/programs/ | jq '.[0]'
```

## Troubleshooting 🔧

### Docker not running
```bash
# Check Docker
docker ps

# If error: Start Docker Desktop app
```

### Database connection failed
```bash
# Check containers
docker compose ps

# View logs
docker compose logs postgres

# Restart
docker compose restart
```

### Re-seed needed
```bash
# Clear table
docker exec -it noapplai_postgres psql -U noapplai_user -d noapplai_db -c "TRUNCATE TABLE programs CASCADE;"

# Run migration again
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

## What Gets Seeded 📊
- **34 programs** from universities in Germany, Switzerland, USA, Japan, Italy
- **8 from TUM**, 4 from DAAD, 2 from ETH Zurich, 2 from UZH, 2 from EPFL
- **7 PhD positions**, 3 Fellowships, 3 Internships, 2 Research positions, 2 Masters

## Files 📁
- **Data**: `programs_seed_data.json` (34 programs)
- **Migration**: `alembic/versions/2025_12_01_seed_programs_data.py`
- **Setup**: `setup_and_seed.sh` (automated)
- **Verify**: `verify_programs.py` (check seeding)
- **Guide**: `SEEDING_GUIDE.md` (full docs)

## Frontend Integration 🌐
```javascript
// Fetch programs in full_page_integrated.html
async function loadPrograms() {
    const response = await fetch('http://localhost:8000/api/v1/programs/');
    const programs = await response.json();
    return programs; // Array of 34 programs
}
```

## Endpoints 🔌
- Programs: `GET http://localhost:8000/api/v1/programs/`
- Single: `GET http://localhost:8000/api/v1/programs/{id}`
- Docs: `http://localhost:8000/docs`

---
**Migration ID**: `seed_programs_001`  
**Idempotent**: ✅ Safe to run multiple times  
**Rollback**: `alembic downgrade -1`
