"""
FN:mode_selector.py
Mode selection manager for Torro CLI with 4-mode selection.

Classes:
- Mode: Enum for available modes
- ModeSelector: Handles mode selection UI and logic

Functions:
- FN:get_mode_description: Get description for a mode (lines 45-60)
- FN:select_mode: Interactive mode selection (lines 62-80)
"""

from enum import Enum
from typing import Optional, List
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings


class Mode(str, Enum):
    """Enum defining available operation modes for Torro CLI."""
    PLAN = "plan"
    GAP_ANALYSIS = "gap_analysis"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    EXECUTE = "execute"


# Mode descriptions for user guidance
MODE_DESCRIPTIONS = {
    Mode.PLAN: "Create a detailed implementation plan with tasks and milestones",
    Mode.GAP_ANALYSIS: "Analyze current state vs target state and identify gaps",
    Mode.ROOT_CAUSE_ANALYSIS: "Investigate and identify root causes of issues",
    Mode.EXECUTE: "Execute tasks and implement changes",
}

# Style for mode selector
MODE_STYLE = Style.from_dict({
    "mode-item": "#00bfff",
    "mode-item.selected": "#ffffff bg:#005f87",
    "mode-description": "#888888",
})

# Key bindings for mode selection
selection_bindings = KeyBindings()


@selection_bindings.add("up")
def _(event):
    """Handle up arrow key."""
    widget = event.app.layout.focus
    if hasattr(widget, 'current_index'):
        widget.current_index = max(0, widget.current_index - 1)


@selection_bindings.add("down")
def _(event):
    """Handle down arrow key."""
    widget = event.app.layout.focus
    if hasattr(widget, 'current_index'):
        widget.current_index = len(Mode) - 1


@selection_bindings.add("enter")
def _(event):
    """Handle enter key for selection."""
    event.app.exit()


class ModeSelector:
    """
    Interactive mode selector for Torro CLI.
    Provides a menu-driven interface for selecting operation mode.
    """

    def __init__(self):
        """Initialize the mode selector."""
        self.modes = list(Mode)
        self.selected_index = 0
        self._selected_mode: Optional[Mode] = None

    @property
    def selected_mode(self) -> Optional[Mode]:
        """Get the currently selected mode."""
        return self._selected_mode

    def get_mode_description(self, mode: Mode) -> str:
        """
        FN:get_mode_description Get description for a specific mode.

        Args:
            mode: Mode enum value

        Returns:
            Description string
        """
        return MODE_DESCRIPTIONS.get(mode, "No description available")

    def _render_menu(self) -> HTML:
        """
        FN:_render_menu Render the mode selection menu.

        Returns:
            Formatted HTML string
        """
        lines = ["<b>Select Operation Mode:</b>", ""]
        for i, mode in enumerate(self.modes):
            prefix = "▶ " if i == self.selected_index else "  "
            style = "mode-item.selected" if i == self.selected_index else "mode-item"
            lines.append(f"<{style}>{prefix}{mode.value.replace('_', ' ').title()}</{style}>")
            if i == self.selected_index:
                lines.append(f"<mode-description>   {self.get_mode_description(mode)}</mode-description>")
        lines.append("")
        lines.append("<mode-description>Use ↑/↓ to navigate, Enter to select</mode-description>")
        return HTML("\n".join(lines))

    def select_mode(self) -> Optional[Mode]:
        """
        FN:select_mode Interactive mode selection with keyboard navigation.

        Returns:
            Selected Mode enum value or None if cancelled
        """
        try:
            # Simple selection using prompt
            choices = "\n".join([
                f"  {i+1}. {mode.value.replace('_', ' ').title()}"
                for i, mode in enumerate(self.modes)
            ])
            prompt_text = HTML(
                f"<b>Select Operation Mode:</b>\n{choices}\n\n"
                f"<mode-description>Enter mode number (1-{len(self.modes)}):</mode-description> "
            )

            result = prompt(
                prompt_text,
                style=MODE_STYLE,
                key_bindings=selection_bindings
            )

            # Parse selection
            try:
                index = int(result) - 1
                if 0 <= index < len(self.modes):
                    self._selected_mode = self.modes[index]
                    return self._selected_mode
            except (ValueError, IndexError):
                pass

            return None

        except (EOFError, KeyboardInterrupt):
            return None


def get_mode_description(mode: Mode) -> str:
    """
    FN:get_mode_description Standalone function to get mode description.

    Args:
        mode: Mode enum value

    Returns:
        Description string
    """
    return MODE_DESCRIPTIONS.get(mode, "No description available")


def select_mode() -> Optional[Mode]:
    """
    FN:select_mode Standalone function for mode selection.

    Returns:
        Selected Mode or None
    """
    selector = ModeSelector()
    return selector.select_mode()
