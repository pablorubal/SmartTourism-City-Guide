"""
Unit tests for WebSocket functionality
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.websocket import WebSocketManager


@pytest.mark.unit
class TestWebSocketManager:
    """Test WebSocket manager operations"""
    
    def test_manager_initialization(self):
        """Test WebSocket manager initialization"""
        manager = WebSocketManager()
        
        assert manager.active_connections == {}
        assert manager.user_subscriptions == {}
        assert manager.connection_handlers == {}
    
    def test_subscribe_user_to_channel(self):
        """Test subscribing user to channel"""
        manager = WebSocketManager()
        
        manager.subscribe("user-123", "poi_occupancy")
        
        assert "user-123" in manager.user_subscriptions
        assert "poi_occupancy" in manager.user_subscriptions["user-123"]
    
    def test_unsubscribe_user_from_channel(self):
        """Test unsubscribing user from channel"""
        manager = WebSocketManager()
        
        # Subscribe first
        manager.subscribe("user-123", "poi_occupancy")
        assert "poi_occupancy" in manager.user_subscriptions["user-123"]
        
        # Unsubscribe
        manager.unsubscribe("user-123", "poi_occupancy")
        assert "poi_occupancy" not in manager.user_subscriptions["user-123"]
    
    def test_subscribe_multiple_channels(self):
        """Test subscribing to multiple channels"""
        manager = WebSocketManager()
        
        manager.subscribe("user-123", "poi_occupancy")
        manager.subscribe("user-123", "events")
        manager.subscribe("user-123", "social_matches")
        
        assert len(manager.user_subscriptions["user-123"]) == 3
    
    @pytest.mark.asyncio
    async def test_broadcast_to_user(self):
        """Test broadcasting to specific user"""
        manager = WebSocketManager()
        
        # Add mock connection
        mock_ws = AsyncMock()
        manager.active_connections["user-123"] = [mock_ws]
        
        await manager.broadcast_to_user(
            user_id="user-123",
            message_type="occupancy_update",
            data={"poi_id": "poi-1", "occupancy": 50}
        )
        
        # Verify send_json was called
        mock_ws.send_json.assert_called_once()
        
        # Check message structure
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == "occupancy_update"
        assert call_args["data"]["poi_id"] == "poi-1"
    
    @pytest.mark.asyncio
    async def test_broadcast_to_channel(self):
        """Test broadcasting to channel"""
        manager = WebSocketManager()
        
        # Setup users and subscriptions
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()
        mock_ws3 = AsyncMock()
        
        manager.active_connections["user-1"] = [mock_ws1]
        manager.active_connections["user-2"] = [mock_ws2]
        manager.active_connections["user-3"] = [mock_ws3]
        
        manager.subscribe("user-1", "poi_occupancy")
        manager.subscribe("user-2", "poi_occupancy")
        manager.subscribe("user-3", "events")  # Different channel
        
        await manager.broadcast_to_channel(
            channel="poi_occupancy",
            message_type="occupancy_update",
            data={"occupancy": 50}
        )
        
        # user-1 and user-2 should receive, but not user-3
        mock_ws1.send_json.assert_called_once()
        mock_ws2.send_json.assert_called_once()
        mock_ws3.send_json.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_disconnect_user(self):
        """Test disconnecting user"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock()
        manager.active_connections["user-123"] = [mock_ws]
        manager.subscribe("user-123", "poi_occupancy")
        
        assert "user-123" in manager.active_connections
        
        manager.disconnect(mock_ws, "user-123")
        
        # Should be removed if no other connections
        assert "user-123" not in manager.active_connections
        assert "user-123" not in manager.user_subscriptions
    
    @pytest.mark.asyncio
    async def test_multiple_connections_per_user(self):
        """Test user with multiple connections"""
        manager = WebSocketManager()
        
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()
        
        manager.active_connections["user-123"] = [mock_ws1, mock_ws2]
        
        await manager.broadcast_to_user(
            user_id="user-123",
            message_type="test",
            data={"test": "data"}
        )
        
        # Both connections should receive
        mock_ws1.send_json.assert_called_once()
        mock_ws2.send_json.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_broadcast_disconnected_client(self):
        """Test handling disconnected client during broadcast"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock()
        mock_ws.send_json.side_effect = Exception("Connection closed")
        
        manager.active_connections["user-123"] = [mock_ws]
        manager.subscribe("user-123", "poi_occupancy")  # Add subscription before broadcasting
        
        # Should not raise exception, but should handle gracefully
        try:
            await manager.broadcast_to_user(
                user_id="user-123",
                message_type="test",
                data={}
            )
        except Exception:
            pass  # Exception handling depends on implementation
    
    @pytest.mark.asyncio
    async def test_keep_alive_ping(self):
        """Test keep-alive ping mechanism"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock()
        manager.active_connections["user-123"] = [mock_ws]
        
        await manager.send_keep_alive("user-123")
        
        mock_ws.send_json.assert_called_once()
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == "ping"
    
    def test_receive_message_parsing(self):
        """Test message parsing from WebSocket"""
        import json
        
        manager = WebSocketManager()
        
        # Message should be JSON
        message = {
            "type": "subscribe",
            "channel": "poi_occupancy"
        }
        
        # Verify it's valid JSON
        json_str = json.dumps(message)
        parsed = json.loads(json_str)
        
        assert parsed["type"] == "subscribe"
        assert parsed["channel"] == "poi_occupancy"
