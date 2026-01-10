"""Helper functions for persona-aware rendering."""

from flask import g


def persona_can_see(feature_id, persona=None):
    """
    Check if current persona can see a feature.

    Args:
        feature_id: The ID of the feature to check
        persona: Optional persona override, defaults to current persona

    Returns:
        Boolean indicating visibility
    """
    if persona is None:
        persona = g.get('persona', 'committee')

    # Staff can see everything
    if persona == 'staff':
        return True

    # Define what committee can see
    committee_features = {
        'overview', 'projects', 'schools', 'ask_ai',
        'concerns', 'watchlist', 'risk',
        'financials', 'documents', 'meeting_minutes', 'annual_report',
        'meeting_mode'
    }

    return feature_id in committee_features


def get_overview_template_for_persona(persona='committee'):
    """
    Return appropriate overview template based on persona.

    Args:
        persona: The current user persona

    Returns:
        Template path string
    """
    if persona == 'committee':
        return 'surtax/committee_overview.html'
    else:
        return 'surtax/executive_dashboard.html'


def should_hide_sidebar(endpoint, persona='committee'):
    """
    Determine if sidebar should be hidden for a given route and persona.

    Args:
        endpoint: Flask endpoint name
        persona: Current persona

    Returns:
        Boolean indicating if sidebar should be hidden
    """
    # Hide sidebar for committee in meeting modes
    if persona == 'committee' and endpoint in ['meeting_mode', 'meeting_present']:
        return True

    return False
