"""
FN:test_storage.py
Unit tests for Torro checkpoint storage.

Tests:
- TestCheckpointStorage: Test CheckpointStorage class
"""

import pytest
from pathlib import Path

from checkpoints.storage import CheckpointStorage


class TestCheckpointStorage:
    """Test CheckpointStorage class."""
    
    @pytest.fixture
    def storage(self, tmp_path):
        """Create a CheckpointStorage with temp directory."""
        return CheckpointStorage(str(tmp_path / "checkpoints"))
    
    def test_storage_init(self, tmp_path):
        """Test CheckpointStorage initialization."""
        storage = CheckpointStorage(str(tmp_path / "checkpoints"))
        assert storage._storage_dir.exists()
        assert storage._storage_dir.is_dir()
    
    def test_storage_init_default_dir(self):
        """Test CheckpointStorage with default directory."""
        storage = CheckpointStorage()
        assert storage._storage_dir == Path("/tmp/torro_checkpoints")
    
    def test_save(self, storage):
        """Test saving checkpoint data."""
        data = b"test data"
        storage.save("checkpoint-123", data)
        
        file_path = storage._storage_dir / "checkpoint-123"
        assert file_path.exists()
        assert file_path.read_bytes() == data
    
    def test_load(self, storage):
        """Test loading checkpoint data."""
        data = b"test data"
        storage.save("checkpoint-123", data)
        
        loaded = storage.load("checkpoint-123")
        assert loaded == data
    
    def test_load_nonexistent(self, storage):
        """Test loading nonexistent checkpoint."""
        with pytest.raises(FileNotFoundError):
            storage.load("nonexistent")
    
    def test_delete(self, storage):
        """Test deleting checkpoint."""
        data = b"test data"
        storage.save("checkpoint-123", data)
        
        storage.delete("checkpoint-123")
        assert not (storage._storage_dir / "checkpoint-123").exists()
    
    def test_delete_nonexistent(self, storage):
        """Test deleting nonexistent checkpoint."""
        # Should not raise
        storage.delete("nonexistent")
    
    def test_exists(self, storage):
        """Test checking if checkpoint exists."""
        assert storage.exists("nonexistent") is False
        
        storage.save("checkpoint-123", b"data")
        assert storage.exists("checkpoint-123") is True
    
    def test_list_all_empty(self, storage):
        """Test listing all checkpoints when empty."""
        checkpoints = storage.list_all()
        assert checkpoints == []
    
    def test_list_all(self, storage):
        """Test listing all checkpoints."""
        storage.save("checkpoint-1", b"data1")
        storage.save("checkpoint-2", b"data2")
        
        checkpoints = storage.list_all()
        assert len(checkpoints) == 2
        assert "checkpoint-1" in checkpoints
        assert "checkpoint-2" in checkpoints
    
    def test_get_size(self, storage):
        """Test getting checkpoint size."""
        data = b"test data"
        storage.save("checkpoint-123", data)
        
        size = storage.get_size("checkpoint-123")
        assert size == len(data)
    
    def test_get_size_nonexistent(self, storage):
        """Test getting size of nonexistent checkpoint."""
        with pytest.raises(FileNotFoundError):
            storage.get_size("nonexistent")
    
    def test_clear(self, storage):
        """Test clearing all checkpoints."""
        storage.save("checkpoint-1", b"data1")
        storage.save("checkpoint-2", b"data2")
        
        count = storage.clear()
        assert count == 2
        assert storage.list_all() == []
    
    def test_clear_empty(self, storage):
        """Test clearing empty storage."""
        count = storage.clear()
        assert count == 0
    
    def test_save_atomic(self, storage):
        """Test atomic save operation."""
        data = b"test data"
        
        # Save should create temp file then rename
        storage.save("checkpoint-123", data)
        
        # Check no temp file remains
        temp_file = storage._storage_dir / "checkpoint-123.tmp"
        assert not temp_file.exists()
        
        # Check final file exists
        final_file = storage._storage_dir / "checkpoint-123"
        assert final_file.exists()
        assert final_file.read_bytes() == data
    
    def test_save_handles_errors(self, storage):
        """Test save handles write errors."""
        # Create a directory with same name as checkpoint file
        dir_path = storage._storage_dir / "checkpoint-123"
        dir_path.mkdir()
        
        with pytest.raises(Exception):
            storage.save("checkpoint-123", b"data")
        
        # Clean up
        dir_path.rmdir()
