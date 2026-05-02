"""
FN:quickstart.py
Quick start guide for Torro Agent Framework.

This example demonstrates the basic usage of Torro components.

Usage:
    python3 examples/quickstart.py
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.base import Tool, ToolContext, ToolResult, ValidationResult, PermissionResult
from tools.registry import registry
from memory.manager import MemoryManager
from memory.provider import MemoryProvider
from innovation.curator import Curator
from sre.errors import ErrorClassifier


# Example 1: Create a custom tool
class FileReadTool(Tool):
    """Example tool for reading files."""
    
    @property
    def name(self) -> str:
        return "read_file"
    
    @property
    def description(self) -> str:
        return "Read contents of a file"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
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


# Example 2: Create a custom memory provider
class SimpleMemoryProvider(MemoryProvider):
    """Simple in-memory storage provider."""
    
    @property
    def name(self) -> str:
        return "simple"
    
    def store(self, user_content: str, assistant_content: str, session_id: str) -> None:
        print(f"Storing memory for session {session_id}")
    
    def retrieve(self, query: str, top_k: int = 5) -> list:
        return [f"Memory: {query}"]
    
    def get_recent_memories(self, limit: int = 5) -> list:
        return ["Recent memory 1", "Recent memory 2"]
    
    def get_stats(self) -> dict:
        return {"count": 2}


def main():
    """Main quickstart function."""
    print("=== Torro Agent Framework Quickstart ===\n")
    
    # 1. Register a tool
    print("1. Registering a tool...")
    registry.register(
        name="read_file",
        toolset="file_ops",
        schema={"type": "object", "properties": {"path": {"type": "string"}}},
        handler=lambda args, ctx: {"content": "file content"}
    )
    print(f"   Registered tools: {registry.get_registered_tool_names()}\n")
    
    # 2. Create memory manager and add provider
    print("2. Setting up memory manager...")
    manager = MemoryManager()
    provider = SimpleMemoryProvider()
    manager.add_provider(provider)
    print(f"   Providers: {manager.get_stats()['providers']}\n")
    
    # 3. Use error classifier
    print("3. Testing error classifier...")
    classifier = ErrorClassifier()
    result = classifier.classify("Connection refused to database")
    print(f"   Error: 'Connection refused'")
    print(f"   Category: {result.category.value}")
    print(f"   Fix: {result.suggested_fix}\n")
    
    # 4. Test tool dispatch
    print("4. Testing tool dispatch...")
    context = ToolContext(session_id="test-123")
    result = registry.dispatch("read_file", {"path": "test.txt"}, context)
    print(f"   Tool result: {result}\n")
    
    # 5. Test memory operations
    print("5. Testing memory operations...")
    memories = manager.prefetch_all("test query", "session-123")
    print(f"   Prefetched: {memories}\n")
    
    print("=== Quickstart Complete ===")
    print("\nNext steps:")
    print("1. Read the documentation: docs/")
    print("2. Run the tests: python3 -m pytest tests/")
    print("3. Check CLI status: python3 -m src.torro.cli status")


if __name__ == "__main__":
    main()
