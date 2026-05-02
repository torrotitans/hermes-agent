"""
FN:__init__.py
Package: .roo.skills.knowledge.analyzers
Summary: Pattern analysis and knowledge suggestion components
Structure:
  - knowledge_suggester.py: Pattern detection and suggestion generation
Entry Points: KnowledgeSuggestionEngine, PatternDetector, Suggestion
Flow: Analyze changes -> Detect patterns -> Generate suggestions
Read First: knowledge_suggester.py
"""

from .knowledge_suggester import (
    KnowledgeSuggestionEngine,
    Suggestion,
    PatternDetector,
    PatternMatch
)

__all__ = [
    "KnowledgeSuggestionEngine",
    "Suggestion",
    "PatternDetector",
    "PatternMatch"
]
