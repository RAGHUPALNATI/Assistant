#!/bin/bash
# Security Monitor Desktop Application Launcher
# Make executable: chmod +x run_security_monitor.sh
# Then double-click or run: ./run_security_monitor.sh

echo "Starting Security Monitor..."
python3 desktop_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Could not start the application!"
    echo "Please make sure:"
    echo "1. Python 3 is installed"
    echo "2. All files are in the same folder"
    echo "3. Run: pip install -r requirements.txt"
    echo ""
    read -p "Press Enter to close..."
fi
