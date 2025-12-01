#!/bin/bash

# NoApplAI Programs Seeding Automation Script
# This script automates the entire process of starting Docker services
# and seeding the Programs table with 34 academic programs.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="/Users/elnurimamaliyev/NoApplAI/.venv/bin/python"
VENV_ALEMBIC="/Users/elnurimamaliyev/NoApplAI/.venv/bin/alembic"
DB_CONTAINER="noapplai_postgres"
DB_USER="noapplai_user"
DB_NAME="noapplai_db"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   NoApplAI Programs Table Seeding Automation${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Step 1: Check if Docker is running
echo -e "${BLUE}[Step 1/6]${NC} Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and try again:"
    echo "  1. Open Docker Desktop application"
    echo "  2. Wait for Docker to fully start (whale icon steady)"
    echo "  3. Run this script again"
    echo ""
    exit 1
fi
print_status "Docker is running"
echo ""

# Step 2: Check if services are already running
echo -e "${BLUE}[Step 2/6]${NC} Checking backend services..."
if docker compose ps | grep -q "noapplai_postgres.*Up"; then
    print_status "Services are already running"
else
    print_info "Starting backend services..."
    docker compose up -d
    print_status "Services started"
fi
echo ""

# Step 3: Wait for PostgreSQL to be ready
echo -e "${BLUE}[Step 3/6]${NC} Waiting for PostgreSQL to be ready..."
MAX_WAIT=30
WAIT_TIME=0
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if docker exec $DB_CONTAINER pg_isready -U $DB_USER -d $DB_NAME > /dev/null 2>&1; then
        print_status "PostgreSQL is ready"
        break
    fi
    echo -n "."
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
done

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    print_error "PostgreSQL failed to start within ${MAX_WAIT} seconds"
    echo ""
    echo "Troubleshooting steps:"
    echo "  docker compose logs postgres"
    exit 1
fi
echo ""

# Step 4: Check current program count
echo -e "${BLUE}[Step 4/6]${NC} Checking Programs table status..."
PROGRAM_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM programs;" 2>/dev/null | xargs || echo "0")

if [ "$PROGRAM_COUNT" != "0" ] && [ "$PROGRAM_COUNT" != "" ]; then
    print_warning "Programs table already contains ${PROGRAM_COUNT} records"
    echo ""
    read -p "Do you want to re-seed the table? This will clear existing data. (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Clearing existing programs..."
        docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE programs CASCADE;" > /dev/null 2>&1
        print_status "Programs table cleared"
    else
        print_info "Skipping seeding (table already populated)"
        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}   Current Status${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "Programs in database: ${PROGRAM_COUNT}"
        echo "API endpoint: http://localhost:8000/api/v1/programs/"
        echo "API docs: http://localhost:8000/docs"
        echo ""
        echo "Test API:"
        echo "  curl http://localhost:8000/api/v1/programs/ | jq 'length'"
        echo ""
        exit 0
    fi
else
    print_status "Programs table is empty (ready for seeding)"
fi
echo ""

# Step 5: Run Alembic migration
echo -e "${BLUE}[Step 5/6]${NC} Running Alembic migration to seed programs..."
cd "$BACKEND_DIR"

if [ ! -f "$VENV_ALEMBIC" ]; then
    print_error "Alembic not found at $VENV_ALEMBIC"
    print_info "Installing requirements..."
    $VENV_PYTHON -m pip install -q -r requirements.txt
fi

print_info "Executing migration..."
$VENV_ALEMBIC upgrade head

echo ""

# Step 6: Verify seeding
echo -e "${BLUE}[Step 6/6]${NC} Verifying seeded data..."
FINAL_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM programs;" | xargs)

if [ "$FINAL_COUNT" == "34" ]; then
    print_status "Successfully seeded ${FINAL_COUNT} programs!"
else
    print_warning "Expected 34 programs, found ${FINAL_COUNT}"
fi
echo ""

# Display summary
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Seeding Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Get program statistics
echo -e "${BLUE}Program Statistics:${NC}"
echo ""

# Count by degree type
echo "By Degree Type:"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "
    SELECT 
        COALESCE(degree_type, 'Unspecified') as degree_type,
        COUNT(*) as count
    FROM programs 
    GROUP BY degree_type 
    ORDER BY count DESC;" | head -10

echo ""

# Count by country
echo "By Country:"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "
    SELECT 
        COALESCE(country, 'Unspecified') as country,
        COUNT(*) as count
    FROM programs 
    GROUP BY country 
    ORDER BY count DESC;" | head -10

echo ""
echo -e "${BLUE}API Access:${NC}"
echo "  Backend API: http://localhost:8000"
echo "  Programs endpoint: http://localhost:8000/api/v1/programs/"
echo "  API documentation: http://localhost:8000/docs"
echo ""

echo -e "${BLUE}Test Commands:${NC}"
echo "  # Get all programs"
echo "  curl http://localhost:8000/api/v1/programs/"
echo ""
echo "  # Count programs"
echo "  curl http://localhost:8000/api/v1/programs/ | jq 'length'"
echo ""
echo "  # Get first program"
echo "  curl http://localhost:8000/api/v1/programs/ | jq '.[0]'"
echo ""

echo -e "${BLUE}Docker Commands:${NC}"
echo "  # View logs"
echo "  docker compose logs -f backend"
echo ""
echo "  # Stop services"
echo "  docker compose down"
echo ""
echo "  # Restart services"
echo "  docker compose restart"
echo ""

echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ All steps completed successfully!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
