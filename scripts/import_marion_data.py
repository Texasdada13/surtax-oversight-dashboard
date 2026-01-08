"""
Marion County Financial Data Import Script

This script imports expenditure and revenue data from Marion County Excel files
and creates summary financial reports for the oversight dashboard.
"""

import pandas as pd
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Paths
DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'
MARION_DATA = Path(__file__).parent.parent / 'data' / 'marion_county'
EXPENDITURES_FILE = MARION_DATA / 'marion_expenditures.xlsx'
REVENUES_FILE = MARION_DATA / 'marion_revenues.xlsx'

def create_financial_tables():
    """Create tables for financial summary data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create expenditures summary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenditures_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_code TEXT,
            account_name TEXT,
            general_fund REAL DEFAULT 0,
            special_revenue REAL DEFAULT 0,
            debt_service REAL DEFAULT 0,
            capital_projects REAL DEFAULT 0,
            enterprise REAL DEFAULT 0,
            internal_service REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            per_capita REAL DEFAULT 0,
            fiscal_year TEXT,
            imported_date DATETIME,
            data_source TEXT DEFAULT 'Marion County Excel Import'
        )
    ''')

    # Create revenues summary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenues_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_code TEXT,
            account_name TEXT,
            general_fund REAL DEFAULT 0,
            special_revenue REAL DEFAULT 0,
            debt_service REAL DEFAULT 0,
            capital_projects REAL DEFAULT 0,
            enterprise REAL DEFAULT 0,
            internal_service REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            per_capita REAL DEFAULT 0,
            fiscal_year TEXT,
            imported_date DATETIME,
            data_source TEXT DEFAULT 'Marion County Excel Import'
        )
    ''')

    conn.commit()
    conn.close()
    print('[OK] Financial tables created')

def parse_expenditures(file_path):
    """Parse Marion County expenditures Excel file"""
    print(f'\n[INFO] Parsing expenditures from {file_path}...')

    # Read Excel with proper header row
    df = pd.read_excel(file_path, skiprows=2)

    # Clean up column names
    df.columns = [
        'account_name', 'account_code', 'description',
        'general', 'special_revenue', 'debt_service', 'capital_projects', 'permanent',
        'enterprise', 'internal_service', 'custodial', 'pension', 'trust',
        'private_purpose', 'component_units', 'total', 'per_capita'
    ]

    # Remove header row and NaN rows
    df = df[df['account_code'].notna()]
    df = df[df['account_code'].apply(lambda x: str(x).replace('.0', '').replace('.', '').isdigit())]

    # Convert numeric columns
    numeric_cols = ['general', 'special_revenue', 'debt_service', 'capital_projects',
                    'enterprise', 'internal_service', 'total', 'per_capita']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    print(f'[OK] Parsed {len(df)} expenditure records')
    return df

def parse_revenues(file_path):
    """Parse Marion County revenues Excel file"""
    print(f'\n[INFO] Parsing revenues from {file_path}...')

    # Read Excel with proper header row
    df = pd.read_excel(file_path, skiprows=2)

    # Clean up column names
    df.columns = [
        'account_name', 'account_code', 'description',
        'general', 'special_revenue', 'debt_service', 'capital_projects', 'permanent',
        'enterprise', 'internal_service', 'custodial', 'pension', 'trust',
        'private_purpose', 'component_units', 'total', 'per_capita'
    ]

    # Remove header row and NaN rows
    df = df[df['account_code'].notna()]
    df = df[df['account_code'].apply(lambda x: str(x).replace('.0', '').replace('.', '').isdigit() if isinstance(x, (int, float, str)) else False)]

    # Convert numeric columns
    numeric_cols = ['general', 'special_revenue', 'debt_service', 'capital_projects',
                    'enterprise', 'internal_service', 'total', 'per_capita']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    print(f'[OK] Parsed {len(df)} revenue records')
    return df

def import_to_database(df, table_name, fiscal_year='2024'):
    """Import DataFrame to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data for this fiscal year
    cursor.execute(f'DELETE FROM {table_name} WHERE fiscal_year = ?', (fiscal_year,))
    print(f'[INFO] Cleared existing {fiscal_year} data from {table_name}')

    imported_count = 0
    for _, row in df.iterrows():
        cursor.execute(f'''
            INSERT INTO {table_name} (
                account_code, account_name, general_fund, special_revenue,
                debt_service, capital_projects, enterprise, internal_service,
                total_amount, per_capita, fiscal_year, imported_date, data_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(row['account_code']).replace('.0', ''),
            row['description'],
            float(row['general']),
            float(row['special_revenue']),
            float(row['debt_service']),
            float(row['capital_projects']),
            float(row['enterprise']),
            float(row['internal_service']),
            float(row['total']),
            float(row['per_capita']),
            fiscal_year,
            datetime.now(),
            'Marion County Excel Import'
        ))
        imported_count += 1

    conn.commit()
    conn.close()
    print(f'[OK] Imported {imported_count} records to {table_name}')

def generate_summary_report():
    """Generate summary statistics from imported data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print('\n' + '='*80)
    print('IMPORT SUMMARY REPORT')
    print('='*80)

    # Expenditures summary
    cursor.execute('SELECT COUNT(*), SUM(total_amount) FROM expenditures_summary')
    exp_count, exp_total = cursor.fetchone()
    print(f'\nExpenditures:')
    print(f'  Records: {exp_count}')
    print(f'  Total: ${exp_total:,.2f}')

    # Top 5 expenditure categories
    cursor.execute('''
        SELECT account_name, total_amount
        FROM expenditures_summary
        ORDER BY total_amount DESC
        LIMIT 5
    ''')
    print(f'\n  Top 5 Expenditure Categories:')
    for name, amount in cursor.fetchall():
        print(f'    - {name}: ${amount:,.2f}')

    # Revenues summary
    cursor.execute('SELECT COUNT(*), SUM(total_amount) FROM revenues_summary')
    rev_count, rev_total = cursor.fetchone()
    print(f'\nRevenues:')
    print(f'  Records: {rev_count}')
    print(f'  Total: ${rev_total:,.2f}')

    # Top 5 revenue sources
    cursor.execute('''
        SELECT account_name, total_amount
        FROM revenues_summary
        ORDER BY total_amount DESC
        LIMIT 5
    ''')
    print(f'\n  Top 5 Revenue Sources:')
    for name, amount in cursor.fetchall():
        print(f'    - {name}: ${amount:,.2f}')

    # Net position
    net = rev_total - exp_total
    print(f'\nNet Position: ${net:,.2f}')
    print(f'Budget Balance: {(net/rev_total*100):.1f}%')

    conn.close()

def main():
    print('='*80)
    print('MARION COUNTY FINANCIAL DATA IMPORT')
    print('='*80)

    # Check if files exist
    if not EXPENDITURES_FILE.exists():
        print(f'[ERROR] File not found: {EXPENDITURES_FILE}')
        return
    if not REVENUES_FILE.exists():
        print(f'[ERROR] File not found: {REVENUES_FILE}')
        return

    # Create tables
    create_financial_tables()

    # Parse Excel files
    expenditures_df = parse_expenditures(EXPENDITURES_FILE)
    revenues_df = parse_revenues(REVENUES_FILE)

    # Import to database
    import_to_database(expenditures_df, 'expenditures_summary', fiscal_year='2024')
    import_to_database(revenues_df, 'revenues_summary', fiscal_year='2024')

    # Generate summary report
    generate_summary_report()

    print('\n[OK] Import complete!')
    print('='*80)

if __name__ == '__main__':
    main()
