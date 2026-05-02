"""
FN:cli.py
Command-line interface for Torro agent framework with interactive chat support.

Functions:
- FN:main: Main CLI entry point (lines 45-150)
- FN:show_status: Show Torro status (lines 152-170)
- FN:show_version: Show version information (lines 172-180)
- FN:run_interactive: Run interactive chat mode (lines 182-220)

Usage:
    python -m torro.cli --help
    python -m torro.cli status
    python -m torro.cli --version
    python -m torro.cli interactive
"""

import argparse
import logging
import sys
import time
from typing import Optional
from pathlib import Path

# Import CLI components
from cli.structured_io import StructuredIO, Message, MessageType, ControlRequest
from cli.tui_renderer import TUIRenderer
from cli.mode_selector import ModeSelector, Mode
from cli.clarification import ClarificationManager
from cli.stream_handler import StreamHandler, StreamState
from cli.permission_mgr import PermissionManager, PermissionLevel
from cli.session_db import SessionDB
from cli.ai_provider import (
    AIProvider,
    ModelRegistry,
    create_provider,
    list_models,
    get_model_config
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def show_status() -> int:
    """FN:show_status Show Torro status.
    
    Returns:
        Exit code (0 for success)
    """
    print("=== Torro Agent Status ===")
    print("Status: Ready")
    print("Version: 0.1.0")
    
    # Check core components
    try:
        from .tools.base import Tool
        print("Tool ABC: OK")
    except ImportError as e:
        print(f"Tool ABC: FAILED - {e}")
        return 1
    
    try:
        from .tools.registry import ToolRegistry
        print("Tool Registry: OK")
    except ImportError as e:
        print(f"Tool Registry: FAILED - {e}")
        return 1
    
    try:
        from .context.base import ContextEngine
        print("ContextEngine ABC: OK")
    except ImportError as e:
        print(f"ContextEngine ABC: FAILED - {e}")
        return 1
    
    try:
        from .memory.manager import MemoryManager
        print("MemoryManager: OK")
    except ImportError as e:
        print(f"MemoryManager: FAILED - {e}")
        return 1
    
    try:
        from .coordinator.mode import is_coordinator_mode
        print("Coordinator Mode: OK")
    except ImportError as e:
        print(f"Coordinator Mode: FAILED - {e}")
        return 1
    
    try:
        from .innovation.auto_dream import AutoDream
        print("autoDream: OK")
    except ImportError as e:
        print(f"autoDream: FAILED - {e}")
        return 1
    
    try:
        from .gateway.base import BasePlatformAdapter
        print("Gateway Pattern: OK")
    except ImportError as e:
        print(f"Gateway Pattern: FAILED - {e}")
        return 1
    
    print("\n=== All Components Ready ===")
    return 0


def show_version() -> None:
    """FN:show_version Show version information."""
    print("Torro Agent Framework v0.1.0")
    print("Built with Python")


def run_interactive(args: argparse.Namespace) -> int:
    """FN:run_interactive Run interactive chat mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    # Initialize model registry
    registry = ModelRegistry()
    model_name = args.model or registry.default_model or "local/qwen2.5:7b"
    
    print("=== Torro Interactive CLI ===")
    print(f"Model: {model_name}")
    print("Type 'exit' to quit, 'help' for commands\n")
    
    # Initialize components
    session_db = SessionDB()
    clarification_mgr = ClarificationManager()
    permission_mgr = PermissionManager()
    stream_handler = StreamHandler()
    mode_selector = ModeSelector()
    
    # Create AI provider from config.ini model name
    try:
        provider = create_provider(model_name)
    except Exception as e:
        print(f"Error creating provider: {e}")
        print("Falling back to default model...")
        provider = create_provider("local/qwen2.5:7b")
    
    # Create session
    session_id = f"session_{int(time.time())}"
    session_db.create_session(session_id, "interactive")
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("Commands: exit, quit, help, mode, model, list")
                print(f"Current model: {model_name}")
                continue
            
            if user_input.lower() == "mode":
                mode = mode_selector.select_mode()
                if mode:
                    print(f"Selected mode: {mode.value}")
                continue
            
            if user_input.lower() == "model":
                new_model = input("Enter model name: ").strip()
                if new_model:
                    try:
                        provider = create_provider(new_model)
                        model_name = new_model
                        print(f"Switched to model: {model_name}")
                    except Exception as e:
                        print(f"Error switching model: {e}")
                continue
            
            if user_input.lower() == "list":
                models = registry.list_models()
                print("\nAvailable models:")
                print(f"{'Name':<30} {'Provider':<12} {'Model':<30} {'Context':<10}")
                print("-" * 82)
                for m in models:
                    print(f"{m.name:<30} {m.provider_type:<12} {m.model_name:<30} {m.context_window:<10}")
                print()
                continue
            
            # Check for ambiguity
            ambiguities = clarification_mgr.detect_ambiguity(user_input)
            if ambiguities:
                print(f"Ambiguity detected: {', '.join(ambiguities)}")
            
            # Generate response
            print("\nAssistant: ", end="")
            response = ""
            for token in provider.stream(user_input):
                print(token, end="", flush=True)
                response += token
            print("\n")
            
            # Save to session
            session_db.add_message(session_id, "user", user_input)
            session_db.add_message(session_id, "assistant", response)
            
        except KeyboardInterrupt:
            print("\nInterrupted!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")
            break
    
    session_db.close()
    return 0


def main(argv: Optional[list] = None) -> int:
    """FN:main Main CLI entry point.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        prog="torro",
        description="Torro Agent Framework - Autonomous AI Agent System"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show Torro status and component health"
    )
    
    # Interactive command
    interactive_parser = subparsers.add_parser(
        "interactive",
        help="Run interactive chat mode"
    )
    interactive_parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name from config.ini"
    )
    interactive_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode"
    )
    
    # Models command
    models_parser = subparsers.add_parser(
        "models",
        help="List available AI models"
    )
    models_parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="Filter by provider type (ollama, openai, etc.)"
    )
    
    args = parser.parse_args(argv)
    
    if args.version:
        show_version()
        return 0
    
    if args.command == "status":
        return show_status()
    
    if args.command == "interactive":
        return run_interactive(args)
    
    if args.command == "models":
        return list_models_cmd(args)
    
    # Default: show help
    parser.print_help()
    return 0


def list_models_cmd(args: argparse.Namespace) -> int:
    """FN:list_models_cmd List available AI models from config.ini.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    registry = ModelRegistry()
    models = registry.list_models()
    
    if not models:
        print("No models configured. Edit config.ini [CLI_MODELS] section.")
        return 0
    
    provider_filter = getattr(args, 'provider', None)
    if provider_filter:
        models = [m for m in models if m.provider_type == provider_filter]
    
    print("=== Available AI Models ===")
    print(f"{'Name':<30} {'Provider':<12} {'Model':<30} {'Context':<10}")
    print("-" * 82)
    for m in models:
        print(f"{m.name:<30} {m.provider_type:<12} {m.model_name:<30} {m.context_window:<10}")
    
    print(f"\nTotal: {len(models)} models")
    print(f"Default: {registry.default_model}")
    print(f"Swarm: {registry.swarm_model}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
