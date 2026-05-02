"""
FN:test_scrubber.py
Unit tests for Torro streaming context scrubber.

Tests:
- TestStreamingContextScrubber: Test scrubber class
- TestStripMemoryTags: Test strip_memory_tags helper function
"""

import pytest

from memory.scrubber import (
    StreamingContextScrubber,
    strip_memory_tags,
)


class TestStripMemoryTags:
    """Test strip_memory_tags helper function."""
    
    def test_strip_memory_tags_empty_string(self):
        """Test stripping tags from empty string."""
        result = strip_memory_tags("")
        assert result == ""
    
    def test_strip_memory_tags_no_tags(self):
        """Test stripping tags from text without tags."""
        text = "Hello world"
        result = strip_memory_tags(text)
        assert result == text
    
    def test_strip_memory_tags_single_tag(self):
        """Test stripping a single memory tag."""
        text = "Before <memory-context>hidden</memory-context> After"
        result = strip_memory_tags(text)
        assert result == "Before  After"
    
    def test_strip_memory_tags_multiple_tags(self):
        """Test stripping multiple memory tags."""
        text = "<memory-context>1</memory-context>Mid<memory-context>2</memory-context>"
        result = strip_memory_tags(text)
        assert result == "Mid"


class TestStreamingContextScrubber:
    """Test StreamingContextScrubber class."""
    
    def test_scrubber_init(self):
        """Test scrubber initialization."""
        scrubber = StreamingContextScrubber()
        assert scrubber._buffer == ""
        assert scrubber._position == 0
    
    def test_scrubber_reset(self):
        """Test scrubber reset method."""
        scrubber = StreamingContextScrubber()
        scrubber._buffer = "test"
        scrubber._position = 4
        
        scrubber.reset()
        assert scrubber._buffer == ""
        assert scrubber._position == 0
    
    def test_scrubber_feed_simple(self):
        """Test feeding simple text to scrubber."""
        scrubber = StreamingContextScrubber()
        result = scrubber.feed("Hello")
        assert result == "Hello"
    
    def test_scrubber_feed_with_tag(self):
        """Test feeding text with memory tag."""
        scrubber = StreamingContextScrubber()
        result = scrubber.feed("Before <memory-context>hidden</memory-context> After")
        assert "hidden" not in result
        assert "Before" in result
        assert "After" in result
    
    def test_scrubber_feed_incomplete_tag(self):
        """Test feeding text with incomplete tag."""
        scrubber = StreamingContextScrubber()
        result = scrubber.feed("Before <memory-context")
        # Incomplete tag should be buffered
        assert result == "Before "
    
    def test_scrubber_feed_complete_tag_later(self):
        """Test completing an incomplete tag."""
        scrubber = StreamingContextScrubber()
        result1 = scrubber.feed("Before <memory-context")
        result2 = scrubber.feed(">hidden</memory-context> After")
        
        assert result1 == "Before "
        assert "hidden" not in result2
    
    def test_scrubber_flush(self):
        """Test flushing remaining buffer."""
        scrubber = StreamingContextScrubber()
        scrubber.feed("Before <memory-context")
        result = scrubber.flush()
        
        assert "memory-context" not in result
    
    def test_scrubber_feed_and_flush(self):
        """Test full feed and flush cycle."""
        scrubber = StreamingContextScrubber()
        
        result1 = scrubber.feed("Start ")
        result2 = scrubber.feed("<memory-context>hidden</memory-context> ")
        result3 = scrubber.feed("End")
        result4 = scrubber.flush()
        
        combined = result1 + result2 + result3 + result4
        assert "hidden" not in combined
        assert "Start" in combined
        assert "End" in combined
    
    def test_scrubber_multiple_tags(self):
        """Test scrubbing multiple tags."""
        scrubber = StreamingContextScrubber()
        text = "<memory-context>1</memory-context>A<internal>2</internal>B<!--3-->C"
        result = scrubber.feed(text)
        
        assert "1" not in result
        assert "2" not in result
        assert "3" not in result
        assert "A" in result
        assert "B" in result
        assert "C" in result
    
    def test_scrubber_strip_comments(self):
        """Test stripping HTML comments."""
        scrubber = StreamingContextScrubber()
        text = "Before <!-- comment --> After"
        result = scrubber.feed(text)
        
        assert "comment" not in result
        assert "Before" in result
        assert "After" in result
