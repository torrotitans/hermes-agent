"""
FN:stream_handler.py
Streaming response handler for token-by-token AI responses in Torro CLI.

Classes:
- StreamHandler: Manages streaming output with progress indicators

Functions:
- FN:stream_text: Stream text token by token (lines 50-75)
- FN:format_token: Format individual token for display (lines 77-90)
"""

import sys
import time
from typing import Optional, Generator, Callable
from dataclasses import dataclass
from enum import Enum


class StreamState(str, Enum):
    """Enum for stream state tracking."""
    IDLE = "idle"
    STREAMING = "streaming"
    COMPLETE = "complete"
    INTERRUPTED = "interrupted"


@dataclass
class StreamMetrics:
    """Metrics for streaming output."""
    token_count: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    tokens_per_second: float = 0.0

    @property
    def duration(self) -> float:
        """Calculate stream duration."""
        return self.end_time - self.start_time


class StreamHandler:
    """
    Handles token-by-token streaming for AI responses.
    Provides progress indicators and metrics tracking.
    """

    def __init__(self, output_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the stream handler.

        Args:
            output_callback: Optional callback for each token
        """
        self.output_callback = output_callback
        self._state = StreamState.IDLE
        self._metrics = StreamMetrics()
        self._buffer = ""

    @property
    def state(self) -> StreamState:
        """Get current stream state."""
        return self._state

    @property
    def metrics(self) -> StreamMetrics:
        """Get stream metrics."""
        return self._metrics

    def start(self):
        """
        FN:start Begin streaming session.
        """
        self._state = StreamState.STREAMING
        self._metrics = StreamMetrics(
            token_count=0,
            start_time=time.time()
        )
        self._buffer = ""

    def write(self, token: str):
        """
        FN:write Write a single token to output.

        Args:
            token: Token string to write
        """
        if self._state != StreamState.STREAMING:
            return

        self._buffer += token
        self._metrics.token_count += 1

        # Output token
        print(token, end="", flush=True)

        # Call callback if provided
        if self.output_callback:
            self.output_callback(token)

    def end(self):
        """
        FN:end End streaming session and finalize metrics.
        """
        self._state = StreamState.COMPLETE
        self._metrics.end_time = time.time()

        # Calculate tokens per second
        if self._metrics.duration > 0:
            self._metrics.tokens_per_second = (
                self._metrics.token_count / self._metrics.duration
            )

        # Print newline after stream
        print()

    def interrupt(self):
        """
        FN:interrupt Interrupt the streaming session.
        """
        self._state = StreamState.INTERRUPTED
        self._metrics.end_time = time.time()

    def stream_text(
        self,
        text: str,
        delay: float = 0.01
    ) -> Generator[str, None, None]:
        """
        FN:stream_text Stream text token by token with optional delay.

        Args:
            text: Text to stream
            delay: Delay between tokens in seconds

        Yields:
            Each token as it's streamed
        """
        self.start()

        try:
            # Simple tokenization by whitespace
            tokens = text.split()

            for token in tokens:
                if self._state != StreamState.STREAMING:
                    break

                # Add space before token (except first)
                if self._metrics.token_count > 0:
                    yield " "
                    self.write(" ")

                yield token + " "
                self.write(token + " ")

                # Small delay for visual effect
                if delay > 0:
                    time.sleep(delay)

        except (KeyboardInterrupt, EOFError):
            self.interrupt()
        finally:
            self.end()

    def get_buffer(self) -> str:
        """
        FN:get_buffer Get the current buffer content.

        Returns:
            Buffered text content
        """
        return self._buffer

    def clear_buffer(self):
        """
        FN:clear_buffer Clear the output buffer.
        """
        self._buffer = ""


def stream_text(
    text: str,
    delay: float = 0.01,
    output_callback: Optional[Callable[[str], None]] = None
) -> Generator[str, None, None]:
    """
    FN:stream_text Standalone function for streaming text.

    Args:
        text: Text to stream
        delay: Delay between tokens
        output_callback: Optional callback for each token

    Yields:
        Each token
    """
    handler = StreamHandler(output_callback)
    yield from handler.stream_text(text, delay)


def format_token(token: str, is_special: bool = False) -> str:
    """
    FN:format_token Format a token for display.

    Args:
        token: Token string
        is_special: Whether token is special

    Returns:
        Formatted token string
    """
    if is_special:
        return f"[{token}]"
    return token
