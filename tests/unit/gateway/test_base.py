"""
FN:test_base.py
Unit tests for Torro gateway pattern.

Tests:
- TestMessage: Test Message dataclass
- TestMessageId: Test MessageId dataclass
- TestBasePlatformAdapter: Test BasePlatformAdapter ABC
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from gateway.base import (
    BasePlatformAdapter,
    Message,
    MessageId,
)


class TestMessage:
    """Test Message dataclass."""
    
    def test_message_creation(self):
        """Test creating a Message."""
        msg = Message(
            content="Hello",
            sender="user1",
            recipient="bot"
        )
        assert msg.content == "Hello"
        assert msg.sender == "user1"
        assert msg.recipient == "bot"
        assert msg.metadata == {}
    
    def test_message_with_metadata(self):
        """Test creating a Message with metadata."""
        msg = Message(
            content="Hello",
            sender="user1",
            recipient="bot",
            metadata={"key": "value"}
        )
        assert msg.metadata == {"key": "value"}


class TestMessageId:
    """Test MessageId dataclass."""
    
    def test_message_id_creation(self):
        """Test creating a MessageId."""
        msg_id = MessageId(id="123", platform="telegram")
        assert msg_id.id == "123"
        assert msg_id.platform == "telegram"


class TestBasePlatformAdapter:
    """Test BasePlatformAdapter ABC."""
    
    def test_platform_name_property(self):
        """Test platform_name property is abstract."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                pass
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return None
        
        adapter = TestAdapter()
        assert adapter.platform_name == "test_platform"
    
    def test_is_connected_default(self):
        """Test is_connected property default value."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                pass
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return None
        
        adapter = TestAdapter()
        assert adapter.is_connected is False
    
    def test_disconnect(self):
        """Test disconnect method."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                self._connected = True
                self._credentials = credentials
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return None
        
        adapter = TestAdapter()
        adapter._connected = True
        adapter._credentials = {"key": "value"}
        
        adapter.disconnect()
        assert adapter.is_connected is False
        assert adapter._credentials is None
    
    @pytest.mark.asyncio
    async def test_connect_abstract(self):
        """Test connect method is abstract."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                self._connected = True
                self._credentials = credentials
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return None
        
        adapter = TestAdapter()
        await adapter.connect({"key": "value"})
        assert adapter.is_connected is True
        assert adapter._credentials == {"key": "value"}
    
    @pytest.mark.asyncio
    async def test_send_message_abstract(self):
        """Test send_message method is abstract."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                pass
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return None
        
        adapter = TestAdapter()
        result = await adapter.send_message("user1", "Hello")
        assert result.id == "1"
        assert result.platform == "test"
    
    @pytest.mark.asyncio
    async def test_receive_message_abstract(self):
        """Test receive_message method is abstract."""
        class TestAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "test_platform"
            
            async def connect(self, credentials):
                pass
            
            async def send_message(self, recipient, content):
                return MessageId(id="1", platform="test")
            
            async def receive_message(self):
                return Message(content="Hello", sender="user1", recipient="bot")
        
        adapter = TestAdapter()
        result = await adapter.receive_message()
        assert result.content == "Hello"
        assert result.sender == "user1"
        assert result.recipient == "bot"
