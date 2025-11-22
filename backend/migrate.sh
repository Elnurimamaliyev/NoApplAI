#!/bin/bash

# Database Migration Script

set -e

echo "🗄️  Running Database Migrations..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if backend container is running
if ! docker compose ps backend | grep -q "Up"; then
    echo "❌ Backend container is not running. Start it with ./start.sh first."
    exit 1
fi

# Create initial migration
echo "📝 Creating initial migration..."
docker compose exec backend alembic revision --autogenerate -m "Initial schema"

# Apply migrations
echo "⬆️  Applying migrations..."
docker compose exec backend alembic upgrade head

echo "✅ Migrations completed successfully!"
