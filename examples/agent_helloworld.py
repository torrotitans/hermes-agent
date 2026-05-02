"""
FN:agent_helloworld.py
Example: Torro agent writes a Hello World Python program.

This example demonstrates how to use the Torro agent framework
to generate and execute a simple Python program.

Usage:
    python3 examples/agent_helloworld.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import load_config, get_config
from tools.base import Tool, ToolContext, ToolResult, ValidationResult, PermissionResult
from tools.registry import registry
from memory.manager import MemoryManager
from sre.errors import ErrorClassifier


# =============================================================================
# Custom Tools for Code Generation
# =============================================================================

class WriteFileTool(Tool):
    """Tool for writing content to a file."""
    
    @property
    def name(self) -> str:
        return "write_file"
    
    @property
    def description(self) -> str:
        return "Write content to a file"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"}
            },
            "required": ["path", "content"]
        }
    
    def check_permissions(self, context: ToolContext) -> PermissionResult:
        return PermissionResult(granted=True)
    
    def validate_input(self, input_data: dict) -> ValidationResult:
        if not input_data.get("path"):
            return ValidationResult(valid=False, message="Path is required")
        if not input_data.get("content"):
            return ValidationResult(valid=False, message="Content is required")
        return ValidationResult(valid=True)
    
    async def call(self, input_data: dict, context: ToolContext) -> ToolResult:
        path = input_data["path"]
        content = input_data["content"]
        
        try:
            # Create directory if needed
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(path, "w") as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                data={"path": path, "bytes_written": len(content)}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ReadFileTool(Tool):
    """Tool for reading file content."""
    
    @property
    def name(self) -> str:
        return "read_file"
    
    @property
    def description(self) -> str:
        return "Read content from a file"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"]
        }
    
    def check_permissions(self, context: ToolContext) -> PermissionResult:
        return PermissionResult(granted=True)
    
    def validate_input(self, input_data: dict) -> ValidationResult:
        if not input_data.get("path"):
            return ValidationResult(valid=False, message="Path is required")
        return ValidationResult(valid=True)
    
    async def call(self, input_data: dict, context: ToolContext) -> ToolResult:
        path = input_data["path"]
        
        try:
            with open(path, "r") as f:
                content = f.read()
            return ToolResult(success=True, data={"content": content})
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ExecutePythonTool(Tool):
    """Tool for executing Python code."""
    
    @property
    def name(self) -> str:
        return "execute_python"
    
    @property
    def description(self) -> str:
        return "Execute Python code and return output"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"}
            },
            "required": ["code"]
        }
    
    def check_permissions(self, context: ToolContext) -> PermissionResult:
        return PermissionResult(granted=True)
    
    def validate_input(self, input_data: dict) -> ValidationResult:
        if not input_data.get("code"):
            return ValidationResult(valid=False, message="Code is required")
        return ValidationResult(valid=True)
    
    async def call(self, input_data: dict, context: ToolContext) -> ToolResult:
        code = input_data["code"]
        
        try:
            # Execute code and capture output
            import io
            import sys
            
            output_buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = output_buffer
            
            try:
                exec(code)
                output = output_buffer.getvalue()
                return ToolResult(
                    success=True,
                    data={"output": output}
                )
            finally:
                sys.stdout = old_stdout
                output_buffer.close()
                
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# =============================================================================
# Agent Implementation
# =============================================================================

class TorroAgent:
    """Simple Torro agent for code generation tasks."""
    
    def __init__(self, config_path: str = "config.ini"):
        """Initialize the agent.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Initialize components
        self.memory_manager = MemoryManager()
        self.error_classifier = ErrorClassifier()
        
        # Register tools
        self._register_tools()
        
        print(f"Agent initialized: {self.config.app_name}")
        print(f"Environment: {self.config.environment}")
        print(f"Model: {self.config.openai.model}")
        print(f"API URL: {self.config.openai.base_url}")
    
    def _register_tools(self):
        """Register available tools."""
        registry.register(
            name="write_file",
            toolset="file_ops",
            schema=WriteFileTool.input_schema.fget(None),
            handler=lambda args, ctx: {"status": "written"}
        )
        registry.register(
            name="read_file",
            toolset="file_ops",
            schema=ReadFileTool.input_schema.fget(None),
            handler=lambda args, ctx: {"content": ""}
        )
        registry.register(
            name="execute_python",
            toolset="code_execution",
            schema=ExecutePythonTool.input_schema.fget(None),
            handler=lambda args, ctx: {"output": ""}
        )
    
    async def generate_hello_world(self) -> str:
        """Generate a Hello World Python program.
        
        Returns:
            Generated Python code
        """
        # Simple code generation (in production, this would call the LLM)
        code = '''
def greet(name: str) -> str:
    """Return a greeting message.
    
    Args:
        name: Name to greet
        
    Returns:
        Greeting message
    """
    return f"Hello, {name}! Welcome to Torro Agent Framework!"


if __name__ == "__main__":
    print(greet("World"))
'''.strip()
        
        return code
    
    async def write_code_to_file(self, code: str, output_path: str) -> ToolResult:
        """Write generated code to a file.
        
        Args:
            code: Python code to write
            output_path: Output file path
            
        Returns:
            ToolResult with write status
        """
        tool = WriteFileTool()
        context = ToolContext(session_id="helloworld-001")
        result = await tool.call(
            {"path": output_path, "content": code},
            context
        )
        return result
    
    async def execute_code(self, code: str) -> ToolResult:
        """Execute generated code.
        
        Args:
            code: Python code to execute
            
        Returns:
            ToolResult with execution output
        """
        tool = ExecutePythonTool()
        context = ToolContext(session_id="helloworld-001")
        result = await tool.call({"code": code}, context)
        return result
    
    async def run(self, output_path: str = "output/hello_world.py") -> dict:
        """Run the agent to generate and execute Hello World.
        
        Args:
            output_path: Path to save the generated file
            
        Returns:
            Dict with generation results
        """
        print("\n=== Torro Agent: Hello World Generation ===\n")
        
        # Step 1: Generate code
        print("Step 1: Generating Hello World code...")
        code = await self.generate_hello_world()
        print(f"Generated code:\n{code}\n")
        
        # Step 2: Write to file
        print(f"Step 2: Writing to {output_path}...")
        write_result = await self.write_code_to_file(code, output_path)
        
        if write_result.success:
            print(f"File written successfully: {output_path}")
        else:
            print(f"File write failed: {write_result.error}")
            return {"success": False, "error": write_result.error}
        
        # Step 3: Execute code
        print("\nStep 3: Executing code...")
        exec_result = await self.execute_code(code)
        
        if exec_result.success:
            print(f"Execution output:\n{exec_result.data['output']}")
        else:
            print(f"Execution failed: {exec_result.error}")
            return {"success": False, "error": exec_result.error}
        
        return {
            "success": True,
            "code": code,
            "output_path": output_path,
            "output": exec_result.data.get("output", "")
        }


# =============================================================================
# Main Entry Point
# =============================================================================

async def main():
    """Main async function."""
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create and run agent
    agent = TorroAgent(config_path="config.ini")
    result = await agent.run()
    
    if result["success"]:
        print("\n=== Hello World Generation Complete ===")
        print(f"Output file: {result['output_path']}")
        print(f"Output: {result['output'].strip()}")
    else:
        print("\n=== Hello World Generation Failed ===")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
