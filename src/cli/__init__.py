"""
FN:__init__.py
Package: src.cli
Summary: Terminal-based interactive CLI for Torro Agent with streaming responses and mode selection.

Structure:
- __init__.py
- structured_io.py
- tui_renderer.py
- mode_selector.py
- clarification.py
- stream_handler.py
- ai_provider.py
- permission_mgr.py
- session_db.py
- command_registry.py

Entry Points:
- src/cli/structured_io.py (NDJSON I/O)
- src/cli/tui_renderer.py (Interactive TUI)

Flow:
- CLI Input -> structured_io -> tui_renderer -> mode_selector -> clarification -> ai_provider -> stream_handler

Read First:
- structured_io.py
- tui_renderer.py
- ai_provider.py
"""

from .structured_io import (
    StructuredIO,
    MessageType,
    Message,
    ControlRequest,
    ControlResponse,
)

__all__ = [
    "StructuredIO",
    "MessageType",
    "Message",
    "ControlRequest",
    "ControlResponse",
]
