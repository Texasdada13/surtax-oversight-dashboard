"""
Import and enrich data from Marion County Excel files.
This script reads marion_expenditures.xlsx and updates the surtax projects.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import json

# Paths
DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'
MARION_DATA = Path(__file__).parent.parent.parent / 'contract-oversight-system' / 'data' / 'marion_county'
EXPENDITURES_FILE = MARION_DATA / 'marion_expenditures.xlsx'

def import_marion_expenditures():
    """Import Marion County expenditure data."""
    if not EXPENDITURES_FILE.exists():
        print(f"[ERROR] File not found: {EXPENDITURES_FILE}")
        print("Please ensure marion_expenditures.xlsx exists in the marion_county folder")
        return

    print(f"Reading Excel file: {EXPENDITURES_FILE}")

    try:
        # Read Excel file
        df = pd.read_excel(EXPENDITURES_FILE)
        print(f"[OK] Loaded {len(df)} rows from Excel file")
        print(f"\nColumns found: {list(df.columns)}\n")

        # Display first few rows to understand structure
        print("First 3 rows:")
        print(df.head(3).to_string())
        print("\n")

        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get existing surtax projects
        cursor.execute("""
            SELECT contract_id, title, school_name, surtax_category, current_amount
            FROM contracts
            WHERE surtax_category IS NOT NULL
            LIMIT 10
        """)

        print("\nExisting surtax projects (first 10):")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]} at {row[2]} (${row[4]:,.0f})")

        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("\n1. Review the Excel columns above")
        print("2. Review the existing database projects above")
        print("3. Identify which Excel columns map to which database fields")
        print("4. Update this script to perform the actual mapping")
        print("\nCommon mappings to look for:")
        print("  - Project name/title columns")
        print("  - School name columns")
        print("  - Budget/amount columns")
        print("  - Category columns")
        print("  - Status columns")
        print("  - Date columns (start, end)")

        conn.close()

    except Exception as e:
        print(f"[ERROR] Failed to read Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Marion County Data Import Tool")
    print("="*80)
    import_marion_expenditures()
