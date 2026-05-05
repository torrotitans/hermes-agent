"""
FN:tui_renderer.py
Interactive TUI renderer using prompt_toolkit for Torro CLI.

Classes:
- TUIRenderer: Main TUI rendering engine

Functions:
- FN:create_application: Create prompt_toolkit Application instance (lines 85-120)
- FN:render_status_bar: Render status bar with metrics (lines 122-150)
"""

from typing import Optional, Dict, Any
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import Frame
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style


# Apple Liquid Glass-inspired style for Torro CLI
TORRO_STYLE = Style.from_dict({
    "status-bar": "bg:#1a1a2e #ffffff bold",
    "status-bar.model": "#00ff88 bold",
    "status-bar.tokens": "#00d4ff",
    "status-bar.duration": "#ff6b6b",
    "input-prompt": "#00ff88 bold",
    "output-text": "#e0e0e0",
    "error-text": "#ff4444 bold",
    "success-text": "#00ff88",
    "warning-text": "#ffaa00",
    "info-text": "#00d4ff",
    "header": "#00ff88 bold",
    "timestamp": "#666666",
})

# Key bindings for TUI
bindings = KeyBindings()


@bindings.add("c-c")
def _(event):
    """Handle Ctrl+C for graceful exit."""
    event.app.exit(exception=KeyboardInterrupt("Interrupted"))


@bindings.add("c-d")
def _(event):
    """Handle Ctrl+D for exit."""
    event.app.exit()


class TUIRenderer:
    """
    Interactive TUI renderer using prompt_toolkit.
    Provides status bar, input buffer, and output display.
    """

    def __init__(self, model_name: str = "local"):
        """
        Initialize the TUI renderer.

        Args:
            model_name: Name of the AI model to display in status bar
        """
        self.model_name = model_name
        self.token_count = 0
        self.duration_seconds = 0
        self.output_buffer = Buffer(read_only=True)
        self.input_buffer = Buffer()
        self._output_control = BufferControl(buffer=self.output_buffer)
        self._status_text = ""
        self._header_text = self._get_header()
        self._input_control = FormattedTextControl(
            text=HTML("<input-prompt>➤ </input-prompt>"),
            focusable=True,
            buffer=self.input_buffer
        )

    def update_status(self, model: str, tokens: int, duration: float):
        """
        FN:update_status Update status bar metrics.

        Args:
            model: Model name
            tokens: Token count
            duration: Duration in seconds
        """
        self.model_name = model
        self.token_count = tokens
        self.duration_seconds = duration

    def add_output(self, text: str):
        """
        FN:add_output Append text to output buffer.

        Args:
            text: Text to append
        """
        self.output_buffer.text += text + "\n"
        self.output_buffer.cursor_position = len(self.output_buffer.text)

    def _get_header(self) -> HTML:
        """
        FN:_get_header Generate header with Torro branding.

        Returns:
            Formatted HTML string for header
        """
        return HTML(
            '<header>╔══════════════════════════════════════════════════════════╗</header>\n'
            '<header>║  </header><header style="color: #00ff88; font-weight: bold">TORRO AGENT</header><header>                              ║</header>\n'
            '<header>║  </header><header style="color: #00d4ff">Autonomous Agent Framework</header><header>                    ║</header>\n'
            '<header>╚══════════════════════════════════════════════════════════╝</header>'
        )

    def _get_status_bar(self) -> HTML:
        """
        FN:render_status_bar Generate status bar HTML with metrics.

        Returns:
            Formatted HTML string for status bar
        """
        return HTML(
            f"<status-bar> 🚀 <status-bar.model>{self.model_name}</status-bar.model> | "
            f"⚡ <status-bar.tokens>{self.token_count} tokens</status-bar.tokens> | "
            f"⏱️  <status-bar.duration>{self.duration_seconds:.1f}s</status-bar.duration> "
            f"</status-bar>"
        )

    def create_application(self) -> Application:
        """
        FN:create_application Create and configure prompt_toolkit Application.

        Returns:
            Configured Application instance
        """
        # Create layout with header, output area, input area, and status bar
        header_window = Window(
            content=FormattedTextControl(self._header_text),
            height=4
        )

        output_window = Window(
            content=self._output_control,
            wrap_lines=True,
            height=12
        )

        input_window = Window(
            content=self._input_control,
            height=1
        )

        # Main layout
        root_container = HSplit([
            header_window,
            Frame(output_window, title="📋 Output"),
            input_window,
            Window(
                content=FormattedTextControl(self._get_status_bar),
                height=1
            )
        ])

        layout = Layout(root_container, focused_element=input_window)

        # Create application
        app = Application(
            layout=layout,
            key_bindings=bindings,
            style=TORRO_STYLE,
            full_screen=True,
            mouse_support=True,
            refresh_interval=0.1
        )

        return app

    def render(self) -> Application:
        """
        FN:render Render the TUI and return the application.

        Returns:
            Application instance for running
        """
        return self.create_application()


def render_status_bar(model: str, tokens: int, duration: float) -> HTML:
    """
    FN:render_status_bar Standalone function to render status bar.

    Args:
        model: Model name
        tokens: Token count
        duration: Duration in seconds

    Returns:
        Formatted HTML string
    """
    return HTML(
        f"<status-bar> 🚀 <status-bar.model>{model}</status-bar.model> | "
        f"⚡ <status-bar.tokens>{tokens} tokens</status-bar.tokens> | "
        f"⏱️  <status-bar.duration>{duration:.1f}s</status-bar.duration> "
        f"</status-bar>"
    )
