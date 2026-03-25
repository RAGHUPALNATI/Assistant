import cv2
import streamlit as st
import time
from monitor import FaceMonitor
from notifier import send_security_alert

def main():
    st.set_page_config(page_title="Security Monitor Pro", page_icon="🔒")
    st.title("🛡️ Portable Security Shield")
    st.sidebar.title("🔐 User Controls")

    # In-memory storage for authorized face encodings
    if 'monitor' not in st.session_state:
        st.session_state.monitor = FaceMonitor()
    
    if 'security_active' not in st.session_state:
        st.session_state.security_active = False

    if 'alert_sent' not in st.session_state:
        st.session_state.alert_sent = False

    # Side bar: Upload authorized users
    st.sidebar.subheader("👤 Step 1: Upload Your Photo (Owner)")
    owner_file = st.sidebar.file_uploader("Must be ONLY you", type=["jpg", "png", "jpeg"], key="owner")
    if owner_file:
        if st.session_state.monitor.add_owner_face(owner_file):
            st.sidebar.success("✅ Owner registered - system will ignore you.")
        else:
            st.sidebar.error("❌ Failed to process owner image.")

    st.sidebar.subheader("👥 Step 2: Upload Friends' Photos")
    friend_files = st.sidebar.file_uploader("Upload photos of friends (System will detect them and send alert)", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="friends")
    if friend_files:
        for file in friend_files:
            if st.session_state.monitor.add_friend_face(file):
                st.sidebar.success(f"Added friend: {file.name}")
            else:
                st.sidebar.error(f"Failed to add friend: {file.name}")

    st.sidebar.divider()
    
    # Toggle switch
    security_toggle = st.sidebar.checkbox("🚀 ACTIVATE Monitoring", value=st.session_state.security_active)
    st.session_state.security_active = security_toggle

    # Main dashboard
    if st.session_state.security_active:
        if not owner_file:
            st.error("⚠️ PLEASE UPLOAD YOUR PHOTO BEFORE STARTING SYSTEM!")
            return

        st.warning("🚨 SYSTEM ENGAGED. DO NOT LEAVE THE SYSTEM UNATTENDED.")
        
        # Initialize video capture
        cap = cv2.VideoCapture(0)
        
        # Frame placeholder
        frame_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Performance/Alert cooldown
        last_alert_time = 0
        
        while st.session_state.security_active:
            ret, frame = cap.read()
            if not ret:
                status_placeholder.error("Error: Webcam not accessible.")
                break
                
            # Perform detection & recognition
            threat, info = st.session_state.monitor.process_frame(frame)
            
            # Update visual status
            if threat:
                status_placeholder.error(f"⚡ ALERT: {info}")
                
                # Check for cooldown (don't spam email)
                current_time = time.time()
                if current_time - last_alert_time > 60: # 1 minute cooldown
                    send_security_alert('raghuvarmapalnati@gmail.com', info)
                    last_alert_time = current_time
                    st.toast("📧 Secret alert sent.")
            else:
                status_placeholder.success("✅ System Clear (Owner Detected or Empty)")
            
            # Show live webcam feed
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB")

        cap.release()
    else:
        st.info("System is currently idle. Upload photos and flip the switch to start monitoring.")

if __name__ == "__main__":
    main()
