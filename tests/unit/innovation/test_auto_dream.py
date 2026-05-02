"""
FN:test_auto_dream.py
Unit tests for Torro autoDream consolidation.

Tests:
- TestAutoDream: Test AutoDream class
- TestConsolidationResult: Test consolidation result dataclass
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from innovation.auto_dream import AutoDream, ConsolidationResult


class TestConsolidationResult:
    """Test ConsolidationResult dataclass."""
    
    def test_consolidation_result_success(self):
        """Test successful consolidation result."""
        result = ConsolidationResult(
            success=True,
            memories_consolidated=10,
            duration_seconds=1.5
        )
        assert result.success is True
        assert result.memories_consolidated == 10
        assert result.duration_seconds == 1.5
        assert result.error is None
    
    def test_consolidation_result_failure(self):
        """Test failed consolidation result."""
        result = ConsolidationResult(
            success=False,
            error="Test error",
            duration_seconds=0.5
        )
        assert result.success is False
        assert result.error == "Test error"
        assert result.memories_consolidated == 0


class TestAutoDream:
    """Test AutoDream class."""
    
    def test_auto_dream_init(self):
        """Test AutoDream initialization."""
        auto_dream = AutoDream()
        assert auto_dream._time_gate_hours == 24
        assert auto_dream._session_gate_count == 5
        assert auto_dream._last_consolidated is None
    
    def test_auto_dream_custom_gates(self):
        """Test AutoDream with custom gate values."""
        auto_dream = AutoDream(
            time_gate_hours=48,
            session_gate_count=10
        )
        assert auto_dream._time_gate_hours == 48
        assert auto_dream._session_gate_count == 10
    
    def test_should_consolidate_time_gate_not_met(self):
        """Test should_consolidate when time gate not met."""
        auto_dream = AutoDream(time_gate_hours=24)
        last_consolidated = datetime.now() - timedelta(hours=12)
        
        result = auto_dream.should_consolidate(last_consolidated_at=last_consolidated)
        assert result is False
    
    def test_should_consolidate_time_gate_met(self):
        """Test should_consolidate when time gate met."""
        auto_dream = AutoDream(time_gate_hours=24)
        last_consolidated = datetime.now() - timedelta(hours=25)
        
        # Provide enough sessions to meet session gate
        sessions = [{"id": str(i)} for i in range(6)]
        result = auto_dream.should_consolidate(last_consolidated_at=last_consolidated, sessions=sessions)
        assert result is True
    
    def test_should_consolidate_session_gate_not_met(self):
        """Test should_consolidate when session gate not met."""
        auto_dream = AutoDream(session_gate_count=5)
        sessions = [{"id": "1"}, {"id": "2"}]
        
        result = auto_dream.should_consolidate(sessions=sessions)
        assert result is False
    
    def test_should_consolidate_session_gate_met(self):
        """Test should_consolidate when session gate met."""
        auto_dream = AutoDream(session_gate_count=5)
        sessions = [{"id": str(i)} for i in range(6)]
        
        result = auto_dream.should_consolidate(sessions=sessions)
        assert result is True
    
    def test_acquire_lock_file_based(self, tmp_path):
        """Test acquiring file-based lock."""
        auto_dream = AutoDream()
        lock_file = tmp_path / "consolidation.lock"
        
        result = auto_dream.acquire_lock(str(lock_file))
        assert result is True
        assert lock_file.exists()
        
        # Try to acquire again (should fail)
        result2 = auto_dream.acquire_lock(str(lock_file))
        assert result2 is False
    
    def test_release_lock(self, tmp_path):
        """Test releasing lock."""
        auto_dream = AutoDream()
        lock_file = tmp_path / "consolidation.lock"
        
        auto_dream.acquire_lock(str(lock_file))
        assert lock_file.exists()
        
        auto_dream.release_lock()
        assert not lock_file.exists()
    
    def test_run_consolidation(self):
        """Test running consolidation."""
        auto_dream = AutoDream()
        result = auto_dream.run_consolidation("session-123")
        
        assert result.success is True
        assert result.memories_consolidated >= 0
        assert result.duration_seconds >= 0
    
    def test_run_consolidation_error(self):
        """Test consolidation with error."""
        auto_dream = AutoDream()
        
        # Mock to simulate error
        with patch.object(auto_dream, '_lock'):
            result = auto_dream.run_consolidation("session-123")
            assert result.success is True
    
    def test_get_stats(self):
        """Test getting AutoDream statistics."""
        auto_dream = AutoDream()
        stats = auto_dream.get_stats()
        
        assert "last_consolidated" in stats
        assert "session_count" in stats
        assert "time_gate_hours" in stats
        assert "session_gate_count" in stats
