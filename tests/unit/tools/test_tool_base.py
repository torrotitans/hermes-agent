"""
FN:test_base.py
Unit tests for Torro tool base classes.

Tests:
- TestToolImplementation: Test tool ABC implementation
- TestToolContext: Test context dataclass
- TestToolResult: Test result dataclass
- TestValidationResult: Test validation result dataclass
- TestPermissionResult: Test permission result dataclass
- TestValidateToolInput: Test input validation helper
"""

import asyncio
import pytest
from typing import Any, Dict

from tools.base import (
    Tool,
    ToolContext,
    ToolResult,
    ValidationResult,
    PermissionResult,
    validate_tool_input,
)


class TestToolImplementation:
    """Test Tool ABC implementation."""
    
    def test_tool_name_property(self):
        """Test tool name property is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        assert tool.name == "test_tool"
    
    def test_tool_description_property(self):
        """Test tool description property is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test description"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        assert tool.description == "Test description"
    
    def test_tool_input_schema_property(self):
        """Test tool input schema property is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {"type": "object", "properties": {"key": {"type": "string"}}}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        assert tool.input_schema == {"type": "object", "properties": {"key": {"type": "string"}}}
    
    def test_tool_check_permissions_method(self):
        """Test tool check_permissions method is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=False, reason="Test denial")
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        context = ToolContext(session_id="test")
        result = tool.check_permissions(context)
        assert result.granted is False
        assert result.reason == "Test denial"
    
    def test_tool_validate_input_method(self):
        """Test tool validate_input method is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=False, message="Invalid input")
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        result = tool.validate_input({"key": "value"})
        assert result.valid is False
        assert result.message == "Invalid input"
    
    def test_tool_call_method(self):
        """Test tool call method is abstract."""
        class TestTool(Tool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {}
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                return ToolResult(success=True, data={"result": "success"})
        
        tool = TestTool()
        context = ToolContext(session_id="test")
        result = asyncio.run(tool.call({}, context))
        assert result.success is True
        assert result.data == {"result": "success"}


class TestToolContext:
    """Test ToolContext dataclass."""
    
    def test_tool_context_creation(self):
        """Test creating ToolContext with required fields."""
        context = ToolContext(session_id="test-123")
        assert context.session_id == "test-123"
        assert context.user_id is None
        assert context.working_directory is None
        assert context.environment == {}
        assert context.metadata == {}
    
    def test_tool_context_with_optional_fields(self):
        """Test creating ToolContext with optional fields."""
        context = ToolContext(
            session_id="test-123",
            user_id="user-456",
            working_directory="/tmp",
            environment={"KEY": "value"},
            metadata={"key": "value"}
        )
        assert context.user_id == "user-456"
        assert context.working_directory == "/tmp"
        assert context.environment == {"KEY": "value"}
        assert context.metadata == {"key": "value"}


class TestToolResult:
    """Test ToolResult dataclass."""
    
    def test_tool_result_success(self):
        """Test ToolResult with success."""
        result = ToolResult(success=True, data={"key": "value"})
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error is None
    
    def test_tool_result_error(self):
        """Test ToolResult with error."""
        result = ToolResult(success=False, error="Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.data is None
    
    def test_tool_result_to_dict(self):
        """Test ToolResult to_dict method."""
        result = ToolResult(
            success=True,
            data={"key": "value"},
            metadata={"meta": "data"}
        )
        result_dict = result.to_dict()
        assert result_dict == {
            "success": True,
            "data": {"key": "value"},
            "error": None,
            "metadata": {"meta": "data"}
        }


class TestValidationResult:
    """Test ValidationResult dataclass."""
    
    def test_validation_result_valid(self):
        """Test ValidationResult with valid=True."""
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert result.message is None
        assert result.errors == []
    
    def test_validation_result_invalid(self):
        """Test ValidationResult with valid=False."""
        result = ValidationResult(
            valid=False,
            message="Invalid input",
            errors=["Error 1", "Error 2"]
        )
        assert result.valid is False
        assert result.message == "Invalid input"
        assert result.errors == ["Error 1", "Error 2"]
    
    def test_validation_result_to_dict(self):
        """Test ValidationResult to_dict method."""
        result = ValidationResult(
            valid=False,
            message="Invalid",
            errors=["Error 1"]
        )
        result_dict = result.to_dict()
        assert result_dict == {
            "valid": False,
            "message": "Invalid",
            "errors": ["Error 1"]
        }


class TestPermissionResult:
    """Test PermissionResult dataclass."""
    
    def test_permission_result_granted(self):
        """Test PermissionResult with granted=True."""
        result = PermissionResult(granted=True)
        assert result.granted is True
        assert result.reason is None
        assert result.required_permissions == []
    
    def test_permission_result_denied(self):
        """Test PermissionResult with granted=False."""
        result = PermissionResult(
            granted=False,
            reason="Permission denied",
            required_permissions=["read", "write"]
        )
        assert result.granted is False
        assert result.reason == "Permission denied"
        assert result.required_permissions == ["read", "write"]
    
    def test_permission_result_to_dict(self):
        """Test PermissionResult to_dict method."""
        result = PermissionResult(
            granted=False,
            reason="Denied",
            required_permissions=["read"]
        )
        result_dict = result.to_dict()
        assert result_dict == {
            "granted": False,
            "reason": "Denied",
            "required_permissions": ["read"]
        }


class TestValidateToolInput:
    """Test validate_tool_input helper function."""
    
    def test_validate_tool_input_valid(self):
        """Test validate_tool_input with valid input."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"}
            },
            "required": ["name"]
        }
        input_data = {"name": "test", "count": 42}
        result = validate_tool_input(input_data, schema)
        assert result.valid is True
        assert result.errors == []
    
    def test_validate_tool_input_missing_required(self):
        """Test validate_tool_input with missing required field."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
        input_data = {}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "Missing required field: name" in result.message
    
    def test_validate_tool_input_wrong_type(self):
        """Test validate_tool_input with wrong type."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"}
            }
        }
        input_data = {"name": "test", "count": "not a number"}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "must be an integer" in result.message
    
    def test_validate_tool_input_string_type(self):
        """Test validate_tool_input with string type check."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }
        input_data = {"name": 123}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "must be a string" in result.message
    
    def test_validate_tool_input_boolean_type(self):
        """Test validate_tool_input with boolean type check."""
        schema = {
            "type": "object",
            "properties": {
                "active": {"type": "boolean"}
            }
        }
        input_data = {"active": "true"}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "must be a boolean" in result.message
    
    def test_validate_tool_input_array_type(self):
        """Test validate_tool_input with array type check."""
        schema = {
            "type": "object",
            "properties": {
                "items": {"type": "array"}
            }
        }
        input_data = {"items": "not an array"}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "must be an array" in result.message
    
    def test_validate_tool_input_object_type(self):
        """Test validate_tool_input with object type check."""
        schema = {
            "type": "object",
            "properties": {
                "config": {"type": "object"}
            }
        }
        input_data = {"config": "not an object"}
        result = validate_tool_input(input_data, schema)
        assert result.valid is False
        assert "must be an object" in result.message
