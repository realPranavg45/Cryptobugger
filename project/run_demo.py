#!/usr/bin/env python3
"""
Demo Script - Run Multiple Instances for Testing
"""
import subprocess
import sys
import time
import threading

def run_server():
    """Run the signaling server"""
    print("🌐 Starting signaling server...")
    subprocess.run([sys.executable, "server.py"])

def run_client(user_id):
    """Run a client instance"""
    print(f"👤 Starting client for user: {user_id}")
    # You would modify main.py to accept command line arguments for demo
    subprocess.run([sys.executable, "main.py", "--user-id", user_id])

def main():
    """Run demo with server and two clients"""
    print("🚀 WebRTC Calling Demo")
    print("======================")
    print("This will start:")
    print("1. Signaling server")
    print("2. Two client instances for testing")
    print()
    
    # Start server in background
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    print("✅ Server started")
    print("📱 You can now run multiple clients manually:")
    print("   python main.py")
    print()
    print("💡 Tips for testing:")
    print("   - Use different User IDs (e.g., 'Alice', 'Bob')")
    print("   - Both clients will connect to localhost:8765")
    print("   - Try video and audio calls between them")
    print()
    print("Press Ctrl+C to stop the server")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped")

if __name__ == "__main__":
    main()