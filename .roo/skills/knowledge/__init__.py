"""
FN:__init__.py
Package: .roo.skills.knowledge
Summary: Dynamic Knowledge Acquisition Skill - Automatic knowledge capture and reference system
Structure:
  - monitors/file_watcher.py: Event-driven file system monitoring
  - analyzers/knowledge_suggester.py: Pattern detection and suggestion generation
  - store/knowledge_store.py: Knowledge ingestion, storage, and retrieval
Entry Points: KnowledgeMonitor, KnowledgeSuggestionEngine, KnowledgeStore
Flow: Monitor changes -> Analyze patterns -> Suggest entries -> Store for reference
Read First: README.md, then SKILL.md
"""

from .monitors.file_watcher import (
    FileWatcher,
    FileChange,
    WatchConfig,
    KnowledgeMonitor
)
from .analyzers.knowledge_suggester import (
    KnowledgeSuggestionEngine,
    Suggestion,
    PatternDetector,
    PatternMatch
)
from .store.knowledge_store import (
    KnowledgeStore,
    KnowledgeEntry,
    KnowledgeIndex,
    search_knowledge,
    capture_knowledge_entry,
    get_knowledge_context,
    get_knowledge_store
)

__all__ = [
    # Monitors
    "FileWatcher",
    "FileChange",
    "WatchConfig",
    "KnowledgeMonitor",
    # Analyzers
    "KnowledgeSuggestionEngine",
    "Suggestion",
    "PatternDetector",
    "PatternMatch",
    # Store
    "KnowledgeStore",
    "KnowledgeEntry",
    "KnowledgeIndex",
    # Convenience functions
    "search_knowledge",
    "capture_knowledge_entry",
    "get_knowledge_context",
    "get_knowledge_store"
]
