#!/usr/bin/env python3
"""
Standalone script to seed Programs table with real academic program data.
This script connects directly to the database and populates the Programs table
if it is currently empty.

Usage:
    python seed_programs.py
"""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
import sys

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.program import Program
from app.core.config import settings


async def seed_programs():
    """
    Seed the programs table with real academic program data.
    Only inserts data if the table is currently empty.
    """
    # Create synchronous engine for direct database access
    sync_db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    engine = create_engine(sync_db_url, echo=True)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if programs table already has data
        result = session.execute(text("SELECT COUNT(*) FROM programs"))
        count = result.scalar()
        
        if count > 0:
            print(f"\n✅ Programs table already contains {count} records. Skipping seed data.\n")
            return
        
        # Load seed data from JSON file
        json_path = Path(__file__).parent / "programs_seed_data.json"
        
        if not json_path.exists():
            print(f"\n❌ Seed data file not found at {json_path}\n")
            return
        
        with open(json_path, 'r', encoding='utf-8') as f:
            seed_data = json.load(f)
        
        print(f"\n📊 Loading {len(seed_data)} programs into database...\n")
        
        # Insert each program
        inserted_count = 0
        errors = []
        
        for idx, program in enumerate(seed_data, 1):
            try:
                # Generate UUID for program
                program_id = str(uuid.uuid4())
                now = datetime.utcnow()
                
                # Skip programs without required fields
                if not program.get('university'):
                    print(f"✗ [{idx}/{len(seed_data)}] Skipped (no university): {program.get('title')[:60]}...")
                    continue
                
                # Prepare required_documents as JSON if requirements exists
                required_docs = None
                if program.get('requirements'):
                    required_docs = [program['requirements']]
                
                # Use defaults for required NOT NULL fields
                degree_type = program.get('degree_type') or 'Other'
                country = program.get('country') or 'Not Specified'
                
                # Map JSON fields to database columns
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
                
                session.execute(insert_query, {
                    'id': program_id,
                    'university_name': program.get('university'),
                    'program_name': program.get('title'),
                    'degree_type': degree_type,
                    'country': country,
                    'program_url': program.get('program_url'),
                    'deadline': program.get('deadline'),
                    'description': program.get('description'),
                    'required_documents': json.dumps(required_docs) if required_docs else None,
                    'created_at': now,
                    'updated_at': now
                })
                
                inserted_count += 1
                print(f"✓ [{idx}/{len(seed_data)}] Inserted: {program.get('title')[:60]}...")
                
            except Exception as e:
                error_msg = f"✗ [{idx}/{len(seed_data)}] Error inserting '{program.get('title')}': {str(e)}"
                errors.append(error_msg)
                print(error_msg)
                continue
        
        # Commit all changes
        session.commit()
        
        print(f"\n{'='*80}")
        print(f"✅ Successfully inserted {inserted_count} programs into database!")
        
        if errors:
            print(f"\n⚠️  {len(errors)} errors occurred:")
            for error in errors:
                print(f"   {error}")
        
        print(f"{'='*80}\n")
        
        # Verify the data
        result = session.execute(text("SELECT COUNT(*) FROM programs"))
        final_count = result.scalar()
        print(f"📊 Programs table now contains {final_count} records.\n")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}\n")
        session.rollback()
        raise
    finally:
        session.close()


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("NoApplAI Programs Seeding Script")
    print("="*80 + "\n")
    
    try:
        # Run the async seeding function
        asyncio.run(seed_programs())
        print("✅ Seeding completed successfully!\n")
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Seeding interrupted by user.\n")
        return 1
    except Exception as e:
        print(f"\n❌ Seeding failed: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
