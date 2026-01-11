"""
Persona-based UI configuration for dashboard simplification.
Defines which features are visible to which user personas.
"""

# Feature flag to enable/disable entire persona system
ENABLE_PERSONA_SYSTEM = True

# Available personas
PERSONAS = {
    'committee': {
        'id': 'committee',
        'name': 'Committee Member',
        'description': 'Simplified view for oversight committee members',
        'is_default': True
    },
    'staff': {
        'id': 'staff',
        'name': 'District Staff',
        'description': 'Full access to all features and analytics',
        'is_default': False
    }
}

# Navigation configuration with visibility rules
NAVIGATION = {
    # Committee Member sees: Main + collapsible More Tools
    'main': {
        'label': 'Main',
        'visible_to': ['committee'],
        'collapsible': False,
        'items': [
            {'id': 'index', 'label': 'Overview', 'path': '/', 'icon': 'home', 'visible_to': ['committee']},
            {'id': 'ask_ai', 'label': 'Ask AI', 'path': '/ask', 'icon': 'chat', 'visible_to': ['committee']},
            {'id': 'concerns', 'label': 'Concerns', 'path': '/concerns', 'icon': 'alert', 'badge': 'concerns_count', 'visible_to': ['committee']},
            {'id': 'risk', 'label': 'Risk Dashboard', 'path': '/risk', 'icon': 'shield', 'visible_to': ['committee']},
            {'id': 'vendors', 'label': 'Vendors', 'path': '/vendors', 'icon': 'users', 'visible_to': ['committee']}
        ]
    },
    'more_tools': {
        'label': 'More Tools',
        'visible_to': ['committee'],
        'collapsible': True,
        'default_collapsed': True,
        'items': [
            {'id': 'projects', 'label': 'Projects', 'path': '/projects', 'icon': 'folder', 'visible_to': ['committee']},
            {'id': 'schools', 'label': 'Schools', 'path': '/schools', 'icon': 'school', 'visible_to': ['committee']},
            {'id': 'watchlist', 'label': 'Watchlist', 'path': '/watchlist', 'icon': 'star', 'visible_to': ['committee']},
            {'id': 'financials', 'label': 'Financials', 'path': '/financials', 'icon': 'dollarSign', 'visible_to': ['committee']},
            {'id': 'capital_projects', 'label': 'Capital Projects', 'path': '/capital-projects', 'icon': 'briefcase', 'visible_to': ['committee']},
            {'id': 'change_orders', 'label': 'Change Orders', 'path': '/change-orders', 'icon': 'document', 'visible_to': ['committee']},
            {'id': 'documents', 'label': 'Document Library', 'path': '/documents', 'icon': 'collection', 'visible_to': ['committee']},
            {'id': 'minutes', 'label': 'Meeting Minutes', 'path': '/minutes', 'icon': 'clipboard', 'visible_to': ['committee']},
            {'id': 'report', 'label': 'Annual Report', 'path': '/report', 'icon': 'document', 'visible_to': ['committee']},
            {'id': 'meeting', 'label': 'Meeting Mode', 'path': '/meeting', 'icon': 'presentation', 'visible_to': ['committee']},
            {'id': 'analytics', 'label': 'Analytics', 'path': '/analytics', 'icon': 'chartBar', 'visible_to': ['committee']},
            {'id': 'compliance', 'label': 'Compliance', 'path': '/compliance', 'icon': 'checkCircle', 'visible_to': ['committee']},
            {'id': 'map', 'label': 'Map View', 'path': '/map', 'icon': 'map', 'visible_to': ['committee']},
            {'id': 'public', 'label': 'Public Portal', 'path': '/public', 'icon': 'globe', 'visible_to': ['committee']},
            {'id': 'alerts', 'label': 'Alerts', 'path': '/alerts', 'icon': 'bell', 'visible_to': ['committee']},
            {'id': 'audit', 'label': 'Audit Trail', 'path': '/audit', 'icon': 'clock', 'visible_to': ['committee']}
        ]
    },

    # Staff sees traditional grouped navigation
    'staff_main': {
        'label': 'Main',
        'visible_to': ['staff'],
        'collapsible': False,
        'items': [
            {'id': 'index', 'label': 'Overview', 'path': '/', 'icon': 'home', 'visible_to': ['staff']},
            {'id': 'projects', 'label': 'Projects', 'path': '/projects', 'icon': 'folder', 'visible_to': ['staff']},
            {'id': 'schools', 'label': 'Schools', 'path': '/schools', 'icon': 'school', 'visible_to': ['staff']},
            {'id': 'ask_ai', 'label': 'Ask AI', 'path': '/ask', 'icon': 'chat', 'visible_to': ['staff']}
        ]
    },
    'staff_monitoring': {
        'label': 'Monitoring',
        'visible_to': ['staff'],
        'collapsible': False,
        'items': [
            {'id': 'concerns', 'label': 'Concerns', 'path': '/concerns', 'icon': 'alert', 'badge': 'concerns_count', 'visible_to': ['staff']},
            {'id': 'watchlist', 'label': 'Watchlist', 'path': '/watchlist', 'icon': 'star', 'visible_to': ['staff']},
            {'id': 'risk', 'label': 'Risk Dashboard', 'path': '/risk', 'icon': 'shield', 'visible_to': ['staff']},
            {'id': 'audit', 'label': 'Audit Trail', 'path': '/audit', 'icon': 'clock', 'visible_to': ['staff']},
            {'id': 'alerts', 'label': 'Alerts', 'path': '/alerts', 'icon': 'bell', 'visible_to': ['staff']}
        ]
    },
    'staff_financials': {
        'label': 'Financials',
        'visible_to': ['staff'],
        'collapsible': False,
        'items': [
            {'id': 'financials', 'label': 'Financials', 'path': '/financials', 'icon': 'dollarSign', 'visible_to': ['staff']},
            {'id': 'capital_projects', 'label': 'Capital Projects', 'path': '/capital-projects', 'icon': 'briefcase', 'visible_to': ['staff']},
            {'id': 'change_orders', 'label': 'Change Orders', 'path': '/change-orders', 'icon': 'document', 'visible_to': ['staff']},
            {'id': 'vendors', 'label': 'Vendors', 'path': '/vendors', 'icon': 'users', 'visible_to': ['staff']},
            {'id': 'analytics', 'label': 'Analytics', 'path': '/analytics', 'icon': 'chartBar', 'visible_to': ['staff']}
        ]
    },
    'staff_documents': {
        'label': 'Documents',
        'visible_to': ['staff'],
        'collapsible': False,
        'items': [
            {'id': 'documents', 'label': 'Document Library', 'path': '/documents', 'icon': 'collection', 'visible_to': ['staff']},
            {'id': 'meeting_minutes', 'label': 'Meeting Minutes', 'path': '/minutes', 'icon': 'clipboard', 'visible_to': ['staff']},
            {'id': 'annual_report', 'label': 'Annual Report', 'path': '/report', 'icon': 'document', 'visible_to': ['staff']}
        ]
    },
    'staff_tools': {
        'label': 'Tools',
        'visible_to': ['staff'],
        'collapsible': False,
        'items': [
            {'id': 'meeting_mode', 'label': 'Meeting Mode', 'path': '/meeting', 'icon': 'presentation', 'visible_to': ['staff']},
            {'id': 'compliance', 'label': 'Compliance', 'path': '/compliance', 'icon': 'checkCircle', 'visible_to': ['staff']},
            {'id': 'map', 'label': 'Map View', 'path': '/map', 'icon': 'map', 'visible_to': ['staff']},
            {'id': 'public', 'label': 'Public Portal', 'path': '/public', 'icon': 'globe', 'visible_to': ['staff']}
        ]
    }
}


def get_visible_navigation(persona='committee'):
    """Filter navigation based on persona."""
    if not ENABLE_PERSONA_SYSTEM:
        # If disabled, return all navigation
        return NAVIGATION

    filtered_nav = {}
    for section_key, section in NAVIGATION.items():
        if persona in section.get('visible_to', []):
            filtered_items = [
                item for item in section['items']
                if persona in item.get('visible_to', [])
            ]
            if filtered_items:
                filtered_nav[section_key] = {
                    **section,
                    'items': filtered_items
                }
    return filtered_nav


# Guided AI Prompts for Committee Members
GUIDED_AI_PROMPTS = [
    {
        'category': 'Financial Oversight',
        'button_text': 'Compare revenue to projections',
        'icon': 'dollarSign',
        'prompt': 'Compare the year-to-date surtax revenue collections against the approved projections. Highlight any significant variances and explain potential impacts on the approved project timeline.'
    },
    {
        'category': 'Compliance',
        'button_text': 'Verify ballot language compliance',
        'icon': 'checkCircle',
        'prompt': 'Review the current surtax expenditures and verify that all spending aligns with the ballot language approved by voters. Identify any concerns about compliance with the capital outlay statutory requirements.'
    },
    {
        'category': 'Project Status',
        'button_text': 'Explain projects behind schedule',
        'icon': 'clock',
        'prompt': 'Identify all projects that are currently behind schedule. For each delayed project, explain the root cause of the delay, the expected impact, and any mitigation plans in place.'
    },
    {
        'category': 'Budget Concerns',
        'button_text': 'Identify projects over budget',
        'icon': 'alert',
        'prompt': 'List all projects that are currently over budget or trending toward budget overruns. For each, summarize the cost drivers and whether additional funding sources are needed.'
    },
    {
        'category': 'Meeting Prep',
        'button_text': 'Prepare 3-bullet meeting summary',
        'icon': 'document',
        'prompt': 'Create a 3-bullet executive summary for the upcoming committee meeting that highlights: (1) key financial metrics, (2) major project updates, and (3) critical issues requiring committee attention.'
    },
    {
        'category': 'Public Transparency',
        'button_text': 'Review public communication efforts',
        'icon': 'globe',
        'prompt': 'Assess the district\'s current public communication and transparency efforts regarding surtax-funded projects. Identify any gaps in public reporting or opportunities to improve community awareness.'
    },
    {
        'category': 'Financial Planning',
        'button_text': 'Explain forecast & contingency',
        'icon': 'chart',
        'prompt': 'Explain the current multi-year surtax revenue forecast and the district\'s contingency plans if collections fall short of projections. Include any recommended adjustments to the project pipeline.'
    },
    {
        'category': 'Vendor Oversight',
        'button_text': 'Summarize vendor performance',
        'icon': 'users',
        'prompt': 'Summarize the performance of the top contractors working on surtax-funded projects. Highlight any quality concerns, delays, or exemplary performance that the committee should be aware of.'
    },
    {
        'category': 'Risk Assessment',
        'button_text': 'Highlight top 3 risks',
        'icon': 'shield',
        'prompt': 'Identify the top 3 risks currently facing the surtax program (financial, operational, or compliance-related). For each risk, explain the potential impact and recommended mitigation strategies.'
    },
    {
        'category': 'Public Communication',
        'button_text': 'Turn into public summary',
        'icon': 'presentation',
        'prompt': 'Convert the current dashboard data into a brief, plain-language summary suitable for public presentation. Focus on accomplishments, current status, and fiscal responsibility in 2-3 short paragraphs or 5-6 bullet points.'
    }
]
