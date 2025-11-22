#!/bin/bash

# NoApplAI Backend Startup Script

set -e

echo "🚀 Starting NoApplAI Backend Services..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Start all services
echo "📦 Starting Docker containers..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check container status
echo ""
echo "📊 Container Status:"
docker compose ps

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Available endpoints:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - MinIO Console: http://localhost:9001"
echo "   - Celery Flower: http://localhost:5555"
echo ""
echo "📝 Useful commands:"
echo "   - View logs: docker compose logs -f"
echo "   - View backend logs: docker compose logs -f backend"
echo "   - Stop services: docker compose down"
echo "   - Restart: docker compose restart"
echo ""
