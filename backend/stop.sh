#!/bin/bash

# NoApplAI Backend Stop Script

set -e

echo "🛑 Stopping NoApplAI Backend Services..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Stop all services
docker compose down

echo "✅ All services stopped successfully!"
