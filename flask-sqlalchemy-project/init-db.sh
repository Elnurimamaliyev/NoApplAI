#!/bin/bash
# Database initialization script

set -e

# Create test database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE flask_app_test;
    GRANT ALL PRIVILEGES ON DATABASE flask_app_test TO $POSTGRES_USER;
EOSQL

echo "Test database created successfully"
