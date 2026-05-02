"""
FN:manager.py
Memory manager for Torro agent framework.

Classes:
- MemoryManager: Orchestrates memory providers and operations

Functions:
- FN:build_system_prompt: Build system prompt from memories (lines 95-110)
"""

import logging
from typing import Any, Dict, List, Optional

from .provider import MemoryProvider

logger = logging.getLogger(__name__)


class MemoryManager:
    """Orchestrates memory providers for agent context management.
    
    The MemoryManager coordinates multiple memory providers (vector, graph, etc.)
    to provide unified memory operations for the agent.
    
    Example:
        ```python
        manager = MemoryManager()
        
        # Add a provider
        provider = BuiltinMemoryProvider()
        manager.add_provider(provider)
        
        # Prefetch memories
        memories = manager.prefetch_all("user query", "session-123")
        
        # Sync memories
        manager.sync_all("user content", "assistant content", "session-123")
        ```
    """
    
    def __init__(self):
        """Initialize the memory manager."""
        self._providers: List[MemoryProvider] = []
        self._system_prompt: Optional[str] = None
        logger.info("FN:MemoryManager.__init__ MemoryManager initialized")
    
    def add_provider(self, provider: MemoryProvider) -> None:
        """FN:add_provider Add a memory provider.
        
        Args:
            provider: Memory provider instance to add
        """
        self._providers.append(provider)
        logger.info("FN:MemoryManager.add_provider Added provider: %s", provider.name)
    
    def remove_provider(self, provider_name: str) -> bool:
        """FN:remove_provider Remove a memory provider by name.
        
        Args:
            provider_name: Name of provider to remove
            
        Returns:
            True if provider was removed
        """
        for i, provider in enumerate(self._providers):
            if provider.name == provider_name:
                self._providers.pop(i)
                logger.info("FN:MemoryManager.remove_provider Removed provider: %s", provider_name)
                return True
        return False
    
    def build_system_prompt(self) -> str:
        """FN:build_system_prompt Build system prompt from memories.
        
        Returns:
            Formatted system prompt string
        """
        if not self._providers:
            return ""
        
        prompt_parts = ["## Memory Context\n"]
        
        for provider in self._providers:
            memories = provider.get_recent_memories(limit=5)
            if memories:
                prompt_parts.append(f"### {provider.name}\n")
                for memory in memories:
                    prompt_parts.append(f"- {memory}\n")
        
        self._system_prompt = "\n".join(prompt_parts)
        return self._system_prompt
    
    def prefetch_all(self, query: str, session_id: str) -> str:
        """FN:prefetch_all Prefetch memories from all providers.
        
        Args:
            query: Search query for memory retrieval
            session_id: Session identifier
            
        Returns:
            Formatted memories string
        """
        logger.info("FN:MemoryManager.prefetch_all Prefetching for session: %s", session_id)
        
        all_memories = []
        for provider in self._providers:
            try:
                memories = provider.retrieve(query, top_k=3)
                all_memories.extend(memories)
            except Exception as e:
                logger.warning("Provider %s prefetch failed: %s", provider.name, e)
        
        return "\n".join(all_memories)
    
    def sync_all(
        self,
        user_content: str,
        assistant_content: str,
        session_id: str
    ) -> None:
        """FN:sync_all Sync memories to all providers.
        
        Args:
            user_content: User message content
            assistant_content: Assistant response content
            session_id: Session identifier
        """
        logger.info("FN:MemoryManager.sync_all Syncing for session: %s", session_id)
        
        for provider in self._providers:
            try:
                provider.store(user_content, assistant_content, session_id)
            except Exception as e:
                logger.warning("Provider %s sync failed: %s", provider.name, e)
    
    def get_stats(self) -> Dict[str, Any]:
        """FN:get_stats Get memory manager statistics.
        
        Returns:
            Dict with provider stats and system prompt info
        """
        provider_stats = {}
        for provider in self._providers:
            provider_stats[provider.name] = provider.get_stats()
        
        return {
            "providers": list(provider_stats.keys()),
            "provider_stats": provider_stats,
            "system_prompt_length": len(self._system_prompt) if self._system_prompt else 0,
        }
