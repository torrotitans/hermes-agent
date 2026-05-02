"""
FN:__init__.py
Package: .roo.skills.knowledge.monitors
Summary: File monitoring components for knowledge capture
Structure:
  - file_watcher.py: File system watcher and event handling
Entry Points: FileWatcher, KnowledgeMonitor
Flow: Initialize watcher -> Monitor changes -> Emit events
Read First: file_watcher.py
"""

from .file_watcher import (
    FileWatcher,
    FileChange,
    WatchConfig,
    KnowledgeMonitor,
    monitor_knowledge
)

__all__ = [
    "FileWatcher",
    "FileChange",
    "WatchConfig",
    "KnowledgeMonitor",
    "monitor_knowledge"
]
