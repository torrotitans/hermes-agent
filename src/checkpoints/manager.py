"""
FN:manager.py
Checkpoint manager for Torro agent framework.

Classes:
- CheckpointManager: Manages checkpoint creation and restoration
- CheckpointId: Checkpoint identifier type
- CheckpointInfo: Checkpoint information data class

Functions:
- FN:create_checkpoint: Create a checkpoint (lines 58-74)
- FN:restore_checkpoint: Restore a checkpoint (lines 76-92)
- FN:list_checkpoints: List all checkpoints (lines 94-108)
- FN:prune_checkpoints: Prune old checkpoints (lines 110-126)
"""

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .storage import CheckpointStorage

logger = logging.getLogger(__name__)


@dataclass
class CheckpointId:
    """Checkpoint identifier.
    
    Attributes:
        id: Unique checkpoint identifier
        created_at: Creation timestamp
    """
    id: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CheckpointInfo:
    """Checkpoint information data class.
    
    Attributes:
        id: Checkpoint identifier
        label: Checkpoint label
        created_at: Creation timestamp
        size_bytes: Size in bytes
    """
    id: str
    label: str
    created_at: datetime
    size_bytes: int = 0


class CheckpointManager:
    """Manages checkpoint creation and restoration.
    
    The CheckpointManager provides a high-level interface for creating,
    restoring, and managing checkpoints with automatic pruning.
    
    Example:
        ```python
        manager = CheckpointManager()
        
        # Create a checkpoint
        state = {"key": "value"}
        checkpoint_id = manager.create_checkpoint(state, "my_checkpoint")
        
        # Restore checkpoint
        restored_state = manager.restore_checkpoint(checkpoint_id)
        
        # List checkpoints
        checkpoints = manager.list_checkpoints()
        
        # Prune old checkpoints
        manager.prune_checkpoints(max_age_hours=24)
        ```
    """
    
    # Default checkpoint settings
    DEFAULT_MAX_AGE_HOURS = 24
    DEFAULT_MAX_CHECKPOINTS = 100
    
    def __init__(
        self,
        storage: Optional[CheckpointStorage] = None,
        max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
        max_checkpoints: int = DEFAULT_MAX_CHECKPOINTS
    ):
        """Initialize CheckpointManager.
        
        Args:
            storage: Checkpoint storage backend
            max_age_hours: Maximum age of checkpoints before pruning
            max_checkpoints: Maximum number of checkpoints to keep
        """
        self._storage = storage or CheckpointStorage()
        self._max_age_hours = max_age_hours
        self._max_checkpoints = max_checkpoints
        self._checkpoints: Dict[str, CheckpointInfo] = {}
        
        logger.info("FN:CheckpointManager.__init__ Manager initialized")
    
    def create_checkpoint(
        self,
        state: Dict[str, Any],
        label: str
    ) -> CheckpointId:
        """FN:create_checkpoint Create a checkpoint.
        
        Args:
            state: State data to checkpoint
            label: Checkpoint label
            
        Returns:
            CheckpointId of created checkpoint
        """
        checkpoint_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        # Serialize state
        import json
        data = json.dumps(state).encode('utf-8')
        
        # Save to storage
        self._storage.save(checkpoint_id, data)
        
        # Track checkpoint info
        info = CheckpointInfo(
            id=checkpoint_id,
            label=label,
            created_at=created_at,
            size_bytes=len(data)
        )
        self._checkpoints[checkpoint_id] = info
        
        logger.info("FN:CheckpointManager.create_checkpoint Created: %s (%s)", checkpoint_id, label)
        return CheckpointId(id=checkpoint_id, created_at=created_at)
    
    def restore_checkpoint(self, checkpoint_id: CheckpointId) -> Dict[str, Any]:
        """FN:restore_checkpoint Restore a checkpoint.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Restored state data
            
        Raises:
            KeyError: If checkpoint not found
        """
        # Load from storage
        data = self._storage.load(checkpoint_id.id)
        
        # Deserialize state
        import json
        state = json.loads(data.decode('utf-8'))
        
        logger.info("FN:CheckpointManager.restore_checkpoint Restored: %s", checkpoint_id.id)
        return state
    
    def list_checkpoints(self) -> List[CheckpointInfo]:
        """FN:list_checkpoints List all checkpoints.
        
        Returns:
            List of checkpoint info sorted by creation time
        """
        checkpoints = list(self._checkpoints.values())
        checkpoints.sort(key=lambda c: c.created_at, reverse=True)
        return checkpoints
    
    def prune_checkpoints(self, max_age_hours: Optional[int] = None) -> int:
        """FN:prune_checkpoints Prune old checkpoints.
        
        Args:
            max_age_hours: Maximum age in hours (default from config)
            
        Returns:
            Number of checkpoints pruned
        """
        if max_age_hours is None:
            max_age_hours = self._max_age_hours
        
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        pruned = 0
        
        # Find checkpoints to prune
        to_prune = [
            info for info in self._checkpoints.values()
            if info.created_at < cutoff
        ]
        
        # Delete old checkpoints
        for info in to_prune:
            try:
                self._storage.delete(info.id)
                del self._checkpoints[info.id]
                pruned += 1
                logger.info("FN:CheckpointManager.prune_checkpoints Pruned: %s", info.id)
            except Exception as e:
                logger.warning("FN:CheckpointManager.prune_checkpoints Failed to prune %s: %s", info.id, e)
        
        # Enforce max checkpoints limit
        if len(self._checkpoints) > self._max_checkpoints:
            # Sort by creation time (oldest first)
            sorted_checkpoints = sorted(
                self._checkpoints.values(),
                key=lambda c: c.created_at
            )
            
            # Delete oldest checkpoints
            excess = len(self._checkpoints) - self._max_checkpoints
            for info in sorted_checkpoints[:excess]:
                try:
                    self._storage.delete(info.id)
                    del self._checkpoints[info.id]
                    pruned += 1
                except Exception as e:
                    logger.warning("FN:CheckpointManager.prune_checkpoints Failed to prune %s: %s", info.id, e)
        
        logger.info("FN:CheckpointManager.prune_checkpoints Pruned %d checkpoints", pruned)
        return pruned
    
    def get_stats(self) -> Dict[str, Any]:
        """FN:get_stats Get checkpoint manager statistics.
        
        Returns:
            Dict with manager stats
        """
        total_size = sum(info.size_bytes for info in self._checkpoints.values())
        return {
            "total_checkpoints": len(self._checkpoints),
            "total_size_bytes": total_size,
            "max_age_hours": self._max_age_hours,
            "max_checkpoints": self._max_checkpoints,
        }
