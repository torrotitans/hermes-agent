"""
FN:test_base.py
Unit tests for Torro context engine base class.

Tests:
- TestContextConfig: Test context configuration dataclass
- TestContextEngine: Test context engine ABC implementation
- TestCalculateTokenCount: Test token counting helper
"""

import pytest
from typing import Any, Dict, List

from context.base import (
    ContextConfig,
    ContextEngine,
    calculate_token_count,
)


class TestContextConfig:
    """Test ContextConfig dataclass."""
    
    def test_context_config_defaults(self):
        """Test ContextConfig default values."""
        config = ContextConfig()
        assert config.max_tokens == 4096
        assert config.compression_ratio == 0.8
        assert config.focus_topics == []
        assert config.preserve_system_prompt is True
        assert config.preserve_recent_messages == 5
    
    def test_context_config_custom_values(self):
        """Test ContextConfig with custom values."""
        config = ContextConfig(
            max_tokens=8192,
            compression_ratio=0.5,
            focus_topics=["topic1", "topic2"],
            preserve_system_prompt=False,
            preserve_recent_messages=10
        )
        assert config.max_tokens == 8192
        assert config.compression_ratio == 0.5
        assert config.focus_topics == ["topic1", "topic2"]
        assert config.preserve_system_prompt is False
        assert config.preserve_recent_messages == 10


class TestContextEngine:
    """Test ContextEngine ABC implementation."""
    
    def test_context_engine_name_property(self):
        """Test context engine name property is abstract."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return False
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine()
        assert engine.name == "test_engine"
    
    def test_context_engine_update_from_response(self):
        """Test context engine update_from_response method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                self._total_tokens += usage.get("total_tokens", 0)
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return False
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine()
        engine.update_from_response({"total_tokens": 100})
        engine.update_from_response({"total_tokens": 200})
        assert engine._total_tokens == 300
    
    def test_context_engine_should_compress(self):
        """Test context engine should_compress method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return prompt_tokens > self.config.max_tokens
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine()
        assert engine.should_compress(1000) is False
        assert engine.should_compress(5000) is True
    
    def test_context_engine_compress(self):
        """Test context engine compress method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return True
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                # Keep only last 2 messages
                return messages[-2:]
        
        engine = TestEngine()
        messages = [
            {"role": "user", "content": "msg1"},
            {"role": "assistant", "content": "msg2"},
            {"role": "user", "content": "msg3"},
        ]
        result = engine.compress(messages, 100, "topic")
        assert len(result) == 2
        assert result[0]["content"] == "msg2"
        assert result[1]["content"] == "msg3"
    
    def test_context_engine_get_stats(self):
        """Test context engine get_stats method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                self._total_tokens += usage.get("total_tokens", 0)
                self._compression_count += 1
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return True
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine(ContextConfig(max_tokens=2048))
        engine.update_from_response({"total_tokens": 100})
        stats = engine.get_stats()
        
        assert stats["total_tokens"] == 100
        assert stats["compression_count"] == 1
        assert stats["config"]["max_tokens"] == 2048
    
    def test_context_engine_count_messages_tokens(self):
        """Test context engine _count_messages_tokens method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return False
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine()
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        token_count = engine._count_messages_tokens(messages)
        assert token_count > 0
    
    def test_context_engine_preserve_system_prompt(self):
        """Test context engine _preserve_system_prompt method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return False
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine(ContextConfig(preserve_system_prompt=True))
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"},
        ]
        result = engine._preserve_system_prompt(messages)
        assert result[0]["role"] == "system"
        assert result[0]["content"] == "System message"
    
    def test_context_engine_trim_to_token_limit(self):
        """Test context engine _trim_to_token_limit method."""
        class TestEngine(ContextEngine):
            @property
            def name(self) -> str:
                return "test_engine"
            
            def update_from_response(self, usage: Dict[str, Any]) -> None:
                pass
            
            def should_compress(self, prompt_tokens: int) -> bool:
                return False
            
            def compress(
                self,
                messages: List[Dict[str, Any]],
                current_tokens: int,
                focus_topic: str
            ) -> List[Dict[str, Any]]:
                return messages
        
        engine = TestEngine()
        messages = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "Second message"},
            {"role": "user", "content": "Third message"},
        ]
        result = engine._trim_to_token_limit(messages, 10)
        assert len(result) <= 3


class TestCalculateTokenCount:
    """Test calculate_token_count helper function."""
    
    def test_calculate_token_count_empty_string(self):
        """Test token count with empty string."""
        count = calculate_token_count("")
        assert count == 0
    
    def test_calculate_token_count_short_string(self):
        """Test token count with short string."""
        count = calculate_token_count("Hello")
        assert count == 1  # 5 chars / 4 = 1
    
    def test_calculate_token_count_medium_string(self):
        """Test token count with medium string."""
        count = calculate_token_count("Hello World!")
        assert count == 3  # 12 chars / 4 = 3
    
    def test_calculate_token_count_long_string(self):
        """Test token count with long string."""
        text = "A" * 100
        count = calculate_token_count(text)
        assert count == 25  # 100 chars / 4 = 25
