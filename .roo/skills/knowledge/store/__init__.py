"""
FN:__init__.py
Package: .roo.skills.knowledge.store
Summary: Knowledge storage, indexing, and retrieval components
Structure:
  - knowledge_store.py: Main storage and retrieval logic
Entry Points: KnowledgeStore, KnowledgeEntry, KnowledgeIndex
Flow: Parse entries -> Index for search -> Retrieve on demand
Read First: knowledge_store.py
"""

from .knowledge_store import (
    KnowledgeStore,
    KnowledgeEntry,
    KnowledgeIndex,
    search_knowledge,
    capture_knowledge_entry,
    get_knowledge_context,
    get_knowledge_store
)

__all__ = [
    "KnowledgeStore",
    "KnowledgeEntry",
    "KnowledgeIndex",
    "search_knowledge",
    "capture_knowledge_entry",
    "get_knowledge_context",
    "get_knowledge_store"
]
