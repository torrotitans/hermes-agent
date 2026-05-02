"""
FN:base.py
Context engine abstract base class for Torro agent framework.

Classes:
- ContextEngine: Abstract base class for context compression strategies
- ContextConfig: Configuration for context engine behavior

Functions:
- FN:calculate_token_count: Estimate token count for text (lines 78-92)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ContextConfig:
    """Configuration for context engine behavior.
    
    Attributes:
        max_tokens: Maximum tokens before compression triggers
        compression_ratio: Target compression ratio (0.0-1.0)
        focus_topics: List of topics to prioritize during compression
        preserve_system_prompt: Whether to preserve system prompt
        preserve_recent_messages: Number of recent messages to preserve
    """
    max_tokens: int = 4096
    compression_ratio: float = 0.8
    focus_topics: List[str] = field(default_factory=list)
    preserve_system_prompt: bool = True
    preserve_recent_messages: int = 5


def calculate_token_count(text: str) -> int:
    """FN:calculate_token_count Estimate token count for text.
    
    Uses a simple heuristic: ~4 characters per token for English text.
    This is an approximation; for production use, consider using tiktoken.
    
    Args:
        text: Text to count tokens for
        
    Returns:
        Estimated token count
    """
    # Simple heuristic: 4 chars per token
    return len(text) // 4


class ContextEngine(ABC):
    """Abstract base class for context compression strategies.
    
    The ContextEngine is responsible for managing conversation context
    and implementing compression strategies when context exceeds limits.
    
    Example:
        ```python
        class SimpleCompressor(ContextEngine):
            @property
            def name(self) -> str:
                return "simple"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                self._total_tokens += usage.get("total_tokens", 0)
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return prompt_tokens > self.config.max_tokens
            
            def compress(
                self,
                messages: List[Dict],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict]:
                # Keep only recent messages
                return messages[-self.config.preserve_recent_messages:]
        ```
    """
    
    def __init__(self, config: Optional[ContextConfig] = None):
        """Initialize the context engine.
        
        Args:
            config: Optional configuration override
        """
        self.config = config or ContextConfig()
        self._total_tokens = 0
        self._compression_count = 0
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Engine name identifier.
        
        Returns:
            Unique engine name (e.g., "builtin", "lcm", "summary")
        """
        pass
    
    @abstractmethod
    def update_from_response(self, usage: Dict[str, Any]) -> None:
        """Update internal state from API response usage.
        
        Args:
            usage: API response usage dict with token counts
        """
        pass
    
    @abstractmethod
    def should_compress(self, prompt_tokens: int) -> bool:
        """Determine if compression should be triggered.
        
        Args:
            prompt_tokens: Current prompt token count
            
        Returns:
            True if compression should be triggered
        """
        pass
    
    @abstractmethod
    def compress(
        self,
        messages: List[Dict[str, Any]],
        current_tokens: int,
        focus_topic: str
    ) -> List[Dict[str, Any]]:
        """Compress message history while preserving relevant context.
        
        Args:
            messages: List of message dicts to compress
            current_tokens: Current token count
            focus_topic: Topic to prioritize during compression
            
        Returns:
            Compressed list of message dicts
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """FN:get_stats Return engine statistics.
        
        Returns:
            Dict with total_tokens, compression_count, and config
        """
        return {
            "total_tokens": self._total_tokens,
            "compression_count": self._compression_count,
            "config": {
                "max_tokens": self.config.max_tokens,
                "compression_ratio": self.config.compression_ratio,
                "preserve_system_prompt": self.config.preserve_system_prompt,
                "preserve_recent_messages": self.config.preserve_recent_messages,
            }
        }
    
    def _count_messages_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """FN:_count_messages_tokens Count tokens in messages.
        
        Args:
            messages: List of message dicts
            
        Returns:
            Total token count
        """
        total = 0
        for message in messages:
            content = message.get("content", "")
            if isinstance(content, str):
                total += calculate_token_count(content)
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text", "")
                        total += calculate_token_count(text)
        return total
    
    def _preserve_system_prompt(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """FN:_preserve_system_prompt Extract and preserve system messages.
        
        Args:
            messages: List of message dicts
            
        Returns:
            List with system messages preserved at the beginning
        """
        if not self.config.preserve_system_prompt:
            return messages
        
        system_messages = []
        other_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_messages.append(msg)
            else:
                other_messages.append(msg)
        
        return system_messages + other_messages
    
    def _trim_to_token_limit(
        self,
        messages: List[Dict[str, Any]],
        max_tokens: int
    ) -> List[Dict[str, Any]]:
        """FN:_trim_to_token_limit Trim messages to fit within token limit.
        
        Args:
            messages: List of message dicts
            max_tokens: Maximum tokens allowed
            
        Returns:
            Trimmed list of messages
        """
        if not messages:
            return messages
        
        # Start from the end (most recent) and work backwards
        result = []
        current_tokens = 0
        
        for msg in reversed(messages):
            msg_tokens = calculate_token_count(str(msg.get("content", "")))
            if current_tokens + msg_tokens <= max_tokens:
                result.insert(0, msg)
                current_tokens += msg_tokens
            else:
                break
        
        return result
