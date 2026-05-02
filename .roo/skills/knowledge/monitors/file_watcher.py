"""
FN:file_watcher Module
Package: .roo.skills.knowledge.monitors
Summary: Event-driven file system watcher for knowledge capture triggers
Structure:
  - FileWatcher: Main class that monitors file changes
  - FileChange: Data class representing file change events
Entry Points: FileWatcher class
Flow: FileWatcher.start() -> observe changes -> emit events -> trigger knowledge suggestions
Read First: FileWatcher class
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class FileChange:
    """Represents a detected file system change."""
    FN: "FileChange"
    
    path: str
    change_type: str  # 'created', 'modified', 'deleted', 'renamed'
    timestamp: datetime = field(default_factory=datetime.now)
    content_hash: Optional[str] = None
    old_path: Optional[str] = None  # For renames
    
    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "change_type": self.change_type,
            "timestamp": self.timestamp.isoformat(),
            "content_hash": self.content_hash,
            "old_path": self.old_path
        }


@dataclass
class WatchConfig:
    """Configuration for the file watcher."""
    FN: "WatchConfig"
    
    root_path: str = "."
    exclude_patterns: List[str] = field(default_factory=lambda: [
        ".git", "node_modules", ".next", "__pycache__", "*.pyc", 
        ".DS_Store", "venv", ".venv", ".env*"
    ])
    include_extensions: List[str] = field(default_factory=lambda: [
        ".py", ".tsx", ".ts", ".js", ".jsx", ".md", ".json", ".ini", ".yaml", ".yml"
    ])
    polling_interval: float = 2.0  # seconds
    debounce_time: float = 1.0  # seconds between same-file changes


class FileWatcher:
    """
    Event-driven file system watcher for monitoring code changes.
    
    Monitors a directory tree for file changes and emits events that can
    trigger knowledge capture workflows.
    """
    FN: "FileWatcher.__init__"
    
    def __init__(self, config: Optional[WatchConfig] = None):
        """Initialize the file watcher with configuration."""
        self.config = config or WatchConfig()
        self.root_path = Path(self.config.root_path).resolve()
        
        # Internal state
        self._file_hashes: Dict[str, str] = {}
        self._last_change: Dict[str, float] = {}
        self._callbacks: List[Callable[[FileChange], None]] = []
        self._running = False
        self._change_queue: List[FileChange] = []
        
        logger.info("FN:__init__ Initialized FileWatcher for path: %s", self.root_path)
        
    def _should_watch(self, path: Path) -> bool:
        """Determine if a path should be watched based on exclude/include patterns."""
        # Check if path is excluded
        for pattern in self.config.exclude_patterns:
            if pattern in str(path):
                return False
        
        # Check if extension is included (if specified)
        if self.config.include_extensions:
            if path.suffix not in self.config.include_extensions:
                return False
        
        return True
    
    def _compute_hash(self, path: Path) -> str:
        """Compute MD5 hash of file content."""
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except (IOError, OSError) as e:
            logger.error("FN:_compute_hash Failed to hash file %s: %s", path, e)
            return ""
    
    def _scan_directory(self) -> Dict[str, str]:
        """Scan directory and return dict of path -> content_hash."""
        hashes = {}
        for root, dirs, files in os.walk(self.root_path):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if not any(p in d for p in self.config.exclude_patterns)]
            
            for file in files:
                path = Path(root) / file
                if self._should_watch(path):
                    file_hash = self._compute_hash(path)
                    rel_path = str(path.relative_to(self.root_path))
                    hashes[rel_path] = file_hash
        
        return hashes
    
    def _detect_changes(self, new_hashes: Dict[str, str]) -> List[FileChange]:
        """Compare hashes and detect file changes."""
        changes = []
        
        # Check for new and modified files
        for path, new_hash in new_hashes.items():
            old_hash = self._file_hashes.get(path)
            
            if old_hash is None:
                # New file
                changes.append(FileChange(
                    path=path,
                    change_type="created",
                    content_hash=new_hash
                ))
            elif old_hash != new_hash:
                # Modified file (debounce check)
                if time.time() - self._last_change.get(path, 0) > self.config.debounce_time:
                    changes.append(FileChange(
                        path=path,
                        change_type="modified",
                        content_hash=new_hash
                    ))
                    self._last_change[path] = time.time()
        
        # Check for deleted files
        for path in self._file_hashes:
            if path not in new_hashes:
                changes.append(FileChange(
                    path=path,
                    change_type="deleted"
                ))
        
        return changes
    
    def register_callback(self, callback: Callable[[FileChange], None]) -> None:
        """Register a callback function to be called on file changes."""
        self._callbacks.append(callback)
        logger.info("FN:register_callback Registered callback for file changes")
    
    def _emit_change(self, change: FileChange) -> None:
        """Emit change event to all registered callbacks."""
        for callback in self._callbacks:
            try:
                callback(change)
            except Exception as e:
                logger.error("FN:_emit_change Callback error: %s", e)
    
    def scan_now(self) -> List[FileChange]:
        """Perform an immediate scan and return detected changes."""
        logger.info("FN:scan_now Performing immediate file system scan")
        new_hashes = self._scan_directory()
        changes = self._detect_changes(new_hashes)
        self._file_hashes = new_hashes
        return changes
    
    def start(self, blocking: bool = True) -> None:
        """
        Start watching for file changes.
        
        Args:
            blocking: If True, run in current thread. If False, run in background.
        """
        self._running = True
        logger.info("FN:start Starting file watcher in %s mode", "blocking" if blocking else "background")
        
        # Initial scan
        self._file_hashes = self._scan_directory()
        logger.info("FN:start Indexed %d files", len(self._file_hashes))
        
        if blocking:
            self._run_blocking()
        else:
            import threading
            thread = threading.Thread(target=self._run_blocking, daemon=True)
            thread.start()
    
    def _run_blocking(self) -> None:
        """Run the watcher loop in current thread."""
        logger.info("FN:_run_blocking File watcher loop started")
        
        while self._running:
            try:
                new_hashes = self._scan_directory()
                changes = self._detect_changes(new_hashes)
                
                for change in changes:
                    self._emit_change(change)
                
                self._file_hashes = new_hashes
                time.sleep(self.config.polling_interval)
                
            except KeyboardInterrupt:
                logger.info("FN:_run_blocking Watcher interrupted")
                self.stop()
            except Exception as e:
                logger.error("FN:_run_blocking Watcher error: %s", e)
                time.sleep(self.config.polling_interval)
    
    def stop(self) -> None:
        """Stop the file watcher."""
        self._running = False
        logger.info("FN:stop File watcher stopped")


class KnowledgeMonitor:
    """
    High-level monitor that orchestrates file watching and knowledge capture.
    
    This class integrates the FileWatcher with the knowledge suggestion engine
    to provide a complete event-driven knowledge capture system.
    """
    FN: "KnowledgeMonitor"
    
    def __init__(self, root_path: str = ".", data_dir: str = ".roo/skills/knowledge"):
        """Initialize the knowledge monitor."""
        self.root_path = Path(root_path)
        self.data_dir = Path(data_dir)
        self.knowledge_file = self.data_dir / "data" / "knowledge.md"
        self.index_file = self.data_dir / "data" / "knowledge_index.json"
        
        self.config = WatchConfig(root_path=str(self.root_path))
        self.watcher = FileWatcher(self.config)
        self.suggestion_engine: Optional["KnowledgeSuggestionEngine"] = None
        
        logger.info("FN:__init__ KnowledgeMonitor initialized")
    
    def setup(self) -> None:
        """Set up the monitor with default components."""
        from .analyzers import KnowledgeSuggestionEngine
        
        self.suggestion_engine = KnowledgeSuggestionEngine(
            knowledge_file=str(self.knowledge_file)
        )
        
        # Register callback for knowledge suggestions
        self.watcher.register_callback(self._on_file_change)
        logger.info("FN:setup KnowledgeMonitor components configured")
    
    def _on_file_change(self, change: FileChange) -> None:
        """Handle file change events by triggering knowledge analysis."""
        logger.info("FN:_on_file_change Detected %s: %s", change.change_type, change.path)
        
        if self.suggestion_engine:
            suggestions = self.suggestion_engine.analyze_change(change)
            
            for suggestion in suggestions:
                logger.info("FN:_on_file_change Suggestion: %s", suggestion.title)
                # TODO: Present suggestion to user for approval
                # For now, log the suggestion
                self._log_suggestion(suggestion)
    
    def _log_suggestion(self, suggestion) -> None:
        """Log a knowledge suggestion."""
        log_path = self.data_dir / "logs"
        log_path.mkdir(parents=True, exist_ok=True)
        
        log_file = log_path / f"suggestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w') as f:
            json.dump(suggestion.to_dict(), f, indent=2)
        
        logger.info("FN:_log_suggestion Suggestion logged to %s", log_file)
    
    def start(self, blocking: bool = True) -> None:
        """Start the knowledge monitor."""
        self.setup()
        self.watcher.start(blocking=blocking)


# Convenience function for quick monitoring
def monitor_knowledge(root_path: str = ".", callback: Optional[Callable[[FileChange], None]] = None):
    """
    Quick-start function for monitoring knowledge changes.
    
    Args:
        root_path: Root directory to monitor
        callback: Optional callback for change events
    """
    monitor = KnowledgeMonitor(root_path)
    monitor.setup()
    
    if callback:
        monitor.watcher.register_callback(callback)
    
    logger.info("FN:monitor_knowledge Starting knowledge monitor for: %s", root_path)
    monitor.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    def handle_change(change: FileChange):
        print(f"Detected change: {change.change_type} - {change.path}")
    
    monitor_knowledge(root_path=".", callback=handle_change)
