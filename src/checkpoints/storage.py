"""
FN:storage.py
Checkpoint storage backend for Torro agent framework.

Classes:
- CheckpointStorage: File-based checkpoint storage

Functions:
- FN:save: Save checkpoint data (lines 42-56)
- FN:load: Load checkpoint data (lines 58-72)
- FN:delete: Delete checkpoint (lines 74-86)
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class CheckpointStorage:
    """File-based checkpoint storage.
    
    The CheckpointStorage provides persistent storage for checkpoints
    using the local filesystem.
    
    Example:
        ```python
        storage = CheckpointStorage("/tmp/checkpoints")
        
        # Save checkpoint
        storage.save("checkpoint-123", b"data")
        
        # Load checkpoint
        data = storage.load("checkpoint-123")
        
        # Delete checkpoint
        storage.delete("checkpoint-123")
        ```
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize CheckpointStorage.
        
        Args:
            storage_dir: Directory for storing checkpoints.
                        Defaults to /tmp/torro_checkpoints
        """
        self._storage_dir = Path(storage_dir) if storage_dir else Path("/tmp/torro_checkpoints")
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info("FN:CheckpointStorage.__init__ Storage initialized: %s", self._storage_dir)
    
    def save(self, checkpoint_id: str, data: bytes) -> None:
        """FN:save Save checkpoint data.
        
        Args:
            checkpoint_id: Checkpoint identifier
            data: Checkpoint data bytes
        """
        file_path = self._storage_dir / checkpoint_id
        
        # Write atomically using temp file
        temp_path = file_path.with_suffix('.tmp')
        try:
            temp_path.write_bytes(data)
            temp_path.rename(file_path)
            logger.debug("FN:CheckpointStorage.save Saved: %s (%d bytes)", checkpoint_id, len(data))
        except Exception as e:
            logger.error("FN:CheckpointStorage.save Failed to save %s: %s", checkpoint_id, e)
            # Clean up temp file on failure
            if temp_path.exists():
                temp_path.unlink()
            raise
    
    def load(self, checkpoint_id: str) -> bytes:
        """FN:load Load checkpoint data.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Checkpoint data bytes
            
        Raises:
            FileNotFoundError: If checkpoint not found
        """
        file_path = self._storage_dir / checkpoint_id
        
        if not file_path.exists():
            logger.warning("FN:CheckpointStorage.load Not found: %s", checkpoint_id)
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
        
        data = file_path.read_bytes()
        logger.debug("FN:CheckpointStorage.load Loaded: %s (%d bytes)", checkpoint_id, len(data))
        return data
    
    def delete(self, checkpoint_id: str) -> None:
        """FN:delete Delete checkpoint.
        
        Args:
            checkpoint_id: Checkpoint identifier
        """
        file_path = self._storage_dir / checkpoint_id
        
        if file_path.exists():
            file_path.unlink()
            logger.debug("FN:CheckpointStorage.delete Deleted: %s", checkpoint_id)
        else:
            logger.debug("FN:CheckpointStorage.delete Not found: %s", checkpoint_id)
    
    def exists(self, checkpoint_id: str) -> bool:
        """FN:exists Check if checkpoint exists.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            True if checkpoint exists
        """
        file_path = self._storage_dir / checkpoint_id
        return file_path.exists()
    
    def list_all(self) -> list:
        """FN:list_all List all checkpoint IDs.
        
        Returns:
            List of checkpoint IDs
        """
        if not self._storage_dir.exists():
            return []
        
        return [f.name for f in self._storage_dir.iterdir() if f.is_file()]
    
    def get_size(self, checkpoint_id: str) -> int:
        """FN:get_size Get checkpoint size.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Size in bytes
            
        Raises:
            FileNotFoundError: If checkpoint not found
        """
        file_path = self._storage_dir / checkpoint_id
        
        if not file_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
        
        return file_path.stat().st_size
    
    def clear(self) -> int:
        """FN:clear Clear all checkpoints.
        
        Returns:
            Number of checkpoints cleared
        """
        if not self._storage_dir.exists():
            return 0
        
        count = 0
        for file_path in self._storage_dir.iterdir():
            if file_path.is_file():
                file_path.unlink()
                count += 1
        
        logger.info("FN:CheckpointStorage.clear Cleared %d checkpoints", count)
        return count
