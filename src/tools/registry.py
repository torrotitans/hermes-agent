"""
FN:registry.py
Tool registry with AST-based discovery for Torro agent framework.

Classes:
- ToolRegistry: Singleton registry for tool discovery and loading

Functions:
- FN:discover_tools: Discover tools from a directory using AST parsing (lines 58-92)
- FN:_is_tool_class: Check if a class is a tool class (lines 45-54)
"""

import ast
import importlib
import importlib.util
import json
import logging
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Type

from .base import Tool, ToolContext, ToolResult, ValidationResult

logger = logging.getLogger(__name__)


def _is_tool_class(node: ast.ClassDef) -> bool:
    """FN:_is_tool_class Check if a class is a tool class.
    
    A tool class is defined as a class that inherits from Tool.
    
    Args:
        node: AST node to check
        
    Returns:
        True if the class inherits from Tool
    """
    if not isinstance(node, ast.ClassDef):
        return False
    
    # Check if any base class is 'Tool'
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id == "Tool":
            return True
        # Also check for qualified names like 'module.Tool'
        if isinstance(base, ast.Attribute) and base.attr == "Tool":
            return True
    
    return False


def discover_tools(tools_dir: Optional[Path] = None) -> List[str]:
    """FN:discover_tools Discover tools from a directory using AST parsing.
    
    Uses AST parsing to find all classes that inherit from Tool.
    This enables automatic tool registration without manual imports.
    
    Args:
        tools_dir: Directory containing tool modules. Defaults to tools package dir.
        
    Returns:
        List of discovered tool module names
    """
    tools_path = Path(tools_dir) if tools_dir is not None else Path(__file__).parent
    module_names = []
    
    for path in sorted(tools_path.glob("*.py")):
        if path.name in {"__init__.py", "registry.py", "base.py"}:
            continue
        
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            
            # Check if file contains any Tool subclasses
            has_tool_class = any(
                _is_tool_class(node) for node in ast.walk(tree)
            )
            
            if has_tool_class:
                module_name = f"tools.{path.stem}"
                module_names.append(module_name)
                logger.debug("Discovered tool module: %s", module_name)
                
        except (OSError, SyntaxError) as e:
            logger.warning("Could not parse tool module %s: %s", path.name, e)
    
    return module_names


class ToolRegistry:
    """Singleton registry for tool discovery and loading.
    
    The registry maintains a collection of registered tools and provides
    methods for discovery, registration, and dispatch.
    
    Example:
        ```python
        registry = ToolRegistry()
        
        # Register a tool
        registry.register(
            name="read_file",
            toolset="file_ops",
            schema={...},
            handler=lambda args, ctx: {...}
        )
        
        # Get tool definitions
        definitions = registry.get_definitions({"read_file"})
        
        # Dispatch a tool call
        result = registry.dispatch("read_file", {"path": "file.txt"}, context)
        ```
    """
    
    _instance: Optional["ToolRegistry"] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> "ToolRegistry":
        """Create or return singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the registry."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._toolset_checks: Dict[str, Callable] = {}
        self._lock = threading.RLock()
        self._generation: int = 0
        self._initialized = True
        logger.info("FN:ToolRegistry.__init__ ToolRegistry initialized")
    
    def _snapshot_state(self) -> Dict[str, Dict[str, Any]]:
        """Return a coherent snapshot of registered tools."""
        with self._lock:
            return dict(self._tools)
    
    def get_entry(self, name: str) -> Optional[Dict[str, Any]]:
        """FN:get_entry Return a registered tool entry by name.
        
        Args:
            name: Tool name to look up
            
        Returns:
            Tool entry dict or None if not found
        """
        with self._lock:
            return self._tools.get(name)
    
    def get_registered_tool_names(self) -> List[str]:
        """FN:get_registered_tool_names Return sorted list of registered tool names."""
        return sorted(self._tools.keys())
    
    def register(
        self,
        name: str,
        toolset: str,
        schema: Dict[str, Any],
        handler: Callable[[Dict[str, Any], ToolContext], str],
        check_fn: Optional[Callable] = None,
        requires_env: Optional[List[str]] = None,
        is_async: bool = False,
        description: str = "",
        emoji: str = "",
        max_result_size_chars: Optional[int] = None,
    ) -> None:
        """FN:register Register a tool.
        
        Args:
            name: Tool name identifier
            toolset: Toolset/category name
            schema: JSON Schema for input validation
            handler: Callable that executes the tool
            check_fn: Optional availability check function
            requires_env: List of required environment variables
            is_async: Whether handler is async
            description: Human-readable description
            emoji: Emoji icon for UI display
            max_result_size_chars: Maximum result size in characters
        """
        with self._lock:
            existing = self._tools.get(name)
            if existing and existing.get("toolset") != toolset:
                logger.warning(
                    "Tool '%s' toolset changed from '%s' to '%s'",
                    name, existing.get("toolset"), toolset
                )
            
            self._tools[name] = {
                "name": name,
                "toolset": toolset,
                "schema": schema,
                "handler": handler,
                "check_fn": check_fn,
                "requires_env": requires_env or [],
                "is_async": is_async,
                "description": description or schema.get("description", ""),
                "emoji": emoji,
                "max_result_size_chars": max_result_size_chars,
            }
            
            if check_fn and toolset not in self._toolset_checks:
                self._toolset_checks[toolset] = check_fn
            
            self._generation += 1
            logger.info("FN:ToolRegistry.register Registered tool: %s", name)
    
    def unregister(self, name: str) -> None:
        """FN:unregister Remove a tool from the registry.
        
        Args:
            name: Tool name to remove
        """
        with self._lock:
            entry = self._tools.pop(name, None)
            if entry is None:
                return
            
            # Clean up toolset check if no other tools remain
            toolset = entry.get("toolset")
            if toolset:
                toolset_still_exists = any(
                    e.get("toolset") == toolset for e in self._tools.values()
                )
                if not toolset_still_exists:
                    self._toolset_checks.pop(toolset, None)
            
            self._generation += 1
            logger.info("FN:ToolRegistry.unregister Unregistered tool: %s", name)
    
    def get_definitions(self, tool_names: Set[str]) -> List[Dict[str, Any]]:
        """FN:get_definitions Return tool definitions for the requested tool names.
        
        Args:
            tool_names: Set of tool names to get definitions for
            
        Returns:
            List of tool definition dicts
        """
        result = []
        entries_by_name = {entry["name"]: entry for entry in self._snapshot_state().values()}
        
        for name in sorted(tool_names):
            entry = entries_by_name.get(name)
            if not entry:
                continue
            
            # Check availability
            check_fn = entry.get("check_fn")
            if check_fn:
                try:
                    if not check_fn():
                        logger.debug("Tool %s unavailable (check failed)", name)
                        continue
                except Exception as e:
                    logger.warning("Tool %s check raised exception: %s", name, e)
                    continue
            
            result.append({
                "type": "function",
                "function": {
                    "name": entry["name"],
                    "description": entry["description"],
                    "parameters": entry["schema"],
                }
            })
        
        return result
    
    def dispatch(
        self,
        name: str,
        args: Dict[str, Any],
        context: ToolContext,
        **kwargs: Any
    ) -> str:
        """FN:dispatch Execute a tool handler by name.
        
        Args:
            name: Tool name to execute
            args: Tool input arguments
            context: Tool execution context
            **kwargs: Additional keyword arguments
            
        Returns:
            JSON string result
        """
        entry = self.get_entry(name)
        if not entry:
            return json.dumps({"error": f"Unknown tool: {name}"})
        
        try:
            handler = entry["handler"]
            result = handler(args, context, **kwargs)
            
            # Handle async handlers
            if entry.get("is_async"):
                import asyncio
                if asyncio.iscoroutine(result):
                    result = asyncio.run(result)
            
            # Convert ToolResult to dict if needed
            if isinstance(result, ToolResult):
                return json.dumps(result.to_dict())
            
            return json.dumps(result)
            
        except Exception as e:
            logger.exception("Tool %s dispatch error: %s", name, e)
            return json.dumps({"error": f"Tool execution failed: {type(e).__name__}: {e}"})
    
    def get_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """FN:get_schema Return a tool's raw schema dict.
        
        Args:
            name: Tool name
            
        Returns:
            Schema dict or None if not found
        """
        entry = self.get_entry(name)
        return entry["schema"] if entry else None
    
    def get_toolset_for_tool(self, name: str) -> Optional[str]:
        """FN:get_toolset_for_tool Return the toolset a tool belongs to.
        
        Args:
            name: Tool name
            
        Returns:
            Toolset name or None
        """
        entry = self.get_entry(name)
        return entry["toolset"] if entry else None
    
    def get_emoji(self, name: str, default: str = "⚡") -> str:
        """FN:get_emoji Return the emoji for a tool.
        
        Args:
            name: Tool name
            default: Default emoji if not set
            
        Returns:
            Emoji string
        """
        entry = self.get_entry(name)
        return entry["emoji"] if entry and entry["emoji"] else default
    
    def get_tool_to_toolset_map(self) -> Dict[str, str]:
        """FN:get_tool_to_toolset_map Return {tool_name: toolset_name} mapping."""
        return {entry["name"]: entry["toolset"] for entry in self._snapshot_state().values()}
    
    def is_toolset_available(self, toolset: str) -> bool:
        """FN:is_toolset_available Check if a toolset's requirements are met.
        
        Args:
            toolset: Toolset name
            
        Returns:
            True if available
        """
        with self._lock:
            check = self._toolset_checks.get(toolset)
        
        if not check:
            return True
        
        try:
            return bool(check())
        except Exception:
            logger.debug("Toolset %s check raised exception", toolset)
            return False
    
    def check_toolset_requirements(self) -> Dict[str, bool]:
        """FN:check_toolset_requirements Return {toolset: available_bool} mapping."""
        entries = self._snapshot_state()
        toolsets = {entry["toolset"] for entry in entries.values()}
        return {
            toolset: self.is_toolset_available(toolset)
            for toolset in toolsets
        }
    
    def get_available_toolsets(self) -> Dict[str, Dict[str, Any]]:
        """FN:get_available_toolsets Return toolset metadata for UI display."""
        toolsets: Dict[str, Dict[str, Any]] = {}
        entries = self._snapshot_state()
        
        for entry in entries.values():
            ts = entry["toolset"]
            if ts not in toolsets:
                toolsets[ts] = {
                    "available": self.is_toolset_available(ts),
                    "tools": [],
                    "description": "",
                    "requirements": [],
                }
            toolsets[ts]["tools"].append(entry["name"])
            if entry.get("requires_env"):
                for env in entry["requires_env"]:
                    if env not in toolsets[ts]["requirements"]:
                        toolsets[ts]["requirements"].append(env)
        
        return toolsets


# Module-level singleton
registry = ToolRegistry()
