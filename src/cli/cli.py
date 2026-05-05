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
from autonomous import AgenticOrchestrator, TaskType, CircuitBreakerError
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
from cli.greetings import get_greeting, get_banner
from cli.greetings import COLORS

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
        from ..tools.base import Tool
        print("Tool ABC: OK")
    except ImportError as e:
        print(f"Tool ABC: FAILED - {e}")
        return 1
    
    try:
        from ..tools.registry import ToolRegistry
        print("Tool Registry: OK")
    except ImportError as e:
        print(f"Tool Registry: FAILED - {e}")
        return 1
    
    try:
        from ..context.base import ContextEngine
        print("ContextEngine ABC: OK")
    except ImportError as e:
        print(f"ContextEngine ABC: FAILED - {e}")
        return 1
    
    try:
        from ..memory.manager import MemoryManager
        print("MemoryManager: OK")
    except ImportError as e:
        print(f"MemoryManager: FAILED - {e}")
        return 1
    
    try:
        from ..coordinator.mode import is_coordinator_mode
        print("Coordinator Mode: OK")
    except ImportError as e:
        print(f"Coordinator Mode: FAILED - {e}")
        return 1
    
    try:
        from ..innovation.auto_dream import AutoDream
        print("autoDream: OK")
    except ImportError as e:
        print(f"autoDream: FAILED - {e}")
        return 1
    
    try:
        from ..gateway.base import BasePlatformAdapter
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
    
    # Use provided model, or default from CLI_MODELS, or fall back to OPENAI_API base model
    model_name = args.model
    if not model_name:
        model_name = registry.default_model or "local_qwen25_7b"
    
    # Create AI provider from config.ini model name
    provider = None
    provider_type = None
    
    try:
        provider = create_provider(model_name)
        provider_type = type(provider).__name__
    except Exception as e:
        print(f"Warning: Could not create provider for '{model_name}': {e}")
        provider = None
    
    # Perform health check on the API BEFORE showing the banner
    if provider is not None and hasattr(provider, 'health_check'):
        is_healthy, health_msg = provider.health_check()
        if not is_healthy:
            print(f"[Info] {health_msg}")
            print("Falling back to OPENAI_API base model...")
            provider = None
    
    # If provider is None (failed creation or health check), try OPENAI_API config
    if provider is None:
        try:
            from cli.ai_provider import ModelConfig, OpenAIProvider
            import configparser
            
            config = configparser.ConfigParser()
            config.read("config.ini")
            
            if config.has_section("OPENAI_API"):
                base_url = config.get("OPENAI_API", "base_url", fallback="http://localhost:8000/v1")
                model = config.get("OPENAI_API", "model", fallback="gpt-3.5-turbo")
                api_key = config.get("OPENAI_API", "api_key", fallback=None)
                
                base_config = ModelConfig(
                    name="base_model",
                    provider_type="openai",
                    model_name=model,
                    base_url=base_url,
                    api_key=api_key if api_key and api_key != "empty" else None
                )
                provider = OpenAIProvider(base_config)
                provider_type = "OpenAIProvider (base model)"
                model_name = f"{base_url}/{model}"
                print(f"Using base model: {model}")
            else:
                print("Error: No [OPENAI_API] section in config.ini")
                return 1
        except Exception as fallback_error:
            print(f"Error: Could not create fallback provider: {fallback_error}")
            print("Please check your config.ini [OPENAI_API] section.")
            return 1
    
    # Show ASCII banner
    banner = get_banner()
    print(banner)
    
    # Display model info with gradient effect
    print(f"{COLORS['cyan']}{COLORS['bold']}┌─ Model:{COLORS['reset']} {COLORS['white']}{model_name}{COLORS['reset']}")
    print(f"{COLORS['cyan']}{COLORS['bold']}├─ Provider:{COLORS['reset']} {COLORS['white']}{provider_type}{COLORS['reset']}")
    print(f"{COLORS['dim']}└─ Type 'exit' to quit, 'help' for commands{COLORS['reset']}")
    
    # Show initial greeting with color and animation effect
    greeting_msg, greeting_emoji, greeting_color = get_greeting()
    color_code = COLORS.get(greeting_color, COLORS['white'])
    print(f"{COLORS['bold']}{COLORS['cyan']}╭─ Torro Agent{COLORS['reset']}")
    print(f"{COLORS['bold']}{COLORS['cyan']}│{COLORS['reset']} Hello! I'm Torro. {color_code}{greeting_msg} {greeting_emoji}{COLORS['reset']}")
    print(f"{COLORS['bold']}{COLORS['cyan']}╰─{COLORS['reset']} How can I help you today?\n")
    
    # Initialize components
    session_db = SessionDB()
    clarification_mgr = ClarificationManager()
    permission_mgr = PermissionManager()
    stream_handler = StreamHandler()
    mode_selector = ModeSelector()
    orchestrator = AgenticOrchestrator()
    
    # Create session
    session_id = f"session_{int(time.time())}"
    session_db.create_session(session_id, "interactive")
    
    # Enhanced input prompt with color
    prompt_symbol = f"{COLORS['green']}{COLORS['bold']}❯{COLORS['reset']} "
    
    # Main loop
    while True:
        try:
            # Get user input with colored prompt
            user_input = input(prompt_symbol).strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit"):
                print(f"\n{COLORS['cyan']}═══════════════════════════════════════════════════════════{COLORS['reset']}")
                print(f"{COLORS['green']}{COLORS['bold']}  👋 Goodbye! Thank you for using Torro Agent!{COLORS['reset']}")
                print(f"{COLORS['cyan']}═══════════════════════════════════════════════════════════{COLORS['reset']}\n")
                break
            
            if user_input.lower() == "help":
                print(f"\n{COLORS['yellow']}{COLORS['bold']}╭─ Available Commands{COLORS['reset']}")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}exit{COLORS['reset']}     - Exit the application")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}quit{COLORS['reset']}     - Exit the application")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}help{COLORS['reset']}     - Show this help message")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}mode{COLORS['reset']}     - Select execution mode")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}model{COLORS['reset']}    - Change AI model")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}list{COLORS['reset']}     - List available models")
                print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['bold']}status{COLORS['reset']}   - Show system status")
                print(f"{COLORS['yellow']}{COLORS['bold']}╰─{COLORS['reset']}\n")
                continue
            
            if user_input.lower() == "mode":
                mode = mode_selector.select_mode()
                if mode:
                    print(f"\n{COLORS['green']}{COLORS['bold']}✓{COLORS['reset']} Selected mode: {COLORS['cyan']}{mode.value}{COLORS['reset']}\n")
                continue
            
            if user_input.lower() == "model":
                new_model = input(f"{COLORS['cyan']}Enter model name: {COLORS['reset']}").strip()
                if new_model:
                    try:
                        provider = create_provider(new_model)
                        model_name = new_model
                        print(f"\n{COLORS['green']}{COLORS['bold']}✓{COLORS['reset']} Switched to model: {COLORS['cyan']}{model_name}{COLORS['reset']}\n")
                    except Exception as e:
                        print(f"\n{COLORS['red']}{COLORS['bold']}✗{COLORS['reset']} Error switching model: {COLORS['red']}{e}{COLORS['reset']}\n")
                continue
            
            if user_input.lower() == "list":
                models = registry.list_models()
                print(f"\n{COLORS['yellow']}{COLORS['bold']}╭─ Available AI Models{COLORS['reset']}")
                print(f"{COLORS['dim']}│{'Name':<30} {'Provider':<12} {'Model':<30} {'Context':<10}{COLORS['reset']}")
                print(f"{COLORS['dim']}├{'─' * 82}{COLORS['reset']}")
                for m in models:
                    print(f"{COLORS['cyan']}│{COLORS['reset']} {COLORS['white']}{m.name:<30}{COLORS['reset']} {COLORS['yellow']}{m.provider_type:<12}{COLORS['reset']} {COLORS['green']}{m.model_name:<30}{COLORS['reset']} {COLORS['blue']}{m.context_window:<10}{COLORS['reset']}")
                print(f"{COLORS['yellow']}{COLORS['bold']}╰─{COLORS['reset']} {COLORS['dim']}Total: {len(models)} models{COLORS['reset']}\n")
                continue
            
            # Check for ambiguity
            ambiguities = clarification_mgr.detect_ambiguity(user_input)
            if ambiguities:
                print(f"Ambiguity detected: {', '.join(ambiguities)}")
            
            # Route task through orchestrator
            try:
                task_id = orchestrator.route_task(
                    task_type=TaskType.SIMPLE,
                    description=user_input,
                    payload={"input": user_input}
                )
                logger.debug("FN:run_interactive Task routed: %s", task_id)
            except CircuitBreakerError as e:
                print(f"\nCircuit Breaker: {e}")
                print("Please rephrase your request or try a different approach.")
                continue
            
            # Generate response with visual indicator
            print(f"\n{COLORS['magenta']}{COLORS['bold']}╭─ Torro Agent Response{COLORS['reset']}")
            response = ""
            try:
                print(f"{COLORS['magenta']}│{COLORS['reset']} ", end="")
                for token in provider.stream(user_input):
                    print(token, end="", flush=True)
                    response += token
                print(f"\n{COLORS['magenta']}{COLORS['bold']}╰─{COLORS['reset']} {COLORS['dim']}Response complete{COLORS['reset']}\n")
            except Exception as e:
                print(f"\n{COLORS['red']}{COLORS['bold']}╰─ ✗ Error: {e}{COLORS['reset']}\n")
                response = f"[Error] {e}"
            
            # Record command for frequency analysis
            orchestrator.record_command(user_input)
            
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
