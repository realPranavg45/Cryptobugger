"""
Main GUI Window for WebRTC Calling Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import logging
from typing import Optional
import cv2
from PIL import Image, ImageTk
import numpy as np

from ..webrtc.peer_connection import WebRTCPeerConnection
from ..signaling.websocket_client import SignalingClient
from ..crypto.kyber import KyberKeyExchange
from .call_window import CallWindow
from .settings_window import SettingsWindow

logger = logging.getLogger(__name__)

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure WebRTC Calling")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Application state
        self.user_id = None
        self.signaling_client = None
        self.peer_connection = None
        self.kyber_exchange = KyberKeyExchange()
        self.connected_users = []
        self.current_call = None
        self.call_window = None
        
        # Async event loop
        self.loop = None
        self.loop_thread = None
        
        # Setup GUI
        self.setup_gui()
        self.setup_styles()
        
        # Start async loop
        self.start_async_loop()
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background='#2c3e50',
                       foreground='#ecf0f1')
        
        style.configure('Status.TLabel',
                       font=('Arial', 10),
                       background='#2c3e50',
                       foreground='#95a5a6')
        
        style.configure('User.TLabel',
                       font=('Arial', 12),
                       background='#34495e',
                       foreground='#ecf0f1',
                       padding=10)
    
    def setup_gui(self):
        """Setup the main GUI"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Secure WebRTC Calling",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection", padding=15)
        conn_frame.pack(fill=tk.X, pady=(0, 20))
        
        # User ID entry
        ttk.Label(conn_frame, text="Your ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_id_var = tk.StringVar()
        self.user_id_entry = ttk.Entry(conn_frame, textvariable=self.user_id_var, width=20)
        self.user_id_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Server URL entry
        ttk.Label(conn_frame, text="Server:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.server_var = tk.StringVar(value="ws://localhost:8765")
        self.server_entry = ttk.Entry(conn_frame, textvariable=self.server_var, width=30)
        self.server_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Connect button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=0, column=2, rowspan=2, padx=(20, 0), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(conn_frame, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        # Users frame
        users_frame = ttk.LabelFrame(main_frame, text="Online Users", padding=15)
        users_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Users listbox with scrollbar
        list_frame = ttk.Frame(users_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.users_listbox = tk.Listbox(list_frame, 
                                       bg="#34495e", 
                                       fg="#ecf0f1",
                                       selectbackground="#3498db",
                                       font=('Arial', 11))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.users_listbox.yview)
        self.users_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Call buttons frame
        call_frame = ttk.Frame(main_frame)
        call_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.video_call_btn = ttk.Button(call_frame, text="📹 Video Call", 
                                        command=lambda: self.initiate_call("video"))
        self.video_call_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.audio_call_btn = ttk.Button(call_frame, text="🎤 Audio Call", 
                                        command=lambda: self.initiate_call("audio"))
        self.audio_call_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.settings_btn = ttk.Button(call_frame, text="⚙️ Settings", 
                                      command=self.open_settings)
        self.settings_btn.pack(side=tk.RIGHT)
        
        # Initially disable call buttons
        self.video_call_btn.configure(state=tk.DISABLED)
        self.audio_call_btn.configure(state=tk.DISABLED)
    
    def start_async_loop(self):
        """Start asyncio event loop in separate thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        
        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()
    
    def run_async(self, coro):
        """Run coroutine in async loop"""
        if self.loop:
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
            return future.result()
    
    def connect_to_server(self):
        """Connect to signaling server"""
        user_id = self.user_id_var.get().strip()
        server_url = self.server_var.get().strip()
        
        if not user_id:
            messagebox.showerror("Error", "Please enter your User ID")
            return
        
        if not server_url:
            messagebox.showerror("Error", "Please enter server URL")
            return
        
        try:
            self.user_id = user_id
            self.signaling_client = SignalingClient(server_url)
            
            # Setup signaling callbacks
            self.setup_signaling_callbacks()
            
            # Connect asynchronously
            asyncio.run_coroutine_threadsafe(
                self.signaling_client.connect(user_id), 
                self.loop
            )
            
            self.status_var.set("Connecting...")
            self.connect_btn.configure(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
    
    def setup_signaling_callbacks(self):
        """Setup signaling event callbacks"""
        
        async def on_user_list(data):
            users = data.get("users", [])
            # Remove self from list
            users = [u for u in users if u != self.user_id]
            self.connected_users = users
            
            # Update GUI in main thread
            self.root.after(0, self.update_users_list)
        
        async def on_call_offer(data):
            caller_id = data.get("from")
            offer = data.get("offer")
            call_type = data.get("call_type", "video")
            
            # Show incoming call dialog in main thread
            self.root.after(0, lambda: self.show_incoming_call(caller_id, offer, call_type))
        
        async def on_call_answer(data):
            answer = data.get("answer")
            if self.peer_connection:
                await self.peer_connection.set_remote_description(answer)
        
        async def on_call_reject(data):
            self.root.after(0, lambda: messagebox.showinfo("Call Rejected", "Call was rejected"))
            self.cleanup_call()
        
        async def on_call_end(data):
            self.root.after(0, lambda: messagebox.showinfo("Call Ended", "Call was ended"))
            self.cleanup_call()
        
        async def on_ice_candidate(data):
            candidate = data.get("candidate")
            if self.peer_connection:
                await self.peer_connection.add_ice_candidate(candidate)
        
        # Register callbacks
        self.signaling_client.on("user_list", on_user_list)
        self.signaling_client.on("call_offer", on_call_offer)
        self.signaling_client.on("call_answer", on_call_answer)
        self.signaling_client.on("call_reject", on_call_reject)
        self.signaling_client.on("call_end", on_call_end)
        self.signaling_client.on("ice_candidate", on_ice_candidate)
        
        # Connection established
        def on_connected():
            self.status_var.set(f"Connected as {self.user_id}")
            self.video_call_btn.configure(state=tk.NORMAL)
            self.audio_call_btn.configure(state=tk.NORMAL)
        
        self.root.after(2000, on_connected)  # Simulate connection delay
    
    def update_users_list(self):
        """Update the users listbox"""
        self.users_listbox.delete(0, tk.END)
        for user in self.connected_users:
            self.users_listbox.insert(tk.END, user)
    
    def initiate_call(self, call_type):
        """Initiate a call to selected user"""
        selection = self.users_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user to call")
            return
        
        target_user = self.users_listbox.get(selection[0])
        
        async def make_call():
            try:
                # Generate Kyber keypair
                public_key = self.kyber_exchange.generate_keypair()
                
                # Create peer connection
                self.peer_connection = WebRTCPeerConnection(self.signaling_client)
                
                # Start local media
                video = call_type == "video"
                await self.peer_connection.start_local_media(video=video, audio=True)
                
                # Create offer
                offer = await self.peer_connection.create_offer()
                
                # Send call offer
                await self.signaling_client.call_user(target_user, offer, call_type)
                
                # Open call window
                self.root.after(0, lambda: self.open_call_window(target_user, call_type))
                
            except Exception as e:
                logger.error(f"Error making call: {e}")
                self.root.after(0, lambda: messagebox.showerror("Call Error", str(e)))
        
        asyncio.run_coroutine_threadsafe(make_call(), self.loop)
    
    def show_incoming_call(self, caller_id, offer, call_type):
        """Show incoming call dialog"""
        result = messagebox.askyesno(
            "Incoming Call", 
            f"Incoming {call_type} call from {caller_id}\n\nAccept?"
        )
        
        if result:
            self.accept_call(caller_id, offer, call_type)
        else:
            self.reject_call(caller_id)
    
    def accept_call(self, caller_id, offer, call_type):
        """Accept incoming call"""
        async def accept():
            try:
                # Generate Kyber keypair
                public_key = self.kyber_exchange.generate_keypair()
                
                # Create peer connection
                self.peer_connection = WebRTCPeerConnection(self.signaling_client)
                
                # Start local media
                video = call_type == "video"
                await self.peer_connection.start_local_media(video=video, audio=True)
                
                # Create answer
                answer = await self.peer_connection.create_answer(offer)
                
                # Send answer
                await self.signaling_client.answer_call(caller_id, answer)
                
                # Open call window
                self.root.after(0, lambda: self.open_call_window(caller_id, call_type))
                
            except Exception as e:
                logger.error(f"Error accepting call: {e}")
                self.root.after(0, lambda: messagebox.showerror("Call Error", str(e)))
        
        asyncio.run_coroutine_threadsafe(accept(), self.loop)
    
    def reject_call(self, caller_id):
        """Reject incoming call"""
        async def reject():
            await self.signaling_client.reject_call(caller_id)
        
        asyncio.run_coroutine_threadsafe(reject(), self.loop)
    
    def open_call_window(self, peer_id, call_type):
        """Open call window"""
        if self.call_window:
            self.call_window.destroy()
        
        self.call_window = CallWindow(
            self.root, 
            peer_id, 
            call_type, 
            self.peer_connection,
            self.end_call
        )
        self.current_call = peer_id
    
    def end_call(self):
        """End current call"""
        if self.current_call and self.signaling_client:
            async def end():
                await self.signaling_client.end_call(self.current_call)
            
            asyncio.run_coroutine_threadsafe(end(), self.loop)
        
        self.cleanup_call()
    
    def cleanup_call(self):
        """Cleanup call resources"""
        if self.call_window:
            self.call_window.destroy()
            self.call_window = None
        
        if self.peer_connection:
            async def cleanup():
                await self.peer_connection.close()
            
            asyncio.run_coroutine_threadsafe(cleanup(), self.loop)
            self.peer_connection = None
        
        self.current_call = None
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root)
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        finally:
            # Cleanup
            if self.loop:
                self.loop.call_soon_threadsafe(self.loop.stop)
            if self.signaling_client:
                asyncio.run_coroutine_threadsafe(
                    self.signaling_client.disconnect(), 
                    self.loop
                )