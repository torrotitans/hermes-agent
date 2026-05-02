"""
FN:post_tool.py
Post-tool hooks for Torro agent framework.

Classes:
- PostToolHooksRegistry: Registry for post-tool execution hooks

Functions:
- FN:log_tool_result: Log tool result hook (lines 47-56)
"""

import json
import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class PostToolHooksRegistry:
    """Registry for post-tool execution hooks.
    
    Post-tool hooks run after a tool is executed, allowing
    for logging, caching, and result processing.
    
    Example:
        ```python
        registry = PostToolHooksRegistry()
        
        # Register a hook
        registry.register_hook("log_result", lambda name, result: None)
        
        # Execute hooks
        registry.execute_hooks("read_file", {"content": "data"})
        ```
    """
    
    def __init__(self):
        """Initialize the post-tool hooks registry."""
        self._hooks: List[Callable] = []
        logger.info("FN:PostToolHooksRegistry.__init__ Registry initialized")
    
    def register_hook(self, hook: Callable[[str, Any], None]) -> None:
        """FN:register_hook Register a post-tool hook.
        
        Args:
            hook: Callable that takes tool_name and result
        """
        self._hooks.append(hook)
        logger.info("FN:PostToolHooksRegistry.register_hook Hook registered: %s", hook.__name__)
    
    def execute_hooks(self, tool_name: str, result: Any) -> None:
        """FN:execute_hooks Execute all registered hooks.
        
        Args:
            tool_name: Name of tool that was executed
            result: Tool execution result
        """
        logger.debug("FN:PostToolHooksRegistry.execute_hooks Executing %d hooks", len(self._hooks))
        
        for hook in self._hooks:
            try:
                hook(tool_name, result)
            except Exception as e:
                logger.warning("FN:PostToolHooksRegistry.execute_hooks Hook failed: %s", e)


def log_tool_result(tool_name: str, result: Any) -> None:
    """FN:log_tool_result Log tool result.
    
    Args:
        tool_name: Name of tool that was executed
        result: Tool execution result
    """
    logger.debug("FN:log_tool_result Tool %s result: %s", tool_name, json.dumps(result))
