"""
Marion County Capital Projects Import Script

This script imports real capital construction projects from Marion County Public Schools
including new school construction and major facility improvements.

Data sources: News articles, MCPS facilities department, public records
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Paths
DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

def create_capital_projects_table():
    """Create table for capital construction projects"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capital_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT UNIQUE,
            project_name TEXT NOT NULL,
            project_type TEXT,
            location TEXT,
            address TEXT,
            budget_amount REAL,
            spent_to_date REAL DEFAULT 0,
            start_date DATE,
            estimated_completion DATE,
            actual_completion DATE,
            status TEXT,
            capacity INTEGER,
            square_footage INTEGER,
            num_classrooms INTEGER,
            num_labs INTEGER,
            contractor TEXT,
            construction_manager TEXT,
            cm_contract_amount REAL,
            description TEXT,
            data_source TEXT,
            source_url TEXT,
            imported_date DATETIME,
            last_updated DATETIME
        )
    ''')

    conn.commit()
    conn.close()
    print('[OK] Capital projects table created')

def import_projects():
    """Import verified capital projects from research"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    projects = [
        {
            'project_code': 'HS-CCC',
            'project_name': 'New High School CCC',
            'project_type': 'New Construction',
            'location': 'South Ocala',
            'address': '1350 SW 165th Street, Ocala, FL',
            'budget_amount': 154000000,  # $154M as of Dec 2024
            'spent_to_date': 0,
            'start_date': '2024-12-01',
            'estimated_completion': '2026-08-01',
            'status': 'Under Construction',
            'capacity': 2000,
            'square_footage': None,
            'num_classrooms': 61,
            'num_labs': 20,
            'contractor': 'TBD',
            'construction_manager': 'Wharton-Smith, Inc.',
            'cm_contract_amount': 5575000,  # $5.575M
            'description': 'New high school in south Ocala with 3 building complexes, 61 classrooms, and 20 labs. Capacity for over 2,000 students. Groundbreaking December 2024, opening August 2026.',
            'data_source': 'Ocala-News.com, Marion County School Board',
            'source_url': 'https://www.ocala-news.com/2024/12/17/marion-officials-break-ground-on-new-154-million-high-school-in-south-ocala/'
        },
        {
            'project_code': 'MS-DD',
            'project_name': 'New Middle School DD',
            'project_type': 'New Construction',
            'location': 'Silver Springs Shores',
            'address': None,
            'budget_amount': None,  # Total construction cost TBD
            'spent_to_date': 0,
            'start_date': '2024-06-25',
            'estimated_completion': None,
            'status': 'Planning/Design',
            'capacity': None,
            'square_footage': None,
            'num_classrooms': None,
            'num_labs': None,
            'contractor': 'TBD',
            'construction_manager': 'Skanska USA Building, Inc.',
            'cm_contract_amount': 2150000,  # $2.15M ($2M CM + $150K pre-construction)
            'description': 'New middle school to replace Lake Weir Middle School in Silver Springs Shores. Construction expected to take 18-24 months. Construction manager pre-qualified June 2024. Total construction cost pending guaranteed maximum price determination.',
            'data_source': 'Marion County Public Schools Facilities Department',
            'source_url': 'https://www.marionschools.net/departments/facilities/new_construction_updates'
        },
        {
            'project_code': 'OMS-GYM',
            'project_name': 'Osceola Middle School Gymnasium',
            'project_type': 'Addition/Expansion',
            'location': 'Osceola Middle School',
            'address': None,
            'budget_amount': None,
            'spent_to_date': 0,
            'start_date': None,
            'estimated_completion': None,
            'status': 'Under Construction',
            'capacity': None,
            'square_footage': None,
            'num_classrooms': None,
            'num_labs': None,
            'contractor': 'TBD',
            'construction_manager': None,
            'cm_contract_amount': None,
            'description': 'New gymnasium facility addition at Osceola Middle School. Construction photos and renderings available on MCPS facilities website.',
            'data_source': 'Marion County Public Schools Facilities Department',
            'source_url': 'https://www.marionschools.net/departments/facilities/new_construction_updates/osceola_middle_school_gymnasium_renderings'
        }
    ]

    imported_count = 0
    for project in projects:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO capital_projects (
                    project_code, project_name, project_type, location, address,
                    budget_amount, spent_to_date, start_date, estimated_completion,
                    status, capacity, square_footage, num_classrooms, num_labs,
                    contractor, construction_manager, cm_contract_amount,
                    description, data_source, source_url, imported_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project['project_code'],
                project['project_name'],
                project['project_type'],
                project['location'],
                project['address'],
                project['budget_amount'],
                project['spent_to_date'],
                project['start_date'],
                project['estimated_completion'],
                project['status'],
                project['capacity'],
                project['square_footage'],
                project['num_classrooms'],
                project['num_labs'],
                project['contractor'],
                project['construction_manager'],
                project['cm_contract_amount'],
                project['description'],
                project['data_source'],
                project['source_url'],
                datetime.now(),
                datetime.now()
            ))
            imported_count += 1
            print(f'[OK] Imported: {project["project_name"]}')
        except Exception as e:
            print(f'[ERROR] Failed to import {project["project_name"]}: {e}')

    conn.commit()
    conn.close()
    print(f'\n[OK] Imported {imported_count} capital projects')

def generate_summary_report():
    """Generate summary statistics from imported projects"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print('\n' + '='*80)
    print('CAPITAL PROJECTS IMPORT SUMMARY')
    print('='*80)

    # Total projects
    cursor.execute('SELECT COUNT(*) FROM capital_projects')
    total_count = cursor.fetchone()[0]
    print(f'\nTotal Projects: {total_count}')

    # Projects by status
    cursor.execute('''
        SELECT status, COUNT(*)
        FROM capital_projects
        GROUP BY status
    ''')
    print('\nProjects by Status:')
    for status, count in cursor.fetchall():
        print(f'  {status}: {count}')

    # Total budget (known projects only)
    cursor.execute('''
        SELECT
            SUM(budget_amount) as total_budget,
            SUM(cm_contract_amount) as total_cm_fees
        FROM capital_projects
        WHERE budget_amount IS NOT NULL OR cm_contract_amount IS NOT NULL
    ''')
    result = cursor.fetchone()
    total_budget = result[0] or 0
    total_cm = result[1] or 0

    print(f'\nTotal Known Budget: ${total_budget:,.0f}')
    print(f'Total CM Fees: ${total_cm:,.0f}')

    # Project details
    cursor.execute('''
        SELECT
            project_name,
            project_type,
            COALESCE(budget_amount, 0) as budget,
            status,
            estimated_completion
        FROM capital_projects
        ORDER BY budget_amount DESC NULLS LAST
    ''')
    print('\nProject Details:')
    for name, ptype, budget, status, completion in cursor.fetchall():
        budget_str = f'${budget:,.0f}' if budget > 0 else 'TBD'
        completion_str = completion if completion else 'TBD'
        print(f'  - {name}')
        print(f'    Type: {ptype} | Budget: {budget_str} | Status: {status}')
        print(f'    Completion: {completion_str}')

    conn.close()

def main():
    print('='*80)
    print('MARION COUNTY CAPITAL PROJECTS IMPORT')
    print('='*80)

    # Create table
    create_capital_projects_table()

    # Import projects
    import_projects()

    # Generate summary report
    generate_summary_report()

    print('\n[OK] Import complete!')
    print('='*80)

if __name__ == '__main__':
    main()
