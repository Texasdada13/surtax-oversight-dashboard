# Git Workflow - Feature Branch Strategy

## Overview
We use **feature branches** for all new work to keep master stable and allow for better code review and testing.

---

## Branch Naming Convention

Use descriptive branch names with category prefixes:

```
feature/name-of-feature       - New features
fix/bug-description           - Bug fixes
enhance/improvement-name      - Enhancements to existing features
docs/documentation-update     - Documentation only
refactor/code-improvement     - Code refactoring
```

### Examples:
- `feature/admin-interface`
- `feature/vendor-performance-page`
- `fix/change-order-sorting`
- `enhance/executive-dashboard-trends`
- `docs/api-documentation`

---

## Workflow for New Features

### Step 1: Create Feature Branch
```bash
# Make sure you're on master and up to date
cd "c:\Users\dada_\OneDrive\Documents\surtax-oversight-dashboard"
git checkout master
git pull origin master

# Create and switch to new feature branch
git checkout -b feature/your-feature-name
```

### Step 2: Work on Feature
```bash
# Make your changes
# Edit files, add new files, etc.

# Check what changed
git status
git diff

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature X with Y functionality

- Detail 1
- Detail 2
- Detail 3

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Step 3: Push Feature Branch
```bash
# Push to GitHub (creates branch on remote)
git push -u origin feature/your-feature-name
```

### Step 4: Create Pull Request
```bash
# Use GitHub CLI to create PR
gh pr create --title "Add feature X" --body "$(cat <<'EOF'
## Summary
Brief description of what this adds

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How to test this feature

## Screenshots
[If applicable]
EOF
)"

# OR create PR manually on GitHub.com
```

### Step 5: Review and Merge
```bash
# After review/approval, merge the PR on GitHub
# Then locally:
git checkout master
git pull origin master

# Delete local feature branch (optional)
git branch -d feature/your-feature-name
```

---

## Current Project Status

### Master Branch
✅ **Latest commit**: Enhanced project detail page with all 44 projects
✅ **Status**: Production-ready demo
✅ **Protected**: Should not be directly committed to (use feature branches)

### Upcoming Features (Should Use Feature Branches)

1. **feature/fix-broken-pages**
   - Fix vendors page
   - Fix change-orders page
   - Fix analytics page
   - Fix map view
   - Fix other non-working pages

2. **feature/executive-dashboard-enhancements**
   - Real data instead of hardcoded metrics
   - Trend indicators (↑↓)
   - Drill-down capability
   - Export to PDF
   - Date range selector

3. **feature/admin-interface**
   - Staff login/authentication
   - Data entry forms
   - Bulk import UI
   - Data verification tools

4. **feature/public-records-import**
   - Import inspection reports
   - Import meeting minutes
   - Import contractor evaluations
   - Update data source tracking

5. **feature/data-verification-ui**
   - Admin view of data sources
   - Bulk verification tools
   - Data quality dashboard
   - Missing data reports

---

## Quick Commands

### Start New Feature
```bash
git checkout master && git pull && git checkout -b feature/name
```

### Save Work
```bash
git add . && git commit -m "Description" && git push
```

### Switch Between Branches
```bash
git checkout master              # Switch to master
git checkout feature/my-feature  # Switch to feature branch
git branch                       # See all local branches
git branch -a                    # See all branches (including remote)
```

### Update Feature Branch with Latest Master
```bash
# If master has changes you want in your feature branch
git checkout feature/my-feature
git merge master
# Resolve any conflicts
git push
```

### Abandon Feature Branch
```bash
git checkout master
git branch -D feature/unwanted-feature  # Delete locally
git push origin --delete feature/unwanted-feature  # Delete on GitHub
```

---

## Example: Fixing Broken Pages

Let's say you want to fix the vendors page:

```bash
# 1. Create feature branch
git checkout master
git pull origin master
git checkout -b fix/vendors-page

# 2. Make changes to fix the page
# Edit app.py, templates/surtax/vendors.html, etc.

# 3. Test locally
# Browse to http://127.0.0.1:5847/vendors and verify it works

# 4. Commit
git add .
git commit -m "Fix vendors page with performance metrics

- Add vendor performance data display
- Fix routing and template errors
- Add contractor quality scores
- Add past projects list

Resolves issue with vendors page not loading.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 5. Push
git push -u origin fix/vendors-page

# 6. Create PR
gh pr create --title "Fix vendors page" --body "Fixes vendors page to show contractor performance metrics"

# 7. After merge on GitHub
git checkout master
git pull origin master
git branch -d fix/vendors-page
```

---

## Best Practices

### ✅ DO:
- Create feature branch for every new piece of work
- Keep feature branches focused on one thing
- Write descriptive commit messages
- Test your changes before pushing
- Keep feature branches up to date with master
- Delete feature branches after merging

### ❌ DON'T:
- Commit directly to master (except for hotfixes)
- Create massive feature branches that do too much
- Leave feature branches unmerged for weeks
- Mix unrelated changes in one branch
- Push broken code to any branch

---

## Commit Message Format

```
Short summary (50 chars or less)

Longer description if needed. Explain WHAT changed and WHY.
- Bullet points for multiple changes
- Keep lines under 72 characters
- Be specific and clear

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Good Examples:
```
Add vendor performance tracking to contractors tab

- Display quality scores with visual indicators
- Show past project count and success rate
- Add local hiring percentage
- Include safety record summary

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

```
Fix broken analytics page rendering

Analytics page was showing 500 error due to missing
data source. Added error handling and sample data
generation for demo purposes.

Fixes #12

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Bad Examples:
```
fix stuff                           # Too vague
Updated several files               # Not descriptive
WIP                                 # Work in progress should not be on master
changes                             # Completely useless
```

---

## Current Branches

**Master Branch**:
- Production-ready code
- Enhanced project detail page ✅
- All 44 projects with data ✅
- Hybrid data approach implemented ✅

**Recommended Next Feature Branches**:
1. `fix/broken-pages` - Fix non-working dashboard pages
2. `enhance/executive-dashboard` - Add real data and trends
3. `feature/admin-interface` - Build data entry interface
4. `docs/user-guide` - Create user documentation

---

## GitHub Integration

### Create PR from Command Line
```bash
# After pushing feature branch
gh pr create --title "Your PR title" \
             --body "Description of changes" \
             --base master \
             --head feature/your-branch
```

### Check PR Status
```bash
gh pr list                    # List all PRs
gh pr view 123                # View specific PR
gh pr checks                  # See CI checks status
```

### Merge PR
```bash
gh pr merge 123 --merge       # Merge PR (creates merge commit)
gh pr merge 123 --squash      # Squash and merge
```

---

## When to Commit Directly to Master

**ONLY in these cases:**
- Emergency hotfixes that need immediate deployment
- Tiny documentation typos (README.md fixes)
- Configuration changes that don't affect code

**For everything else: USE FEATURE BRANCHES**

---

## Summary

✅ **Current Status**: Master is clean with major enhancement committed
✅ **Going Forward**: All new work should be on feature branches
✅ **Workflow**: branch → work → commit → push → PR → review → merge
✅ **Benefits**: Cleaner history, easier reviews, safer deployments

Start your next feature with:
```bash
git checkout master && git pull && git checkout -b feature/my-new-feature
```

---

Last Updated: 2026-01-08
