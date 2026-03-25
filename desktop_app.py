import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import os
from monitor import FaceMonitor
from locker import lock_pc

class SecurityMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Security Monitor - PC Lock System")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.monitor = FaceMonitor()
        self.running = False
        self.camera = None
        
        # Title
        title_label = tk.Label(root, text="🛡️ Security Monitor", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Owner Photo Section
        owner_frame = tk.LabelFrame(root, text="Step 1: Upload YOUR Photo (Owner)", font=("Arial", 12, "bold"))
        owner_frame.pack(padx=10, pady=10, fill="x")
        
        self.owner_label = tk.Label(owner_frame, text="No photo selected", fg="red", font=("Arial", 10))
        self.owner_label.pack(pady=5)
        
        owner_btn = tk.Button(owner_frame, text="📸 Select Your Photo", command=self.select_owner_photo, 
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        owner_btn.pack(pady=5)
        
        # Friends Photo Section
        friends_frame = tk.LabelFrame(root, text="Step 2: Upload Friends' Photos (Optional)", font=("Arial", 12, "bold"))
        friends_frame.pack(padx=10, pady=10, fill="x")
        
        self.friends_label = tk.Label(friends_frame, text="0 friends added", fg="blue", font=("Arial", 10))
        self.friends_label.pack(pady=5)
        
        friends_btn = tk.Button(friends_frame, text="👥 Add Friend's Photo", command=self.select_friend_photo,
                                bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        friends_btn.pack(pady=5)
        
        # Status Section
        status_frame = tk.LabelFrame(root, text="System Status", font=("Arial", 12, "bold"))
        status_frame.pack(padx=10, pady=10, fill="x")
        
        self.status_label = tk.Label(status_frame, text="⚠️ System Idle - Ready to Start", fg="orange", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Webcam Feed Display
        self.camera_label = tk.Label(root, bg="black", width=60, height=15)
        self.camera_label.pack(padx=10, pady=10)
        
        # Buttons Section
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="🚀 START MONITORING", command=self.start_monitoring,
                                    bg="#FF5722", fg="white", font=("Arial", 12, "bold"), padx=15, pady=10,
                                    state="disabled")
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ STOP", command=self.stop_monitoring,
                                   bg="#9C27B0", fg="white", font=("Arial", 12, "bold"), padx=15, pady=10,
                                   state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Owner registered flag
        self.owner_registered = False
        self.friends_count = 0
        
    def select_owner_photo(self):
        """Allow user to select their own photo"""
        file_path = filedialog.askopenfilename(
            title="Select YOUR Photo",
            filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.monitor.add_owner_face(file_path):
                self.owner_registered = True
                self.owner_label.config(text=f"✅ Owner registered: {os.path.basename(file_path)}", fg="green")
                self.start_btn.config(state="normal")
                messagebox.showinfo("Success", "Your face has been registered!")
            else:
                messagebox.showerror("Error", "Could not detect a face in the photo. Try another photo.")
    
    def select_friend_photo(self):
        """Allow user to add friend's photos"""
        file_path = filedialog.askopenfilename(
            title="Select Friend's Photo",
            filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.monitor.add_friend_face(file_path):
                self.friends_count += 1
                self.friends_label.config(text=f"✅ {self.friends_count} friend(s) added", fg="green")
                messagebox.showinfo("Success", f"Friend added! Total: {self.friends_count}")
            else:
                messagebox.showerror("Error", "Could not detect a face in the photo. Try another photo.")
    
    def start_monitoring(self):
        """Start the security monitoring"""
        if not self.owner_registered:
            messagebox.showerror("Error", "Please register your photo first!")
            return
        
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="🟢 SYSTEM ACTIVE - Monitoring...", fg="green")
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.camera = cv2.VideoCapture(0)
        
        if not self.camera.isOpened():
            self.status_label.config(text="❌ Webcam not found!", fg="red")
            self.running = False
            return
        
        while self.running:
            ret, frame = self.camera.read()
            
            if not ret:
                self.status_label.config(text="❌ Webcam error!", fg="red")
                break
            
            # Perform face detection
            threat, info = self.monitor.process_frame(frame)
            
            # Update status
            if threat:
                self.status_label.config(text=f"🔴 THREAT DETECTED: {info} - LOCKING PC!", fg="red")
                
                # LOCK THE PC IMMEDIATELY
                lock_pc()
                self.running = False
                messagebox.showwarning("Security Alert", f"PC Locked!\nReason: {info}")
                break
            else:
                self.status_label.config(text="🟢 System Clear - All Safe", fg="green")
            
            # Display the camera feed
            self.display_frame(frame)
            
            # Small delay to avoid excessive CPU usage
            self.root.after(30)
        
        if self.camera:
            self.camera.release()
        
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="⚠️ System Stopped", fg="orange")
    
    def display_frame(self, frame):
        """Display the camera frame in the GUI"""
        # Resize frame to fit the label
        frame = cv2.resize(frame, (480, 360))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)
        
        self.camera_label.config(image=photo)
        self.camera_label.image = photo  # Keep a reference
    
    def stop_monitoring(self):
        """Stop the security monitoring"""
        self.running = False
        self.status_label.config(text="⚠️ System Stopped", fg="orange")
        self.stop_btn.config(state="disabled")
        self.start_btn.config(state="normal")

def main():
    root = tk.Tk()
    app = SecurityMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
