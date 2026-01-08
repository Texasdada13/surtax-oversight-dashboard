"""
Add sample data to demonstrate enhanced project detail features.
This populates the new tables with realistic demo data.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json

# Database path
DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

def add_sample_data():
    """Add sample data to enhanced tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Adding sample data...")

    try:
        # Get a sample contract ID
        cursor.execute("SELECT contract_id FROM contracts LIMIT 1")
        result = cursor.fetchone()

        if not result:
            print("No contracts found in database. Please import contracts first.")
            return

        contract_id = result[0]
        print(f"Using contract ID: {contract_id}")

        # Update sample contract with enhanced fields
        print("\nUpdating contract with enhanced fields...")
        cursor.execute("""
            UPDATE contracts
            SET project_purpose = ?,
                project_scope = ?,
                community_impact = ?,
                priority_level = ?,
                risk_score = ?,
                funding_sources = ?,
                square_footage = ?,
                cost_per_sqft = ?
            WHERE contract_id = ?
        """, (
            "Replace aging HVAC systems to improve indoor air quality and energy efficiency",
            "Complete replacement of 15 rooftop HVAC units including ductwork, controls, and electrical upgrades. Project includes asbestos abatement and roof repairs.",
            "Improved learning environment for 850 students and 65 staff members. Reduced energy costs by estimated 30% annually. Better air quality reduces student sick days.",
            "High",
            "Medium",
            json.dumps({
                "Surtax Revenue": 2500000,
                "State Matching Funds": 500000,
                "Energy Rebates": 150000
            }),
            125000,
            25.20,
            contract_id
        ))
        print(f"  [OK] Updated contract {contract_id}")

        # Add project phases
        print("\nAdding project phases...")
        phases = [
            ("Design & Planning", "2024-01-15", "2024-03-30", "Completed", 100),
            ("Permitting & Approvals", "2024-03-15", "2024-05-15", "Completed", 100),
            ("Asbestos Abatement", "2024-06-01", "2024-07-15", "Completed", 100),
            ("HVAC Installation", "2024-07-20", "2024-11-30", "In Progress", 65),
            ("Controls & Testing", "2024-11-15", "2025-01-31", "Not Started", 0),
            ("Final Inspection & Closeout", "2025-01-15", "2025-02-28", "Not Started", 0),
        ]

        for phase_name, start, end, status, pct in phases:
            cursor.execute("""
                INSERT INTO project_phases (contract_id, phase_name, start_date, end_date, status, percent_complete)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contract_id, phase_name, start, end, status, pct))
        print(f"  [OK] Added {len(phases)} project phases")

        # Add inspection records
        print("\nAdding inspection records...")
        inspections = [
            ("2024-08-15", "James Martinez", "Pre-construction site review completed. All permits in order.", 0, "Passed"),
            ("2024-09-22", "Sarah Johnson", "Phase 1 inspection - HVAC units 1-5 installed per specifications.", 0, "Passed"),
            ("2024-10-18", "James Martinez", "Phase 2 inspection - Minor issues with ductwork sealing on unit 7.", 2, "Conditional"),
            ("2024-11-12", "Sarah Johnson", "Follow-up inspection - Previous deficiencies corrected.", 0, "Passed"),
        ]

        for insp_date, inspector, findings, deficiencies, status in inspections:
            cursor.execute("""
                INSERT INTO inspection_log (contract_id, inspection_date, inspector_name, findings, deficiencies_count, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contract_id, insp_date, inspector, findings, deficiencies, status))
        print(f"  [OK] Added {len(inspections)} inspections")

        # Add community engagement records
        print("\nAdding community engagement records...")
        engagements = [
            ("2024-02-10", 45, "Overwhelmingly positive response to project. Parents expressed relief about improved air quality.", "Concerns about construction noise during school hours"),
            ("2024-06-05", 32, "Update on project timeline and summer construction schedule. Community appreciates transparency.", "Questions about energy savings verification"),
            ("2024-10-15", 28, "Progress update and tour of completed work. Strong support for project continuation.", "Request for similar upgrades at neighboring schools"),
        ]

        for meet_date, attendees, feedback, concerns in engagements:
            cursor.execute("""
                INSERT INTO community_engagement (contract_id, meeting_date, attendees, feedback_summary, concerns_raised)
                VALUES (?, ?, ?, ?, ?)
            """, (contract_id, meet_date, attendees, feedback, concerns))
        print(f"  [OK] Added {len(engagements)} community engagement records")

        # Add committee actions
        print("\nAdding committee actions...")
        actions = [
            ("2024-03-20", "Approve design plans and contractor selection", "Matt Fabian", "Completed", "2024-03-20"),
            ("2024-06-15", "Review and approve change order #1 for additional asbestos remediation", "Committee", "Completed", "2024-06-15"),
            ("2024-09-18", "Request monthly progress reports during installation phase", "Staff", "In Progress", "2025-02-28"),
            ("2024-11-20", "Schedule site visit for committee members", "Matt Fabian", "Pending", "2025-01-15"),
            ("2025-01-05", "Review energy savings verification plan", "Committee", "Pending", "2025-02-01"),
        ]

        for meet_date, action, assigned, status, due in actions:
            cursor.execute("""
                INSERT INTO committee_actions (contract_id, meeting_date, action_item, assigned_to, status, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contract_id, meet_date, action, assigned, status, due))
        print(f"  [OK] Added {len(actions)} committee actions")

        # Get vendor_id for contractor performance
        cursor.execute("SELECT vendor_id FROM contracts WHERE contract_id = ?", (contract_id,))
        vendor_result = cursor.fetchone()

        if vendor_result:
            vendor_id = vendor_result[0]
            print("\nAdding contractor performance data...")
            cursor.execute("""
                INSERT OR REPLACE INTO contractor_performance
                (vendor_id, safety_record, quality_score, past_projects_count, deficiency_rate, local_hiring_percent)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (vendor_id, "Excellent - Zero lost-time accidents in 3 years", 4.6, 12, 1.2, 78.5))
            print(f"  [OK] Added performance data for vendor {vendor_id}")

        conn.commit()
        print("\n[SUCCESS] Sample data added successfully!")
        print("\nYou can now view enhanced project details in the web interface.")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Failed to add sample data: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    add_sample_data()
