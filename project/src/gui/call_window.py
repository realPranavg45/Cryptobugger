"""
Call Window for Active Video/Audio Calls
"""
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
import threading
import time

class CallWindow:
    """Window for active video/audio calls"""
    
    def __init__(self, parent, peer_id, call_type, peer_connection, end_call_callback):
        self.parent = parent
        self.peer_id = peer_id
        self.call_type = call_type
        self.peer_connection = peer_connection
        self.end_call_callback = end_call_callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"{call_type.title()} Call - {peer_id}")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a1a")
        
        # Call state
        self.call_active = True
        self.video_enabled = call_type == "video"
        self.audio_enabled = True
        self.muted = False
        
        # Video capture for local preview
        self.local_cap = None
        self.video_thread = None
        
        self.setup_gui()
        self.setup_video()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_gui(self):
        """Setup call window GUI"""
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with peer info
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        peer_label = ttk.Label(header_frame, 
                              text=f"Connected to: {self.peer_id}",
                              font=('Arial', 14, 'bold'))
        peer_label.pack(side=tk.LEFT)
        
        # Call duration
        self.duration_var = tk.StringVar(value="00:00")
        duration_label = ttk.Label(header_frame, 
                                  textvariable=self.duration_var,
                                  font=('Arial', 12))
        duration_label.pack(side=tk.RIGHT)
        
        # Video frame (if video call)
        if self.video_enabled:
            video_frame = ttk.Frame(main_frame)
            video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Remote video (main)
            self.remote_video_label = tk.Label(video_frame, 
                                              bg="#000000",
                                              text="Waiting for remote video...",
                                              fg="white",
                                              font=('Arial', 16))
            self.remote_video_label.pack(fill=tk.BOTH, expand=True)
            
            # Local video preview (small overlay)
            self.local_video_frame = tk.Frame(video_frame, bg="#333333")
            self.local_video_frame.place(relx=0.02, rely=0.02, relwidth=0.25, relheight=0.25)
            
            self.local_video_label = tk.Label(self.local_video_frame,
                                             bg="#000000",
                                             text="Local Video",
                                             fg="white",
                                             font=('Arial', 10))
            self.local_video_label.pack(fill=tk.BOTH, expand=True)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X)
        
        # Control buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(expand=True)
        
        # Mute button
        self.mute_btn = tk.Button(button_frame,
                                 text="🎤" if not self.muted else "🔇",
                                 font=('Arial', 16),
                                 bg="#4CAF50" if not self.muted else "#f44336",
                                 fg="white",
                                 width=4,
                                 command=self.toggle_mute)
        self.mute_btn.pack(side=tk.LEFT, padx=5)
        
        # Video toggle (if video call)
        if self.video_enabled:
            self.video_btn = tk.Button(button_frame,
                                      text="📹",
                                      font=('Arial', 16),
                                      bg="#4CAF50",
                                      fg="white",
                                      width=4,
                                      command=self.toggle_video)
            self.video_btn.pack(side=tk.LEFT, padx=5)
        
        # End call button
        self.end_btn = tk.Button(button_frame,
                                text="📞",
                                font=('Arial', 16),
                                bg="#f44336",
                                fg="white",
                                width=4,
                                command=self.end_call)
        self.end_btn.pack(side=tk.LEFT, padx=5)
        
        # Start call timer
        self.start_time = time.time()
        self.update_duration()
    
    def setup_video(self):
        """Setup video capture and display"""
        if self.video_enabled:
            try:
                # Try to open webcam
                self.local_cap = cv2.VideoCapture(0)
                if self.local_cap.isOpened():
                    self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
                    self.video_thread.start()
            except Exception as e:
                print(f"Error setting up video: {e}")
    
    def video_loop(self):
        """Video capture and display loop"""
        while self.call_active and self.local_cap and self.local_cap.isOpened():
            ret, frame = self.local_cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize for local preview
                local_frame = cv2.resize(frame_rgb, (160, 120))
                
                # Convert to PIL Image
                local_image = Image.fromarray(local_frame)
                local_photo = ImageTk.PhotoImage(local_image)
                
                # Update local video preview
                if hasattr(self, 'local_video_label'):
                    self.local_video_label.configure(image=local_photo, text="")
                    self.local_video_label.image = local_photo
            
            time.sleep(1/30)  # 30 FPS
    
    def update_duration(self):
        """Update call duration display"""
        if self.call_active:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.duration_var.set(f"{minutes:02d}:{seconds:02d}")
            
            # Schedule next update
            self.window.after(1000, self.update_duration)
    
    def toggle_mute(self):
        """Toggle audio mute"""
        self.muted = not self.muted
        self.mute_btn.configure(
            text="🔇" if self.muted else "🎤",
            bg="#f44336" if self.muted else "#4CAF50"
        )
        
        # TODO: Actually mute/unmute audio in peer connection
    
    def toggle_video(self):
        """Toggle video on/off"""
        self.video_enabled = not self.video_enabled
        self.video_btn.configure(
            bg="#4CAF50" if self.video_enabled else "#f44336"
        )
        
        if not self.video_enabled:
            # Show "Video Off" message
            self.local_video_label.configure(image="", text="Video Off")
        
        # TODO: Actually enable/disable video in peer connection
    
    def end_call(self):
        """End the call"""
        self.call_active = False
        self.end_call_callback()
        self.destroy()
    
    def on_close(self):
        """Handle window close"""
        self.end_call()
    
    def destroy(self):
        """Cleanup and destroy window"""
        self.call_active = False
        
        # Cleanup video capture
        if self.local_cap:
            self.local_cap.release()
        
        # Destroy window
        if self.window:
            self.window.destroy()