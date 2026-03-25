@echo off
REM Security Monitor Desktop Application Launcher
REM Double-click this file to start the security monitor

echo Starting Security Monitor...
python desktop_app.py

if errorlevel 1 (
    echo.
    echo Error: Python not found or desktop_app.py missing!
    echo Please make sure:
    echo 1. Python is installed and added to PATH
    echo 2. All files are in the same folder
    echo 3. Run: pip install -r requirements.txt
    pause
)
