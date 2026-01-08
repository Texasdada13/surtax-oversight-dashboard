# Marion County School Surtax Oversight Dashboard

A focused, transparent dashboard for the Marion County School Capital Outlay Surtax Oversight Committee.

## Features

- **Overview Dashboard** - High-level statistics and spending trends
- **Project Tracking** - Comprehensive project listings with filtering
- **School Views** - Per-school project breakdowns
- **Concerns Monitoring** - Auto-detected issues requiring attention
- **AI Assistant** - Natural language Q&A about projects
- **Compliance Dashboard** - Prop 39-style compliance tracking
- **Annual Reports** - Automated report generation
- **Meeting Mode** - Presentation views for committee meetings
- **Watchlist** - Personal project tracking

## Quick Start

1. Install dependencies:
```bash
pip install Flask
```

2. Run the app:
```bash
python app.py
```

3. Open browser to: http://127.0.0.1:5847

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: TailwindCSS + Vanilla JavaScript
- **Charts**: Plotly.js

## Project Structure

```
surtax-oversight-dashboard/
├── app.py                  # Main Flask application
├── data/
│   └── contracts.db        # SQLite database
├── scripts/
│   ├── migrate_surtax_fields.py
│   └── map_school_projects.py
└── templates/
    └── surtax/             # HTML templates
```

## Port

The app runs on port **5847** by default.

## License

© Marion County School District
