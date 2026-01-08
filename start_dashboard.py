#!/usr/bin/env python3
"""
Surtax Oversight Dashboard Startup Script
Automatically starts the Flask server and opens the dashboard in your browser
"""

import subprocess
import webbrowser
import time
import sys
import os

def start_dashboard():
    """Start the Flask server and open browser."""
    print("=" * 50)
    print("Starting Surtax Oversight Dashboard")
    print("=" * 50)
    print()

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'app.py')

    # Check if app.py exists
    if not os.path.exists(app_path):
        print(f"ERROR: app.py not found at {app_path}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Change to the script directory
    os.chdir(script_dir)

    print("Starting Flask server on http://127.0.0.1:5847...")
    print()

    # Wait a moment for server to start
    time.sleep(2)

    # Open browser
    print("Opening dashboard in your browser...")
    webbrowser.open('http://127.0.0.1:5847')

    print()
    print("=" * 50)
    print("Dashboard is running!")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()

    # Start Flask server (this will block and show output)
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\nShutting down dashboard...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    start_dashboard()
