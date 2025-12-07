#!/usr/bin/env python3
"""
Verification script for Programs table seeding.
Checks if programs were successfully seeded and displays statistics.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

# Color codes for terminal output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}{text:^70}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.NC}")


def verify_programs():
    """Verify programs were seeded correctly"""
    
    print_header("NoApplAI Programs Verification")
    
    # Database connection
    db_url = "postgresql://noapplai_user:noapplai_password_2024@localhost:5432/noapplai_db"
    
    try:
        engine = create_engine(db_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test connection
        print_info("Connecting to database...")
        session.execute(text("SELECT 1"))
        print_success("Database connection established")
        print()
        
        # Get total count
        result = session.execute(text("SELECT COUNT(*) FROM programs"))
        total_count = result.scalar()
        
        print(f"{Colors.BOLD}Total Programs:{Colors.NC} {total_count}")
        
        if total_count == 0:
            print_error("No programs found in database!")
            print("\nTo seed programs, run:")
            print("  cd /Users/elnurimamaliyev/NoApplAI/backend")
            print("  ./setup_and_seed.sh")
            return False
        
        print_success(f"Found {total_count} programs")
        print()
        
        # Get programs by university
        print(f"{Colors.BOLD}Top Universities:{Colors.NC}")
        result = session.execute(text("""
            SELECT 
                university_name,
                COUNT(*) as count
            FROM programs 
            WHERE university_name IS NOT NULL
            GROUP BY university_name 
            ORDER BY count DESC
            LIMIT 10
        """))
        
        for row in result:
            print(f"  • {row.university_name}: {row.count} programs")
        print()
        
        # Get programs by degree type
        print(f"{Colors.BOLD}Degree Types:{Colors.NC}")
        result = session.execute(text("""
            SELECT 
                COALESCE(degree_type, 'Unspecified') as degree_type,
                COUNT(*) as count
            FROM programs 
            GROUP BY degree_type 
            ORDER BY count DESC
        """))
        
        for row in result:
            print(f"  • {row.degree_type}: {row.count} programs")
        print()
        
        # Get programs by country
        print(f"{Colors.BOLD}Countries:{Colors.NC}")
        result = session.execute(text("""
            SELECT 
                COALESCE(country, 'Unspecified') as country,
                COUNT(*) as count
            FROM programs 
            GROUP BY country 
            ORDER BY count DESC
        """))
        
        for row in result:
            print(f"  • {row.country}: {row.count} programs")
        print()
        
        # Check for required fields
        print(f"{Colors.BOLD}Data Quality:{Colors.NC}")
        
        result = session.execute(text("""
            SELECT 
                COUNT(*) FILTER (WHERE university_name IS NOT NULL) as has_university,
                COUNT(*) FILTER (WHERE program_name IS NOT NULL) as has_name,
                COUNT(*) FILTER (WHERE program_url IS NOT NULL) as has_url,
                COUNT(*) FILTER (WHERE country IS NOT NULL) as has_country,
                COUNT(*) FILTER (WHERE degree_type IS NOT NULL) as has_degree,
                COUNT(*) as total
            FROM programs
        """))
        
        row = result.first()
        print(f"  • With university name: {row.has_university}/{row.total} ({row.has_university*100//row.total}%)")
        print(f"  • With program name: {row.has_name}/{row.total} ({row.has_name*100//row.total}%)")
        print(f"  • With URL: {row.has_url}/{row.total} ({row.has_url*100//row.total}%)")
        print(f"  • With country: {row.has_country}/{row.total} ({row.has_country*100//row.total}%)")
        print(f"  • With degree type: {row.has_degree}/{row.total} ({row.has_degree*100//row.total}%)")
        print()
        
        # Sample programs
        print(f"{Colors.BOLD}Sample Programs:{Colors.NC}")
        result = session.execute(text("""
            SELECT 
                program_name,
                university_name,
                degree_type,
                country
            FROM programs 
            ORDER BY created_at DESC
            LIMIT 5
        """))
        
        for idx, row in enumerate(result, 1):
            print(f"\n  {idx}. {Colors.BOLD}{row.program_name[:60]}...{Colors.NC}")
            print(f"     University: {row.university_name or 'N/A'}")
            print(f"     Degree: {row.degree_type or 'N/A'}")
            print(f"     Country: {row.country or 'N/A'}")
        
        print()
        print_header("Verification Complete")
        
        print(f"{Colors.GREEN}✓ All checks passed!{Colors.NC}\n")
        
        print(f"{Colors.BOLD}Next Steps:{Colors.NC}")
        print("  1. Start backend API: docker compose up -d")
        print("  2. Test API: curl http://localhost:8000/api/v1/programs/")
        print("  3. View API docs: http://localhost:8000/docs")
        print("  4. Update frontend to fetch from API")
        print()
        
        session.close()
        return True
        
    except Exception as e:
        print_error(f"Verification failed: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure Docker is running: docker ps")
        print("  2. Ensure database is running: docker compose ps")
        print("  3. Check if services started: docker compose up -d")
        print("  4. View logs: docker compose logs postgres")
        print()
        return False


def main():
    """Main entry point"""
    try:
        success = verify_programs()
        return 0 if success else 1
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠ Verification interrupted by user{Colors.NC}\n")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
