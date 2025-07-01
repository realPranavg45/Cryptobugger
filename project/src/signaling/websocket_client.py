"""
WebSocket Signaling Client
"""
import asyncio
import json
import logging
import websockets
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class SignalingClient:
    """WebSocket-based signaling client"""
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.websocket = None
        self.user_id = None
        self.callbacks = {}
        self.running = False
    
    def on(self, event: str, callback: Callable):
        """Register event callback"""
        self.callbacks[event] = callback
    
    async def connect(self, user_id: str):
        """Connect to signaling server"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.user_id = user_id
            self.running = True
            
            # Register with server
            await self.send_message({
                "type": "register",
                "user_id": user_id
            })
            
            # Start message handler
            asyncio.create_task(self.message_handler())
            
            logger.info(f"Connected to signaling server as {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to connect to signaling server: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from signaling server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()
    
    async def send_message(self, message: dict):
        """Send message to signaling server"""
        if self.websocket:
            await self.websocket.send(json.dumps(message))
    
    async def message_handler(self):
        """Handle incoming messages"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                message_type = data.get("type")
                
                if message_type in self.callbacks:
                    await self.callbacks[message_type](data)
                else:
                    logger.warning(f"Unhandled message type: {message_type}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error in message handler: {e}")
    
    async def call_user(self, target_user: str, offer: dict, call_type: str = "video"):
        """Initiate call to another user"""
        await self.send_message({
            "type": "call_offer",
            "from": self.user_id,
            "to": target_user,
            "offer": offer,
            "call_type": call_type
        })
    
    async def answer_call(self, caller_id: str, answer: dict):
        """Answer incoming call"""
        await self.send_message({
            "type": "call_answer",
            "from": self.user_id,
            "to": caller_id,
            "answer": answer
        })
    
    async def reject_call(self, caller_id: str):
        """Reject incoming call"""
        await self.send_message({
            "type": "call_reject",
            "from": self.user_id,
            "to": caller_id
        })
    
    async def end_call(self, peer_id: str):
        """End ongoing call"""
        await self.send_message({
            "type": "call_end",
            "from": self.user_id,
            "to": peer_id
        })
    
    async def send_ice_candidate(self, peer_id: str, candidate: dict):
        """Send ICE candidate"""
        await self.send_message({
            "type": "ice_candidate",
            "from": self.user_id,
            "to": peer_id,
            "candidate": candidate
        })