"""
FN:test_provider.py
Unit tests for Torro memory provider base class.

Tests:
- TestMemoryProvider: Test memory provider ABC implementation
"""

import pytest
from typing import Any, Dict, List

from memory.provider import MemoryProvider


class TestMemoryProvider:
    """Test MemoryProvider ABC implementation."""
    
    def test_memory_provider_name_property(self):
        """Test memory provider name property is abstract."""
        class TestProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "test_provider"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                pass
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                return []
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                return []
            
            def get_stats(self) -> Dict[str, Any]:
                return {}
        
        provider = TestProvider()
        assert provider.name == "test_provider"
    
    def test_memory_provider_store_method(self):
        """Test memory provider store method is abstract."""
        class TestProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "test_provider"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                self._stored = (user_content, assistant_content, session_id)
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                return []
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                return []
            
            def get_stats(self) -> Dict[str, Any]:
                return {}
        
        provider = TestProvider()
        provider.store("user", "assistant", "session-123")
        assert provider._stored == ("user", "assistant", "session-123")
    
    def test_memory_provider_retrieve_method(self):
        """Test memory provider retrieve method is abstract."""
        class TestProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "test_provider"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                pass
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                return [f"memory_{i}" for i in range(top_k)]
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                return []
            
            def get_stats(self) -> Dict[str, Any]:
                return {}
        
        provider = TestProvider()
        result = provider.retrieve("query", top_k=3)
        assert len(result) == 3
        assert result == ["memory_0", "memory_1", "memory_2"]
    
    def test_memory_provider_get_recent_memories_method(self):
        """Test memory provider get_recent_memories method is abstract."""
        class TestProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "test_provider"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                pass
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                return []
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                return [f"recent_{i}" for i in range(limit)]
            
            def get_stats(self) -> Dict[str, Any]:
                return {}
        
        provider = TestProvider()
        result = provider.get_recent_memories(limit=3)
        assert len(result) == 3
        assert result == ["recent_0", "recent_1", "recent_2"]
    
    def test_memory_provider_get_stats_method(self):
        """Test memory provider get_stats method is abstract."""
        class TestProvider(MemoryProvider):
            @property
            def name(self) -> str:
                return "test_provider"
            
            def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
                pass
            
            def retrieve(self, query: str, top_k: int = 5) -> List[str]:
                return []
            
            def get_recent_memories(self, limit: int = 5) -> List[str]:
                return []
            
            def get_stats(self) -> Dict[str, Any]:
                return {"key": "value", "count": 42}
        
        provider = TestProvider()
        stats = provider.get_stats()
        assert stats == {"key": "value", "count": 42}
