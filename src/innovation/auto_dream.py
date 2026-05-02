"""
FN:auto_dream.py
AutoDream consolidation for Torro agent framework.

Classes:
- AutoDream: Manages memory consolidation triggers and execution
- ConsolidationResult: Result of consolidation operation

Functions:
- FN:should_consolidate: Check if consolidation should run (lines 48-62)
"""

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ConsolidationResult:
    """Result of a consolidation operation.
    
    Attributes:
        success: Whether consolidation succeeded
        memories_consolidated: Number of memories consolidated
        duration_seconds: Time taken for consolidation
        error: Error message if failed
    """
    success: bool = False
    memories_consolidated: int = 0
    duration_seconds: float = 0.0
    error: Optional[str] = None


class AutoDream:
    """Manages memory consolidation triggers and execution.
    
    AutoDream implements time-gated and session-gated consolidation
    to prevent memory fragmentation and improve retrieval quality.
    
    Example:
        ```python
        auto_dream = AutoDream()
        
        # Check if consolidation should run
        if auto_dream.should_consolidate(sessions):
            result = auto_dream.run_consolidation("session-123")
        ```
    """
    
    # Consolidation thresholds
    DEFAULT_TIME_GATE_HOURS = 24
    DEFAULT_SESSION_GATE_COUNT = 5
    
    def __init__(
        self,
        time_gate_hours: int = DEFAULT_TIME_GATE_HOURS,
        session_gate_count: int = DEFAULT_SESSION_GATE_COUNT
    ):
        """Initialize AutoDream.
        
        Args:
            time_gate_hours: Hours between consolidations
            session_gate_count: Sessions before consolidation
        """
        self._time_gate_hours = time_gate_hours
        self._session_gate_count = session_gate_count
        self._last_consolidated: Optional[datetime] = None
        self._session_count = 0
        self._lock = threading.Lock()
        self._consolidation_lock_file: Optional[str] = None
        
        logger.info("FN:AutoDream.__init__ AutoDream initialized")
    
    def should_consolidate(
        self,
        last_consolidated_at: Optional[datetime] = None,
        sessions: Optional[List[Dict]] = None
    ) -> bool:
        """FN:should_consolidate Check if consolidation should run.
        
        Args:
            last_consolidated_at: Last consolidation timestamp
            sessions: List of session dicts
            
        Returns:
            True if consolidation should run
        """
        with self._lock:
            # Time gate check
            if last_consolidated_at:
                elapsed = datetime.now() - last_consolidated_at
                if elapsed < timedelta(hours=self._time_gate_hours):
                    logger.debug(
                        "FN:AutoDream.should_consolidate Time gate not met: %s hours",
                        elapsed.total_seconds() / 3600
                    )
                    return False
            
            # Session gate check
            session_count = len(sessions) if sessions else self._session_count
            if session_count < self._session_gate_count:
                logger.debug(
                    "FN:AutoDream.should_consolidate Session gate not met: %s sessions",
                    session_count
                )
                return False
            
            logger.info("FN:AutoDream.should_consolidate Consolidation triggered")
            return True
    
    def acquire_lock(self, lock_file: Optional[str] = None) -> bool:
        """FN:acquire_lock Acquire consolidation lock.
        
        Args:
            lock_file: Path to lock file
            
        Returns:
            True if lock acquired
        """
        if lock_file:
            self._consolidation_lock_file = lock_file
        
        # Simple file-based lock
        if self._consolidation_lock_file:
            try:
                with open(self._consolidation_lock_file, 'x') as f:
                    f.write(str(os.getpid()))
                logger.info("FN:AutoDream.acquire_lock Lock acquired: %s", self._consolidation_lock_file)
                return True
            except FileExistsError:
                logger.warning("FN:AutoDream.acquire_lock Lock already held: %s", self._consolidation_lock_file)
                return False
        
        # In-memory lock
        if hasattr(self, '_lock_acquired') and self._lock_acquired:
            return False
        self._lock_acquired = True
        return True
    
    def release_lock(self) -> None:
        """FN:release_lock Release consolidation lock."""
        if self._consolidation_lock_file:
            try:
                os.remove(self._consolidation_lock_file)
                logger.info("FN:AutoDream.release_lock Lock released: %s", self._consolidation_lock_file)
            except OSError:
                pass
            self._consolidation_lock_file = None
        else:
            self._lock_acquired = False
    
    def run_consolidation(self, session_id: str) -> ConsolidationResult:
        """FN:run_consolidation Run consolidation for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Consolidation result
        """
        start_time = time.time()
        logger.info("FN:AutoDream.run_consolidation Starting consolidation for %s", session_id)
        
        try:
            # Placeholder for actual consolidation logic
            # In production, this would:
            # 1. Fetch memories from the session
            # 2. Run LLM-based consolidation
            # 3. Store consolidated memories
            
            memories_consolidated = 1  # Placeholder
            duration = time.time() - start_time
            
            self._last_consolidated = datetime.now()
            self._session_count = 0
            
            result = ConsolidationResult(
                success=True,
                memories_consolidated=memories_consolidated,
                duration_seconds=duration
            )
            logger.info("FN:AutoDream.run_consolidation Consolidation complete: %s memories", memories_consolidated)
            return result
            
        except Exception as e:
            logger.exception("FN:AutoDream.run_consolidation Consolidation failed: %s", e)
            return ConsolidationResult(
                success=False,
                error=str(e),
                duration_seconds=time.time() - start_time
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """FN:get_stats Get AutoDream statistics.
        
        Returns:
            Dict with consolidation stats
        """
        return {
            "last_consolidated": self._last_consolidated.isoformat() if self._last_consolidated else None,
            "session_count": self._session_count,
            "time_gate_hours": self._time_gate_hours,
            "session_gate_count": self._session_gate_count,
        }
