# Programs Table Seeding Guide

## Overview
This guide will help you populate the Programs table with 34 real academic programs from universities across Germany, Switzerland, USA, Japan, and Italy.

## Prerequisites
- Docker Desktop installed and running on macOS
- Virtual environment activated at `/Users/elnurimamaliyev/NoApplAI/.venv`

## Quick Start (Automated)

### Option 1: One-Command Setup
```bash
cd /Users/elnurimamaliyev/NoApplAI/backend
./setup_and_seed.sh
```

This script will:
1. ✅ Check if Docker Desktop is running
2. ✅ Start PostgreSQL and Redis services
3. ✅ Wait for database to be healthy
4. ✅ Run Alembic migration to seed 34 programs
5. ✅ Verify data was inserted successfully
6. ✅ Display summary of seeded programs

---

## Manual Setup (Step-by-Step)

### Step 1: Start Docker Desktop
1. Open Docker Desktop application on macOS
2. Wait until Docker is fully running (whale icon in menu bar should be steady)
3. Verify Docker is running:
   ```bash
   docker ps
   ```
   Expected: List of containers or empty list (not an error)

### Step 2: Start Backend Services
```bash
cd /Users/elnurimamaliyev/NoApplAI/backend
bash start.sh
```

This will start:
- **PostgreSQL** (port 5432): Database for storing programs
- **Redis** (port 6379): Cache service
- **FastAPI Backend** (port 8000): API server

Wait ~10 seconds for services to be fully ready.

### Step 3: Run Database Migration
```bash
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> seed_programs_001
Loading 34 programs into database...
Successfully inserted 34 programs into database.
```

### Step 4: Verify Data
```bash
# Option A: Using psql
docker exec -it noapplai_postgres psql -U noapplai_user -d noapplai_db -c "SELECT COUNT(*) FROM programs;"

# Option B: Using Python script
/Users/elnurimamaliyev/NoApplAI/.venv/bin/python verify_programs.py
```

Expected: `count: 34`

---

## What Gets Seeded

### Data Source
- **File**: `backend/programs_seed_data.json`
- **Size**: 11 KB
- **Programs**: 34 academic programs

### Field Mapping
The migration maps JSON fields to database columns:

| JSON Field      | Database Column     | Example                                    |
|-----------------|---------------------|--------------------------------------------|
| `title`         | `program_name`      | "PhD Positions at TUM"                     |
| `university`    | `university_name`   | "Technical University of Munich"           |
| `degree_type`   | `degree_type`       | "PhD", "Master", "Fellowship"              |
| `country`       | `country`           | "Germany", "Switzerland"                   |
| `program_url`   | `program_url`       | "https://www.tum.de/..."                   |
| `deadline`      | `deadline`          | null (to be added later)                   |
| `requirements`  | `required_documents`| Stored as JSON array                       |
| `description`   | `description`       | null (to be added later)                   |

Auto-generated fields:
- `id`: UUID4 for each program
- `created_at`: Current timestamp
- `updated_at`: Current timestamp

### Program Distribution

**By University:**
- Technical University of Munich (TUM): 8 programs
- DAAD (German Academic Exchange): 4 programs
- ETH Zurich: 2 programs
- University of Zurich (UZH): 2 programs
- EPFL: 2 programs
- Others: 16 programs

**By Degree Type:**
- PhD: 7 programs
- Fellowship/Scholarship: 3 programs
- Internship: 3 programs
- Research Position: 2 programs
- Master: 2 programs
- Other/Unspecified: 17 programs

**By Country:**
- Germany: 13 programs
- Switzerland: 6 programs
- USA: 1 program
- Japan: 1 program
- Italy: 1 program
- Unspecified: 12 programs

---

## Idempotency & Safety

### Migration Safety Features
1. **Check Before Insert**: Migration checks if Programs table has any data
2. **Skip If Populated**: If `COUNT(*) > 0`, migration skips insertion
3. **Safe to Re-run**: Running `alembic upgrade head` multiple times is safe
4. **Rollback Support**: Downgrade removes seeded programs by `program_url`

### Re-seeding (If Needed)
If you need to re-seed the table:

```bash
# 1. Downgrade to remove seeded data
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic downgrade -1

# 2. Re-run upgrade to seed again
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

Or manually clear the table:
```bash
docker exec -it noapplai_postgres psql -U noapplai_user -d noapplai_db -c "TRUNCATE TABLE programs CASCADE;"
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

---

## Frontend Integration

### API Endpoint
Once seeded, programs are available at:
```
GET http://localhost:8000/api/v1/programs/
```

### Testing the API
```bash
# Test with curl
curl http://localhost:8000/api/v1/programs/ | jq '.[0]'

# Expected response (first program):
{
  "id": "uuid-here",
  "university_name": "Technical University of Munich",
  "program_name": "Information on enrollment as a Practical Project Student at TUM - TUM Global",
  "degree_type": null,
  "country": "Germany",
  "program_url": "https://www.international.tum.de/en/global/comingtotum/research-stays-for-students/practical-project-students/",
  "deadline": null,
  "description": null,
  ...
}
```

### Frontend Update
The frontend at `full_page_integrated.html` can now fetch real data:

```javascript
// In programs page section (around line 1600-1700)
async function loadPrograms() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/programs/');
        const programs = await response.json();
        // Display programs in UI
        renderPrograms(programs);
    } catch (error) {
        console.error('Failed to load programs:', error);
    }
}
```

---

## Troubleshooting

### Issue: Docker not running
**Error**: `Cannot connect to the Docker daemon`

**Solution**:
1. Open Docker Desktop application
2. Wait for Docker to fully start
3. Verify: `docker ps` should work without errors

### Issue: Port 5432 already in use
**Error**: `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Solution**:
```bash
# Find process using port 5432
lsof -i :5432

# Stop it or change docker-compose.yml ports to 5433:5432
```

### Issue: Migration fails - "relation programs does not exist"
**Error**: `ProgrammingError: relation "programs" does not exist`

**Solution**: Run initial schema migrations first:
```bash
# Check migration history
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic history

# Run all migrations
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

### Issue: "Programs table already contains X records"
**Message**: `Programs table already contains 34 records. Skipping seed data.`

**Status**: ✅ This is normal! Migration is idempotent and won't duplicate data.

### Issue: Connection refused to localhost:5432
**Error**: `Connection refused` or `OSError: Connect call failed`

**Solution**:
```bash
# Check if containers are running
docker compose ps

# If not running, start them
cd /Users/elnurimamaliyev/NoApplAI/backend
docker compose up -d

# Wait 10 seconds, then retry migration
sleep 10
/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic upgrade head
```

---

## Verification Checklist

After seeding, verify everything works:

- [ ] Docker containers running: `docker compose ps`
- [ ] Database has 34 programs: `docker exec -it noapplai_postgres psql -U noapplai_user -d noapplai_db -c "SELECT COUNT(*) FROM programs;"`
- [ ] API returns programs: `curl http://localhost:8000/api/v1/programs/ | jq 'length'`
- [ ] API docs accessible: Open `http://localhost:8000/docs` in browser
- [ ] No errors in backend logs: `docker compose logs backend | tail -20`

---

## Files Created/Modified

1. **Migration File**: `backend/alembic/versions/2025_12_01_seed_programs_data.py`
   - Alembic migration for seeding programs
   - Safe, idempotent, with rollback support

2. **Seed Data**: `backend/programs_seed_data.json`
   - 34 cleaned academic programs
   - Ready for database insertion

3. **Setup Script**: `backend/setup_and_seed.sh`
   - Automated setup and seeding
   - One-command execution

4. **Verification Script**: `backend/verify_programs.py`
   - Check seeded data
   - Display program statistics

5. **Guide**: `backend/SEEDING_GUIDE.md` (this file)
   - Complete documentation
   - Step-by-step instructions

---

## Next Steps

After successful seeding:

1. ✅ Mark todo item complete: **🔴 P1: Add Programs Seed Data**
2. 🔜 **P1: Connect Frontend Programs Page to API**
   - Update `full_page_integrated.html` to fetch from API
   - Replace hardcoded data with real programs
3. 🔜 **P1: Connect Frontend Applications Page to API**
   - Users can now create applications (programs available!)

---

## Support

If you encounter issues not covered in this guide:

1. Check Docker logs: `docker compose logs`
2. Check Alembic history: `/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic history`
3. Verify database connection in `backend/app/core/config.py`
4. Check `backend/.env` for correct DATABASE_URL

---

**Last Updated**: December 1, 2025
**Migration ID**: `seed_programs_001`
**Data Version**: Cleaned dataset (34 programs)
