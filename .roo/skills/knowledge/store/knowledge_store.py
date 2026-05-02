"""
FN:knowledge_store Module
Package: .roo.skills.knowledge.store
Summary: Knowledge ingestion, storage, and retrieval functions for AI reference
Structure:
  - KnowledgeStore: Main class for knowledge management
  - KnowledgeEntry: Data class for structured entries
  - KnowledgeIndex: Searchable index for fast lookups
Entry Points: KnowledgeStore class
Flow: capture_entry() -> parse_and_index() -> search() -> return results
Read First: KnowledgeStore class
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """Represents a structured knowledge entry."""
    FN: "KnowledgeEntry"
    
    title: str
    entry_type: str
    category: str
    date: str
    context: str
    problem: str
    solution: str
    code_reference: str
    tags: List[str]
    validation: str = "Pending verification"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'KnowledgeEntry':
        return cls(
            title=data.get('title', ''),
            entry_type=data.get('type', 'pattern'),
            category=data.get('category', 'general'),
            date=data.get('date', datetime.now().strftime('%Y-%m-%d')),
            context=data.get('context', ''),
            problem=data.get('problem', ''),
            solution=data.get('solution', ''),
            code_reference=data.get('code_reference', ''),
            tags=data.get('tags', []),
            validation=data.get('validation', 'Pending verification')
        )
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "type": self.entry_type,
            "category": self.category,
            "date": self.date,
            "context": self.context,
            "problem": self.problem,
            "solution": self.solution,
            "code_reference": self.code_reference,
            "tags": self.tags,
            "validation": self.validation
        }


class KnowledgeIndex:
    """
    Maintains a searchable index of knowledge entries.
    """
    FN: "KnowledgeIndex"
    
    def __init__(self):
        """Initialize the knowledge index."""
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.by_category: Dict[str, List[str]] = {}
        self.by_type: Dict[str, List[str]] = {}
        self.by_tag: Dict[str, List[str]] = {}
        self._index_file: Optional[Path] = None
        
        logger.info("FN:__init__ KnowledgeIndex initialized")
    
    def add_entry(self, entry_id: str, knowledge_entry: KnowledgeEntry) -> None:
        """Add an entry to the index."""
        self.entries[entry_id] = knowledge_entry
        
        # Index by category
        if knowledge_entry.category not in self.by_category:
            self.by_category[knowledge_entry.category] = []
        self.by_category[knowledge_entry.category].append(entry_id)
        
        # Index by type
        if knowledge_entry.entry_type not in self.by_type:
            self.by_type[knowledge_entry.entry_type] = []
        self.by_type[knowledge_entry.entry_type].append(entry_id)
        
        # Index by tags
        for tag in knowledge_entry.tags:
            tag_normalized = tag.lower()
            if tag_normalized not in self.by_tag:
                self.by_tag[tag_normalized] = []
            self.by_tag[tag_normalized].append(entry_id)
        
        logger.info("FN:add_entry Indexed entry: %s", entry_id)
    
    def remove_entry(self, entry_id: str) -> None:
        """Remove an entry from the index."""
        if entry_id not in self.entries:
            return
        
        entry = self.entries[entry_id]
        
        # Remove from category index
        if entry.category in self.by_category:
            self.by_category[entry.category].remove(entry_id)
        
        # Remove from type index
        if entry.entry_type in self.by_type:
            self.by_type[entry.entry_type].remove(entry_id)
        
        # Remove from tag indexes
        for tag in entry.tags:
            tag_normalized = tag.lower()
            if tag_normalized in self.by_tag:
                self.by_tag[tag_normalized].remove(entry_id)
        
        del self.entries[entry_id]
        logger.info("FN:remove_entry Removed entry: %s", entry_id)
    
    def search_by_query(self, query: str, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Search entries by keyword query.
        
        Args:
            query: Search keywords
            limit: Maximum results to return
            
        Returns:
            List of matching knowledge entries
        """
        query_lower = query.lower()
        results = []
        scores = {}
        
        for entry_id, entry in self.entries.items():
            score = 0
            
            # Check title
            if query_lower in entry.title.lower():
                score += 5
            
            # Check problem and solution
            if query_lower in entry.problem.lower():
                score += 3
            if query_lower in entry.solution.lower():
                score += 3
            
            # Check context
            if query_lower in entry.context.lower():
                score += 2
            
            # Check tags
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 4
            
            # Check category
            if query_lower in entry.category.lower():
                score += 2
            
            if score > 0:
                scores[entry_id] = score
                results.append((score, entry))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [entry for score, entry in results[:limit]]
    
    def search_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Get all entries in a category."""
        entry_ids = self.by_category.get(category, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        """Get all entries with a specific tag."""
        tag_normalized = tag.lower()
        entry_ids = self.by_tag.get(tag_normalized, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def search_by_type(self, entry_type: str) -> List[KnowledgeEntry]:
        """Get all entries of a specific type."""
        entry_ids = self.by_type.get(entry_type, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def get_related(self, entry_id: str, limit: int = 5) -> List[KnowledgeEntry]:
        """
        Get related entries based on shared tags and categories.
        
        Args:
            entry_id: Source entry ID
            limit: Maximum related entries to return
            
        Returns:
            List of related knowledge entries
        """
        if entry_id not in self.entries:
            return []
        
        source = self.entries[entry_id]
        related_scores = {}
        
        for other_id, other_entry in self.entries.items():
            if other_id == entry_id:
                continue
            
            score = 0
            
            # Same category bonus
            if other_entry.category == source.category:
                score += 3
            
            # Shared tags
            source_tags = set(t.lower() for t in source.tags)
            other_tags = set(t.lower() for t in other_entry.tags)
            shared_tags = source_tags & other_tags
            score += len(shared_tags) * 2
            
            if score > 0:
                related_scores[other_id] = score
        
        # Sort by relevance
        sorted_related = sorted(related_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [self.entries[eid] for eid, score in sorted_related[:limit]]
    
    def save(self, index_path: str) -> None:
        """Save index to JSON file."""
        data = {
            "entries": {eid: entry.to_dict() for eid, entry in self.entries.items()},
            "by_category": self.by_category,
            "by_type": self.by_type,
            "by_tag": self.by_tag
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info("FN:save Index saved to %s", index_path)
    
    def load(self, index_path: str) -> None:
        """Load index from JSON file."""
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Rebuild entries
        for entry_id, entry_data in data.get("entries", {}).items():
            self.entries[entry_id] = KnowledgeEntry.from_dict(entry_data)
        
        # Rebuild indexes
        self.by_category = data.get("by_category", {})
        self.by_type = data.get("by_type", {})
        self.by_tag = data.get("by_tag", {})
        
        logger.info("FN:load Index loaded from %s with %d entries", index_path, len(self.entries))


class KnowledgeStore:
    """
    Main class for knowledge management.
    
    Provides functions for capturing, storing, searching, and retrieving
    knowledge entries for AI reference.
    """
    FN: "KnowledgeStore"
    
    def __init__(self, knowledge_file: str, index_file: Optional[str] = None):
        """
        Initialize the knowledge store.
        
        Args:
            knowledge_file: Path to the knowledge.md file
            index_file: Optional path to the index JSON file
        """
        self.knowledge_file = Path(knowledge_file)
        self.index_file = Path(index_file) if index_file else self.knowledge_file.parent / "knowledge_index.json"
        
        self.index = KnowledgeIndex()
        self._parse_knowledge_file()
        
        logger.info("FN:__init__ KnowledgeStore initialized with %d entries", len(self.index.entries))
    
    def _parse_knowledge_file(self) -> None:
        """Parse the knowledge.md file and build the index."""
        if not self.knowledge_file.exists():
            logger.warning("FN:_parse_knowledge_file Knowledge file not found: %s", self.knowledge_file)
            return
        
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse markdown entries
            entries = self._parse_markdown_entries(content)
            
            for entry_id, entry in entries.items():
                self.index.add_entry(entry_id, entry)
            
            # Try to load existing index
            if self.index_file.exists():
                self.index.load(str(self.index_file))
            
        except Exception as e:
            logger.error("FN:_parse_knowledge_file Failed to parse knowledge file: %s", e)
    
    def _parse_markdown_entries(self, content: str) -> Dict[str, KnowledgeEntry]:
        """
        Parse knowledge entries from markdown content.
        
        Args:
            content: Full markdown content
            
        Returns:
            Dictionary of entry_id -> KnowledgeEntry
        """
        entries = {}
        
        # Split by section headers (## Title)
        sections = re.split(r'\n##\s+', content)
        
        for section in sections[1:]:  # Skip first empty section
            # Parse entry fields
            entry_data = {}
            
            # Extract title from first line
            lines = section.strip().split('\n')
            title = lines[0].strip()
            
            # Parse key-value pairs
            for line in lines[1:]:
                match = re.match(r'-\s*\*\*(\w+)\*\*:\s*(.+)', line)
                if match:
                    key = match.group(1).lower()
                    value = match.group(2).strip()
                    
                    # Handle tags list
                    if key == 'tags':
                        tags = re.findall(r'\[([^\]]+)\]', value)
                        value = [t.strip().strip('[]').split(', ') for t in tags]
                        if value and isinstance(value[0], list):
                            value = value[0]
                    else:
                        # Clean up tags format if still present
                        if key == 'tags':
                            value = [t.strip().strip('[]').strip("'\"") for t in re.findall(r'[^,\[\]"\'\s]+', value) if t.strip()]
                    
                    entry_data[key] = value
            
            if entry_data:
                entry_id = self._generate_entry_id(title)
                entry = KnowledgeEntry.from_dict({
                    "title": title,
                    **entry_data
                })
                entries[entry_id] = entry
        
        logger.info("FN:_parse_markdown_entries Parsed %d entries", len(entries))
        return entries
    
    def _generate_entry_id(self, title: str) -> str:
        """Generate a unique entry ID from title."""
        # Use lowercase slug format
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        return slug
    
    def capture_entry(self, entry: KnowledgeEntry) -> bool:
        """
        Capture a new knowledge entry.
        
        Args:
            entry: KnowledgeEntry to capture
            
        Returns:
            True if successful, False otherwise
        """
        try:
            entry_id = self._generate_entry_id(entry.title)
            
            # Check for duplicate
            if entry_id in self.index.entries:
                logger.warning("FN:capture_entry Duplicate entry detected: %s", entry_id)
                # Update existing entry
                self.index.remove_entry(entry_id)
            
            # Add to index
            self.index.add_entry(entry_id, entry)
            
            # Append to markdown file
            self._append_to_markdown(entry)
            
            # Save index
            self.index.save(str(self.index_file))
            
            logger.info("FN:capture_entry Captured entry: %s", entry_id)
            return True
            
        except Exception as e:
            logger.error("FN:capture_entry Failed to capture entry: %s", e)
            return False
    
    def _append_to_markdown(self, entry: KnowledgeEntry) -> None:
        """Append entry to the markdown file."""
        # Ensure parent directory exists
        self.knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        
        markdown = entry.to_markdown()
        
        with open(self.knowledge_file, 'a', encoding='utf-8') as f:
            f.write('\n---\n\n')
            f.write(markdown)
    
    def search(self, query: str, category: Optional[str] = None, 
               tags: Optional[List[str]] = None, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Search for knowledge entries.
        
        Args:
            query: Search keywords
            category: Optional category filter
            tags: Optional tag filters (all must match)
            limit: Maximum results
            
        Returns:
            List of matching knowledge entries
        """
        results = []
        
        if query:
            results = self.index.search_by_query(query, limit)
        elif category:
            results = self.index.search_by_category(category)
        elif tags:
            # Find entries with all specified tags
            all_tagged = None
            for tag in tags:
                tag_results = self.index.search_by_tag(tag)
                if all_tagged is None:
                    all_tagged = set(e.title for e in tag_results)
                else:
                    all_tagged &= set(e.title for e in tag_results)
            
            results = [e for e in self.index.entries.values() if e.title in all_tagged]
        else:
            # Return recent entries
            results = list(self.index.entries.values())[:limit]
        
        logger.info("FN:search Found %d results for query: %s", len(results), query)
        return results
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """
        Get a specific entry by ID.
        
        Args:
            entry_id: Entry identifier
            
        Returns:
            KnowledgeEntry if found, None otherwise
        """
        return self.index.entries.get(entry_id)
    
    def get_related(self, entry_id: str, limit: int = 5) -> List[KnowledgeEntry]:
        """
        Get entries related to a specific entry.
        
        Args:
            entry_id: Source entry ID
            limit: Maximum related entries
            
        Returns:
            List of related knowledge entries
        """
        return self.index.get_related(entry_id, limit)
    
    def get_categories(self) -> Dict[str, int]:
        """
        Get all categories with entry counts.
        
        Returns:
            Dictionary of category -> count
        """
        return {cat: len(entries) for cat, entries in self.index.by_category.items()}
    
    def get_tags(self) -> Dict[str, int]:
        """
        Get all tags with usage counts.
        
        Returns:
            Dictionary of tag -> count
        """
        return {tag: len(entries) for tag, entries in self.index.by_tag.items()}
    
    def suggest_context(self, user_query: str) -> List[Dict]:
        """
        Suggest relevant knowledge context for a user query.
        
        Args:
            user_query: The user's current question or task description
            
        Returns:
            List of relevant knowledge entries with context
        """
        # Search for relevant entries
        results = self.search(user_query, limit=5)
        
        # Format for AI consumption
        context = []
        for entry in results:
            context.append({
                "title": entry.title,
                "relevance": entry.entry_type,
                "solution": entry.solution,
                "problem": entry.problem,
                "tags": entry.tags
            })
        
        return context


# Convenience functions for AI agents
_default_store: Optional[KnowledgeStore] = None

def get_knowledge_store() -> KnowledgeStore:
    """Get the default knowledge store instance."""
    global _default_store
    if _default_store is None:
        _default_store = KnowledgeStore(
            knowledge_file=".roo/skills/knowledge/data/knowledge.md",
            index_file=".roo/skills/knowledge/data/knowledge_index.json"
        )
    return _default_store

def search_knowledge(query: str, category: Optional[str] = None, limit: int = 5) -> List[KnowledgeEntry]:
    """
    Quick search function for AI agents.
    
    Args:
        query: Search keywords
        category: Optional category filter
        limit: Maximum results
        
    Returns:
        List of relevant knowledge entries
    """
    store = get_knowledge_store()
    return store.search(query, category=category, limit=limit)

def capture_knowledge_entry(entry: KnowledgeEntry) -> bool:
    """
    Capture a new knowledge entry.
    
    Args:
        entry: KnowledgeEntry to capture
        
    Returns:
        True if successful
    """
    store = get_knowledge_store()
    return store.capture_entry(entry)

def get_knowledge_context(query: str) -> List[Dict]:
    """
    Get contextual knowledge for a query.
    
    Args:
        query: User query
        
    Returns:
        List of relevant knowledge context
    """
    store = get_knowledge_store()
    return store.suggest_context(query)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize store
    store = KnowledgeStore(".roo/skills/knowledge/data/knowledge.md")
    
    # Search
    results = store.search("nextjs")
    for r in results:
        print(f"- {r.title} ({r.category})")
    
    # Show stats
    print(f"\nCategories: {store.get_categories()}")
    print(f"Tags: {store.get_tags()}")
