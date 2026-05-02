"""
FN:provider.py
Memory provider abstract base class for Torro agent framework.

Classes:
- MemoryProvider: Abstract base class for memory storage backends
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class MemoryProvider(ABC):
    """Abstract base class for memory storage backends.
    
    Memory providers are responsible for storing and retrieving
    memory content for the agent.
    
    Example:
        ```python
        class BuiltinMemoryProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "builtin"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                # Store implementation
                pass
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                # Retrieve implementation
                return []
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                # Get recent memories
                return []
            
            def get_stats(self) -> Dict[str, Any]:
                return {"count": 0}
        ```
    """
    
    def __init__(self):
        """Initialize the memory provider."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name identifier.
        
        Returns:
            Unique provider name
        """
        pass
    
    @abstractmethod
    def store(
        self,
        user_content: str,
        assistant_content: str,
        session_id: str
    ) -> None:
        """Store memory content.
        
        Args:
            user_content: User message content
            assistant_content: Assistant response content
            session_id: Session identifier
        """
        pass
    
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve memories matching query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of memory strings
        """
        pass
    
    @abstractmethod
    def get_recent_memories(self, limit: int = 5) -> List[str]:
        """Get recent memories.
        
        Args:
            limit: Maximum number of memories to return
            
        Returns:
            List of recent memory strings
        """
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics.
        
        Returns:
            Dict with provider stats
        """
        pass
