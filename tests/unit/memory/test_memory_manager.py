"""
FN:test_manager.py
Unit tests for Torro memory manager.

Tests:
- TestMemoryManager: Test memory manager class
- TestMemoryManagerProviders: Test memory manager with providers
"""

import pytest
from unittest.mock import Mock, MagicMock

from memory.manager import MemoryManager
from memory.provider import MemoryProvider


class TestMemoryManager:
    """Test MemoryManager class."""
    
    def test_memory_manager_init(self):
        """Test memory manager initialization."""
        manager = MemoryManager()
        assert manager._providers == []
        assert manager._system_prompt is None
    
    def test_memory_manager_add_provider(self):
        """Test adding a provider to the manager."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        
        manager.add_provider(provider)
        assert len(manager._providers) == 1
        assert manager._providers[0] == provider
    
    def test_memory_manager_remove_provider(self):
        """Test removing a provider from the manager."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        
        manager.add_provider(provider)
        assert len(manager._providers) == 1
        
        result = manager.remove_provider("test_provider")
        assert result is True
        assert len(manager._providers) == 0
    
    def test_memory_manager_remove_nonexistent_provider(self):
        """Test removing a nonexistent provider."""
        manager = MemoryManager()
        result = manager.remove_provider("nonexistent")
        assert result is False
    
    def test_memory_manager_build_system_prompt_empty(self):
        """Test building system prompt with no providers."""
        manager = MemoryManager()
        prompt = manager.build_system_prompt()
        assert prompt == ""
    
    def test_memory_manager_build_system_prompt(self):
        """Test building system prompt with providers."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        provider.get_recent_memories.return_value = ["memory1", "memory2"]
        
        manager.add_provider(provider)
        prompt = manager.build_system_prompt()
        
        assert "## Memory Context" in prompt
        assert "### test_provider" in prompt
        assert "memory1" in prompt
        assert "memory2" in prompt
    
    def test_memory_manager_prefetch_all(self):
        """Test prefetching memories from all providers."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        provider.retrieve.return_value = ["memory1", "memory2"]
        
        manager.add_provider(provider)
        result = manager.prefetch_all("query", "session-123")
        
        assert "memory1" in result
        assert "memory2" in result
        provider.retrieve.assert_called_once_with("query", top_k=3)
    
    def test_memory_manager_prefetch_all_handles_errors(self):
        """Test prefetching handles provider errors."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        provider.retrieve.side_effect = Exception("Test error")
        
        manager.add_provider(provider)
        result = manager.prefetch_all("query", "session-123")
        
        assert result == ""
    
    def test_memory_manager_sync_all(self):
        """Test syncing memories to all providers."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        
        manager.add_provider(provider)
        manager.sync_all("user content", "assistant content", "session-123")
        
        provider.store.assert_called_once_with(
            "user content", "assistant content", "session-123"
        )
    
    def test_memory_manager_sync_all_handles_errors(self):
        """Test syncing handles provider errors."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        provider.store.side_effect = Exception("Test error")
        
        manager.add_provider(provider)
        # Should not raise
        manager.sync_all("user content", "assistant content", "session-123")
    
    def test_memory_manager_get_stats(self):
        """Test getting memory manager statistics."""
        manager = MemoryManager()
        provider = Mock(spec=MemoryProvider)
        provider.name = "test_provider"
        provider.get_stats.return_value = {"count": 10}
        
        manager.add_provider(provider)
        stats = manager.get_stats()
        
        assert "providers" in stats
        assert "test_provider" in stats["providers"]
        assert "provider_stats" in stats
        assert stats["provider_stats"]["test_provider"] == {"count": 10}


class TestMemoryManagerProviders:
    """Test MemoryManager with multiple providers."""
    
    def test_memory_manager_multiple_providers(self):
        """Test memory manager with multiple providers."""
        manager = MemoryManager()
        
        provider1 = Mock(spec=MemoryProvider)
        provider1.name = "provider1"
        provider1.get_recent_memories.return_value = ["mem1"]
        
        provider2 = Mock(spec=MemoryProvider)
        provider2.name = "provider2"
        provider2.get_recent_memories.return_value = ["mem2"]
        
        manager.add_provider(provider1)
        manager.add_provider(provider2)
        
        prompt = manager.build_system_prompt()
        
        assert "### provider1" in prompt
        assert "### provider2" in prompt
        assert "mem1" in prompt
        assert "mem2" in prompt
    
    def test_memory_manager_prefetch_multiple_providers(self):
        """Test prefetching from multiple providers."""
        manager = MemoryManager()
        
        provider1 = Mock(spec=MemoryProvider)
        provider1.name = "provider1"
        provider1.retrieve.return_value = ["mem1"]
        
        provider2 = Mock(spec=MemoryProvider)
        provider2.name = "provider2"
        provider2.retrieve.return_value = ["mem2"]
        
        manager.add_provider(provider1)
        manager.add_provider(provider2)
        
        result = manager.prefetch_all("query", "session-123")
        
        assert "mem1" in result
        assert "mem2" in result
