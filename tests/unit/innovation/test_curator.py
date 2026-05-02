"""
FN:test_curator.py
Unit tests for Torro Curator memory maintenance.

Tests:
- TestMaintenanceResult: Test maintenance result dataclass
- TestCurator: Test Curator class
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from innovation.curator import Curator, MaintenanceResult


class TestMaintenanceResult:
    """Test MaintenanceResult dataclass."""
    
    def test_maintenance_result_success(self):
        """Test successful maintenance result."""
        result = MaintenanceResult(
            success=True,
            memories_pruned=10,
            memories_merged=5,
            duration_seconds=2.0
        )
        assert result.success is True
        assert result.memories_pruned == 10
        assert result.memories_merged == 5
        assert result.duration_seconds == 2.0
        assert result.error is None
    
    def test_maintenance_result_failure(self):
        """Test failed maintenance result."""
        result = MaintenanceResult(
            success=False,
            error="Test error",
            duration_seconds=0.5
        )
        assert result.success is False
        assert result.error == "Test error"


class TestCurator:
    """Test Curator class."""
    
    def test_curator_init(self):
        """Test Curator initialization."""
        curator = Curator()
        assert curator._max_age_days == 30
        assert curator._similarity_threshold == 0.95
        assert curator._last_maintenance is None
    
    def test_curator_custom_thresholds(self):
        """Test Curator with custom threshold values."""
        curator = Curator(
            max_age_days=60,
            similarity_threshold=0.99
        )
        assert curator._max_age_days == 60
        assert curator._similarity_threshold == 0.99
    
    def test_curator_with_memory_manager(self):
        """Test Curator with memory manager."""
        memory_manager = Mock()
        curator = Curator(memory_manager=memory_manager)
        assert curator._memory_manager is memory_manager
    
    def test_maintain_memories(self):
        """Test running memory maintenance."""
        curator = Curator()
        result = curator.maintain_memories()
        
        assert result.success is True
        assert result.duration_seconds > 0
        assert curator._last_maintenance is not None
    
    def test_maintain_memories_error(self):
        """Test maintenance with error."""
        curator = Curator()
        
        # Mock to simulate error
        with patch.object(curator, 'prune_stale_memories', side_effect=Exception("Test error")):
            result = curator.maintain_memories()
            assert result.success is False
            assert result.error == "Test error"
    
    def test_prune_stale_memories(self):
        """Test pruning stale memories."""
        curator = Curator()
        result = curator.prune_stale_memories()
        
        assert isinstance(result, int)
        assert result >= 0
    
    def test_prune_stale_memories_custom_max_age(self):
        """Test pruning with custom max age."""
        curator = Curator()
        result = curator.prune_stale_memories(max_age_days=60)
        
        assert isinstance(result, int)
    
    def test_merge_duplicate_memories(self):
        """Test merging duplicate memories."""
        curator = Curator()
        result = curator.merge_duplicate_memories()
        
        assert isinstance(result, int)
        assert result >= 0
    
    def test_get_stats(self):
        """Test getting Curator statistics."""
        curator = Curator()
        stats = curator.get_stats()
        
        assert "last_maintenance" in stats
        assert "max_age_days" in stats
        assert "similarity_threshold" in stats
        
        # last_maintenance should be None before maintenance
        assert stats["last_maintenance"] is None
        
        # Run maintenance and check again
        curator.maintain_memories()
        stats = curator.get_stats()
        assert stats["last_maintenance"] is not None
