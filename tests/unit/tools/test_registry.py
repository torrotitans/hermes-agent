"""
FN:test_registry.py
Unit tests for Torro tool registry.

Tests:
- TestToolRegistry: Test registry singleton and operations
- TestToolRegistryDiscovery: Test AST-based tool discovery
- TestToolRegistryDispatch: Test tool dispatch functionality
- TestToolRegistryHelpers: Test helper methods
"""

import pytest
from typing import Any, Dict

from tools.base import ToolContext, ToolResult
from tools.registry import ToolRegistry, discover_tools, registry


class TestToolRegistry:
    """Test ToolRegistry singleton and operations."""
    
    @pytest.fixture
    def clean_registry(self):
        """Fixture to provide clean registry instance."""
        # Reset singleton for testing
        ToolRegistry._instance = None
        reg = ToolRegistry()
        yield reg
        ToolRegistry._instance = None
    
    def test_registry_singleton(self, clean_registry):
        """Test registry is a singleton."""
        reg1 = ToolRegistry()
        reg2 = ToolRegistry()
        assert reg1 is reg2
        assert reg1 is clean_registry
    
    def test_registry_register_tool(self, clean_registry):
        """Test registering a tool."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        entry = clean_registry.get_entry("test_tool")
        assert entry is not None
        assert entry["name"] == "test_tool"
        assert entry["toolset"] == "test"
    
    def test_registry_unregister_tool(self, clean_registry):
        """Test unregistering a tool."""
        clean_registry.register(
            name="temp_tool",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        assert clean_registry.get_entry("temp_tool") is not None
        
        clean_registry.unregister("temp_tool")
        assert clean_registry.get_entry("temp_tool") is None
    
    def test_registry_get_registered_tool_names(self, clean_registry):
        """Test getting registered tool names."""
        clean_registry.register(
            name="tool_a",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        clean_registry.register(
            name="tool_b",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        names = clean_registry.get_registered_tool_names()
        assert names == ["tool_a", "tool_b"]
    
    def test_registry_get_definitions(self, clean_registry):
        """Test getting tool definitions."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object", "properties": {"key": {"type": "string"}}},
            description="Test tool description",
            handler=lambda args, ctx: {"result": "success"}
        )
        definitions = clean_registry.get_definitions({"test_tool"})
        assert len(definitions) == 1
        assert definitions[0]["type"] == "function"
        assert definitions[0]["function"]["name"] == "test_tool"
        assert definitions[0]["function"]["description"] == "Test tool description"
    
    def test_registry_get_definitions_filters_unavailable(self, clean_registry):
        """Test get_definitions filters unavailable tools."""
        def check_fn():
            return False
        
        clean_registry.register(
            name="unavailable_tool",
            toolset="test",
            schema={"type": "object"},
            check_fn=check_fn,
            handler=lambda args, ctx: {"result": "success"}
        )
        definitions = clean_registry.get_definitions({"unavailable_tool"})
        assert len(definitions) == 0
    
    def test_registry_dispatch(self, clean_registry):
        """Test dispatching a tool call."""
        def handler(args, ctx):
            return {"result": "success", "args": args}
        
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            handler=handler
        )
        
        context = ToolContext(session_id="test")
        result = clean_registry.dispatch("test_tool", {"key": "value"}, context)
        assert '"result": "success"' in result
    
    def test_registry_dispatch_unknown_tool(self, clean_registry):
        """Test dispatching unknown tool returns error."""
        context = ToolContext(session_id="test")
        result = clean_registry.dispatch("unknown_tool", {}, context)
        assert '"error": "Unknown tool: unknown_tool"' in result
    
    def test_registry_dispatch_with_error(self, clean_registry):
        """Test dispatch handles handler errors."""
        def handler(args, ctx):
            raise ValueError("Test error")
        
        clean_registry.register(
            name="error_tool",
            toolset="test",
            schema={"type": "object"},
            handler=handler
        )
        
        context = ToolContext(session_id="test")
        result = clean_registry.dispatch("error_tool", {}, context)
        assert '"error": "Tool execution failed: ValueError: Test error"' in result
    
    def test_registry_get_schema(self, clean_registry):
        """Test getting tool schema."""
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema=schema,
            handler=lambda args, ctx: {"result": "success"}
        )
        result = clean_registry.get_schema("test_tool")
        assert result == schema
    
    def test_registry_get_toolset_for_tool(self, clean_registry):
        """Test getting toolset for a tool."""
        clean_registry.register(
            name="test_tool",
            toolset="my_toolset",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        toolset = clean_registry.get_toolset_for_tool("test_tool")
        assert toolset == "my_toolset"
    
    def test_registry_get_emoji(self, clean_registry):
        """Test getting tool emoji."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            emoji="🔧",
            handler=lambda args, ctx: {"result": "success"}
        )
        emoji = clean_registry.get_emoji("test_tool")
        assert emoji == "🔧"
    
    def test_registry_get_emoji_default(self, clean_registry):
        """Test getting tool emoji with default."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        emoji = clean_registry.get_emoji("test_tool", default="⚙️")
        assert emoji == "⚙️"
    
    def test_registry_get_tool_to_toolset_map(self, clean_registry):
        """Test getting tool to toolset mapping."""
        clean_registry.register(
            name="tool_a",
            toolset="set_a",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        clean_registry.register(
            name="tool_b",
            toolset="set_b",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        mapping = clean_registry.get_tool_to_toolset_map()
        assert mapping == {"tool_a": "set_a", "tool_b": "set_b"}


class TestToolRegistryDiscovery:
    """Test AST-based tool discovery."""
    
    def test_discover_tools_empty_dir(self, tmp_path):
        """Test discovering tools in empty directory."""
        tools = discover_tools(tmp_path)
        assert tools == []
    
    def test_discover_tools_with_tool_file(self, tmp_path):
        """Test discovering tools with actual tool file."""
        tool_file = tmp_path / "my_tool.py"
        tool_file.write_text("""
from base import Tool

class MyTool(Tool):
    @property
    def name(self):
        return "my_tool"
    
    @property
    def description(self):
        return "My tool"
    
    @property
    def input_schema(self):
        return {}
    
    def check_permissions(self, context):
        return True
    
    def validate_input(self, input_data):
        return True
    
    async def call(self, input_data, context):
        return {}
""")
        tools = discover_tools(tmp_path)
        assert "tools.my_tool" in tools


class TestToolRegistryHelpers:
    """Test registry helper methods."""
    
    @pytest.fixture
    def clean_registry(self):
        """Fixture to provide clean registry instance."""
        ToolRegistry._instance = None
        reg = ToolRegistry()
        yield reg
        ToolRegistry._instance = None
    
    def test_registry_check_toolset_requirements(self, clean_registry):
        """Test checking toolset requirements."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        requirements = clean_registry.check_toolset_requirements()
        assert "test" in requirements
    
    def test_registry_get_available_toolsets(self, clean_registry):
        """Test getting available toolsets."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            requires_env=["TEST_ENV"],
            handler=lambda args, ctx: {"result": "success"}
        )
        toolsets = clean_registry.get_available_toolsets()
        assert "test" in toolsets
        assert toolsets["test"]["tools"] == ["test_tool"]
        assert toolsets["test"]["requirements"] == ["TEST_ENV"]
    
    def test_registry_is_toolset_available(self, clean_registry):
        """Test checking if toolset is available."""
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            handler=lambda args, ctx: {"result": "success"}
        )
        assert clean_registry.is_toolset_available("test") is True
    
    def test_registry_is_toolset_available_with_check(self, clean_registry):
        """Test checking toolset availability with check function."""
        def check_fn():
            return False
        
        clean_registry.register(
            name="test_tool",
            toolset="test",
            schema={"type": "object"},
            check_fn=check_fn,
            handler=lambda args, ctx: {"result": "success"}
        )
        assert clean_registry.is_toolset_available("test") is False
