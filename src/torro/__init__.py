"""
Torro Agent Framework - Autonomous AI Agent System.

This package provides a comprehensive framework for building and running
autonomous AI agents with tool support, memory management, and more.

Example:
    ```python
    from torro.config import load_config
    from torro.tools.base import Tool, ToolContext, ToolResult
    
    # Load configuration
    config = load_config("config.ini")
    
    # Create and use tools
    class MyTool(Tool):
        @property
        def name(self) -> str:
            return "my_tool"
        
        # ... implement tool methods
    
    # Run agent
    agent = TorroAgent()
    result = await agent.run()
    ```
"""

__version__ = "0.1.0"
__author__ = "Torro Team"

from .config import load_config, get_config
from .tools.base import Tool, ToolContext, ToolResult, ValidationResult, PermissionResult
from .tools.registry import ToolRegistry, registry

__all__ = [
    "__version__",
    "__author__",
    "load_config",
    "get_config",
    "Tool",
    "ToolContext",
    "ToolResult",
    "ValidationResult",
    "PermissionResult",
    "ToolRegistry",
    "registry",
]
