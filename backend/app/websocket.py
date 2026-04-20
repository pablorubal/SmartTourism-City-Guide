"""
WebSocket support for real-time updates
"""
from typing import Dict, List, Callable, Optional
from datetime import datetime
import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect, status
from loguru import logger

from app.auth.jwt import verify_token


class WebSocketManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        """Initialize WebSocket manager"""
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_subscriptions: Dict[str, set] = {}
        self.connection_handlers: Dict[str, Callable] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, token: str):
        """
        Register new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            token: JWT authentication token
        """
        # Verify token
        payload = verify_token(token)
        if not payload:
            logger.warning(f"❌ WebSocket auth failed for user {user_id}")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return False
        
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
            self.user_subscriptions[user_id] = set()
        
        self.active_connections[user_id].append(websocket)
        logger.info(f"✅ WebSocket connected: {user_id} ({len(self.active_connections[user_id])} connection(s))")
        
        return True
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """
        Unregister WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
        """
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                del self.user_subscriptions[user_id]
                logger.info(f"🔌 WebSocket disconnected: {user_id}")
            else:
                logger.info(f"🔌 WebSocket disconnected: {user_id} ({len(self.active_connections[user_id])} connection(s) remaining)")
    
    async def broadcast_to_user(
        self,
        user_id: str,
        message_type: str,
        data: dict
    ):
        """
        Broadcast message to all connections of a user
        
        Args:
            user_id: Target user ID
            message_type: Message type (e.g., "poi_occupancy", "event_alert")
            data: Message data
        """
        if user_id not in self.active_connections:
            logger.debug(f"⚠️ No active connections for user {user_id}")
            return
        
        message = {
            "type": message_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        disconnected = []
        for websocket in self.active_connections[user_id]:
            try:
                await websocket.send_json(message)
                logger.debug(f"📤 Sent {message_type} to {user_id}")
            except Exception as e:
                logger.error(f"❌ Failed to send message to {user_id}: {str(e)}")
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for ws in disconnected:
            self.disconnect(ws, user_id)
    
    async def broadcast_to_channel(
        self,
        channel: str,
        message_type: str,
        data: dict,
        exclude_user: Optional[str] = None
    ):
        """
        Broadcast message to all users subscribed to channel
        
        Args:
            channel: Channel name (e.g., "poi_occupancy", "events")
            message_type: Message type
            data: Message data
            exclude_user: Optional user ID to exclude
        """
        count = 0
        for user_id, subscriptions in self.user_subscriptions.items():
            if channel in subscriptions and user_id != exclude_user:
                await self.broadcast_to_user(user_id, message_type, data)
                count += 1
        
        logger.debug(f"📢 Broadcast {message_type} to {count} users on {channel}")
    
    def subscribe(self, user_id: str, channel: str):
        """
        Subscribe user to channel
        
        Args:
            user_id: User ID
            channel: Channel name
        """
        if user_id not in self.user_subscriptions:
            self.user_subscriptions[user_id] = set()
        
        self.user_subscriptions[user_id].add(channel)
        logger.info(f"📬 Subscribed {user_id} to {channel}")
    
    def unsubscribe(self, user_id: str, channel: str):
        """
        Unsubscribe user from channel
        
        Args:
            user_id: User ID
            channel: Channel name
        """
        if user_id in self.user_subscriptions:
            self.user_subscriptions[user_id].discard(channel)
            logger.info(f"📭 Unsubscribed {user_id} from {channel}")
    
    async def send_keep_alive(self, user_id: str):
        """
        Send keep-alive ping to user
        
        Args:
            user_id: User ID
        """
        message = {
            "type": "ping",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    pass  # Connection might be dead
    
    async def receive_message(self, websocket: WebSocket) -> Optional[dict]:
        """
        Receive and parse message from WebSocket
        
        Args:
            websocket: WebSocket connection
            
        Returns:
            Parsed message or None if connection closed
        """
        try:
            data = await websocket.receive_text()
            return json.loads(data)
        except WebSocketDisconnect:
            return None
        except json.JSONDecodeError:
            logger.warning("⚠️ Invalid JSON received from WebSocket")
            return None


# Global WebSocket manager instance
ws_manager = WebSocketManager()


async def handle_websocket_messages(
    websocket: WebSocket,
    user_id: str,
    message_handler: Optional[Callable] = None
):
    """
    Handle incoming WebSocket messages
    
    Args:
        websocket: WebSocket connection
        user_id: User ID
        message_handler: Optional custom message handler
    """
    while True:
        message = await ws_manager.receive_message(websocket)
        
        if not message:
            ws_manager.disconnect(websocket, user_id)
            break
        
        logger.debug(f"📥 Received from {user_id}: {message.get('type')}")
        
        # Handle different message types
        message_type = message.get("type")
        
        if message_type == "subscribe":
            channel = message.get("channel")
            if channel:
                ws_manager.subscribe(user_id, channel)
        
        elif message_type == "unsubscribe":
            channel = message.get("channel")
            if channel:
                ws_manager.unsubscribe(user_id, channel)
        
        elif message_type == "pong":
            # Keep-alive response
            pass
        
        elif message_handler:
            # Custom message handling
            await message_handler(user_id, message)
        
        else:
            logger.warning(f"⚠️ Unknown message type: {message_type}")
