"""
Screenshot Tool for Surtax Oversight Dashboard
Automatically captures screenshots of all pages and tabs in the application.

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python screenshot_app.py
    python screenshot_app.py --mobile      # Include mobile/tablet views
    python screenshot_app.py --dark        # Include dark mode (if supported)
"""

import os
import sys
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Configuration
BASE_URL = "http://127.0.0.1:5847"
OUTPUT_DIR = "screenshots"

# Viewport configurations
VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}

# Define all pages and their tabs/interactions
PAGES = [
    {
        "name": "Overview",
        "url": "/overview",
        "wait_for": ".grid"
    },
    {
        "name": "Executive Dashboard",
        "url": "/",
        "wait_for": ".grid"
    },
    {
        "name": "Projects",
        "url": "/projects",
        "wait_for": "table",
        "filters": [
            {"name": "Delayed", "params": "?delayed=1"},
            {"name": "Over Budget", "params": "?over_budget=1"},
            {"name": "Delayed and Over Budget", "params": "?delayed=1&over_budget=1"},
            {"name": "Status In Progress", "params": "?status=In Progress"},
            {"name": "Status Completed", "params": "?status=Completed"},
        ]
    },
    {
        "name": "Schools",
        "url": "/schools",
        "wait_for": ".grid",
        "click_filters": [
            {"name": "Elementary", "selector": "button:has-text('Elementary')"},
            {"name": "Middle", "selector": "button:has-text('Middle')"},
            {"name": "High", "selector": "button:has-text('High')"},
        ]
    },
    {
        "name": "Ask AI",
        "url": "/ask",
        "wait_for": "textarea"
    },
    {
        "name": "Concerns",
        "url": "/concerns",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Watchlist",
        "url": "/watchlist",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Risk Dashboard",
        "url": "/risk",
        "wait_for": "table"
    },
    {
        "name": "Audit Trail",
        "url": "/audit",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Capital Projects",
        "url": "/capital-projects",
        "wait_for": "table"
    },
    {
        "name": "Change Orders",
        "url": "/change-orders",
        "wait_for": "table"
    },
    {
        "name": "Vendors",
        "url": "/vendors",
        "wait_for": "table"
    },
    {
        "name": "Analytics",
        "url": "/analytics",
        "wait_for": ".grid"
    },
    {
        "name": "Financials",
        "url": "/financials",
        "wait_for": ".grid"
    },
    {
        "name": "Document Library",
        "url": "/documents",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Meeting Minutes",
        "url": "/minutes",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Meeting Prep",
        "url": "/meeting",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Meeting Presentation",
        "url": "/meeting/present",
        "wait_for": ".min-h-screen"
    },
    {
        "name": "Compliance",
        "url": "/compliance",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Report",
        "url": "/report",
        "wait_for": ".space-y-6"
    },
    {
        "name": "Report Print View",
        "url": "/report/print",
        "wait_for": ".print-container, body"
    },
    {
        "name": "Map View",
        "url": "/map",
        "wait_for": "#map"
    },
    {
        "name": "Public Portal",
        "url": "/public",
        "wait_for": ".min-h-screen"
    },
    {
        "name": "Alerts",
        "url": "/alerts",
        "wait_for": ".space-y-6"
    },
]

# Project detail page has tabs
PROJECT_DETAIL_TABS = [
    "overview",
    "financials",
    "schedule",
    "quality",
    "contractor",
    "community",
    "committee",
    "documents"
]


def sanitize_filename(name):
    """Convert a name to a safe filename."""
    return name.lower().replace(" ", "_").replace("/", "_").replace("?", "_").replace("&", "_")


async def take_screenshot(page, name, output_path):
    """Take a screenshot and save it."""
    await page.screenshot(path=output_path, full_page=True)
    print(f"  [OK] Captured: {name}")


async def capture_page(page, page_config, output_dir, viewport_name="desktop"):
    """Capture a single page and its variations."""
    name = page_config["name"]
    url = page_config["url"]
    wait_for = page_config.get("wait_for", "body")
    prefix = f"{viewport_name}_" if viewport_name != "desktop" else ""

    # Navigate to page
    await page.goto(f"{BASE_URL}{url}")

    # Wait for content to load
    try:
        await page.wait_for_selector(wait_for, timeout=10000)
    except:
        print(f"  [WARN] Warning: Could not find {wait_for} on {name}")

    # Small delay for any animations
    await asyncio.sleep(0.5)

    # Take main screenshot
    filename = f"{prefix}{sanitize_filename(name)}.png"
    await take_screenshot(page, f"{name} ({viewport_name})" if viewport_name != "desktop" else name,
                          os.path.join(output_dir, filename))

    # Capture URL-based filter variations if defined
    if "filters" in page_config and viewport_name == "desktop":
        for filter_config in page_config["filters"]:
            filter_name = filter_config["name"]
            filter_params = filter_config["params"]

            await page.goto(f"{BASE_URL}{url}{filter_params}")
            try:
                await page.wait_for_selector(wait_for, timeout=10000)
            except:
                pass
            await asyncio.sleep(0.5)

            filename = f"{sanitize_filename(name)}_{sanitize_filename(filter_name)}.png"
            await take_screenshot(page, f"{name} - {filter_name}", os.path.join(output_dir, filename))

    # Capture click-based filter variations if defined
    if "click_filters" in page_config and viewport_name == "desktop":
        for filter_config in page_config["click_filters"]:
            filter_name = filter_config["name"]
            selector = filter_config["selector"]

            # Navigate back to clean page
            await page.goto(f"{BASE_URL}{url}")
            try:
                await page.wait_for_selector(wait_for, timeout=10000)
            except:
                pass
            await asyncio.sleep(0.3)

            # Click the filter
            try:
                await page.click(selector)
                await asyncio.sleep(0.3)

                filename = f"{sanitize_filename(name)}_{sanitize_filename(filter_name)}.png"
                await take_screenshot(page, f"{name} - {filter_name}", os.path.join(output_dir, filename))
            except Exception as e:
                print(f"  [WARN] Warning: Could not click filter {filter_name}: {e}")


async def capture_project_detail_tabs(page, output_dir, project_url, project_name=""):
    """Capture all tabs on a project detail page."""
    await page.goto(f"{BASE_URL}{project_url}")

    try:
        await page.wait_for_selector(".tab-button", timeout=10000)
    except:
        print("  [WARN] Warning: Could not find tabs on project detail page")
        return

    await asyncio.sleep(0.5)

    prefix = f"{sanitize_filename(project_name)}_" if project_name else "project_detail_"

    for tab in PROJECT_DETAIL_TABS:
        # Click the tab
        try:
            await page.click(f"#tab-{tab}")
            await asyncio.sleep(0.3)  # Wait for tab content to show

            filename = f"{prefix}tab_{tab}.png"
            display_name = f"{project_name} - {tab.title()} Tab" if project_name else f"Project Detail - {tab.title()} Tab"
            await take_screenshot(page, display_name, os.path.join(output_dir, filename))
        except Exception as e:
            print(f"  [WARN] Warning: Could not capture tab {tab}: {e}")


async def get_project_urls_by_type(page):
    """Get URLs of different project types (critical, completed, etc.)."""
    projects = {}

    # Get a critical risk project
    await page.goto(f"{BASE_URL}/risk")
    try:
        await page.wait_for_selector("table a", timeout=10000)
        link = await page.query_selector("table tr:has-text('CRITICAL') a[href*='/project/']")
        if link:
            projects["critical"] = await link.get_attribute("href")
    except:
        pass

    # Get a completed project
    await page.goto(f"{BASE_URL}/projects?status=Completed")
    try:
        await page.wait_for_selector("table a", timeout=10000)
        link = await page.query_selector("table a[href*='/project/']")
        if link:
            projects["completed"] = await link.get_attribute("href")
    except:
        pass

    # Get a regular in-progress project
    await page.goto(f"{BASE_URL}/projects?status=In Progress")
    try:
        await page.wait_for_selector("table a", timeout=10000)
        link = await page.query_selector("table a[href*='/project/']")
        if link:
            projects["in_progress"] = await link.get_attribute("href")
    except:
        pass

    return projects


async def get_sample_capital_project_url(page):
    """Get the URL of a sample capital project."""
    await page.goto(f"{BASE_URL}/capital-projects")

    try:
        await page.wait_for_selector("table a", timeout=10000)
        link = await page.query_selector("table a[href*='/project/']")
        if link:
            href = await link.get_attribute("href")
            return href
    except:
        pass

    return None


async def get_sample_school_url(page):
    """Get the URL of a sample school from the schools page."""
    await page.goto(f"{BASE_URL}/schools")

    try:
        await page.wait_for_selector("a[href*='/school/']", timeout=10000)
        link = await page.query_selector("a[href*='/school/']")
        if link:
            href = await link.get_attribute("href")
            return href
    except:
        pass

    return None


async def capture_modals(page, output_dir):
    """Capture modal dialogs throughout the application."""
    modals_captured = []

    # Concerns page - Type Info Modal
    print("  Capturing Concerns type info modal...")
    await page.goto(f"{BASE_URL}/concerns")
    try:
        await page.wait_for_selector(".space-y-6", timeout=10000)
        await asyncio.sleep(0.5)

        # Find and click a "Learn more" button to open the modal
        learn_more_btn = await page.query_selector("button:has-text('Learn more')")
        if learn_more_btn:
            await learn_more_btn.click()
            await asyncio.sleep(0.3)

            # Wait for modal to appear
            modal = await page.query_selector("#typeModal:not(.hidden)")
            if modal:
                await take_screenshot(page, "Concerns - Type Info Modal",
                                     os.path.join(output_dir, "modal_concerns_type_info.png"))
                modals_captured.append("Concerns Type Info")

                # Close the modal
                await page.keyboard.press("Escape")
                await asyncio.sleep(0.2)
    except Exception as e:
        print(f"    [WARN] Could not capture concerns modal: {e}")

    # Concerns page - Education Guide expanded
    print("  Capturing Concerns education guide...")
    try:
        await page.goto(f"{BASE_URL}/concerns")
        await page.wait_for_selector(".space-y-6", timeout=10000)
        await asyncio.sleep(0.3)

        # Click "Show Guide" button if it exists
        guide_btn = await page.query_selector("button:has-text('Show Guide')")
        if guide_btn:
            await guide_btn.click()
            await asyncio.sleep(0.3)
            await take_screenshot(page, "Concerns - Education Guide",
                                 os.path.join(output_dir, "concerns_education_guide.png"))
            modals_captured.append("Concerns Education Guide")
    except Exception as e:
        print(f"    [WARN] Could not capture education guide: {e}")

    return modals_captured


async def capture_dark_mode(page, output_dir):
    """Capture pages in dark mode if supported."""
    dark_pages = [
        {"name": "Overview Dark", "url": "/overview", "wait_for": ".grid"},
        {"name": "Executive Dashboard Dark", "url": "/", "wait_for": ".grid"},
        {"name": "Projects Dark", "url": "/projects", "wait_for": "table"},
        {"name": "Risk Dashboard Dark", "url": "/risk", "wait_for": "table"},
    ]

    # Check if there's a dark mode toggle
    await page.goto(BASE_URL)
    await asyncio.sleep(0.5)

    # Try to find and click dark mode toggle (common patterns)
    dark_toggle = await page.query_selector("[data-theme-toggle], .dark-mode-toggle, #darkModeToggle, button:has-text('Dark')")

    if dark_toggle:
        await dark_toggle.click()
        await asyncio.sleep(0.3)

        for page_config in dark_pages:
            try:
                await page.goto(f"{BASE_URL}{page_config['url']}")
                await page.wait_for_selector(page_config["wait_for"], timeout=10000)
                await asyncio.sleep(0.3)

                filename = f"dark_{page_config['name'].lower().replace(' ', '_')}.png"
                await take_screenshot(page, page_config["name"], os.path.join(output_dir, filename))
            except Exception as e:
                print(f"    [WARN] Could not capture {page_config['name']}: {e}")

        return True
    else:
        print("  [WARN] No dark mode toggle found")
        return False


async def main():
    """Main function to capture all screenshots."""
    # Parse command line arguments
    include_mobile = "--mobile" in sys.argv
    include_dark = "--dark" in sys.argv

    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Create subdirectories
    if include_mobile:
        os.makedirs(os.path.join(output_dir, "mobile"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "tablet"), exist_ok=True)

    print(f"\n{'='*60}")
    print("Surtax Dashboard Screenshot Tool")
    print(f"{'='*60}")
    print(f"Output directory: {output_dir}")
    print(f"Base URL: {BASE_URL}")
    print(f"Options: mobile={include_mobile}, dark={include_dark}")
    print(f"{'='*60}\n")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)

        # Desktop context
        desktop_context = await browser.new_context(
            viewport=VIEWPORTS["desktop"]
        )
        page = await desktop_context.new_page()

        # Test connection
        print("Testing connection to dashboard...")
        try:
            await page.goto(BASE_URL, timeout=5000)
            print("[OK] Connected successfully\n")
        except Exception as e:
            print(f"[ERROR] Could not connect to {BASE_URL}")
            print(f"  Make sure the Flask server is running (start_dashboard.bat)")
            await browser.close()
            return

        # Capture all main pages (desktop)
        print("Capturing main pages (desktop)...")
        print("-" * 40)
        for page_config in PAGES:
            try:
                await capture_page(page, page_config, output_dir, "desktop")
            except Exception as e:
                print(f"  [ERROR] Error capturing {page_config['name']}: {e}")

        print()

        # Capture project detail pages with tabs for different project types
        print("Capturing project detail pages by type...")
        print("-" * 40)
        project_urls = await get_project_urls_by_type(page)

        for project_type, project_url in project_urls.items():
            if project_url:
                print(f"  Capturing {project_type} project tabs...")
                await capture_project_detail_tabs(page, output_dir, project_url, f"project_{project_type}")

        # If no typed projects found, capture generic
        if not project_urls:
            await page.goto(f"{BASE_URL}/projects")
            try:
                await page.wait_for_selector("table a", timeout=10000)
                link = await page.query_selector("table a[href*='/project/']")
                if link:
                    href = await link.get_attribute("href")
                    await capture_project_detail_tabs(page, output_dir, href, "project_detail")
            except:
                print("  [WARN] Could not find any projects to capture tabs")

        print()

        # Capture capital project detail
        print("Capturing capital project detail...")
        print("-" * 40)
        capital_url = await get_sample_capital_project_url(page)
        if capital_url:
            await page.goto(f"{BASE_URL}{capital_url}")
            await asyncio.sleep(0.5)
            await take_screenshot(page, "Capital Project Detail", os.path.join(output_dir, "capital_project_detail.png"))
        else:
            print("  [WARN] Could not find a capital project to capture")

        print()

        # Capture school detail page
        print("Capturing school detail page...")
        print("-" * 40)
        school_url = await get_sample_school_url(page)
        if school_url:
            await page.goto(f"{BASE_URL}{school_url}")
            await asyncio.sleep(0.5)
            await take_screenshot(page, "School Detail", os.path.join(output_dir, "school_detail.png"))
        else:
            print("  [WARN] Could not find a sample school to capture")

        print()

        # Capture modals and dialogs
        print("Capturing modals and dialogs...")
        print("-" * 40)
        modals = await capture_modals(page, output_dir)
        if modals:
            print(f"  Captured {len(modals)} modal(s)")

        # Capture dark mode if requested
        if include_dark:
            print()
            print("Capturing dark mode views...")
            print("-" * 40)
            dark_captured = await capture_dark_mode(page, output_dir)

        await desktop_context.close()

        # Mobile and tablet views
        if include_mobile:
            print()
            print("Capturing mobile and tablet views...")
            print("-" * 40)

            # Key pages to capture in mobile/tablet
            responsive_pages = [
                {"name": "Overview", "url": "/overview", "wait_for": ".grid"},
                {"name": "Executive Dashboard", "url": "/", "wait_for": ".grid"},
                {"name": "Projects", "url": "/projects", "wait_for": "table"},
                {"name": "Risk Dashboard", "url": "/risk", "wait_for": "table"},
                {"name": "Financials", "url": "/financials", "wait_for": ".grid"},
                {"name": "Public Portal", "url": "/public", "wait_for": ".min-h-screen"},
            ]

            for viewport_name in ["tablet", "mobile"]:
                print(f"  {viewport_name.title()} viewport...")
                context = await browser.new_context(viewport=VIEWPORTS[viewport_name])
                resp_page = await context.new_page()

                for page_config in responsive_pages:
                    try:
                        await capture_page(resp_page, page_config,
                                          os.path.join(output_dir, viewport_name),
                                          viewport_name)
                    except Exception as e:
                        print(f"    [ERROR] Error: {e}")

                await context.close()

        await browser.close()

    # Summary
    total_screenshots = 0
    for root, dirs, files in os.walk(output_dir):
        total_screenshots += len([f for f in files if f.endswith('.png')])

    print(f"\n{'='*60}")
    print(f"Complete! Captured {total_screenshots} screenshots")
    print(f"Location: {os.path.abspath(output_dir)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
