# 🛡️ AI-Powered Stealth Security Monitor

A professional-grade, desktop-based security application designed to monitor your workstation when you step away.

### ✨ Key Features
- **Face Recognition**: Uses `face_recognition` and `OpenCV` to identify authorized users.
- **Whitelist System**: Easy photo uploads via GUI for defining 'Authorized' individuals.
- **Intruder Logic**: Detects unauthorized faces and multiple faces (anti-shoulder surfing).
- **Instant PC Lock**: Automatically locks the screen (Win+L) when an intruder is detected.
- **Simple Desktop GUI**: Built with Tkinter for a smooth, native Windows/Mac/Linux interface.
- **No Streamlit Needed**: Pure desktop application - just double-click to run!

### 🚀 Getting Started

1. **Install Dependencies** (One-time setup):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   
   **Windows**: Double-click `run_security_monitor.bat`
   
   **Mac/Linux**: Make executable and run:
   ```bash
   chmod +x run_security_monitor.sh
   ./run_security_monitor.sh
   ```
   
   Or run directly:
   ```bash
   python desktop_app.py
   ```

3. **How to Use**:
   - Click **"📸 Select Your Photo"** to register your face (Owner).
   - (Optional) Click **"👥 Add Friend's Photo"** to add trusted friends.
   - Click **"🚀 START MONITORING"** to activate the system.
   - Walk away from your laptop.
   - If someone else appears on camera, your PC **locks instantly** (Win+L).

### 🛡️ How It Works
- **Owner Detected**: System stays green ✅ - PC remains unlocked.
- **Friend/Stranger Detected**: System locks PC 🔒 immediately.
- **Multiple People**: System locks PC 🔒 (anti-shoulder surfing).

### 📁 Files Included
- **`desktop_app.py`**: Main desktop GUI application.
- **`monitor.py`**: Face recognition and threat detection logic.
- **`locker.py`**: OS-level PC locking mechanism.
- **`run_security_monitor.bat`**: Quick launcher for Windows.
- **`run_security_monitor.sh`**: Quick launcher for Mac/Linux.
- **`requirements.txt`**: Python dependencies.

### 🤖 Author
Designed for Raghupalnati - Desktop Security Monitoring.

