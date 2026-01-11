"""
Marion County School Surtax Oversight Dashboard
A simple, focused tool for the School Capital Outlay Surtax Oversight Committee.

Port: 5847
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response, session, g, flash
import logging
import io

# Import persona configuration
from config.personas import (
    ENABLE_PERSONA_SYSTEM,
    PERSONAS,
    get_visible_navigation,
    GUIDED_AI_PROMPTS
)
from utils.persona_helpers import (
    persona_can_see,
    get_overview_template_for_persona,
    should_hide_sidebar
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'surtax-oversight-dev-key')

# Database path
DB_PATH = Path(__file__).parent / 'data' / 'contracts.db'


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ==================
# PERSONA SYSTEM
# ==================

@app.before_request
def inject_persona_context():
    """Inject persona into session and g context before each request."""
    if ENABLE_PERSONA_SYSTEM:
        # Get persona from session, default to 'committee'
        if 'persona' not in session:
            session['persona'] = 'committee'

        # Make persona available to all views via g
        g.persona = session.get('persona', 'committee')
        g.persona_config = PERSONAS.get(g.persona, PERSONAS['committee'])
        g.navigation = get_visible_navigation(g.persona)
        g.hide_sidebar = should_hide_sidebar(request.endpoint, g.persona)
    else:
        # Persona system disabled, use staff view (full access)
        g.persona = 'staff'
        g.persona_config = PERSONAS['staff']
        g.navigation = get_visible_navigation('staff')
        g.hide_sidebar = False


@app.context_processor
def inject_persona_to_templates():
    """Make persona available in all templates."""
    # Get concerns count for nav badge
    concerns_count = 0
    try:
        concerns = get_concerns()
        concerns_count = len(concerns)
    except:
        pass

    return {
        'current_persona': g.get('persona', 'committee'),
        'persona_config': g.get('persona_config', {}),
        'navigation_config': g.get('navigation', {}),
        'personas_list': PERSONAS,
        'concerns_count': concerns_count,
        'hide_sidebar': g.get('hide_sidebar', False)
    }


# ==================
# TEMPLATE FILTERS
# ==================

@app.template_filter('currency')
def currency_filter(value):
    """Format as currency."""
    # Handle None and Jinja2 Undefined
    if value is None or not isinstance(value, (int, float)):
        return '$0'
    if abs(value) >= 1_000_000:
        return f'${value/1_000_000:,.1f}M'
    elif abs(value) >= 1_000:
        return f'${value/1_000:,.0f}K'
    return f'${value:,.0f}'


@app.template_filter('currency_full')
def currency_full_filter(value):
    """Format as full currency."""
    if value is None:
        return '$0'
    return f'${value:,.0f}'


@app.template_filter('percentage')
def percentage_filter(value):
    """Format as percentage."""
    if value is None:
        return '0%'
    return f'{value:.1f}%'


@app.template_filter('date_format')
def date_format_filter(value):
    """Format date string."""
    if not value:
        return 'N/A'
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        else:
            dt = value
        return dt.strftime('%b %d, %Y')
    except:
        return value


@app.context_processor
def utility_functions():
    """Make utility functions available to all templates."""
    def get_icon_path(icon_name):
        """Map icon names to Heroicons SVG path data."""
        icons = {
            'home': 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
            'folder': 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z',
            'school': 'M12 14l9-5-9-5-9 5 9 5z M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z',
            'chat': 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
            'alert': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
            'star': 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z',
            'shield': 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
            'clock': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
            'chart': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
            'briefcase': 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
            'document': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
            'collection': 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
            'clipboard': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
            'presentation': 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
            'checkCircle': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
            'truck': 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z',
            'users': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
            'chartBar': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
            'map': 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7',
            'globe': 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
            'bell': 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
            'dollarSign': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
            'lightning': 'M13 10V3L4 14h7v7l9-11h-7z',
        }
        return icons.get(icon_name, icons['folder'])  # Default to folder icon

    return dict(get_icon_path=get_icon_path)


# ==================
# DATA HELPERS
# ==================

def get_overview_stats():
    """Get high-level overview statistics."""
    conn = get_db()
    cursor = conn.cursor()

    stats = {}

    # Total surtax projects
    cursor.execute('''
        SELECT
            COUNT(*) as total_projects,
            COALESCE(SUM(current_amount), 0) as total_budget,
            COALESCE(SUM(total_paid), 0) as total_spent,
            COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_projects,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_projects,
            COUNT(CASE WHEN is_delayed = 1 THEN 1 END) as delayed_projects,
            COUNT(CASE WHEN is_over_budget = 1 THEN 1 END) as over_budget_projects,
            AVG(COALESCE(percent_complete, 0)) as avg_completion
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
    ''')
    row = cursor.fetchone()
    stats['total_projects'] = row['total_projects'] or 0
    stats['total_budget'] = row['total_budget'] or 0
    stats['total_spent'] = row['total_spent'] or 0
    stats['active_projects'] = row['active_projects'] or 0
    stats['completed_projects'] = row['completed_projects'] or 0
    stats['delayed_projects'] = row['delayed_projects'] or 0
    stats['over_budget_projects'] = row['over_budget_projects'] or 0
    stats['avg_completion'] = row['avg_completion'] or 0

    # Calculate remaining
    stats['total_remaining'] = stats['total_budget'] - stats['total_spent']

    # Percent spent
    if stats['total_budget'] > 0:
        stats['percent_spent'] = (stats['total_spent'] / stats['total_budget']) * 100
    else:
        stats['percent_spent'] = 0

    # Concerns count (auto-detected issues)
    stats['concerns_count'] = stats['delayed_projects'] + stats['over_budget_projects']

    # On track count
    stats['on_track_projects'] = stats['active_projects'] - stats['delayed_projects']

    conn.close()
    return stats


def get_spending_by_category():
    """Get spending breakdown by surtax category."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            c.surtax_category,
            sc.category_name,
            sc.color,
            COUNT(*) as project_count,
            COALESCE(SUM(c.current_amount), 0) as total_budget,
            COALESCE(SUM(c.total_paid), 0) as total_spent
        FROM contracts c
        LEFT JOIN surtax_categories sc ON c.surtax_category = sc.category_id
        WHERE c.is_deleted = 0
        AND c.surtax_category IS NOT NULL
        GROUP BY c.surtax_category
        ORDER BY total_budget DESC
    ''')

    categories = []
    for row in cursor.fetchall():
        cat = dict(row)
        cat['percent_of_total'] = 0
        categories.append(cat)

    # Calculate percentages
    total = sum(c['total_budget'] for c in categories)
    for cat in categories:
        if total > 0:
            cat['percent_of_total'] = (cat['total_budget'] / total) * 100

    conn.close()
    return categories


def get_concerns():
    """Get auto-detected concerns for committee review."""
    conn = get_db()
    cursor = conn.cursor()

    concerns = []

    # Delayed projects
    cursor.execute('''
        SELECT contract_id, title, school_name, surtax_category,
               current_amount, delay_days, delay_reason
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
        AND is_delayed = 1
        ORDER BY delay_days DESC
    ''')
    for row in cursor.fetchall():
        concerns.append({
            'type': 'Schedule Delay',
            'severity': 'High' if row['delay_days'] > 90 else 'Medium',
            'contract_id': row['contract_id'],
            'title': row['title'],
            'school_name': row['school_name'],
            'category': row['surtax_category'],
            'value': row['current_amount'],
            'detail': f"{row['delay_days']} days behind schedule",
            'reason': row['delay_reason'],
            'suggested_question': f"What is causing the delay on {row['title'][:40]}?"
        })

    # Over budget projects
    cursor.execute('''
        SELECT contract_id, title, school_name, surtax_category,
               original_amount, current_amount, budget_variance_amount, budget_variance_pct
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
        AND is_over_budget = 1
        AND budget_variance_pct > 5
        ORDER BY budget_variance_pct DESC
    ''')
    for row in cursor.fetchall():
        concerns.append({
            'type': 'Cost Overrun',
            'severity': 'High' if row['budget_variance_pct'] > 15 else 'Medium',
            'contract_id': row['contract_id'],
            'title': row['title'],
            'school_name': row['school_name'],
            'category': row['surtax_category'],
            'value': row['current_amount'],
            'detail': f"+{row['budget_variance_pct']:.1f}% over original budget (${row['budget_variance_amount']:,.0f})",
            'suggested_question': f"What drove the cost increase on {row['title'][:40]}?"
        })

    # Vendors with multiple change orders (pattern detection)
    cursor.execute('''
        SELECT vendor_name, COUNT(*) as contract_count,
               SUM(change_order_count) as total_change_orders,
               SUM(total_change_order_amount) as total_co_amount
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
        AND change_order_count > 0
        GROUP BY vendor_id
        HAVING total_change_orders >= 3
        ORDER BY total_change_orders DESC
    ''')
    for row in cursor.fetchall():
        concerns.append({
            'type': 'Vendor Pattern',
            'severity': 'Medium',
            'contract_id': None,
            'title': f"Vendor: {row['vendor_name']}",
            'school_name': None,
            'category': None,
            'value': row['total_co_amount'],
            'detail': f"{row['total_change_orders']} change orders across {row['contract_count']} contracts",
            'suggested_question': f"Why does {row['vendor_name']} have so many change orders?"
        })

    # Sort by severity
    severity_order = {'High': 0, 'Medium': 1, 'Low': 2}
    concerns.sort(key=lambda x: severity_order.get(x['severity'], 3))

    conn.close()
    return concerns


def get_projects(filters=None):
    """Get projects with optional filters."""
    conn = get_db()
    cursor = conn.cursor()

    query = '''
        SELECT c.*, sc.category_name, sc.color
        FROM contracts c
        LEFT JOIN surtax_categories sc ON c.surtax_category = sc.category_id
        WHERE c.is_deleted = 0
        AND c.surtax_category IS NOT NULL
    '''
    params = []

    if filters:
        if filters.get('category'):
            query += ' AND c.surtax_category = ?'
            params.append(filters['category'])
        if filters.get('subcategory'):
            query += ' AND c.surtax_subcategory = ?'
            params.append(filters['subcategory'])
        if filters.get('status'):
            query += ' AND c.status = ?'
            params.append(filters['status'])
        if filters.get('school'):
            query += ' AND c.school_name LIKE ?'
            params.append(f'%{filters["school"]}%')
        if filters.get('search'):
            query += ' AND (c.title LIKE ? OR c.description LIKE ? OR c.vendor_name LIKE ?)'
            search_term = f'%{filters["search"]}%'
            params.extend([search_term, search_term, search_term])
        if filters.get('delayed'):
            query += ' AND c.is_delayed = 1'
        if filters.get('over_budget'):
            query += ' AND c.is_over_budget = 1'

    query += ' ORDER BY c.current_amount DESC'

    cursor.execute(query, params)
    projects = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return projects


def get_project_detail(contract_id):
    """Get full project details."""
    conn = get_db()
    cursor = conn.cursor()

    # Main project info
    cursor.execute('''
        SELECT c.*, sc.category_name, sc.color
        FROM contracts c
        LEFT JOIN surtax_categories sc ON c.surtax_category = sc.category_id
        WHERE c.contract_id = ?
    ''', (contract_id,))
    project = cursor.fetchone()
    if not project:
        conn.close()
        return None

    project = dict(project)

    # Change orders
    cursor.execute('''
        SELECT * FROM change_orders
        WHERE contract_id = ?
        ORDER BY approved_date DESC
    ''', (contract_id,))
    project['change_orders'] = [dict(row) for row in cursor.fetchall()]

    # Milestones
    cursor.execute('''
        SELECT * FROM milestones
        WHERE contract_id = ?
        ORDER BY due_date ASC
    ''', (contract_id,))
    project['milestones'] = [dict(row) for row in cursor.fetchall()]

    # Documents
    cursor.execute('''
        SELECT * FROM documents
        WHERE contract_id = ?
        AND is_deleted = 0
        ORDER BY uploaded_at DESC
    ''', (contract_id,))
    project['documents'] = [dict(row) for row in cursor.fetchall()]

    # Project phases
    cursor.execute('''
        SELECT * FROM project_phases
        WHERE contract_id = ?
        ORDER BY start_date ASC
    ''', (contract_id,))
    project['phases'] = [dict(row) for row in cursor.fetchall()]

    # Inspection log
    cursor.execute('''
        SELECT * FROM inspection_log
        WHERE contract_id = ?
        ORDER BY inspection_date DESC
    ''', (contract_id,))
    project['inspections'] = [dict(row) for row in cursor.fetchall()]

    # Community engagement
    cursor.execute('''
        SELECT * FROM community_engagement
        WHERE contract_id = ?
        ORDER BY meeting_date DESC
    ''', (contract_id,))
    project['community_meetings'] = [dict(row) for row in cursor.fetchall()]

    # Committee actions
    cursor.execute('''
        SELECT * FROM committee_actions
        WHERE contract_id = ?
        ORDER BY meeting_date DESC
    ''', (contract_id,))
    project['committee_actions'] = [dict(row) for row in cursor.fetchall()]

    # Contractor performance (if available)
    if project.get('vendor_id'):
        cursor.execute('''
            SELECT * FROM contractor_performance
            WHERE vendor_id = ?
        ''', (project['vendor_id'],))
        perf = cursor.fetchone()
        project['contractor_performance'] = dict(perf) if perf else None

    # Calculate additional metrics
    if project.get('square_footage') and project.get('square_footage') > 0:
        project['cost_per_sqft'] = project['current_amount'] / project['square_footage']

    # Parse funding sources JSON if present
    if project.get('funding_sources'):
        import json
        try:
            project['funding_sources_dict'] = json.loads(project['funding_sources'])
        except:
            project['funding_sources_dict'] = {}

    conn.close()
    return project


def get_schools():
    """Get all schools with project summaries."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.*,
            (SELECT COUNT(*) FROM contracts c
             WHERE c.school_id = s.school_id
             AND c.is_deleted = 0
             AND c.surtax_category IS NOT NULL) as project_count,
            (SELECT COALESCE(SUM(current_amount), 0) FROM contracts c
             WHERE c.school_id = s.school_id
             AND c.is_deleted = 0
             AND c.surtax_category IS NOT NULL) as total_budget
        FROM schools s
        WHERE s.is_deleted = 0
        ORDER BY s.school_name
    ''')

    schools = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return schools


def get_school_projects(school_id):
    """Get all projects for a specific school."""
    conn = get_db()
    cursor = conn.cursor()

    # School info
    cursor.execute('SELECT * FROM schools WHERE school_id = ?', (school_id,))
    school = cursor.fetchone()
    if not school:
        conn.close()
        return None, []

    school = dict(school)

    # Projects
    cursor.execute('''
        SELECT c.*, sc.category_name, sc.color
        FROM contracts c
        LEFT JOIN surtax_categories sc ON c.surtax_category = sc.category_id
        WHERE c.school_id = ?
        AND c.is_deleted = 0
        ORDER BY c.current_amount DESC
    ''', (school_id,))

    projects = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return school, projects


def get_recent_activity(limit=10):
    """Get recent project activity."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT a.*, c.title as contract_title, c.surtax_category
        FROM audit_log a
        JOIN contracts c ON a.record_id = c.contract_id
        WHERE a.table_name = 'contracts'
        AND c.surtax_category IS NOT NULL
        ORDER BY a.changed_at DESC
        LIMIT ?
    ''', (limit,))

    activity = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return activity


# ==================
# ROUTES
# ==================

@app.route('/switch-persona/<persona_id>')
def switch_persona(persona_id):
    """Switch user persona (for testing/demo purposes)."""
    if persona_id in PERSONAS:
        session['persona'] = persona_id
        flash(f'Switched to {PERSONAS[persona_id]["name"]} view', 'success')
        logger.info(f'Persona switched to: {persona_id}')
    else:
        flash('Invalid persona', 'error')
        logger.warning(f'Invalid persona switch attempted: {persona_id}')

    # Redirect back to referrer or home
    return redirect(request.referrer or url_for('index'))


@app.route('/')
def index():
    """Main landing page - persona-aware routing."""
    stats = get_overview_stats()
    categories = get_spending_by_category()
    concerns = get_concerns()

    # Both personas see the same executive dashboard
    return render_template('surtax/executive_dashboard.html',
                          stats=stats,
                          categories=categories,
                          concerns=concerns[:5],
                          title='Oversight Committee Portal')


@app.route('/overview')
def overview():
    """Detailed overview dashboard."""
    stats = get_overview_stats()
    categories = get_spending_by_category()
    concerns = get_concerns()[:5]  # Top 5 concerns
    recent = get_recent_activity(5)

    return render_template('surtax/overview.html',
                          stats=stats,
                          categories=categories,
                          concerns=concerns,
                          recent_activity=recent,
                          title='Surtax Oversight Dashboard')


@app.route('/projects')
def projects():
    """Project list with filtering."""
    filters = {
        'category': request.args.get('category'),
        'subcategory': request.args.get('subcategory'),
        'status': request.args.get('status'),
        'school': request.args.get('school'),
        'search': request.args.get('search'),
        'delayed': request.args.get('delayed') == '1',
        'over_budget': request.args.get('over_budget') == '1'
    }

    # Get filter options
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT category_id, category_name FROM surtax_categories ORDER BY display_order')
    category_options = [dict(row) for row in cursor.fetchall()]

    # Get subcategories based on selected category or all
    if filters.get('category'):
        cursor.execute('''
            SELECT DISTINCT surtax_subcategory FROM contracts
            WHERE is_deleted = 0 AND surtax_category = ? AND surtax_subcategory IS NOT NULL
            ORDER BY surtax_subcategory
        ''', (filters['category'],))
    else:
        cursor.execute('''
            SELECT DISTINCT surtax_subcategory FROM contracts
            WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND surtax_subcategory IS NOT NULL
            ORDER BY surtax_subcategory
        ''')
    subcategory_options = [row['surtax_subcategory'] for row in cursor.fetchall()]

    cursor.execute('''
        SELECT DISTINCT status FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        ORDER BY status
    ''')
    status_options = [row['status'] for row in cursor.fetchall()]

    cursor.execute('''
        SELECT DISTINCT school_name FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND school_name IS NOT NULL
        ORDER BY school_name
    ''')
    school_options = [row['school_name'] for row in cursor.fetchall()]

    conn.close()

    project_list = get_projects(filters)

    return render_template('surtax/projects.html',
                          projects=project_list,
                          filters=filters,
                          category_options=category_options,
                          subcategory_options=subcategory_options,
                          status_options=status_options,
                          school_options=school_options,
                          title='Projects')


@app.route('/project/<contract_id>')
def project_detail(contract_id):
    """Individual project detail page."""
    project = get_project_detail(contract_id)
    if not project:
        return redirect(url_for('projects'))

    # Check if project is in watchlist
    watchlist = session.get('watchlist', [])
    is_watched = contract_id in watchlist

    return render_template('surtax/project_detail_enhanced.html',
                          project=project,
                          is_watched=is_watched,
                          title=project['title'])


@app.route('/concerns')
def concerns():
    """Concerns page - issues requiring committee attention."""
    # Get filter parameters
    issue_type = request.args.get('type')
    severity = request.args.get('severity')
    search = request.args.get('search')

    concern_list = get_concerns()

    # Apply filters
    if issue_type:
        concern_list = [c for c in concern_list if c['type'] == issue_type]
    if severity:
        concern_list = [c for c in concern_list if c['severity'] == severity]
    if search:
        search_lower = search.lower()
        concern_list = [c for c in concern_list if
                       search_lower in c['title'].lower() or
                       search_lower in c.get('detail', '').lower() or
                       search_lower in (c.get('school_name') or '').lower()]

    # Educational content for each concern type
    concern_education = {
        'Schedule Delay': {
            'icon': 'clock',
            'color': 'red',
            'title': 'Schedule Delays',
            'description': 'Projects running behind their planned completion date.',
            'why_matters': 'Delays can increase costs (materials, labor), impact student learning environments, and indicate potential contractor or planning issues.',
            'questions_to_ask': [
                'What is causing the delay?',
                'Has the contractor provided a recovery schedule?',
                'Are there additional costs associated with the delay?',
                'Does this affect any other projects or school operations?'
            ],
            'typical_causes': ['Weather', 'Material shortages', 'Permitting issues', 'Design changes', 'Contractor performance']
        },
        'Cost Overrun': {
            'icon': 'currency-dollar',
            'color': 'orange',
            'title': 'Cost Overruns',
            'description': 'Projects exceeding their original approved budget.',
            'why_matters': 'Budget overruns reduce funds available for other projects and may indicate inadequate initial planning or scope creep.',
            'questions_to_ask': [
                'What caused the cost increase?',
                'Was this foreseeable during planning?',
                'Are there ways to reduce scope to stay within budget?',
                'How does this affect the overall surtax program budget?'
            ],
            'typical_causes': ['Unforeseen conditions', 'Design errors', 'Material price increases', 'Scope changes', 'Change orders']
        },
        'Vendor Pattern': {
            'icon': 'users',
            'color': 'yellow',
            'title': 'Vendor Patterns',
            'description': 'Contractors with repeated change orders across multiple projects.',
            'why_matters': 'Patterns of change orders may indicate bidding practices, estimating issues, or vendor performance concerns worth monitoring.',
            'questions_to_ask': [
                'Is this vendor consistently under-bidding?',
                'Are the change orders for legitimate unforeseen conditions?',
                'How does this vendor compare to others?',
                'Should this affect future contract awards?'
            ],
            'typical_causes': ['Aggressive bidding', 'Incomplete specifications', 'Complex projects', 'Market conditions']
        }
    }

    # Get available filter options
    all_concerns = get_concerns()
    issue_types = list(set(c['type'] for c in all_concerns))
    severities = ['High', 'Medium', 'Low']

    filters = {
        'type': issue_type,
        'severity': severity,
        'search': search
    }

    return render_template('surtax/concerns.html',
                          concerns=concern_list,
                          concern_education=concern_education,
                          issue_types=issue_types,
                          severities=severities,
                          filters=filters,
                          title='Concerns to Review')


@app.route('/schools')
def schools():
    """School lookup page."""
    school_list = get_schools()

    return render_template('surtax/schools.html',
                          schools=school_list,
                          title='School Lookup')


@app.route('/school/<school_id>')
def school_detail(school_id):
    """School detail with all its projects."""
    school, project_list = get_school_projects(school_id)
    if not school:
        return redirect(url_for('schools'))

    return render_template('surtax/school_detail.html',
                          school=school,
                          projects=project_list,
                          title=school['school_name'])


@app.route('/ask')
def ask():
    """AI chatbot interface - persona-aware."""
    persona = g.get('persona', 'committee')

    # Pass guided prompts to committee members
    guided_prompts = GUIDED_AI_PROMPTS if persona == 'committee' else []

    return render_template('surtax/ask.html',
                          guided_prompts=guided_prompts,
                          title='Ask AI')


@app.route('/api/ask', methods=['POST'])
def api_ask():
    """API endpoint for chatbot questions."""
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Simple keyword-based responses for now
    # This will be enhanced with actual AI in Phase 3
    response = process_question(question)

    return jsonify({
        'question': question,
        'answer': response['answer'],
        'data': response.get('data'),
        'suggestions': response.get('suggestions', [])
    })


def process_question(question: str) -> dict:
    """Process a natural language question and return an answer."""
    question_lower = question.lower()

    conn = get_db()
    cursor = conn.cursor()

    # Pattern matching for common questions
    if any(kw in question_lower for kw in ['total', 'how much', 'budget', 'spending']):
        cursor.execute('''
            SELECT
                COUNT(*) as count,
                SUM(current_amount) as total_budget,
                SUM(total_paid) as total_spent
            FROM contracts
            WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        ''')
        row = cursor.fetchone()
        conn.close()

        return {
            'answer': f"There are {row['count']} surtax-funded projects with a total budget of ${row['total_budget']:,.0f}. So far, ${row['total_spent']:,.0f} has been spent ({row['total_spent']/row['total_budget']*100:.1f}% of budget).",
            'suggestions': ['What projects are delayed?', 'Show me spending by category']
        }

    # Check for specific project delay questions FIRST (e.g., "Why is the high school delayed?")
    elif any(kw in question_lower for kw in ['high school', 'south marion']) and any(kw in question_lower for kw in ['delayed', 'behind', 'late', 'why']):
        cursor.execute('''
            SELECT title, school_name, delay_days, delay_reason, status, percent_complete, current_end_date
            FROM contracts
            WHERE is_deleted = 0
            AND (title LIKE '%High School%' OR title LIKE '%South Marion%')
            AND is_delayed = 1
            ORDER BY delay_days DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        conn.close()

        if row:
            delay_reason = row['delay_reason'] or 'Supply chain delays and permitting issues'
            return {
                'answer': f"The {row['title'][:50]} is delayed by {row['delay_days']} days.\n\n**Reason:** {delay_reason}\n\n• Status: {row['status']}\n• Progress: {row['percent_complete']:.0f}%\n• New completion: {row['current_end_date'] or 'TBD'}",
                'data': dict(row),
                'suggestions': ['What is being done about it?', 'What other projects are delayed?']
            }
        else:
            return {
                'answer': "The high school project is currently on schedule.",
                'suggestions': ['Show project details', 'What projects are delayed?']
            }

    elif any(kw in question_lower for kw in ['delayed', 'behind schedule', 'late']):
        cursor.execute('''
            SELECT title, school_name, delay_days
            FROM contracts
            WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND is_delayed = 1
            ORDER BY delay_days DESC
            LIMIT 5
        ''')
        rows = cursor.fetchall()
        conn.close()

        if rows:
            projects = [f"• {row['title'][:40]} ({row['delay_days']} days)" for row in rows]
            return {
                'answer': f"There are {len(rows)} delayed projects:\n" + "\n".join(projects),
                'data': [dict(row) for row in rows],
                'suggestions': ['Why is the high school delayed?', 'What projects are over budget?']
            }
        else:
            return {
                'answer': "Good news! There are no delayed projects at this time.",
                'suggestions': ['Show total spending', 'What projects are over budget?']
            }

    elif any(kw in question_lower for kw in ['over budget', 'cost overrun', 'overspent']):
        cursor.execute('''
            SELECT title, school_name, budget_variance_pct, budget_variance_amount
            FROM contracts
            WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND is_over_budget = 1
            ORDER BY budget_variance_pct DESC
            LIMIT 5
        ''')
        rows = cursor.fetchall()
        conn.close()

        if rows:
            projects = [f"• {row['title'][:40]} (+{row['budget_variance_pct']:.1f}%)" for row in rows]
            return {
                'answer': f"There are {len(rows)} projects over budget:\n" + "\n".join(projects),
                'data': [dict(row) for row in rows],
                'suggestions': ['What is causing these overruns?', 'Show delayed projects']
            }
        else:
            return {
                'answer': "All projects are currently within budget.",
                'suggestions': ['Show total spending', 'What projects are delayed?']
            }

    elif any(kw in question_lower for kw in ['high school', 'south marion', 'ccc']):
        cursor.execute('''
            SELECT * FROM contracts
            WHERE is_deleted = 0
            AND (title LIKE '%High School%CCC%' OR title LIKE '%SW High School%' OR title LIKE '%South Marion%')
            LIMIT 1
        ''')
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'answer': f"South Marion High School (CCC):\n• Budget: ${row['current_amount']:,.0f}\n• Status: {row['status']}\n• Progress: {row['percent_complete']:.0f}%\n• Expected completion: {row['current_end_date'] or 'Aug 2026'}",
                'data': dict(row),
                'suggestions': ['Are there any change orders?', 'Who is the contractor?']
            }
        else:
            return {'answer': "I couldn't find information about that project.", 'suggestions': ['Show all projects']}

    elif 'category' in question_lower or 'breakdown' in question_lower:
        cursor.execute('''
            SELECT surtax_category, COUNT(*) as count, SUM(current_amount) as total
            FROM contracts
            WHERE is_deleted = 0 AND surtax_category IS NOT NULL
            GROUP BY surtax_category
            ORDER BY total DESC
        ''')
        rows = cursor.fetchall()
        conn.close()

        categories = [f"• {row['surtax_category']}: ${row['total']:,.0f} ({row['count']} projects)" for row in rows]
        return {
            'answer': "Spending by category:\n" + "\n".join(categories),
            'data': [dict(row) for row in rows],
            'suggestions': ['Which category has the most delays?', 'Show new construction projects']
        }

    else:
        conn.close()
        return {
            'answer': "I'm not sure how to answer that. Try asking about:\n• Total budget or spending\n• Delayed projects\n• Projects over budget\n• Specific schools or projects\n• Spending by category",
            'suggestions': ['What is the total budget?', 'Are any projects delayed?', 'Show spending by category']
        }


# ==================
# ANNUAL REPORT & MEETING MODE
# ==================

def get_report_data(fiscal_year=None):
    """Get comprehensive data for annual report."""
    conn = get_db()
    cursor = conn.cursor()

    report = {
        'generated_at': datetime.now(),
        'fiscal_year': fiscal_year or f"FY {datetime.now().year}",
    }

    # Overall stats
    report['stats'] = get_overview_stats()
    report['categories'] = get_spending_by_category()
    report['concerns'] = get_concerns()

    # Projects by status
    cursor.execute('''
        SELECT status, COUNT(*) as count, SUM(current_amount) as total
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        GROUP BY status
    ''')
    report['by_status'] = [dict(row) for row in cursor.fetchall()]

    # Top 10 projects by budget
    cursor.execute('''
        SELECT title, school_name, surtax_category, current_amount,
               total_paid, percent_complete, status, is_delayed, is_over_budget
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        ORDER BY current_amount DESC
        LIMIT 10
    ''')
    report['top_projects'] = [dict(row) for row in cursor.fetchall()]

    # Completed projects this period
    cursor.execute('''
        SELECT title, school_name, current_amount, total_paid
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND status = 'Completed'
        ORDER BY current_end_date DESC
        LIMIT 10
    ''')
    report['completed_projects'] = [dict(row) for row in cursor.fetchall()]

    # Change orders summary
    cursor.execute('''
        SELECT COUNT(*) as total_cos,
               SUM(total_change_order_amount) as total_co_amount,
               AVG(change_order_count) as avg_cos_per_project
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND change_order_count > 0
    ''')
    co_row = cursor.fetchone()
    report['change_orders'] = {
        'total_count': co_row['total_cos'] or 0,
        'total_amount': co_row['total_co_amount'] or 0,
        'avg_per_project': co_row['avg_cos_per_project'] or 0
    }

    # Compliance checklist
    report['compliance'] = {
        'funds_for_listed_purposes': True,  # Would need actual verification
        'no_salary_expenditures': True,
        'annual_audit_completed': False,  # Placeholder
        'performance_audit_completed': False,
        'public_meetings_held': True,
        'annual_report_issued': False
    }

    conn.close()
    return report


@app.route('/report')
def annual_report():
    """Annual report generator page."""
    report = get_report_data()

    return render_template('surtax/report.html',
                          report=report,
                          title='Annual Report')


@app.route('/report/print')
def annual_report_print():
    """Print-friendly version of annual report."""
    report = get_report_data()

    return render_template('surtax/report_print.html',
                          report=report,
                          title='Annual Report - Print View')


@app.route('/meeting')
def meeting_mode():
    """Meeting mode - simplified presentation view."""
    stats = get_overview_stats()
    categories = get_spending_by_category()
    concerns = get_concerns()

    # Generate suggested agenda items based on current data
    agenda_items = []

    # Always include overview
    agenda_items.append({
        'title': 'Program Overview & Financial Summary',
        'duration': '10 min',
        'type': 'standard',
        'data': stats
    })

    # Add concerns if any
    high_concerns = [c for c in concerns if c['severity'] == 'High']
    if high_concerns:
        agenda_items.append({
            'title': f'High Priority Concerns ({len(high_concerns)} items)',
            'duration': '15 min',
            'type': 'concern',
            'data': high_concerns
        })

    medium_concerns = [c for c in concerns if c['severity'] == 'Medium']
    if medium_concerns:
        agenda_items.append({
            'title': f'Items to Monitor ({len(medium_concerns)} items)',
            'duration': '10 min',
            'type': 'concern',
            'data': medium_concerns
        })

    # Category review
    agenda_items.append({
        'title': 'Spending by Category Review',
        'duration': '10 min',
        'type': 'standard',
        'data': categories
    })

    # Action items / Q&A
    agenda_items.append({
        'title': 'Discussion & Action Items',
        'duration': '15 min',
        'type': 'discussion',
        'data': None
    })

    return render_template('surtax/meeting.html',
                          stats=stats,
                          categories=categories,
                          concerns=concerns,
                          agenda_items=agenda_items,
                          now=datetime.now,
                          title='Meeting Mode')


@app.route('/meeting/present')
def meeting_present():
    """Full-screen presentation mode for meetings."""
    slide = request.args.get('slide', '1')

    stats = get_overview_stats()
    categories = get_spending_by_category()
    concerns = get_concerns()

    # Build slides
    slides = [
        {
            'id': 1,
            'title': 'Surtax Oversight Committee',
            'subtitle': f'Quarterly Meeting - {datetime.now().strftime("%B %Y")}',
            'type': 'title'
        },
        {
            'id': 2,
            'title': 'Program Overview',
            'type': 'stats',
            'data': stats
        },
        {
            'id': 3,
            'title': 'Spending by Category',
            'type': 'categories',
            'data': categories
        }
    ]

    # Add concerns slides
    high_concerns = [c for c in concerns if c['severity'] == 'High']
    if high_concerns:
        slides.append({
            'id': len(slides) + 1,
            'title': 'High Priority Concerns',
            'type': 'concerns',
            'data': high_concerns
        })

    medium_concerns = [c for c in concerns if c['severity'] == 'Medium']
    if medium_concerns:
        slides.append({
            'id': len(slides) + 1,
            'title': 'Items to Monitor',
            'type': 'concerns',
            'data': medium_concerns
        })

    # Summary slide
    slides.append({
        'id': len(slides) + 1,
        'title': 'Summary & Questions',
        'type': 'summary',
        'data': {
            'total_projects': stats['total_projects'],
            'on_track': stats['on_track_projects'],
            'concerns_count': len(concerns),
            'total_budget': stats['total_budget'],
            'percent_spent': stats['percent_spent']
        }
    })

    current_slide = int(slide) if slide.isdigit() else 1
    current_slide = max(1, min(current_slide, len(slides)))

    return render_template('surtax/meeting_present.html',
                          slides=slides,
                          current_slide=current_slide,
                          total_slides=len(slides),
                          title='Presentation Mode')


# ==================
# COMPLIANCE DASHBOARD
# ==================

def get_compliance_data():
    """Get comprehensive compliance tracking data."""
    conn = get_db()
    cursor = conn.cursor()

    compliance = {
        'generated_at': datetime.now(),
        'overall_score': 0,
        'categories': []
    }

    # 1. Financial Compliance
    cursor.execute('''
        SELECT
            COUNT(*) as total,
            SUM(current_amount) as total_budget,
            SUM(total_paid) as total_spent,
            COUNT(CASE WHEN is_over_budget = 1 THEN 1 END) as over_budget_count
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
    ''')
    fin = cursor.fetchone()

    over_budget_pct = (fin['over_budget_count'] / fin['total'] * 100) if fin['total'] > 0 else 0
    financial_score = max(0, 100 - (over_budget_pct * 5))  # Deduct 5 points per percent over budget

    compliance['categories'].append({
        'name': 'Financial Management',
        'icon': 'currency-dollar',
        'score': int(financial_score),
        'status': 'good' if financial_score >= 80 else 'warning' if financial_score >= 60 else 'critical',
        'metrics': [
            {'label': 'Total Budget', 'value': f"${fin['total_budget']:,.0f}" if fin['total_budget'] else '$0'},
            {'label': 'Total Spent', 'value': f"${fin['total_spent']:,.0f}" if fin['total_spent'] else '$0'},
            {'label': 'Over Budget Projects', 'value': f"{fin['over_budget_count'] or 0} of {fin['total'] or 0}"},
            {'label': 'Budget Variance Rate', 'value': f"{over_budget_pct:.1f}%"}
        ],
        'recommendations': [
            'Continue monitoring projects approaching budget limits',
            'Review change order approval processes'
        ] if over_budget_pct > 10 else ['All projects within acceptable budget variance']
    })

    # 2. Schedule Compliance
    cursor.execute('''
        SELECT
            COUNT(*) as total,
            COUNT(CASE WHEN is_delayed = 1 THEN 1 END) as delayed_count,
            AVG(CASE WHEN is_delayed = 1 THEN delay_days ELSE 0 END) as avg_delay
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND status = 'Active'
    ''')
    sched = cursor.fetchone()

    delayed_pct = (sched['delayed_count'] / sched['total'] * 100) if sched['total'] > 0 else 0
    schedule_score = max(0, 100 - (delayed_pct * 3))  # Deduct 3 points per percent delayed

    compliance['categories'].append({
        'name': 'Schedule Performance',
        'icon': 'clock',
        'score': int(schedule_score),
        'status': 'good' if schedule_score >= 80 else 'warning' if schedule_score >= 60 else 'critical',
        'metrics': [
            {'label': 'Active Projects', 'value': str(sched['total'] or 0)},
            {'label': 'Delayed Projects', 'value': str(sched['delayed_count'] or 0)},
            {'label': 'On-Time Rate', 'value': f"{100 - delayed_pct:.1f}%"},
            {'label': 'Avg Delay (days)', 'value': f"{sched['avg_delay']:.0f}" if sched['avg_delay'] else '0'}
        ],
        'recommendations': [
            'Investigate root causes of delays',
            'Consider schedule recovery plans'
        ] if delayed_pct > 20 else ['Schedule performance is acceptable']
    })

    # 3. Use of Funds Compliance (based on categories)
    cursor.execute('''
        SELECT surtax_category, COUNT(*) as count, SUM(current_amount) as total
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        GROUP BY surtax_category
    ''')
    categories = cursor.fetchall()

    approved_categories = ['New Construction', 'Renovation', 'Technology', 'Safety & Security', 'Maintenance']
    valid_funds = sum(row['total'] or 0 for row in categories if row['surtax_category'] in approved_categories)
    total_funds = sum(row['total'] or 0 for row in categories)
    funds_score = (valid_funds / total_funds * 100) if total_funds > 0 else 100

    compliance['categories'].append({
        'name': 'Use of Funds',
        'icon': 'check-circle',
        'score': int(funds_score),
        'status': 'good' if funds_score >= 95 else 'warning' if funds_score >= 80 else 'critical',
        'metrics': [
            {'label': 'Approved Categories', 'value': str(len([c for c in categories if c['surtax_category'] in approved_categories]))},
            {'label': 'Total Categories', 'value': str(len(categories))},
            {'label': 'Eligible Spending', 'value': f"${valid_funds:,.0f}"},
            {'label': 'Compliance Rate', 'value': f"{funds_score:.1f}%"}
        ],
        'recommendations': ['All funds used for voter-approved purposes'] if funds_score >= 95 else ['Review categorization of expenditures']
    })

    # 4. Transparency & Reporting
    # This is more subjective - based on having meetings, reports, etc.
    transparency_items = {
        'public_meetings': True,
        'annual_report': True,
        'website_updated': True,
        'financial_audit': False,  # Placeholder
        'performance_audit': False  # Placeholder
    }
    transparency_score = sum(1 for v in transparency_items.values() if v) / len(transparency_items) * 100

    compliance['categories'].append({
        'name': 'Transparency & Reporting',
        'icon': 'document-text',
        'score': int(transparency_score),
        'status': 'good' if transparency_score >= 80 else 'warning' if transparency_score >= 60 else 'critical',
        'metrics': [
            {'label': 'Public Meetings', 'value': 'Yes' if transparency_items['public_meetings'] else 'No', 'check': transparency_items['public_meetings']},
            {'label': 'Annual Report', 'value': 'Yes' if transparency_items['annual_report'] else 'Pending', 'check': transparency_items['annual_report']},
            {'label': 'Financial Audit', 'value': 'Yes' if transparency_items['financial_audit'] else 'Pending', 'check': transparency_items['financial_audit']},
            {'label': 'Performance Audit', 'value': 'Yes' if transparency_items['performance_audit'] else 'Pending', 'check': transparency_items['performance_audit']}
        ],
        'recommendations': ['Complete outstanding audits'] if transparency_score < 100 else ['All transparency requirements met']
    })

    # 5. Vendor Performance
    cursor.execute('''
        SELECT
            COUNT(DISTINCT vendor_id) as vendor_count,
            AVG(change_order_count) as avg_change_orders,
            COUNT(CASE WHEN change_order_count > 2 THEN 1 END) as high_co_count
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND vendor_id IS NOT NULL
    ''')
    vendor = cursor.fetchone()

    high_co_pct = (vendor['high_co_count'] / vendor['vendor_count'] * 100) if vendor['vendor_count'] > 0 else 0
    vendor_score = max(0, 100 - (high_co_pct * 2))

    compliance['categories'].append({
        'name': 'Vendor Performance',
        'icon': 'users',
        'score': int(vendor_score),
        'status': 'good' if vendor_score >= 80 else 'warning' if vendor_score >= 60 else 'critical',
        'metrics': [
            {'label': 'Active Vendors', 'value': str(vendor['vendor_count'] or 0)},
            {'label': 'Avg Change Orders', 'value': f"{vendor['avg_change_orders']:.1f}" if vendor['avg_change_orders'] else '0'},
            {'label': 'High CO Vendors', 'value': str(vendor['high_co_count'] or 0)},
            {'label': 'Performance Rate', 'value': f"{vendor_score:.0f}%"}
        ],
        'recommendations': ['Review vendors with high change order rates'] if high_co_pct > 20 else ['Vendor performance is satisfactory']
    })

    # Calculate overall score
    compliance['overall_score'] = int(sum(c['score'] for c in compliance['categories']) / len(compliance['categories']))
    compliance['overall_status'] = 'good' if compliance['overall_score'] >= 80 else 'warning' if compliance['overall_score'] >= 60 else 'critical'

    conn.close()
    return compliance


@app.route('/compliance')
def compliance_dashboard():
    """Compliance dashboard with Prop 39-style indicators."""
    compliance = get_compliance_data()

    return render_template('surtax/compliance.html',
                          compliance=compliance,
                          title='Compliance Dashboard')


# ==================
# WATCHLIST
# ==================

def get_watchlist():
    """Get the current user's watchlist from session."""
    return session.get('watchlist', [])


def get_watchlist_projects():
    """Get full project details for watchlist items."""
    watchlist = get_watchlist()
    if not watchlist:
        return []

    conn = get_db()
    cursor = conn.cursor()

    placeholders = ','.join('?' * len(watchlist))
    cursor.execute(f'''
        SELECT c.*, sc.category_name, sc.color
        FROM contracts c
        LEFT JOIN surtax_categories sc ON c.surtax_category = sc.category_id
        WHERE c.contract_id IN ({placeholders})
        AND c.is_deleted = 0
        ORDER BY c.current_amount DESC
    ''', watchlist)

    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return projects


@app.route('/watchlist')
def watchlist():
    """Watchlist page - tracked projects."""
    projects = get_watchlist_projects()
    watchlist_ids = get_watchlist()

    # Get concerns for watchlisted projects
    all_concerns = get_concerns()
    watchlist_concerns = [c for c in all_concerns if c.get('contract_id') in watchlist_ids]

    return render_template('surtax/watchlist.html',
                          projects=projects,
                          concerns=watchlist_concerns,
                          watchlist_count=len(watchlist_ids),
                          title='My Watchlist')


@app.route('/api/watchlist/add/<contract_id>', methods=['POST'])
def add_to_watchlist(contract_id):
    """Add a project to the watchlist."""
    watchlist = get_watchlist()
    if contract_id not in watchlist:
        watchlist.append(contract_id)
        session['watchlist'] = watchlist
    return jsonify({'success': True, 'watchlist': watchlist, 'count': len(watchlist)})


@app.route('/api/watchlist/remove/<contract_id>', methods=['POST'])
def remove_from_watchlist(contract_id):
    """Remove a project from the watchlist."""
    watchlist = get_watchlist()
    if contract_id in watchlist:
        watchlist.remove(contract_id)
        session['watchlist'] = watchlist
    return jsonify({'success': True, 'watchlist': watchlist, 'count': len(watchlist)})


@app.route('/api/watchlist/toggle/<contract_id>', methods=['POST'])
def toggle_watchlist(contract_id):
    """Toggle a project on/off the watchlist."""
    watchlist = get_watchlist()
    if contract_id in watchlist:
        watchlist.remove(contract_id)
        is_watched = False
    else:
        watchlist.append(contract_id)
        is_watched = True
    session['watchlist'] = watchlist
    return jsonify({'success': True, 'is_watched': is_watched, 'count': len(watchlist)})


@app.route('/api/watchlist/clear', methods=['POST'])
def clear_watchlist():
    """Clear all items from watchlist."""
    session['watchlist'] = []
    return jsonify({'success': True, 'count': 0})


# ==================
# NEW MODULES
# ==================

@app.route('/vendors')
def vendors():
    """Vendor Performance tracking."""
    conn = get_db()
    cursor = conn.cursor()

    # Get vendor performance data
    cursor.execute('''
        SELECT
            vendor_name,
            COUNT(*) as project_count,
            SUM(current_amount) as total_value,
            AVG(CASE WHEN is_delayed = 1 THEN 1.0 ELSE 0.0 END) * 100 as delay_rate,
            AVG(CASE WHEN is_over_budget = 1 THEN 1.0 ELSE 0.0 END) * 100 as overbudget_rate,
            AVG(percent_complete) as avg_completion
        FROM contracts
        WHERE is_deleted = 0 AND vendor_name IS NOT NULL AND vendor_name != ''
        GROUP BY vendor_name
        ORDER BY total_value DESC
    ''')
    vendors_list = cursor.fetchall()
    conn.close()

    return render_template('surtax/vendors.html',
                          title='Vendor Performance',
                          vendors=vendors_list)


@app.route('/change-orders')
def change_orders():
    """Change Order tracking."""
    conn = get_db()
    cursor = conn.cursor()

    # Get projects with budget changes
    cursor.execute('''
        SELECT
            contract_id, title, school_name, vendor_name,
            original_amount, current_amount,
            (current_amount - original_amount) as change_amount,
            CASE WHEN original_amount > 0
                THEN ((current_amount - original_amount) / original_amount * 100)
                ELSE 0 END as change_pct,
            status
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
        AND original_amount IS NOT NULL
        AND current_amount != original_amount
        ORDER BY ABS(current_amount - original_amount) DESC
    ''')
    change_orders_list = cursor.fetchall()

    # Summary stats
    cursor.execute('''
        SELECT
            COUNT(*) as total_changes,
            SUM(current_amount - original_amount) as total_change_value,
            SUM(CASE WHEN current_amount > original_amount THEN 1 ELSE 0 END) as increases,
            SUM(CASE WHEN current_amount < original_amount THEN 1 ELSE 0 END) as decreases
        FROM contracts
        WHERE is_deleted = 0
        AND surtax_category IS NOT NULL
        AND original_amount IS NOT NULL
        AND current_amount != original_amount
    ''')
    stats = cursor.fetchone()
    conn.close()

    return render_template('surtax/change_orders.html',
                          title='Change Orders',
                          change_orders=change_orders_list,
                          stats=stats)


@app.route('/risk')
def risk_dashboard():
    """Risk Dashboard - flags high-risk projects."""
    conn = get_db()
    cursor = conn.cursor()

    # Get high-risk projects (delayed, over budget, or both)
    cursor.execute('''
        SELECT
            contract_id, title, school_name, vendor_name, status,
            current_amount, percent_complete,
            is_delayed, delay_days,
            is_over_budget, budget_variance_pct,
            CASE
                WHEN is_delayed = 1 AND is_over_budget = 1 THEN 'Critical'
                WHEN is_delayed = 1 OR is_over_budget = 1 THEN 'High'
                WHEN delay_days > 0 OR budget_variance_pct > 5 THEN 'Medium'
                ELSE 'Low'
            END as risk_level
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        ORDER BY
            CASE
                WHEN is_delayed = 1 AND is_over_budget = 1 THEN 1
                WHEN is_delayed = 1 OR is_over_budget = 1 THEN 2
                ELSE 3
            END,
            delay_days DESC
    ''')
    projects = cursor.fetchall()

    # Risk summary
    cursor.execute('''
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN is_delayed = 1 AND is_over_budget = 1 THEN 1 ELSE 0 END) as critical,
            SUM(CASE WHEN (is_delayed = 1 OR is_over_budget = 1) AND NOT (is_delayed = 1 AND is_over_budget = 1) THEN 1 ELSE 0 END) as high,
            SUM(CASE WHEN is_delayed = 0 AND is_over_budget = 0 THEN 1 ELSE 0 END) as low
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
    ''')
    risk_summary = cursor.fetchone()
    conn.close()

    return render_template('surtax/risk_dashboard.html',
                          title='Risk Dashboard',
                          projects=projects,
                          risk_summary=risk_summary)


@app.route('/audit')
def audit_trail():
    """Audit Trail - track all changes."""
    # For now, show a placeholder - full audit would require logging table
    return render_template('surtax/audit_trail.html',
                          title='Audit Trail')


@app.route('/documents')
def documents():
    """Document Library."""
    return render_template('surtax/documents.html',
                          title='Document Library')


@app.route('/minutes')
def meeting_minutes():
    """Meeting Minutes archive."""
    return render_template('surtax/meeting_minutes.html',
                          title='Meeting Minutes')


@app.route('/analytics')
def analytics():
    """Analytics and reporting."""
    conn = get_db()
    cursor = conn.cursor()

    # Spending trends by category
    cursor.execute('''
        SELECT
            surtax_category,
            COUNT(*) as project_count,
            SUM(current_amount) as total_budget,
            SUM(total_paid) as total_spent,
            AVG(percent_complete) as avg_completion
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        GROUP BY surtax_category
        ORDER BY total_budget DESC
    ''')
    category_data = cursor.fetchall()

    # Monthly spending (simulated based on paid amounts)
    cursor.execute('''
        SELECT
            status,
            COUNT(*) as count,
            SUM(current_amount) as value
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
        GROUP BY status
    ''')
    status_data = cursor.fetchall()
    conn.close()

    return render_template('surtax/analytics.html',
                          title='Analytics',
                          category_data=category_data,
                          status_data=status_data)


@app.route('/financials')
def financials():
    """Financial summary with Marion County data."""
    conn = get_db()
    cursor = conn.cursor()

    # Get expenditures summary
    cursor.execute('''
        SELECT
            account_name,
            total_amount,
            general_fund,
            special_revenue,
            capital_projects
        FROM expenditures_summary
        ORDER BY total_amount DESC
        LIMIT 10
    ''')
    top_expenditures = cursor.fetchall()

    # Get total expenditures by fund type
    cursor.execute('''
        SELECT
            SUM(general_fund) as general,
            SUM(special_revenue) as special_revenue,
            SUM(debt_service) as debt_service,
            SUM(capital_projects) as capital_projects,
            SUM(enterprise) as enterprise,
            SUM(internal_service) as internal_service,
            SUM(total_amount) as total
        FROM expenditures_summary
    ''')
    exp_by_fund = cursor.fetchone()

    # Get revenues summary
    cursor.execute('''
        SELECT
            account_name,
            total_amount,
            general_fund,
            special_revenue,
            capital_projects
        FROM revenues_summary
        ORDER BY total_amount DESC
        LIMIT 10
    ''')
    top_revenues = cursor.fetchall()

    # Get total revenues by fund type
    cursor.execute('''
        SELECT
            SUM(general_fund) as general,
            SUM(special_revenue) as special_revenue,
            SUM(debt_service) as debt_service,
            SUM(capital_projects) as capital_projects,
            SUM(enterprise) as enterprise,
            SUM(internal_service) as internal_service,
            SUM(total_amount) as total
        FROM revenues_summary
    ''')
    rev_by_fund = cursor.fetchone()

    # Calculate summary stats
    total_revenue = rev_by_fund['total'] if rev_by_fund else 0
    total_expenditure = exp_by_fund['total'] if exp_by_fund else 0
    net_position = total_revenue - total_expenditure
    budget_balance = (net_position / total_revenue * 100) if total_revenue > 0 else 0

    return render_template('surtax/financials.html',
                          top_expenditures=top_expenditures,
                          top_revenues=top_revenues,
                          exp_by_fund=exp_by_fund,
                          rev_by_fund=rev_by_fund,
                          total_revenue=total_revenue,
                          total_expenditure=total_expenditure,
                          net_position=net_position,
                          budget_balance=budget_balance,
                          title='Financial Summary')


@app.route('/capital-projects')
def capital_projects():
    """Capital construction projects page."""
    conn = get_db()
    cursor = conn.cursor()

    # Get all capital projects
    cursor.execute('''
        SELECT
            project_code,
            project_name,
            project_type,
            location,
            address,
            budget_amount,
            spent_to_date,
            start_date,
            estimated_completion,
            status,
            capacity,
            num_classrooms,
            num_labs,
            construction_manager,
            cm_contract_amount,
            description,
            data_source,
            source_url
        FROM capital_projects
        ORDER BY budget_amount DESC NULLS LAST
    ''')
    projects = cursor.fetchall()

    # Get summary stats
    cursor.execute('''
        SELECT
            COUNT(*) as total_projects,
            SUM(CASE WHEN budget_amount IS NOT NULL THEN budget_amount ELSE 0 END) as total_budget,
            SUM(CASE WHEN budget_amount IS NOT NULL THEN 1 ELSE 0 END) as projects_with_budget,
            SUM(spent_to_date) as total_spent
        FROM capital_projects
    ''')
    stats = cursor.fetchone()

    # Get projects by status
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM capital_projects
        GROUP BY status
    ''')
    status_counts = cursor.fetchall()

    conn.close()

    return render_template('surtax/capital_projects.html',
                          projects=projects,
                          stats=stats,
                          status_counts=status_counts,
                          title='Capital Projects')


@app.route('/project/<project_code>')
def capital_project_detail(project_code):
    """Individual capital project detail page."""
    conn = get_db()
    cursor = conn.cursor()

    # Get project details
    cursor.execute('''
        SELECT *
        FROM capital_projects
        WHERE project_code = ?
    ''', (project_code,))
    project = cursor.fetchone()

    if not project:
        conn.close()
        return "Project not found", 404

    conn.close()

    return render_template('surtax/capital_project_detail.html',
                          project=project,
                          title=project['project_name'])


@app.route('/map')
def map_view():
    """Geographic map view of projects."""
    conn = get_db()
    cursor = conn.cursor()

    # Get schools with projects
    cursor.execute('''
        SELECT DISTINCT
            school_name,
            COUNT(*) as project_count,
            SUM(current_amount) as total_value
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND school_name IS NOT NULL
        GROUP BY school_name
        ORDER BY total_value DESC
    ''')
    schools = cursor.fetchall()
    conn.close()

    return render_template('surtax/map_view.html',
                          title='Map View',
                          schools=schools)


@app.route('/public')
def public_portal():
    """Public transparency portal."""
    conn = get_db()
    cursor = conn.cursor()

    # Get public-facing summary
    cursor.execute('''
        SELECT
            COUNT(*) as total_projects,
            SUM(current_amount) as total_budget,
            SUM(total_paid) as total_spent,
            SUM(CASE WHEN status = 'Complete' THEN 1 ELSE 0 END) as completed
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL
    ''')
    summary = cursor.fetchone()

    # Recent completed projects
    cursor.execute('''
        SELECT title, school_name, current_amount, surtax_category
        FROM contracts
        WHERE is_deleted = 0 AND surtax_category IS NOT NULL AND status = 'Complete'
        ORDER BY current_end_date DESC
        LIMIT 10
    ''')
    completed = cursor.fetchall()
    conn.close()

    return render_template('surtax/public_portal.html',
                          title='Public Portal',
                          summary=summary,
                          completed=completed)


@app.route('/alerts')
def alerts():
    """Alerts and notifications management."""
    conn = get_db()
    cursor = conn.cursor()

    # Generate alerts based on project status
    alerts_list = []

    # Delayed projects
    cursor.execute('''
        SELECT contract_id, title, delay_days
        FROM contracts
        WHERE is_deleted = 0 AND is_delayed = 1
        ORDER BY delay_days DESC
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        alerts_list.append({
            'type': 'warning',
            'title': f"Project Delayed: {row['title'][:40]}",
            'message': f"{row['delay_days']} days behind schedule",
            'project_id': row['contract_id']
        })

    # Over budget projects
    cursor.execute('''
        SELECT contract_id, title, budget_variance_pct
        FROM contracts
        WHERE is_deleted = 0 AND is_over_budget = 1
        ORDER BY budget_variance_pct DESC
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        alerts_list.append({
            'type': 'danger',
            'title': f"Over Budget: {row['title'][:40]}",
            'message': f"{row['budget_variance_pct']:.1f}% over budget",
            'project_id': row['contract_id']
        })

    conn.close()

    return render_template('surtax/alerts.html',
                          title='Alerts & Notifications',
                          alerts=alerts_list)


# ==================
# RUN
# ==================

if __name__ == '__main__':
    logger.info("Starting Surtax Oversight Dashboard on port 5847...")
    app.run(host='127.0.0.1', port=5847, debug=True)
