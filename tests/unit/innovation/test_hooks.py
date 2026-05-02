"""
FN:test_hooks.py
Unit tests for Torro hooks system.

Tests:
- TestPreToolHooksRegistry: Test pre-tool hooks registry
- TestPostToolHooksRegistry: Test post-tool hooks registry
- TestValidateToolPermissions: Test validate_tool_permissions function
- TestLogToolResult: Test log_tool_result function
"""

import pytest
from unittest.mock import Mock, patch

from innovation.hooks.pre_tool import PreToolHooksRegistry, validate_tool_permissions
from innovation.hooks.post_tool import PostToolHooksRegistry, log_tool_result


class TestPreToolHooksRegistry:
    """Test PreToolHooksRegistry class."""
    
    def test_pre_tool_hooks_registry_init(self):
        """Test PreToolHooksRegistry initialization."""
        registry = PreToolHooksRegistry()
        assert registry._hooks == []
    
    def test_pre_tool_hooks_registry_register_hook(self):
        """Test registering a pre-tool hook."""
        registry = PreToolHooksRegistry()
        hook = Mock(__name__="test_hook")
        
        registry.register_hook(hook)
        assert len(registry._hooks) == 1
        assert hook in registry._hooks
    
    def test_pre_tool_hooks_registry_execute_hooks(self):
        """Test executing pre-tool hooks."""
        registry = PreToolHooksRegistry()
        hook1 = Mock(__name__="hook1")
        hook2 = Mock(__name__="hook2")
        
        registry.register_hook(hook1)
        registry.register_hook(hook2)
        
        registry.execute_hooks("test_tool", {"arg": "value"})
        
        hook1.assert_called_once_with("test_tool", {"arg": "value"})
        hook2.assert_called_once_with("test_tool", {"arg": "value"})
    
    def test_pre_tool_hooks_registry_execute_hooks_handles_errors(self):
        """Test executing hooks handles errors."""
        registry = PreToolHooksRegistry()
        hook1 = Mock(__name__="hook1", side_effect=Exception("Test error"))
        hook2 = Mock(__name__="hook2")
        
        registry.register_hook(hook1)
        registry.register_hook(hook2)
        
        # Should not raise
        registry.execute_hooks("test_tool", {})
        
        # Second hook should still be called
        hook2.assert_called_once()


class TestPostToolHooksRegistry:
    """Test PostToolHooksRegistry class."""
    
    def test_post_tool_hooks_registry_init(self):
        """Test PostToolHooksRegistry initialization."""
        registry = PostToolHooksRegistry()
        assert registry._hooks == []
    
    def test_post_tool_hooks_registry_register_hook(self):
        """Test registering a post-tool hook."""
        registry = PostToolHooksRegistry()
        hook = Mock(__name__="test_hook")
        
        registry.register_hook(hook)
        assert len(registry._hooks) == 1
        assert hook in registry._hooks
    
    def test_post_tool_hooks_registry_execute_hooks(self):
        """Test executing post-tool hooks."""
        registry = PostToolHooksRegistry()
        hook1 = Mock(__name__="hook1")
        hook2 = Mock(__name__="hook2")
        
        registry.register_hook(hook1)
        registry.register_hook(hook2)
        
        result = {"output": "data"}
        registry.execute_hooks("test_tool", result)
        
        hook1.assert_called_once_with("test_tool", result)
        hook2.assert_called_once_with("test_tool", result)
    
    def test_post_tool_hooks_registry_execute_hooks_handles_errors(self):
        """Test executing hooks handles errors."""
        registry = PostToolHooksRegistry()
        hook1 = Mock(__name__="hook1", side_effect=Exception("Test error"))
        hook2 = Mock(__name__="hook2")
        
        registry.register_hook(hook1)
        registry.register_hook(hook2)
        
        # Should not raise
        registry.execute_hooks("test_tool", {})
        
        # Second hook should still be called
        hook2.assert_called_once()


class TestValidateToolPermissions:
    """Test validate_tool_permissions function."""
    
    def test_validate_tool_permissions_success(self):
        """Test successful permission validation."""
        # Should not raise
        validate_tool_permissions("test_tool", {"arg": "value"})
    
    def test_validate_tool_permissions_logging(self):
        """Test that permission validation logs."""
        with patch('src.torro.innovation.hooks.pre_tool.logger') as mock_logger:
            validate_tool_permissions("test_tool", {"arg": "value"})
            mock_logger.debug.assert_called_once()


class TestLogToolResult:
    """Test log_tool_result function."""
    
    def test_log_tool_result(self):
        """Test logging tool result."""
        with patch('src.torro.innovation.hooks.post_tool.logger') as mock_logger:
            log_tool_result("test_tool", {"result": "success"})
            mock_logger.debug.assert_called_once()
    
    def test_log_tool_result_json_serializable(self):
        """Test logging with JSON-serializable result."""
        with patch('src.torro.innovation.hooks.post_tool.logger') as mock_logger:
            log_tool_result("test_tool", {"key": "value", "count": 42})
            mock_logger.debug.assert_called_once()
