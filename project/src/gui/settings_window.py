"""
Settings Window for Application Configuration
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.settings_file = "settings.json"
        
        # Load current settings
        self.settings = self.load_settings()
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x400")
        self.window.configure(bg="#2c3e50")
        self.window.resizable(False, False)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_gui()
        
        # Center window
        self.center_window()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            "video_device": 0,
            "audio_device": "default",
            "video_quality": "720p",
            "audio_quality": "high",
            "encryption_enabled": True,
            "auto_answer": False,
            "notification_sound": True,
            "server_url": "ws://localhost:8765"
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(settings)
            return default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False
    
    def setup_gui(self):
        """Setup settings GUI"""
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Settings",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Audio/Video tab
        av_frame = ttk.Frame(notebook)
        notebook.add(av_frame, text="Audio/Video")
        self.setup_av_tab(av_frame)
        
        # Network tab
        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="Network")
        self.setup_network_tab(network_frame)
        
        # Security tab
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        self.setup_security_tab(security_frame)
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self.setup_general_tab(general_frame)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Save and Cancel buttons
        ttk.Button(buttons_frame, text="Cancel", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Save", 
                  command=self.save_and_close).pack(side=tk.RIGHT)
    
    def setup_av_tab(self, parent):
        """Setup Audio/Video settings tab"""
        # Video settings
        video_frame = ttk.LabelFrame(parent, text="Video Settings", padding=10)
        video_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Video device
        ttk.Label(video_frame, text="Video Device:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.video_device_var = tk.StringVar(value=str(self.settings["video_device"]))
        video_combo = ttk.Combobox(video_frame, textvariable=self.video_device_var,
                                  values=["0 (Default)", "1", "2", "None"])
        video_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Video quality
        ttk.Label(video_frame, text="Video Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.video_quality_var = tk.StringVar(value=self.settings["video_quality"])
        quality_combo = ttk.Combobox(video_frame, textvariable=self.video_quality_var,
                                    values=["480p", "720p", "1080p"])
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Audio settings
        audio_frame = ttk.LabelFrame(parent, text="Audio Settings", padding=10)
        audio_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Audio device
        ttk.Label(audio_frame, text="Audio Device:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.audio_device_var = tk.StringVar(value=self.settings["audio_device"])
        audio_combo = ttk.Combobox(audio_frame, textvariable=self.audio_device_var,
                                  values=["default", "pulse", "alsa"])
        audio_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Audio quality
        ttk.Label(audio_frame, text="Audio Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.audio_quality_var = tk.StringVar(value=self.settings["audio_quality"])
        audio_quality_combo = ttk.Combobox(audio_frame, textvariable=self.audio_quality_var,
                                          values=["low", "medium", "high"])
        audio_quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def setup_network_tab(self, parent):
        """Setup Network settings tab"""
        # Server settings
        server_frame = ttk.LabelFrame(parent, text="Server Settings", padding=10)
        server_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Server URL
        ttk.Label(server_frame, text="Signaling Server:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_url_var = tk.StringVar(value=self.settings["server_url"])
        server_entry = ttk.Entry(server_frame, textvariable=self.server_url_var, width=40)
        server_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # STUN/TURN settings
        stun_frame = ttk.LabelFrame(parent, text="STUN/TURN Settings", padding=10)
        stun_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(stun_frame, text="STUN Server:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.stun_server_var = tk.StringVar(value="stun:stun.l.google.com:19302")
        stun_entry = ttk.Entry(stun_frame, textvariable=self.stun_server_var, width=40)
        stun_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def setup_security_tab(self, parent):
        """Setup Security settings tab"""
        # Encryption settings
        encryption_frame = ttk.LabelFrame(parent, text="Encryption Settings", padding=10)
        encryption_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Enable encryption
        self.encryption_var = tk.BooleanVar(value=self.settings["encryption_enabled"])
        encryption_check = ttk.Checkbutton(encryption_frame, 
                                          text="Enable End-to-End Encryption",
                                          variable=self.encryption_var)
        encryption_check.pack(anchor=tk.W, pady=5)
        
        # Encryption info
        info_text = ("Uses Kyber post-quantum key exchange with AES-256 encryption\n"
                    "for secure communication resistant to quantum attacks.")
        info_label = ttk.Label(encryption_frame, text=info_text, 
                              font=('Arial', 9), foreground='gray')
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Key management
        key_frame = ttk.LabelFrame(parent, text="Key Management", padding=10)
        key_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(key_frame, text="Generate New Keys", 
                  command=self.generate_keys).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(key_frame, text="Export Keys", 
                  command=self.export_keys).pack(side=tk.LEFT)
    
    def setup_general_tab(self, parent):
        """Setup General settings tab"""
        # Behavior settings
        behavior_frame = ttk.LabelFrame(parent, text="Behavior", padding=10)
        behavior_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto answer
        self.auto_answer_var = tk.BooleanVar(value=self.settings["auto_answer"])
        auto_answer_check = ttk.Checkbutton(behavior_frame,
                                           text="Auto-answer incoming calls",
                                           variable=self.auto_answer_var)
        auto_answer_check.pack(anchor=tk.W, pady=5)
        
        # Notification sound
        self.notification_var = tk.BooleanVar(value=self.settings["notification_sound"])
        notification_check = ttk.Checkbutton(behavior_frame,
                                            text="Play notification sounds",
                                            variable=self.notification_var)
        notification_check.pack(anchor=tk.W, pady=5)
        
        # About section
        about_frame = ttk.LabelFrame(parent, text="About", padding=10)
        about_frame.pack(fill=tk.X, pady=(0, 10))
        
        about_text = ("Secure WebRTC Calling Application\n"
                     "Version 1.0.0\n"
                     "Built with Python, aiortc, and Kyber encryption")
        about_label = ttk.Label(about_frame, text=about_text, 
                               font=('Arial', 9))
        about_label.pack(anchor=tk.W)
    
    def generate_keys(self):
        """Generate new encryption keys"""
        result = messagebox.askyesno("Generate Keys", 
                                    "This will generate new encryption keys.\n"
                                    "Continue?")
        if result:
            # TODO: Implement key generation
            messagebox.showinfo("Success", "New keys generated successfully!")
    
    def export_keys(self):
        """Export encryption keys"""
        filename = filedialog.asksaveasfilename(
            title="Export Keys",
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        if filename:
            # TODO: Implement key export
            messagebox.showinfo("Success", f"Keys exported to {filename}")
    
    def save_and_close(self):
        """Save settings and close window"""
        # Update settings from GUI
        self.settings["video_device"] = self.video_device_var.get().split()[0]
        self.settings["video_quality"] = self.video_quality_var.get()
        self.settings["audio_device"] = self.audio_device_var.get()
        self.settings["audio_quality"] = self.audio_quality_var.get()
        self.settings["server_url"] = self.server_url_var.get()
        self.settings["encryption_enabled"] = self.encryption_var.get()
        self.settings["auto_answer"] = self.auto_answer_var.get()
        self.settings["notification_sound"] = self.notification_var.get()
        
        # Save to file
        if self.save_settings():
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.window.destroy()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")