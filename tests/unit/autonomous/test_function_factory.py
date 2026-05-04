"""
FN:test_function_factory.py
Unit tests for Torro autonomous layer function factory.

Tests:
- TestFunctionFactory: Test function factory functions
- TestMacroConfig: Test macro configuration
- TestMacroResult: Test macro result
"""

import pytest
import tempfile
import shutil
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.autonomous.function_factory import (
    FunctionFactory,
    MacroConfig,
    MacroResult,
)


class TestFunctionFactory:
    """Test function factory functions."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_factory_creation(self, temp_output_dir):
        """Test creating a function factory instance."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        assert factory is not None
        assert Path(temp_output_dir).exists()
    
    def test_record_command(self, temp_output_dir):
        """Test recording a command."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        factory.record_command("test command")
        
        assert len(factory._command_history) == 1
        assert factory._command_history[0] == "test command"
    
    def test_analyze_frequency(self, temp_output_dir):
        """Test analyzing command frequency."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        # Record some commands
        factory.record_command("cmd1")
        factory.record_command("cmd1")
        factory.record_command("cmd2")
        factory.record_command("cmd1")
        
        frequency = factory.analyze_frequency()
        
        assert frequency["cmd1"] == 3
        assert frequency["cmd2"] == 1
    
    def test_analyze_frequency_custom_commands(self, temp_output_dir):
        """Test analyzing custom command list."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        commands = ["a", "a", "b", "c", "c", "c"]
        frequency = factory.analyze_frequency(commands)
        
        assert frequency["a"] == 2
        assert frequency["c"] == 3
    
    def test_get_frequent_commands(self, temp_output_dir):
        """Test getting frequent commands."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        # Record commands exceeding threshold
        for _ in range(5):
            factory.record_command("frequent_cmd")
        
        frequent = factory.get_frequent_commands(threshold=3)
        
        assert len(frequent) == 1
        assert frequent[0][0] == "frequent_cmd"
        assert frequent[0][1] == 5
    
    def test_generate_macro_basic(self, temp_output_dir):
        """Test generating a basic macro."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        result = factory.generate_macro(
            command="git status",
            name="git_status"
        )
        
        assert result.macro_id == "git_status"
        assert result.code is not None
        assert "def git_status" in result.code
        assert "git status" in result.code
    
    def test_generate_macro_auto_name(self, temp_output_dir):
        """Test generating macro with auto-generated name."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        result = factory.generate_macro(command="ls -la")
        
        assert result.macro_id is not None
        assert "ls_" in result.macro_id
    
    def test_generate_macro_sanitizes_name(self, temp_output_dir):
        """Test that macro name is sanitized."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        result = factory.generate_macro(
            command="command with spaces & special!"
        )
        
        # Name should be sanitized
        assert " " not in result.macro_id
        assert "&" not in result.macro_id
    
    def test_generate_macro_with_parameters(self, temp_output_dir):
        """Test generating macro with parameters."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        result = factory.generate_macro(
            command="git commit -m 'test message'"
        )
        
        assert result.config.parameters is not None
    
    def test_get_macro(self, temp_output_dir):
        """Test getting a macro from library."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        factory.generate_macro(
            command="test command",
            name="test_macro"
        )
        
        macro = factory.get_macro("test_macro")
        
        assert macro is not None
        assert macro.macro_id == "test_macro"
    
    def test_get_macro_not_found(self, temp_output_dir):
        """Test getting a non-existent macro."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        macro = factory.get_macro("non_existent")
        
        assert macro is None
    
    def test_list_macros(self, temp_output_dir):
        """Test listing macros."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        factory.generate_macro("cmd1", name="macro1")
        factory.generate_macro("cmd2", name="macro2")
        
        macros = factory.list_macros()
        
        assert len(macros) == 2
        assert "macro1" in macros
        assert "macro2" in macros
    
    def test_get_token_savings(self, temp_output_dir):
        """Test getting token savings."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        # Record command multiple times
        for _ in range(5):
            factory.record_command("test_cmd")
        
        factory.generate_macro("test_cmd", name="test_macro")
        
        savings = factory.get_token_savings("test_macro")
        
        # Token savings can be negative if macro is larger than original
        assert isinstance(savings, int)
    
    def test_export_macro(self, temp_output_dir):
        """Test exporting a macro."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        factory.generate_macro(
            command="test command",
            name="export_test"
        )
        
        output_path = factory.export_macro("export_test")
        
        assert Path(output_path).exists()
        assert output_path.endswith("export_test.py")
    
    def test_export_macro_not_found(self, temp_output_dir):
        """Test exporting a non-existent macro."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        with pytest.raises(ValueError):
            factory.export_macro("non_existent")
    
    def test_clear_history(self, temp_output_dir):
        """Test clearing command history."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        factory.record_command("cmd1")
        factory.record_command("cmd2")
        
        factory.clear_history()
        
        assert len(factory._command_history) == 0
    
    def test_generate_macro_token_savings(self, temp_output_dir):
        """Test that macro generation calculates token savings."""
        factory = FunctionFactory(output_dir=temp_output_dir)
        
        # Record command multiple times
        for _ in range(5):
            factory.record_command("lengthy command with many tokens")
        
        result = factory.generate_macro(
            command="lengthy command with many tokens",
            name="lengthy_cmd"
        )
        
        assert result.token_savings >= 0


class TestMacroConfig:
    """Test MacroConfig dataclass."""
    
    def test_macro_config_creation(self):
        """Test creating a macro config."""
        config = MacroConfig(
            name="test_macro",
            description="Test macro",
            command="test command"
        )
        
        assert config.name == "test_macro"
        assert config.description == "Test macro"
        assert config.command == "test command"
        assert config.parameters == []
    
    def test_macro_config_with_parameters(self):
        """Test creating a macro config with parameters."""
        config = MacroConfig(
            name="param_macro",
            description="Parameterized macro",
            command="test command",
            parameters=["arg1", "arg2"]
        )
        
        assert config.parameters == ["arg1", "arg2"]


class TestMacroResult:
    """Test MacroResult dataclass."""
    
    def test_macro_result_creation(self):
        """Test creating a macro result."""
        config = MacroConfig(
            name="test_macro",
            description="Test macro",
            command="test command"
        )
        
        result = MacroResult(
            macro_id="test-123",
            config=config,
            code="def test(): pass",
            token_savings=100
        )
        
        assert result.macro_id == "test-123"
        assert result.token_savings == 100
        assert result.code == "def test(): pass"
        assert result.created_at is not None
