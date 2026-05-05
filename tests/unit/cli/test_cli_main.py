"""
FN:test_cli_main.py
Unit tests for CLI main function.

Functions:
- FN:test_cli_help: Test --help flag (lines 20-35)
- FN:test_cli_version: Test --version flag (lines 38-50)
- FN:test_cli_status: Test status command (lines 53-70)
- FN:test_cli_no_args_shows_help: Test no args shows help (lines 73-85)
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import io

# Import the main function from cli module
sys.path.insert(0, 'src')
from cli.cli import main


class TestCliMain(unittest.TestCase):
    """Test cases for CLI main function."""
    
    def test_cli_help(self):
        """FN:test_cli_help Test --help flag shows help message."""
        # Capture stdout and stderr
        captured_out = io.StringIO()
        captured_err = io.StringIO()
        sys.stdout = captured_out
        sys.stderr = captured_err
        
        try:
            # Run with --help (should raise SystemExit)
            with self.assertRaises(SystemExit):
                main(['--help'])
            
            # Check help message was printed
            output = captured_out.getvalue() + captured_err.getvalue()
            
            # Verify help message contains expected content
            self.assertIn('Torro Agent Framework', output)
            self.assertIn('--help', output)
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
    
    def test_cli_version(self):
        """FN:test_cli_version Test --version flag shows version."""
        captured = io.StringIO()
        sys.stdout = captured
        
        try:
            result = main(['--version'])
            output = captured.getvalue()
            
            self.assertIn('Torro', output)
            self.assertIn('v0.1.0', output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_cli_status(self):
        """FN:test_cli_status Test status command."""
        captured = io.StringIO()
        sys.stdout = captured
        
        try:
            result = main(['status'])
            output = captured.getvalue()
            
            self.assertIn('Torro Agent Status', output)
            self.assertIn('Ready', output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_cli_no_args_shows_help(self):
        """FN:test_cli_no_args_shows_help Test no args shows help."""
        captured = io.StringIO()
        sys.stdout = captured
        
        try:
            result = main([])
            output = captured.getvalue()
            
            self.assertIn('Torro Agent Framework', output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
