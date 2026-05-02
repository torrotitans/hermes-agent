"""
FN:scrubber.py
Streaming context scrubber for Torro agent framework.

Classes:
- StreamingContextScrubber: Stateful text scrubber for streaming content

Functions:
- FN:strip_memory_tags: Strip memory context tags from text (lines 52-62)
"""

import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


# Memory context XML tag pattern
MEMORY_TAG_PATTERN = re.compile(r'<memory-context[^>]*>.*?</memory-context>', re.DOTALL)


def strip_memory_tags(text: str) -> str:
    """FN:strip_memory_tags Strip memory context tags from text.
    
    Args:
        text: Text to process
        
    Returns:
        Text with memory tags removed
    """
    return MEMORY_TAG_PATTERN.sub('', text)


class StreamingContextScrubber:
    """Stateful scrubber for streaming text content.
    
    The scrubber processes text incrementally, removing sensitive
    or internal context markers from streaming output.
    
    Example:
        ```python
        scrubber = StreamingContextScrubber()
        
        # Feed text chunks
        chunk1 = scrubber.feed("Start of text <memory-context>")
        chunk2 = scrubber.feed("hidden content</memory-context> end")
        
        # Flush remaining content
        final = scrubber.flush()
        ```
    """
    
    # Tag patterns to scrub
    TAG_PATTERNS = [
        (re.compile(r'<memory-context[^>]*>.*?</memory-context>', re.DOTALL), ''),
        (re.compile(r'<internal[^>]*>.*?</internal>', re.DOTALL), ''),
        (re.compile(r'<!--.*?-->', re.DOTALL), ''),
    ]
    
    def __init__(self):
        """Initialize the scrubber."""
        self._buffer = ""
        self._position = 0
        logger.info("FN:StreamingContextScrubber.__init__ Scrubber initialized")
    
    def reset(self) -> None:
        """FN:reset Reset the scrubber state."""
        self._buffer = ""
        self._position = 0
        logger.debug("FN:StreamingContextScrubber.reset Scrubber reset")
    
    def feed(self, text: str) -> str:
        """FN:feed Feed text into the scrubber.
        
        Args:
            text: Text chunk to process
            
        Returns:
            Scrubbed text output
        """
        self._buffer += text
        
        # Process complete tags in buffer
        result = self._process_buffer()
        
        logger.debug("FN:StreamingContextScrubber.feed Processed %d chars", len(text))
        return result
    
    def flush(self) -> str:
        """FN:flush Flush remaining buffered content.
        
        Returns:
            Final scrubbed output
        """
        # Process any remaining buffer
        result = self._process_buffer(force=True)
        # Strip any incomplete tags when flushing
        result = self._strip_incomplete_tag(result)
        self.reset()
        logger.debug("FN:StreamingContextScrubber.flush Flushed %d chars", len(result))
        return result
    
    def _process_buffer(self, force: bool = False) -> str:
        """FN:_process_buffer Process the internal buffer.
        
        Args:
            force: Force processing of incomplete tags
            
        Returns:
            Processed text from buffer
        """
        if not self._buffer:
            return ""
        
        result = self._buffer
        
        # Apply all tag patterns
        for pattern, replacement in self.TAG_PATTERNS:
            result = pattern.sub(replacement, result)
        
        # Update position
        self._position = len(result)
        
        # Clear buffer if forced or if no incomplete tags
        if force or not self._has_incomplete_tag(result):
            output = result
            self._buffer = ""
            return output
        
        # Keep incomplete tag in buffer
        incomplete_pos = self._find_incomplete_tag(result)
        if incomplete_pos >= 0:
            output = result[:incomplete_pos]
            self._buffer = result[incomplete_pos:]
            return output
        
        return result
    
    def _strip_incomplete_tag(self, text: str) -> str:
        """FN:_strip_incomplete_tag Strip incomplete tags from text.
        
        Args:
            text: Text to process
            
        Returns:
            Text with incomplete tags removed
        """
        # Pattern to match incomplete tags at end of string
        pattern = re.compile(r'<(memory-context|internal)[^>]*$')
        return pattern.sub('', text)
    
    def _has_incomplete_tag(self, text: str) -> bool:
        """FN:_has_incomplete_tag Check for incomplete XML tag.
        
        Args:
            text: Text to check
            
        Returns:
            True if incomplete tag found
        """
        # Check for opening tag without closing
        open_pattern = re.compile(r'<(memory-context|internal)[^>]*$')
        return bool(open_pattern.search(text))
    
    def _find_incomplete_tag(self, text: str) -> int:
        """FN:_find_incomplete_tag Find position of incomplete tag.
        
        Args:
            text: Text to search
            
        Returns:
            Position of incomplete tag, or -1
        """
        # Find last opening tag without closing
        last_open = text.rfind('<')
        if last_open >= 0:
            # Check if there's a closing tag after
            close_pos = text.find('>', last_open)
            if close_pos < 0:
                return last_open
        return -1
