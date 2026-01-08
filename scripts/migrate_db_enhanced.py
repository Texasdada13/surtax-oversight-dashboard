"""
Database migration script to add enhanced project tracking fields.
Run this to upgrade the database schema for the enhanced project detail page.
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

def migrate():
    """Apply database migrations for enhanced project tracking."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Starting database migration...")

    try:
        # Add new fields to contracts table
        print("Adding new columns to contracts table...")

        new_columns = [
            ("project_purpose", "TEXT"),
            ("project_scope", "TEXT"),
            ("community_impact", "TEXT"),
            ("priority_level", "TEXT"),
            ("risk_score", "TEXT"),
            ("funding_sources", "TEXT"),  # Store as JSON string
            ("contingency_remaining", "DECIMAL"),
            ("cost_per_sqft", "DECIMAL"),
            ("square_footage", "INTEGER"),
        ]

        for col_name, col_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE contracts ADD COLUMN {col_name} {col_type}")
                print(f"  [OK] Added {col_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"  [SKIP] {col_name} already exists, skipping")
                else:
                    raise

        # Create project_phases table
        print("\nCreating project_phases table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_phases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                phase_name TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                status TEXT,
                percent_complete DECIMAL,
                FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
            )
        """)
        print("  [OK] project_phases table created")

        # Create contractor_performance table
        print("\nCreating contractor_performance table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contractor_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id TEXT NOT NULL,
                safety_record TEXT,
                quality_score DECIMAL,
                past_projects_count INTEGER,
                deficiency_rate DECIMAL,
                local_hiring_percent DECIMAL,
                FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
            )
        """)
        print("  [OK] contractor_performance table created")

        # Create inspection_log table
        print("\nCreating inspection_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inspection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                inspection_date DATE NOT NULL,
                inspector_name TEXT,
                findings TEXT,
                deficiencies_count INTEGER DEFAULT 0,
                status TEXT,
                FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
            )
        """)
        print("  [OK] inspection_log table created")

        # Create community_engagement table
        print("\nCreating community_engagement table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS community_engagement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                meeting_date DATE NOT NULL,
                attendees INTEGER,
                feedback_summary TEXT,
                concerns_raised TEXT,
                FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
            )
        """)
        print("  [OK] community_engagement table created")

        # Create committee_actions table
        print("\nCreating committee_actions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS committee_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                meeting_date DATE NOT NULL,
                action_item TEXT NOT NULL,
                assigned_to TEXT,
                status TEXT DEFAULT 'Pending',
                due_date DATE,
                FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
            )
        """)
        print("  [OK] committee_actions table created")

        conn.commit()
        print("\n[SUCCESS] Migration completed successfully!")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
