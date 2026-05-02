"""
FN:base.py
Tool abstract base class for Torro agent framework.

Classes:
- Tool: Abstract base class defining the tool contract
- ToolContext: Context data passed to tool calls
- ToolResult: Result data returned from tool calls
- ValidationResult: Result of input validation
- PermissionResult: Result of permission check

Functions:
- FN:validate_tool_input: Validate input against JSON schema (lines 85-102)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolContext:
    """Context data passed to tool calls.
    
    Attributes:
        session_id: Unique session identifier
        user_id: User identifier (if authenticated)
        working_directory: Current working directory
        environment: Environment variables dict
        metadata: Additional context metadata
    """
    session_id: str
    user_id: Optional[str] = None
    working_directory: Optional[str] = None
    environment: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """Result data returned from tool calls.
    
    Attributes:
        success: Whether the tool call succeeded
        data: Result data payload
        error: Error message if failed
        metadata: Additional result metadata
    """
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class ValidationResult:
    """Result of input validation.
    
    Attributes:
        valid: Whether input is valid
        message: Error message if invalid
        errors: List of validation errors
    """
    valid: bool = True
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "valid": self.valid,
            "message": self.message,
            "errors": self.errors,
        }


@dataclass
class PermissionResult:
    """Result of permission check.
    
    Attributes:
        granted: Whether permission is granted
        reason: Reason for denial if not granted
        required_permissions: List of required permissions
    """
    granted: bool = True
    reason: Optional[str] = None
    required_permissions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "granted": self.granted,
            "reason": self.reason,
            "required_permissions": self.required_permissions,
        }


class Tool(ABC):
    """Abstract base class for all Torro tools.
    
    This class defines the contract that all tools must implement.
    Tools are the primary mechanism for extending agent capabilities.
    
    Example:
        ```python
        class FileReadTool(Tool):
            @property
            def name(self) -> str:
                return "read_file"
            
            @property
            def description(self) -> str:
                return "Read contents of a file"
            
            @property
            def input_schema(self) -> Dict[str, Any]:
                return {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to read"}
                    },
                    "required": ["path"]
                }
            
            def check_permissions(self, context: ToolContext) -> PermissionResult:
                return PermissionResult(granted=True)
            
            def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
                if not input_data.get("path"):
                    return ValidationResult(
                        valid=False,
                        message="Path is required"
                    )
                return ValidationResult(valid=True)
            
            async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
                path = input_data["path"]
                with open(path, "r") as f:
                    content = f.read()
                return ToolResult(success=True, data={"content": content})
        ```
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name identifier.
        
        Returns:
            Unique tool name (snake_case convention)
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description.
        
        Returns:
            One-line description of tool capability
        """
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for input validation.
        
        Returns:
            JSON Schema dict defining valid input structure
        """
        pass
    
    @abstractmethod
    def check_permissions(self, context: ToolContext) -> PermissionResult:
        """Verify tool execution permissions.
        
        Args:
            context: Tool execution context
            
        Returns:
            PermissionResult indicating if execution is allowed
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
        """Validate input against schema.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            ValidationResult indicating validity
        """
        pass
    
    @abstractmethod
    async def call(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        """Execute tool logic.
        
        Args:
            input_data: Validated input data
            context: Tool execution context
            
        Returns:
            ToolResult with success status and data
        """
        pass


def validate_tool_input(input_data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    """FN:validate_tool_input Validate input against JSON schema.
    
    Args:
        input_data: Input data to validate
        schema: JSON Schema definition
        
    Returns:
        ValidationResult with validation status
    """
    errors = []
    
    # Check required fields
    required = schema.get("required", [])
    for field_name in required:
        if field_name not in input_data:
            errors.append(f"Missing required field: {field_name}")
    
    # Check property types
    properties = schema.get("properties", {})
    for field_name, field_schema in properties.items():
        if field_name in input_data:
            value = input_data[field_name]
            expected_type = field_schema.get("type")
            
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field_name}' must be a string")
            elif expected_type == "integer" and not isinstance(value, int):
                errors.append(f"Field '{field_name}' must be an integer")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(f"Field '{field_name}' must be a number")
            elif expected_type == "boolean" and not isinstance(value, bool):
                errors.append(f"Field '{field_name}' must be a boolean")
            elif expected_type == "array" and not isinstance(value, list):
                errors.append(f"Field '{field_name}' must be an array")
            elif expected_type == "object" and not isinstance(value, dict):
                errors.append(f"Field '{field_name}' must be an object")
    
    if errors:
        return ValidationResult(valid=False, message="; ".join(errors), errors=errors)
    
    return ValidationResult(valid=True)
