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
    'main': {
        'label': 'Main',
        'visible_to': ['committee', 'staff'],
        'items': [
            {
                'id': 'index',
                'label': 'Overview',
                'path': '/',
                'icon': 'home',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'projects',
                'label': 'Projects',
                'path': '/projects',
                'icon': 'briefcase',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'schools',
                'label': 'Schools',
                'path': '/schools',
                'icon': 'building',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'ask_ai',
                'label': 'Ask AI',
                'path': '/ask',
                'icon': 'chat',
                'visible_to': ['committee', 'staff']
            }
        ]
    },
    'monitoring': {
        'label': 'Monitoring',
        'visible_to': ['committee', 'staff'],
        'items': [
            {
                'id': 'concerns',
                'label': 'Concerns',
                'path': '/concerns',
                'icon': 'alert',
                'badge': 'concerns_count',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'watchlist',
                'label': 'Watchlist',
                'path': '/watchlist',
                'icon': 'star',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'risk',
                'label': 'Risk Dashboard',
                'path': '/risk',
                'icon': 'shield',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'audit',
                'label': 'Audit Trail',
                'path': '/audit',
                'icon': 'clock',
                'visible_to': ['staff']  # HIDDEN from committee
            }
        ]
    },
    'financials': {
        'label': 'Financials',
        'visible_to': ['committee', 'staff'],
        'items': [
            {
                'id': 'financials',
                'label': 'Financials',
                'path': '/financials',
                'icon': 'chart',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'capital_projects',
                'label': 'Capital Projects',
                'path': '/capital-projects',
                'icon': 'building',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'change_orders',
                'label': 'Change Orders',
                'path': '/change-orders',
                'icon': 'document',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'vendors',
                'label': 'Vendors',
                'path': '/vendors',
                'icon': 'users',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'analytics',
                'label': 'Analytics',
                'path': '/analytics',
                'icon': 'chart-bar',
                'visible_to': ['staff']  # HIDDEN from committee
            }
        ]
    },
    'documents': {
        'label': 'Documents',
        'visible_to': ['committee', 'staff'],
        'items': [
            {
                'id': 'documents',
                'label': 'Document Library',
                'path': '/documents',
                'icon': 'folder',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'meeting_minutes',
                'label': 'Meeting Minutes',
                'path': '/minutes',
                'icon': 'document-text',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'annual_report',
                'label': 'Annual Report',
                'path': '/report',
                'icon': 'document-report',
                'visible_to': ['committee', 'staff']
            }
        ]
    },
    'tools': {
        'label': 'Tools',
        'visible_to': ['committee', 'staff'],
        'items': [
            {
                'id': 'meeting_mode',
                'label': 'Meeting Mode',
                'path': '/meeting',
                'icon': 'presentation',
                'visible_to': ['committee', 'staff']
            },
            {
                'id': 'compliance',
                'label': 'Compliance',
                'path': '/compliance',
                'icon': 'clipboard-check',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'map',
                'label': 'Map View',
                'path': '/map',
                'icon': 'map',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'public',
                'label': 'Public Portal',
                'path': '/public',
                'icon': 'globe',
                'visible_to': ['staff']  # HIDDEN from committee
            },
            {
                'id': 'alerts',
                'label': 'Alerts',
                'path': '/alerts',
                'icon': 'bell',
                'visible_to': ['staff']  # HIDDEN from committee
            }
        ]
    }
}

# Icon mappings to Heroicons SVG paths
ICON_PATHS = {
    'home': 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
    'briefcase': 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    'building': 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    'chat': 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
    'alert': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    'star': 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z',
    'shield': 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
    'clock': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'chart': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    'document': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'users': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    'chart-bar': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    'folder': 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z',
    'document-text': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'document-report': 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'presentation': 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    'clipboard-check': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    'map': 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7',
    'globe': 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'bell': 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
}

# Guided AI prompts for committee members
GUIDED_AI_PROMPTS = [
    {
        'id': 'revenue_vs_projections',
        'category': 'Financial Oversight',
        'label': 'Revenue vs Projections',
        'button_text': 'Compare revenue to projections',
        'prompt': 'Summarize year-to-date surtax revenue compared with projections. Explain any variance and its impact on the project timeline in plain language suitable for committee members.',
        'context': ['financials', 'projects'],
        'icon': 'chart-bar'
    },
    {
        'id': 'ballot_language_compliance',
        'category': 'Compliance',
        'label': 'Ballot Language Alignment',
        'button_text': 'Verify ballot language compliance',
        'prompt': 'Verify whether current surtax expenditures align with ballot language and capital outlay requirements. List any potential concerns.',
        'context': ['financials', 'compliance'],
        'icon': 'clipboard-check'
    },
    {
        'id': 'delayed_projects_summary',
        'category': 'Project Status',
        'label': 'Projects Behind Schedule',
        'button_text': 'Explain projects behind schedule',
        'prompt': 'List all projects that are behind schedule and explain the main reasons for delays in plain language. Prioritize by impact.',
        'context': ['projects', 'concerns'],
        'icon': 'clock'
    },
    {
        'id': 'overbudget_projects_summary',
        'category': 'Budget Concerns',
        'label': 'Projects Over Budget',
        'button_text': 'Identify projects over budget',
        'prompt': 'Identify all projects that are over budget and summarize the cost drivers. Highlight what I should ask staff about.',
        'context': ['projects', 'concerns', 'change-orders'],
        'icon': 'chart'
    },
    {
        'id': 'meeting_talking_points',
        'category': 'Meeting Prep',
        'label': 'Meeting Talking Points',
        'button_text': 'Prepare 3-bullet meeting summary',
        'prompt': 'Prepare a three-bullet explanation of current project status and budget adjustments that I can read aloud at the committee meeting. Make it clear and concise.',
        'context': ['projects', 'financials', 'concerns'],
        'icon': 'presentation'
    },
    {
        'id': 'public_communication_status',
        'category': 'Public Transparency',
        'label': 'Public Communication',
        'button_text': 'Review public communication efforts',
        'prompt': 'How is the district currently communicating surtax spending and project status to the public? Are there gaps in transparency?',
        'context': ['projects', 'documents'],
        'icon': 'globe'
    },
    {
        'id': 'contingency_forecast',
        'category': 'Financial Planning',
        'label': 'Multi-Year Forecast',
        'button_text': 'Explain forecast & contingency',
        'prompt': "Explain the district's multi-year surtax forecast and contingency plan. What are the major assumptions and risks?",
        'context': ['financials', 'projects'],
        'icon': 'chart-bar'
    },
    {
        'id': 'vendor_performance',
        'category': 'Vendor Oversight',
        'label': 'Vendor Performance',
        'button_text': 'Summarize vendor performance',
        'prompt': 'Summarize the performance of major contractors/vendors. Flag any concerns about quality, timeliness, or cost overruns.',
        'context': ['vendors', 'projects', 'concerns'],
        'icon': 'users'
    },
    {
        'id': 'high_priority_concerns',
        'category': 'Risk Assessment',
        'label': 'Top Risks',
        'button_text': 'Highlight top 3 risks',
        'prompt': 'What are the top 3 risks the oversight committee should discuss at the next meeting? Explain each in plain language.',
        'context': ['concerns', 'risk', 'projects'],
        'icon': 'alert'
    },
    {
        'id': 'public_summary',
        'category': 'Public Communication',
        'label': 'Public Summary',
        'button_text': 'Turn into public summary',
        'prompt': 'Turn the current project and financial status into a 2-minute summary suitable for reading aloud to the public. Use simple language.',
        'context': ['projects', 'financials'],
        'icon': 'document-text'
    }
]


def get_visible_navigation(persona='committee'):
    """
    Filter navigation based on persona.

    Args:
        persona: The current user persona ('committee' or 'staff')

    Returns:
        Filtered navigation dictionary
    """
    if not ENABLE_PERSONA_SYSTEM:
        # Persona system disabled, return all navigation (staff view)
        return NAVIGATION

    filtered_nav = {}
    for section_key, section in NAVIGATION.items():
        # Check if section is visible to this persona
        if persona in section.get('visible_to', []):
            filtered_items = [
                item for item in section['items']
                if persona in item.get('visible_to', [])
            ]
            # Only include section if it has visible items
            if filtered_items:
                filtered_nav[section_key] = {
                    **section,
                    'items': filtered_items
                }

    return filtered_nav


def get_icon_path(icon_name):
    """Get SVG path for an icon by name."""
    return ICON_PATHS.get(icon_name, ICON_PATHS['document'])
