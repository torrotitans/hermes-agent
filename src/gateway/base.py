"""
FN:base.py
Gateway pattern base class for Torro agent framework.

Classes:
- BasePlatformAdapter: Abstract base class for platform adapters
- Message: Message data class for platform communication
- MessageId: Message identifier type

Functions:
- FN:connect: Connect to platform (lines 52-62)
- FN:send_message: Send message to platform (lines 64-76)
- FN:receive_message: Receive message from platform (lines 78-90)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Message data class for platform communication.
    
    Attributes:
        content: Message content
        sender: Message sender identifier
        recipient: Message recipient identifier
        metadata: Additional message metadata
    """
    content: str
    sender: str
    recipient: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageId:
    """Message identifier.
    
    Attributes:
        id: Unique message identifier
        platform: Platform name
    """
    id: str
    platform: str


class BasePlatformAdapter(ABC):
    """Abstract base class for platform adapters.
    
    The Gateway Pattern provides a unified interface for communicating
    with different messaging platforms (Telegram, Discord, Slack, etc.).
    
    Example:
        ```python
        class TelegramAdapter(BasePlatformAdapter):
            @property
            def platform_name(self) -> str:
                return "telegram"
            
            async def connect(self, credentials: Dict[str, str]) -> None:
                # Connect to Telegram API
                pass
            
            async def send_message(self, recipient: str, content: str) -> MessageId:
                # Send message via Telegram
                return MessageId(id="123", platform="telegram")
            
            async def receive_message(self) -> Optional[Message]:
                # Receive message from Telegram
                return Message(content="Hello", sender="user", recipient="bot")
        ```
    """
    
    def __init__(self):
        """Initialize the platform adapter."""
        self._connected = False
        self._credentials: Optional[Dict[str, str]] = None
        logger.info("FN:BasePlatformAdapter.__init__ Adapter initialized: %s", self.platform_name)
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Platform name identifier.
        
        Returns:
            Unique platform name (e.g., "telegram", "discord", "slack")
        """
        pass
    
    @abstractmethod
    async def connect(self, credentials: Dict[str, str]) -> None:
        """Connect to platform.
        
        Args:
            credentials: Platform-specific credentials
            
        Raises:
            ConnectionError: If connection fails
        """
        pass
    
    @abstractmethod
    async def send_message(self, recipient: str, content: str) -> MessageId:
        """Send message to platform.
        
        Args:
            recipient: Recipient identifier
            content: Message content
            
        Returns:
            MessageId of sent message
        """
        pass
    
    @abstractmethod
    async def receive_message(self) -> Optional[Message]:
        """Receive message from platform.
        
        Returns:
            Message object or None if no messages
        """
        pass
    
    @property
    def is_connected(self) -> bool:
        """FN:is_connected Check if connected to platform.
        
        Returns:
            True if connected
        """
        return self._connected
    
    def disconnect(self) -> None:
        """FN:disconnect Disconnect from platform."""
        self._connected = False
        self._credentials = None
        logger.info("FN:BasePlatformAdapter.disconnect Disconnected: %s", self.platform_name)
