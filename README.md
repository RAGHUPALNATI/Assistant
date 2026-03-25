# 🛡️ AI-Powered Stealth Security Monitor

A professional-grade, privacy-focused security application designed to monitor your workstation when you step away.

### ✨ Key Features
- **Face Recognition**: Uses `face_recognition` and `OpenCV` to identify authorized users.
- **Whitelist System**: Easy photo uploads via Streamlit for defining 'Authorized' individuals.
- **Intruder Logic**: Detects unauthorized faces and multiple faces (anti-shoulder surfing).
- **Silent Email Alerts**: Automatically sends a discrete notification to `raghuvarmapalnati@gmail.com` without alerting the intruder.
- **Effortless UI**: Built with Streamlit for a smooth toggle-based interface.

### 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Credentials**:
   Set environment variables for your Gmail account (using a Google App Password):
   ```bash
   export SENDER_EMAIL="your-email@gmail.com"
   export SENDER_PASSWORD="your-google-app-password"
   ```
3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

### 🤝 Author
Designed for Raghupalnati - Security Monitoring.

