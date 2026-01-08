"""
Add data source tracking to tables.
This allows us to show which data is real vs generated vs needs public records.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

def add_tracking_fields():
    """Add data source tracking fields to tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Adding data source tracking fields...")
    print("="*80)

    # Tables and their tracking fields
    tables_to_update = [
        'contracts',
        'project_phases',
        'inspection_log',
        'community_engagement',
        'committee_actions',
        'contractor_performance'
    ]

    tracking_fields = [
        ('data_source', 'TEXT DEFAULT "Generated"'),  # Generated, Excel Import, Public Records, User Entered, Official
        ('needs_verification', 'INTEGER DEFAULT 1'),  # 0 = verified, 1 = needs verification
        ('last_updated', 'DATETIME'),
        ('updated_by', 'TEXT')
    ]

    for table in tables_to_update:
        print(f"\nUpdating table: {table}")

        for field_name, field_def in tracking_fields:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {field_name} {field_def}")
                print(f"  [OK] Added {field_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"  [SKIP] {field_name} already exists")
                else:
                    print(f"  [ERROR] {e}")

    # Update all existing generated data to mark it as such
    print("\n" + "="*80)
    print("Marking existing data as 'Generated - Needs Public Records'...")

    cursor.execute("""
        UPDATE contracts
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
        WHERE surtax_category IS NOT NULL
        AND project_purpose IS NOT NULL
    """)
    print(f"  [OK] Updated {cursor.rowcount} contracts")

    cursor.execute("""
        UPDATE project_phases
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
    """)
    print(f"  [OK] Updated {cursor.rowcount} project phases")

    cursor.execute("""
        UPDATE inspection_log
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
    """)
    print(f"  [OK] Updated {cursor.rowcount} inspections")

    cursor.execute("""
        UPDATE community_engagement
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
    """)
    print(f"  [OK] Updated {cursor.rowcount} community meetings")

    cursor.execute("""
        UPDATE committee_actions
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
    """)
    print(f"  [OK] Updated {cursor.rowcount} committee actions")

    cursor.execute("""
        UPDATE contractor_performance
        SET data_source = 'Generated - Needs Public Records',
            needs_verification = 1
    """)
    print(f"  [OK] Updated {cursor.rowcount} contractor performance records")

    conn.commit()
    conn.close()

    print("\n[SUCCESS] Data source tracking enabled!")
    print("\nData Source Values:")
    print("  - 'Generated - Needs Public Records' = Algorithmic placeholder")
    print("  - 'Excel Import' = Imported from Marion County Excel files")
    print("  - 'Public Records' = Official documents/records")
    print("  - 'User Entered' = Staff manual entry")
    print("  - 'Official' = Verified official source")

if __name__ == '__main__':
    add_tracking_fields()
