@echo off
REM Surtax Oversight Dashboard Startup Script
REM This script starts the Flask server and opens the dashboard in your browser

echo ========================================
echo Starting Surtax Oversight Dashboard
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Start Flask server in background
echo Starting Flask server on http://127.0.0.1:5847...
start /B python app.py

REM Wait 3 seconds for server to start
timeout /t 3 /nobreak >nul

REM Open dashboard in default browser
echo Opening dashboard in your browser...
start http://127.0.0.1:5847

echo.
echo ========================================
echo Dashboard is running!
echo Press Ctrl+C in this window to stop the server
echo ========================================
echo.

REM Keep the window open and show server output
python app.py
