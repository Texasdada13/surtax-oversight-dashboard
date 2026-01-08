# Surtax Oversight Dashboard - Implementation Plan

## Phase 1: Enhanced Project Detail Page (CURRENT)

### Database Schema Updates Needed
```sql
-- Add new fields to contracts table
ALTER TABLE contracts ADD COLUMN project_purpose TEXT;
ALTER TABLE contracts ADD COLUMN project_scope TEXT;
ALTER TABLE contracts ADD COLUMN community_impact TEXT;
ALTER TABLE contracts ADD COLUMN priority_level TEXT;
ALTER TABLE contracts ADD COLUMN risk_score TEXT;
ALTER TABLE contracts ADD COLUMN funding_sources JSON;
ALTER TABLE contracts ADD COLUMN contingency_remaining DECIMAL;
ALTER TABLE contracts ADD COLUMN cost_per_sqft DECIMAL;
ALTER TABLE contracts ADD COLUMN square_footage INTEGER;

-- Create new tables for enhanced tracking
CREATE TABLE project_phases (
    id INTEGER PRIMARY KEY,
    contract_id TEXT,
    phase_name TEXT,
    start_date DATE,
    end_date DATE,
    status TEXT,
    percent_complete DECIMAL
);

CREATE TABLE contractor_performance (
    id INTEGER PRIMARY KEY,
    vendor_id TEXT,
    safety_record TEXT,
    quality_score DECIMAL,
    past_projects_count INTEGER,
    deficiency_rate DECIMAL,
    local_hiring_percent DECIMAL
);

CREATE TABLE inspection_log (
    id INTEGER PRIMARY KEY,
    contract_id TEXT,
    inspection_date DATE,
    inspector_name TEXT,
    findings TEXT,
    deficiencies_count INTEGER,
    status TEXT
);

CREATE TABLE community_engagement (
    id INTEGER PRIMARY KEY,
    contract_id TEXT,
    meeting_date DATE,
    attendees INTEGER,
    feedback_summary TEXT,
    concerns_raised TEXT
);

CREATE TABLE committee_actions (
    id INTEGER PRIMARY KEY,
    contract_id TEXT,
    meeting_date DATE,
    action_item TEXT,
    assigned_to TEXT,
    status TEXT,
    due_date DATE
);
```

### New Template: Enhanced Project Detail
**File**: `templates/surtax/project_detail_enhanced.html`

**Sections to Build**:
1. ✅ Header with breadcrumb navigation
2. ✅ Budget cards (existing, enhance with sparklines)
3. 🔨 Risk Dashboard Card (Red/Yellow/Green indicators)
4. 🔨 Project Snapshot Card (Purpose, scope, priority)
5. 🔨 Tabbed Interface:
   - Tab 1: Overview (current view enhanced)
   - Tab 2: Financials (detailed breakdown)
   - Tab 3: Schedule (Gantt chart, milestones)
   - Tab 4: Quality & Safety
   - Tab 5: Change Orders Detail
   - Tab 6: Contractor Performance
   - Tab 7: Documents & Photos
   - Tab 8: Committee Actions & Meeting Notes
6. 🔨 Sidebar with Quick Facts, Recent Activity, Upcoming Milestones
7. 🔨 Action buttons (Watch, Download Report, Ask Question)

### Backend Routes to Add
```python
@app.route('/project/<contract_id>/financials')
def project_financials(contract_id):
    # Detailed financial breakdown

@app.route('/project/<contract_id>/schedule')
def project_schedule(contract_id):
    # Timeline and milestone tracking

@app.route('/project/<contract_id>/quality')
def project_quality(contract_id):
    # Inspection reports, photos, deficiencies

@app.route('/project/<contract_id>/contractor')
def project_contractor(contract_id):
    # Contractor performance metrics
```

---

## Phase 2: Fix Non-Working Pages

### Pages to Audit & Fix:
- [ ] `/vendors` - Vendor Performance page
- [ ] `/change-orders` - Change Order tracking
- [ ] `/risk` - Risk Dashboard
- [ ] `/audit` - Audit Trail
- [ ] `/documents` - Document Library
- [ ] `/minutes` - Meeting Minutes
- [ ] `/analytics` - Analytics & Reporting
- [ ] `/map` - Geographic Map View
- [ ] `/public` - Public Portal
- [ ] `/alerts` - Alerts & Notifications

### For Each Page:
1. Test current functionality
2. Document what's broken/missing
3. Add sample data if needed
4. Implement missing features
5. Add to navigation if not present

---

## Phase 3: Executive Dashboard Enhancements

### Current Executive Dashboard Improvements:
- [ ] Make metrics pull from real database (currently hardcoded)
- [ ] Add trend indicators (up/down arrows with % change)
- [ ] Add drill-down capability (click cards to filter)
- [ ] Implement "Fullscreen" button functionality
- [ ] Add export to PDF functionality
- [ ] Add date range selector
- [ ] Add comparison view (YoY, QoQ)

### New Executive Features:
- [ ] Executive Summary Generator (AI-powered)
- [ ] Key Insights Panel (auto-detected trends)
- [ ] Watchlist Quick Access
- [ ] Calendar Integration (upcoming meetings, deadlines)
- [ ] Quick Actions Menu (approve, flag, note)

---

## Phase 4: Data Quality & Integration

### Data Needs:
- [ ] Import real Marion County project data
- [ ] Populate contractor performance history
- [ ] Add inspection records
- [ ] Import meeting minutes/notes
- [ ] Add document attachments
- [ ] Link to GIS/mapping data
- [ ] Import community feedback

### Data Migration Scripts:
- [ ] `scripts/import_projects.py`
- [ ] `scripts/import_contractors.py`
- [ ] `scripts/import_inspections.py`
- [ ] `scripts/generate_sample_data.py` (for demo)

---

## Phase 5: Advanced Features

### AI/ML Enhancements:
- [ ] Predictive delay warnings
- [ ] Budget overrun forecasting
- [ ] Contractor risk scoring
- [ ] Anomaly detection
- [ ] Natural language report generation

### Collaboration Features:
- [ ] User accounts & roles (Committee members, Staff, Public)
- [ ] Comments/Notes on projects
- [ ] Task assignment & tracking
- [ ] Email notifications
- [ ] Voting/Approval workflow

### Reporting:
- [ ] Automated monthly reports
- [ ] Custom report builder
- [ ] Export to Excel/PDF
- [ ] Email distribution lists
- [ ] Public-facing summaries

---

## Technical Debt & Cleanup

### Code Quality:
- [ ] Add comprehensive error handling
- [ ] Implement logging
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Document all functions
- [ ] Code review & refactor

### Performance:
- [ ] Database indexing
- [ ] Query optimization
- [ ] Caching strategy
- [ ] Asset minification
- [ ] Lazy loading images

### Security:
- [ ] Input validation
- [ ] SQL injection prevention (use parameterized queries)
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Authentication/Authorization

---

## Priority Order

### Week 1 (High Priority):
1. ✅ Enhanced Project Detail Page (Main view)
2. Database schema updates
3. Fix broken navigation links
4. Audit all existing pages

### Week 2 (Medium Priority):
1. Implement tabbed interface on project detail
2. Fix non-working pages (vendors, change orders, etc.)
3. Executive dashboard real data integration
4. Add sample/demo data

### Week 3 (Nice-to-Have):
1. Advanced visualizations
2. Export functionality
3. Email notifications
4. Public portal enhancements

---

## Notes & Decisions Log

### Design Decisions:
- Using TailwindCSS for consistency
- Dark theme for executive dashboard (per user preference)
- Mobile-responsive throughout
- Accessibility considerations (WCAG 2.1 AA)

### Technology Stack:
- Backend: Flask (Python)
- Database: SQLite (consider PostgreSQL for production)
- Frontend: TailwindCSS + Vanilla JS
- Charts: Plotly.js
- Future: Consider adding htmx for interactivity

### Questions to Resolve:
- [ ] Should we support multiple districts/counties?
- [ ] What level of public access should be allowed?
- [ ] How should we handle document storage? (S3, local, database?)
- [ ] Email server configuration for notifications?
- [ ] Backup strategy?

---

## Success Metrics

### Committee Effectiveness:
- Time to find project information (target: <30 seconds)
- Questions answered per meeting (track improvement)
- Member satisfaction survey scores
- Action item completion rate

### System Performance:
- Page load time (<2 seconds)
- Uptime (99.9% target)
- User engagement (pages per session)
- Error rate (<0.1%)

---

## Resources & References

### Documentation:
- Flask: https://flask.palletsprojects.com/
- TailwindCSS: https://tailwindcss.com/docs
- Plotly: https://plotly.com/javascript/

### Inspiration:
- California Prop 39 dashboards
- OpenGov transparency platforms
- ProjectManager.com interfaces

---

Last Updated: 2026-01-08
