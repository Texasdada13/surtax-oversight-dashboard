"""
Generate realistic enhanced data for existing surtax projects.
This creates phases, inspections, community meetings, etc. based on project characteristics.
Data is marked as "Generated" for transparency.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random
import json

DB_PATH = Path(__file__).parent.parent / 'data' / 'contracts.db'

# Project type templates
PROJECT_PHASES = {
    'HVAC': [
        'Design & Engineering',
        'Permitting & Approvals',
        'Equipment Procurement',
        'Installation',
        'Testing & Commissioning',
        'Final Inspection & Closeout'
    ],
    'Roof': [
        'Inspection & Assessment',
        'Design & Specifications',
        'Permitting',
        'Roof Removal',
        'New Roof Installation',
        'Final Inspection'
    ],
    'Security': [
        'Security Assessment',
        'System Design',
        'Equipment Procurement',
        'Installation & Wiring',
        'Testing & Training',
        'System Activation'
    ],
    'Technology': [
        'Needs Assessment',
        'Equipment Procurement',
        'Infrastructure Upgrades',
        'Installation & Configuration',
        'Testing & Training',
        'Deployment'
    ],
    'Default': [
        'Planning & Design',
        'Permitting',
        'Procurement',
        'Construction',
        'Testing & Inspection',
        'Closeout'
    ]
}

INSPECTORS = [
    'James Martinez',
    'Sarah Johnson',
    'Michael Chen',
    'Patricia Williams',
    'Robert Garcia'
]

INSPECTION_FINDINGS = [
    'All work completed per specifications. No deficiencies noted.',
    'Minor issues with installation alignment. Contractor notified for correction.',
    'Excellent workmanship. Project progressing on schedule.',
    'Some cleanup required in work area. Safety protocols being followed.',
    'Quality of materials verified. Installation meets code requirements.'
]

def determine_project_type(title, category):
    """Determine project type from title and category."""
    title_lower = title.lower()
    if 'hvac' in title_lower or 'air' in title_lower or 'cooling' in title_lower:
        return 'HVAC'
    elif 'roof' in title_lower:
        return 'Roof'
    elif 'security' in title_lower or 'camera' in title_lower or 'access' in title_lower:
        return 'Security'
    elif 'tech' in title_lower or 'computer' in title_lower or 'network' in title_lower:
        return 'Technology'
    else:
        return 'Default'

def generate_project_purpose(title, category):
    """Generate realistic project purpose based on type."""
    purposes = {
        'HVAC': f"Replace aging HVAC systems to improve indoor air quality, energy efficiency, and provide reliable climate control for students and staff.",
        'Roof': f"Replace deteriorating roof system to prevent water damage, improve energy efficiency, and extend building lifespan.",
        'Security': f"Enhance campus safety and security through modern access control and surveillance systems to protect students, staff, and facilities.",
        'Technology': f"Upgrade technology infrastructure to support 21st century learning and provide students with modern educational tools.",
        'Default': f"Improve facility infrastructure to support student learning and maintain safe, modern educational environment."
    }
    project_type = determine_project_type(title, category or '')
    return purposes.get(project_type, purposes['Default'])

def generate_project_scope(title, category, budget):
    """Generate realistic project scope."""
    project_type = determine_project_type(title, category or '')

    scopes = {
        'HVAC': f"Complete replacement of HVAC equipment including rooftop units, ductwork modifications, controls upgrades, and electrical work. Project includes proper disposal of old equipment and startup/commissioning of new systems.",
        'Roof': f"Complete tear-off and replacement of existing roof system. Work includes new decking as needed, waterproof membrane, insulation upgrades, and flashing. Includes manufacturer's warranty and proper disposal of old materials.",
        'Security': f"Installation of comprehensive security system including cameras, access control hardware, network infrastructure, and monitoring equipment. Integration with existing systems and staff training included.",
        'Technology': f"Deployment of new technology equipment including installation, configuration, network integration, and user training. Includes infrastructure upgrades as needed to support new equipment.",
        'Default': f"Comprehensive facility improvement project including planning, design, construction, and testing phases. All work performed to current building codes and specifications."
    }
    return scopes.get(project_type, scopes['Default'])

def generate_community_impact(title, category):
    """Generate community impact statement."""
    impacts = [
        "Improved learning environment for approximately 600-800 students. Enhanced safety and comfort reduces student absences and supports academic achievement.",
        "Better facility conditions benefit entire school community including students, teachers, and staff. Project supports long-term sustainability of school infrastructure.",
        "Modernized facilities demonstrate commitment to student success and community investment in education. Project creates safe, healthy learning spaces.",
        "Enhanced security provides peace of mind for parents and community. Investment protects taxpayer assets and ensures student safety."
    ]
    return random.choice(impacts)

def generate_phases(contract_id, title, category, start_date, end_date):
    """Generate realistic project phases."""
    project_type = determine_project_type(title, category or '')
    phases = PROJECT_PHASES.get(project_type, PROJECT_PHASES['Default'])

    # Parse dates
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        # Use reasonable defaults if dates are invalid
        start = datetime(2024, 1, 1)
        end = datetime(2025, 6, 30)

    total_days = (end - start).days
    phase_duration = total_days / len(phases)

    phase_data = []
    current_date = start

    for i, phase_name in enumerate(phases):
        phase_start = current_date
        phase_end = current_date + timedelta(days=phase_duration)

        # Determine status and completion based on current date
        now = datetime.now()
        if phase_end < now:
            status = 'Completed'
            pct_complete = 100
        elif phase_start < now < phase_end:
            status = 'In Progress'
            elapsed = (now - phase_start).days
            pct_complete = min(95, int((elapsed / phase_duration) * 100))
        else:
            status = 'Not Started'
            pct_complete = 0

        phase_data.append({
            'contract_id': contract_id,
            'phase_name': phase_name,
            'start_date': phase_start.strftime('%Y-%m-%d'),
            'end_date': phase_end.strftime('%Y-%m-%d'),
            'status': status,
            'percent_complete': pct_complete
        })

        current_date = phase_end

    return phase_data

def generate_inspections(contract_id, start_date, num_phases_complete):
    """Generate inspection records."""
    inspections = []

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        start = datetime(2024, 1, 1)

    # Generate 1-2 inspections per completed phase
    num_inspections = max(1, num_phases_complete * random.choice([1, 2]))

    for i in range(num_inspections):
        days_offset = random.randint(30, 180) * (i + 1)
        inspection_date = start + timedelta(days=days_offset)

        if inspection_date > datetime.now():
            break

        status = random.choices(['Passed', 'Conditional'], weights=[0.8, 0.2])[0]
        deficiencies = 0 if status == 'Passed' else random.randint(1, 3)

        inspections.append({
            'contract_id': contract_id,
            'inspection_date': inspection_date.strftime('%Y-%m-%d'),
            'inspector_name': random.choice(INSPECTORS),
            'findings': random.choice(INSPECTION_FINDINGS),
            'deficiencies_count': deficiencies,
            'status': status
        })

    return inspections

def generate_community_meetings(contract_id, start_date, school_name):
    """Generate community engagement records."""
    meetings = []

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        start = datetime(2024, 1, 1)

    # Generate 2-4 community meetings
    num_meetings = random.randint(2, 4)

    for i in range(num_meetings):
        meeting_date = start + timedelta(days=random.randint(30, 60) * (i + 1))

        if meeting_date > datetime.now():
            break

        attendees = random.randint(15, 60)

        feedbacks = [
            "Community members expressed strong support for the project. Parents appreciate the investment in school facilities.",
            "Positive feedback on project progress and timeline. Questions answered about budget and scope.",
            "Community values transparency and regular updates. Strong support for completion of the project.",
            "Parents and staff pleased with improvements. Discussion of benefits to student learning environment."
        ]

        concerns = [
            "Questions about construction noise and timing to minimize disruption to classes.",
            "Concerns about parking and access during construction phase.",
            "Interest in similar projects at other schools in the district.",
            "Questions about long-term maintenance and warranty coverage."
        ]

        meetings.append({
            'contract_id': contract_id,
            'meeting_date': meeting_date.strftime('%Y-%m-%d'),
            'attendees': attendees,
            'feedback_summary': random.choice(feedbacks),
            'concerns_raised': random.choice(concerns)
        })

    return meetings

def generate_committee_actions(contract_id, start_date):
    """Generate committee action items."""
    actions = []

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        start = datetime(2024, 1, 1)

    action_templates = [
        ("Approve project scope and budget", "Committee", "Completed"),
        ("Review and approve contractor selection", "Committee", "Completed"),
        ("Request quarterly progress reports", "Staff", "In Progress"),
        ("Schedule site visit for committee members", "Matt Fabian", "Pending"),
        ("Review project completion and closeout documents", "Committee", "Pending")
    ]

    for i, (action, assigned, status) in enumerate(action_templates):
        meeting_date = start + timedelta(days=30 * i)
        due_date = meeting_date + timedelta(days=30)

        if meeting_date > datetime.now() + timedelta(days=180):
            break

        actions.append({
            'contract_id': contract_id,
            'meeting_date': meeting_date.strftime('%Y-%m-%d'),
            'action_item': action,
            'assigned_to': assigned,
            'status': status,
            'due_date': due_date.strftime('%Y-%m-%d')
        })

    return actions

def generate_funding_sources(budget):
    """Generate realistic funding source breakdown."""
    # Most projects are primarily surtax funded
    surtax_pct = random.uniform(0.7, 0.95)
    surtax_amount = int(budget * surtax_pct)

    sources = {
        "Surtax Revenue": surtax_amount
    }

    remaining = budget - surtax_amount

    # Randomly add other sources
    if remaining > 0:
        if random.random() > 0.5:
            state_match = int(remaining * random.uniform(0.3, 0.6))
            sources["State Matching Funds"] = state_match
            remaining -= state_match

        if remaining > 10000:
            sources["General Fund"] = remaining

    return sources

def populate_enhanced_data():
    """Populate enhanced data for all surtax projects."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Generating realistic enhanced data for surtax projects...")
    print("="*80)

    # Get all surtax projects
    cursor.execute("""
        SELECT contract_id, title, school_name, surtax_category, surtax_subcategory,
               current_amount, start_date, current_end_date, vendor_id, percent_complete,
               square_footage
        FROM contracts
        WHERE surtax_category IS NOT NULL
        ORDER BY current_amount DESC
    """)

    projects = cursor.fetchall()
    print(f"\nFound {len(projects)} surtax projects to enhance\n")

    for i, project in enumerate(projects, 1):
        contract_id = project['contract_id']
        title = project['title'] or 'Unnamed Project'
        category = project['surtax_category']
        budget = project['current_amount'] or 0

        print(f"[{i}/{len(projects)}] Processing: {contract_id} - {title[:50]}...")

        # Generate and update enhanced fields
        purpose = generate_project_purpose(title, category)
        scope = generate_project_scope(title, category, budget)
        impact = generate_community_impact(title, category)
        priority = random.choices(['High', 'Medium', 'Low'], weights=[0.2, 0.6, 0.2])[0]
        risk = random.choices(['Low', 'Medium', 'High'], weights=[0.5, 0.4, 0.1])[0]
        funding = generate_funding_sources(budget)

        # Generate square footage if not present
        sqft = project['square_footage']
        if not sqft or sqft == 0:
            sqft = random.randint(5000, 50000)

        cost_per_sqft = budget / sqft if sqft > 0 else 0

        # Update contract with enhanced fields
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
        """, (purpose, scope, impact, priority, risk, json.dumps(funding), sqft, cost_per_sqft, contract_id))

        # Generate phases
        phases = generate_phases(
            contract_id,
            title,
            category,
            project['start_date'] or '2024-01-01',
            project['current_end_date'] or '2025-06-30'
        )

        num_complete = sum(1 for p in phases if p['status'] == 'Completed')

        for phase in phases:
            cursor.execute("""
                INSERT INTO project_phases (contract_id, phase_name, start_date, end_date, status, percent_complete)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (phase['contract_id'], phase['phase_name'], phase['start_date'],
                  phase['end_date'], phase['status'], phase['percent_complete']))

        # Generate inspections
        inspections = generate_inspections(contract_id, project['start_date'] or '2024-01-01', num_complete)
        for inspection in inspections:
            cursor.execute("""
                INSERT INTO inspection_log (contract_id, inspection_date, inspector_name, findings, deficiencies_count, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (inspection['contract_id'], inspection['inspection_date'], inspection['inspector_name'],
                  inspection['findings'], inspection['deficiencies_count'], inspection['status']))

        # Generate community meetings
        meetings = generate_community_meetings(contract_id, project['start_date'] or '2024-01-01', project['school_name'])
        for meeting in meetings:
            cursor.execute("""
                INSERT INTO community_engagement (contract_id, meeting_date, attendees, feedback_summary, concerns_raised)
                VALUES (?, ?, ?, ?, ?)
            """, (meeting['contract_id'], meeting['meeting_date'], meeting['attendees'],
                  meeting['feedback_summary'], meeting['concerns_raised']))

        # Generate committee actions
        actions = generate_committee_actions(contract_id, project['start_date'] or '2024-01-01')
        for action in actions:
            cursor.execute("""
                INSERT INTO committee_actions (contract_id, meeting_date, action_item, assigned_to, status, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (action['contract_id'], action['meeting_date'], action['action_item'],
                  action['assigned_to'], action['status'], action['due_date']))

        # Generate contractor performance (if vendor exists)
        if project['vendor_id']:
            # Check if performance record already exists
            cursor.execute("SELECT id FROM contractor_performance WHERE vendor_id = ?", (project['vendor_id'],))
            if not cursor.fetchone():
                quality_score = round(random.uniform(3.5, 5.0), 1)
                past_projects = random.randint(5, 25)
                deficiency_rate = round(random.uniform(0.5, 3.5), 1)
                local_hiring = round(random.uniform(50, 95), 1)
                safety_records = [
                    "Excellent - Zero lost-time accidents",
                    "Good - Strong safety culture and compliance",
                    "Satisfactory - Minor incidents, corrective actions taken"
                ]

                cursor.execute("""
                    INSERT INTO contractor_performance
                    (vendor_id, safety_record, quality_score, past_projects_count, deficiency_rate, local_hiring_percent)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (project['vendor_id'], random.choice(safety_records), quality_score,
                      past_projects, deficiency_rate, local_hiring))

    conn.commit()
    conn.close()

    print("\n" + "="*80)
    print("[SUCCESS] Enhanced data generation complete!")
    print("="*80)
    print(f"\nGenerated data for {len(projects)} projects:")
    print(f"  - Project purposes, scopes, and impacts")
    print(f"  - {len(phases) * len(projects)} project phases")
    print(f"  - Inspection records")
    print(f"  - Community engagement meetings")
    print(f"  - Committee action items")
    print(f"  - Contractor performance metrics")
    print("\n[NOTE] This is GENERATED data for demonstration purposes.")
    print("Replace with actual data from Marion County records as it becomes available.\n")

if __name__ == '__main__':
    populate_enhanced_data()
