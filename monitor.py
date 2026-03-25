import cv2
import face_recognition
import numpy as np
from PIL import Image

class FaceMonitor:
    def __init__(self, authorized_face_encodings=None):
        """
        Initializes the face recognition monitor.
        authorized_face_encodings: List of encodings for authorized users.
        """
        self.owner_encoding = None  # Specifically your face
        self.friend_encodings = []   # Your friends who are allowed but trigger a 'Friend' alert
        self.detected_threat = False
        self.last_alert_time = 0 
        
    def add_owner_face(self, image_input):
        """Processes and sets the image as the 'Owner' (you) - No alerts for you."""
        try:
            image = Image.open(image_input)
            img_array = np.array(image)
            face_locations = face_recognition.face_locations(img_array)
            face_encodings = face_recognition.face_encodings(img_array, face_locations)
            
            if len(face_encodings) > 0:
                self.owner_encoding = face_encodings[0]
                return True
            return False
        except Exception as e:
            print(f"Error processing owner image: {e}")
            return False

    def add_friend_face(self, image_input):
        """Processes and adds image to 'Friends' - Allows access but sends alert."""
        try:
            image = Image.open(image_input)
            img_array = np.array(image)
            face_locations = face_recognition.face_locations(img_array)
            face_encodings = face_recognition.face_encodings(img_array, face_locations)
            
            if len(face_encodings) > 0:
                self.friend_encodings.append(face_encodings[0])
                return True
            return False
        except Exception as e:
            print(f"Error processing friend image: {e}")
            return False

    def process_frame(self, frame):
        """
        Analyzes a single webcam frame for threats.
        Logic:
        1. If Owner (You) is detected -> NO ALERT (System is safe).
        2. If Friend is detected -> SEND ALERT (Identifying them).
        3. If Stranger is detected -> SEND ALERT.
        4. If Multiple people -> SEND ALERT.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Detect Threat Logic
        threat_detected = False
        threat_type = None

        if len(face_locations) == 0:
            return False, None

        # Threat 1: Multiple people detected (always a threat)
        if len(face_locations) > 1:
            threat_detected = True
            threat_type = "Multiple People Detected (Potential Shoulder Surfing)"
            return threat_detected, threat_type

        # Threat 2: Check the single face
        face_encoding = face_encodings[0]

        # Check if it's the Owner
        if self.owner_encoding is not None:
            match = face_recognition.compare_faces([self.owner_encoding], face_encoding, tolerance=0.6)
            if match[0]:
                return False, None # It's YOU! No alert.

        # Check if it's a Friend
        if self.friend_encodings:
            friend_matches = face_recognition.compare_faces(self.friend_encodings, face_encoding, tolerance=0.6)
            if any(friend_matches):
                threat_detected = True
                threat_type = "Authorized Friend detected looking at laptop"
                return threat_detected, threat_type

        # If it's not the owner and not a friend -> Stranger
        threat_detected = True
        threat_type = "Stranger/Unknown Person detected"
        
        return threat_detected, threat_type
