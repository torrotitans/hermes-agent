"""
FN:test_manager.py
Unit tests for Torro checkpoint manager.

Tests:
- TestCheckpointId: Test CheckpointId dataclass
- TestCheckpointInfo: Test CheckpointInfo dataclass
- TestCheckpointManager: Test CheckpointManager class
"""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from checkpoints.manager import CheckpointManager, CheckpointId, CheckpointInfo
from checkpoints.storage import CheckpointStorage


class TestCheckpointId:
    """Test CheckpointId dataclass."""
    
    def test_checkpoint_id_creation(self):
        """Test creating a CheckpointId."""
        checkpoint_id = CheckpointId(id="123")
        assert checkpoint_id.id == "123"
        assert isinstance(checkpoint_id.created_at, datetime)
    
    def test_checkpoint_id_custom_created_at(self):
        """Test creating a CheckpointId with custom created_at."""
        created_at = datetime.now() - timedelta(days=1)
        checkpoint_id = CheckpointId(id="123", created_at=created_at)
        assert checkpoint_id.id == "123"
        assert checkpoint_id.created_at == created_at


class TestCheckpointInfo:
    """Test CheckpointInfo dataclass."""
    
    def test_checkpoint_info_creation(self):
        """Test creating CheckpointInfo."""
        info = CheckpointInfo(
            id="123",
            label="test",
            created_at=datetime.now()
        )
        assert info.id == "123"
        assert info.label == "test"
        assert info.size_bytes == 0
    
    def test_checkpoint_info_with_size(self):
        """Test creating CheckpointInfo with size."""
        info = CheckpointInfo(
            id="123",
            label="test",
            created_at=datetime.now(),
            size_bytes=1024
        )
        assert info.size_bytes == 1024


class TestCheckpointManager:
    """Test CheckpointManager class."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create a CheckpointManager with temp storage."""
        storage = CheckpointStorage(str(tmp_path / "checkpoints"))
        return CheckpointManager(storage=storage)
    
    def test_checkpoint_manager_init(self, manager):
        """Test CheckpointManager initialization."""
        assert manager._checkpoints == {}
        assert manager._max_age_hours == 24
        assert manager._max_checkpoints == 100
    
    def test_create_checkpoint(self, manager):
        """Test creating a checkpoint."""
        state = {"key": "value"}
        checkpoint_id = manager.create_checkpoint(state, "test_label")
        
        assert checkpoint_id.id is not None
        assert isinstance(checkpoint_id.created_at, datetime)
        assert "test_label" in manager._checkpoints[checkpoint_id.id].label
    
    def test_restore_checkpoint(self, manager):
        """Test restoring a checkpoint."""
        state = {"key": "value", "count": 42}
        checkpoint_id = manager.create_checkpoint(state, "test_label")
        
        restored = manager.restore_checkpoint(checkpoint_id)
        assert restored == state
    
    def test_restore_nonexistent_checkpoint(self, manager):
        """Test restoring nonexistent checkpoint."""
        checkpoint_id = CheckpointId(id="nonexistent")
        
        with pytest.raises(FileNotFoundError):
            manager.restore_checkpoint(checkpoint_id)
    
    def test_list_checkpoints_empty(self, manager):
        """Test listing checkpoints when empty."""
        checkpoints = manager.list_checkpoints()
        assert checkpoints == []
    
    def test_list_checkpoints(self, manager):
        """Test listing checkpoints."""
        # Create multiple checkpoints
        for i in range(3):
            manager.create_checkpoint({"index": i}, f"label_{i}")
        
        checkpoints = manager.list_checkpoints()
        assert len(checkpoints) == 3
        
        # Check sorted by creation time (newest first)
        for i in range(len(checkpoints) - 1):
            assert checkpoints[i].created_at >= checkpoints[i + 1].created_at
    
    def test_prune_checkpoints_by_age(self, manager):
        """Test pruning checkpoints by age."""
        # Create a checkpoint
        checkpoint_id = manager.create_checkpoint({"key": "value"}, "test")
        
        # Modify creation time to be old
        old_time = datetime.now() - timedelta(hours=25)
        manager._checkpoints[checkpoint_id.id].created_at = old_time
        
        # Prune
        pruned = manager.prune_checkpoints(max_age_hours=24)
        assert pruned == 1
        assert checkpoint_id.id not in manager._checkpoints
    
    def test_prune_checkpoints_by_count(self, manager):
        """Test pruning checkpoints by count."""
        # Set max checkpoints to 2
        manager._max_checkpoints = 2
        
        # Create 4 checkpoints
        for i in range(4):
            manager.create_checkpoint({"index": i}, f"label_{i}")
        
        # Prune
        pruned = manager.prune_checkpoints(max_age_hours=9999)
        assert pruned == 2
        assert len(manager._checkpoints) == 2
    
    def test_get_stats(self, manager):
        """Test getting manager statistics."""
        # Create checkpoints
        manager.create_checkpoint({"key": "value"}, "test")
        
        stats = manager.get_stats()
        assert "total_checkpoints" in stats
        assert "total_size_bytes" in stats
        assert stats["total_checkpoints"] == 1
    
    def test_prune_checkpoints_handles_errors(self, manager):
        """Test pruning handles storage errors."""
        # Create a checkpoint
        checkpoint_id = manager.create_checkpoint({"key": "value"}, "test")
        
        # Modify creation time to be old
        old_time = datetime.now() - timedelta(hours=25)
        manager._checkpoints[checkpoint_id.id].created_at = old_time
        
        # Mock storage delete to raise error
        with patch.object(manager._storage, 'delete', side_effect=Exception("Test error")):
            pruned = manager.prune_checkpoints(max_age_hours=24)
            assert pruned == 0
