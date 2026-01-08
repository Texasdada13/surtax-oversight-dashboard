"""
Import Marion County capital projects from FLDOE 2024-2025 Work Plan

This script extracts capital outlay projects from the official Florida Department
of Education 5-Year Facilities Work Plan for Marion County School District.

Data Source: MARION2025.pdf (FLDOE Official Work Plan)
Approved: 9/24/2024 by Marion County School Board
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

def import_capacity_projects():
    """Import capacity-adding projects from pages 10-12 of work plan"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Projects from "Capacity Project Schedules" section
    capacity_projects = [
        {
            'project_code': 'HARBOR-VIEW-ADD',
            'project_name': 'Harbour View Elementary - 16 Classroom and Cafeteria Addition',
            'project_type': 'Addition/Expansion',
            'location': 'Harbour View Elementary',
            'budget_amount': 14000000,
            'start_date': '2027-07-01',
            'estimated_completion': '2028-06-30',
            'status': 'Planning',
            'capacity': 328,
            'num_classrooms': 16,
            'square_footage': 18960,
            'description': 'New 16 classroom and cafeteria addition to address capacity needs. Will add 328 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': False
        },
        {
            'project_code': 'LIBERTY-MS-ADD',
            'project_name': 'Liberty Middle - 16 Classroom Addition to Replace Portables',
            'project_type': 'Addition/Expansion',
            'location': 'Liberty Middle School',
            'budget_amount': 10230418,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 384,
            'num_classrooms': 16,
            'square_footage': 18000,
            'description': '16 classroom addition to replace portable classrooms. Adds 384 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'OCALA-SPRINGS-ADD',
            'project_name': 'Ocala Springs Elementary - 12 Classroom Addition',
            'project_type': 'Addition/Expansion',
            'location': 'Ocala Springs Elementary',
            'budget_amount': 10500000,
            'start_date': '2027-07-01',
            'estimated_completion': '2028-06-30',
            'status': 'Planning',
            'capacity': 248,
            'num_classrooms': 12,
            'square_footage': 12720,
            'description': '12 classroom addition to replace portable classrooms.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': False
        },
        {
            'project_code': 'MS-DD-NEW',
            'project_name': 'New Middle School DD (Replaces Lake Weir Middle)',
            'project_type': 'New Construction',
            'location': 'Silver Springs Shores',
            'budget_amount': 64329977,
            'start_date': '2024-07-01',
            'estimated_completion': '2026-06-30',
            'status': 'Under Construction',
            'square_footage': 340361,
            'description': 'New middle school to replace Lake Weir Middle School. Total project area 340,361 sq ft (141,000 sq ft in 2024-25, 199,361 sq ft in 2025-26).',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True,
            'construction_manager': 'Skanska USA Building, Inc.',
            'cm_contract_amount': 2150000
        },
        {
            'project_code': 'ELEM-W-SW',
            'project_name': 'New Southwest Elementary School W',
            'project_type': 'New Construction',
            'location': 'Southwest Marion County (Location TBD)',
            'budget_amount': 45233977,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 860,
            'square_footage': 115000,
            'description': 'New elementary school in southwest Marion County. Will provide 860 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'ELEM-X-SW',
            'project_name': 'New Southwest Elementary School X',
            'project_type': 'New Construction',
            'location': 'Southwest Marion County (Location TBD)',
            'budget_amount': 47059418,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 860,
            'square_footage': 115000,
            'description': 'Second new elementary school in southwest Marion County. Will provide 860 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'HORIZON-ADD',
            'project_name': 'Horizon Academy at Marion Oaks - 16 Classroom Building and Cafeteria',
            'project_type': 'Addition/Expansion',
            'location': 'Horizon Academy at Marion Oaks',
            'budget_amount': 7515014,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 328,
            'num_classrooms': 16,
            'square_footage': 18000,
            'description': '16 classroom building and cafeteria addition. Adds 328 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'MTC-AUTO',
            'project_name': 'Marion Technical College - Auto/Diesel/Aviation Building',
            'project_type': 'Addition/Expansion',
            'location': 'Marion Technical College',
            'budget_amount': 5334674,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'square_footage': 16000,
            'description': 'New Auto/Diesel/Aviation Building addition at Marion Technical College.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'HAMMETT-ADD',
            'project_name': 'Hammett Bowen Jr Elementary - 16 Classroom Addition',
            'project_type': 'Addition/Expansion',
            'location': 'Hammett Bowen Jr Elementary',
            'budget_amount': 7814450,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 328,
            'num_classrooms': 16,
            'square_footage': 18000,
            'description': '16 classroom addition to replace portable classrooms. Adds 328 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        },
        {
            'project_code': 'HS-CCC-NEW',
            'project_name': 'New Southwest High School CCC',
            'project_type': 'New Construction',
            'location': 'Southwest Marion County (1350 SW 165th Street, Ocala)',
            'address': '1350 SW 165th Street, Ocala, FL',
            'budget_amount': 135601456,
            'start_date': '2024-12-01',
            'estimated_completion': '2026-08-01',
            'status': 'Under Construction',
            'capacity': 2011,
            'num_classrooms': 108,
            'square_footage': 310000,
            'description': 'New high school in southwest Ocala with capacity for over 2,000 students. 108 classrooms in 310,000 sq ft facility. Groundbreaking December 2024.',
            'data_source': 'FLDOE 2024-2025 Work Plan + Ocala-News.com',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True,
            'construction_manager': 'Wharton-Smith, Inc.',
            'cm_contract_amount': 5575000
        },
        {
            'project_code': 'MARION-OAKS-ADD',
            'project_name': 'Marion Oaks Elementary - 16 Classroom and Cafeteria Addition',
            'project_type': 'Addition/Expansion',
            'location': 'Marion Oaks Elementary School',
            'budget_amount': 7814450,
            'start_date': '2024-07-01',
            'estimated_completion': '2025-06-30',
            'status': 'Under Construction',
            'capacity': 328,
            'num_classrooms': 16,
            'square_footage': 18000,
            'description': '16 classroom and cafeteria addition. Adds 328 student stations.',
            'data_source': 'FLDOE 2024-2025 Work Plan',
            'source_url': 'https://www.fldoe.org/core/fileparse.php/9948/urlt/MARION2025.pdf',
            'funded': True
        }
    ]

    imported = 0
    for project in capacity_projects:
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
                project.get('address'),
                project.get('budget_amount'),
                0,
                project.get('start_date'),
                project.get('estimated_completion'),
                project.get('status'),
                project.get('capacity'),
                project.get('square_footage'),
                project.get('num_classrooms'),
                project.get('num_labs'),
                project.get('contractor'),
                project.get('construction_manager'),
                project.get('cm_contract_amount'),
                project['description'],
                project['data_source'],
                project['source_url'],
                datetime.now(),
                datetime.now()
            ))
            imported += 1
            print(f'[OK] Imported: {project["project_name"]}')
        except Exception as e:
            print(f'[ERROR] Failed to import {project["project_name"]}: {e}')

    conn.commit()
    conn.close()
    return imported

def generate_summary():
    """Generate summary report"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print('\n' + '='*80)
    print('FLDOE WORK PLAN IMPORT SUMMARY')
    print('='*80)

    cursor.execute('SELECT COUNT(*) FROM capital_projects')
    total = cursor.fetchone()[0]
    print(f'\nTotal Capital Projects in Database: {total}')

    cursor.execute('''
        SELECT status, COUNT(*) as count,
               SUM(CASE WHEN budget_amount IS NOT NULL THEN budget_amount ELSE 0 END) as total_budget
        FROM capital_projects
        GROUP BY status
    ''')

    print('\nProjects by Status:')
    for status, count, budget in cursor.fetchall():
        budget_str = f'${budget:,.0f}' if budget > 0 else 'TBD'
        print(f'  {status}: {count} projects ({budget_str})')

    cursor.execute('''
        SELECT SUM(CASE WHEN budget_amount IS NOT NULL THEN budget_amount ELSE 0 END) as total
        FROM capital_projects
    ''')
    total_budget = cursor.fetchone()[0] or 0
    print(f'\nTotal Known Budget: ${total_budget:,.0f}')

    cursor.execute('''
        SELECT SUM(capacity) FROM capital_projects WHERE capacity IS NOT NULL
    ''')
    total_capacity = cursor.fetchone()[0] or 0
    print(f'Total New Student Capacity: {total_capacity:,} stations')

    conn.close()

def main():
    print('='*80)
    print('IMPORTING MARION COUNTY CAPITAL PROJECTS FROM FLDOE WORK PLAN')
    print('Source: MARION2025.pdf (2024-2025 5-Year Facilities Work Program)')
    print('='*80)

    imported = import_capacity_projects()
    print(f'\n[OK] Imported {imported} projects from FLDOE Work Plan')

    generate_summary()

    print('\n[OK] Import complete!')
    print('='*80)

if __name__ == '__main__':
    main()
