"""seed_programs_data

Revision ID: seed_programs_001
Revises: 
Create Date: 2025-12-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
import json
import os
from pathlib import Path
import uuid
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'seed_programs_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Seed the programs table with real academic program data.
    Only inserts data if the table is currently empty.
    """
    # Get database connection
    connection = op.get_bind()
    
    # Check if programs table already has data
    result = connection.execute(text("SELECT COUNT(*) FROM programs"))
    count = result.scalar()
    
    if count > 0:
        print(f"Programs table already contains {count} records. Skipping seed data.")
        return
    
    # Load seed data from JSON file
    backend_dir = Path(__file__).parent.parent.parent
    json_path = backend_dir / "programs_seed_data.json"
    
    if not json_path.exists():
        print(f"Seed data file not found at {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        seed_data = json.load(f)
    
    print(f"Loading {len(seed_data)} programs into database...")
    
    # Prepare insert statement
    insert_query = text("""
        INSERT INTO programs (
            id, university_name, program_name, degree_type, country, 
            program_url, deadline, description, required_documents,
            created_at, updated_at
        ) VALUES (
            :id, :university_name, :program_name, :degree_type, :country,
            :program_url, :deadline, :description, :required_documents,
            :created_at, :updated_at
        )
    """)
    
    # Insert each program
    inserted_count = 0
    for program in seed_data:
        try:
            # Generate UUID for program
            program_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            # Map JSON fields to database columns
            # title -> program_name
            # university -> university_name
            # program_url -> program_url
            # country -> country
            # degree_type -> degree_type
            # requirements -> required_documents (as JSON)
            # description -> description
            
            # Prepare required_documents as JSON if requirements exists
            required_docs = None
            if program.get('requirements'):
                required_docs = json.dumps([program['requirements']])
            
            # Use defaults for required NOT NULL fields
            degree_type = program.get('degree_type') or 'Other'
            country = program.get('country') or 'Not Specified'
            
            connection.execute(insert_query, {
                'id': program_id,
                'university_name': program.get('university'),
                'program_name': program.get('title'),
                'degree_type': degree_type,
                'country': country,
                'program_url': program.get('program_url'),
                'deadline': program.get('deadline'),
                'description': program.get('description'),
                'required_documents': required_docs,
                'created_at': now,
                'updated_at': now
            })
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting program '{program.get('title')}': {str(e)}")
            continue
    
    print(f"Successfully inserted {inserted_count} programs into database.")


def downgrade() -> None:
    """
    Remove seeded programs data.
    This will delete all programs that were inserted by this migration.
    """
    connection = op.get_bind()
    
    # Load seed data to get program URLs (unique identifier)
    backend_dir = Path(__file__).parent.parent.parent
    json_path = backend_dir / "programs_seed_data.json"
    
    if not json_path.exists():
        print(f"Seed data file not found at {json_path}. Cannot downgrade.")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        seed_data = json.load(f)
    
    # Delete programs by matching program_url
    delete_query = text("DELETE FROM programs WHERE program_url = :url")
    
    deleted_count = 0
    for program in seed_data:
        try:
            result = connection.execute(delete_query, {'url': program.get('program_url')})
            deleted_count += result.rowcount
        except Exception as e:
            print(f"Error deleting program '{program.get('title')}': {str(e)}")
            continue
    
    print(f"Successfully deleted {deleted_count} programs from database.")
