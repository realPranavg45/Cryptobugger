"""
WebSocket Signaling Server
"""
import asyncio
import json
import logging
import websockets
from typing import Dict, Set

logger = logging.getLogger(__name__)

class SignalingServer:
    """WebSocket-based signaling server"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.running = False
    
    async def register_client(self, websocket, user_id: str):
        """Register a new client"""
        self.clients[user_id] = websocket
        logger.info(f"Client {user_id} registered")
        
        # Send user list to all clients
        await self.broadcast_user_list()
    
    async def unregister_client(self, user_id: str):
        """Unregister a client"""
        if user_id in self.clients:
            del self.clients[user_id]
            logger.info(f"Client {user_id} unregistered")
            await self.broadcast_user_list()
    
    async def broadcast_user_list(self):
        """Broadcast current user list to all clients"""
        user_list = list(self.clients.keys())
        message = {
            "type": "user_list",
            "users": user_list
        }
        
        disconnected_clients = []
        for user_id, websocket in self.clients.items():
            try:
                await websocket.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(user_id)
        
        # Clean up disconnected clients
        for user_id in disconnected_clients:
            await self.unregister_client(user_id)
    
    async def forward_message(self, from_user: str, to_user: str, message: dict):
        """Forward message between users"""
        if to_user in self.clients:
            try:
                await self.clients[to_user].send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                await self.unregister_client(to_user)
        else:
            # Send error back to sender
            error_message = {
                "type": "error",
                "message": f"User {to_user} not found"
            }
            if from_user in self.clients:
                await self.clients[from_user].send(json.dumps(error_message))
    
    async def handle_client(self, websocket, path):
        """Handle client connection"""
        user_id = None
        try:
            async for message in websocket:
                data = json.loads(message)
                message_type = data.get("type")
                
                if message_type == "register":
                    user_id = data.get("user_id")
                    await self.register_client(websocket, user_id)
                
                elif message_type in ["call_offer", "call_answer", "call_reject", "call_end", "ice_candidate"]:
                    from_user = data.get("from")
                    to_user = data.get("to")
                    await self.forward_message(from_user, to_user, data)
                
                else:
                    logger.warning(f"Unknown message type: {message_type}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            if user_id:
                await self.unregister_client(user_id)
    
    async def start(self):
        """Start the signaling server"""
        self.running = True
        logger.info(f"Starting signaling server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            logger.info("Signaling server started")
            await asyncio.Future()  # Run forever
    
    def stop(self):
        """Stop the signaling server"""
        self.running = False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = SignalingServer()
    asyncio.run(server.start())