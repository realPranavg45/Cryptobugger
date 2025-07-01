#!/usr/bin/env python3
"""
Standalone Signaling Server
Run this separately to provide signaling services
"""
import asyncio
import logging
from src.signaling.websocket_server import SignalingServer

def main():
    """Run the signaling server"""
    print("🌐 WebRTC Signaling Server")
    print("==========================")
    print("Starting server on ws://localhost:8765")
    print("Press Ctrl+C to stop")
    print()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create and start server
    server = SignalingServer(host="localhost", port=8765)
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main()