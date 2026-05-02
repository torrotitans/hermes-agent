# Dynamic Knowledge Acquisition Skill

An event-driven system that automatically captures, organizes, and makes available knowledge discovered during coding sessions. This skill enables the AI to learn from patterns, best practices, and lessons learned, creating an evolving knowledge base for future reference.

## Overview

The knowledge skill consists of three main components:

1. **File Monitor** - Watches for code changes in real-time
2. **Suggestion Engine** - Analyzes changes and proposes knowledge entries
3. **Knowledge Store** - Stores, indexes, and retrieves knowledge for AI reference

## Installation

The skill is automatically available when the `.roo/skills/knowledge` directory is present in the workspace.

## Quick Start

### Manual Knowledge Capture

```python
from .roo.skills.knowledge import KnowledgeStore, KnowledgeEntry

# Initialize store
store = KnowledgeStore(".roo/skills/knowledge/data/knowledge.md")

# Create a knowledge entry
entry = KnowledgeEntry(
    title="Next.js Server Action Caching Pattern",
    entry_type="best-practice",
    category="frontend",
    date="2026-04-16",
    context="Implementing data fetching with Next.js 14 Server Actions",
    problem="Client components were re-rendering unnecessarily",
    solution="Used react.cache() to memoize expensive computations",
    code_reference="UI/src/features/dashboard/ui/analytics-charts.tsx",
    tags=["nextjs", "caching", "performance"]
)

# Capture the entry
store.capture_entry(entry)

# Search for related knowledge
results = store.search("caching", category="frontend")
```

### Event-Driven Monitoring

```python
from .roo.skills.knowledge import KnowledgeMonitor

# Start monitoring for changes
monitor = KnowledgeMonitor(root_path=".")
monitor.setup()

# Start watching (blocks)
monitor.start(blocking=True)

# Or run in background
monitor.start(blocking=False)
```

### Using the Convenience Functions

```python
from .roo.skills.knowledge import (
    search_knowledge,
    capture_knowledge_entry,
    get_knowledge_context
)

# Quick search
results = search_knowledge("authentication", category="security")

# Capture an entry
entry = KnowledgeEntry(...)
capture_knowledge_entry(entry)

# Get contextual knowledge for a query
context = get_knowledge_context("How to implement rate limiting?")
```

## Knowledge Entry Format

Knowledge entries follow a standardized markdown format:

```markdown
## [Entry Title]
- **Type:** pattern | best-practice | lesson-learned | discovery | anti-pattern
- **Category:** frontend | backend | architecture | security | testing | devops | development
- **Date:** YYYY-MM-DD
- **Context:** Brief description of the situation
- **Problem:** What challenge was encountered
- **Solution:** How it was resolved
- **Code Reference:** File paths or code snippets
- **Tags:** [tag1, tag2, ...]
- **Validation:** How this knowledge was confirmed
```

## Entry Types

| Type | Description |
|------|-------------|
| `pattern` | Reusable code structure or design pattern |
| `best-practice` | Recommended approach or implementation |
| `lesson-learned` | Insight from resolving issues |
| `discovery` | New finding or optimization |
| `anti-pattern` | What to avoid and why |

## Categories

| Category | Description |
|----------|-------------|
| `frontend` | UI, React, Next.js, styling |
| `backend` | APIs, databases, business logic |
| `architecture` | System design, patterns, structure |
| `security` | Authentication, authorization, vulnerabilities |
| `testing` | Unit tests, integration tests, test patterns |
| `devops` | Deployment, CI/CD, infrastructure |
| `development` | Tooling, IDE, debugging |

## Search and Retrieval

### Basic Search

```python
# Search by keyword
results = store.search("authentication")

# Search with category filter
results = store.search("caching", category="frontend")

# Search by tags
results = store.search("", tags=["nextjs", "performance"])
```

### Get Related Entries

```python
# Get entries related to a specific entry
related = store.get_related("nextjs-server-action-caching-pattern", limit=5)
```

### Browse by Category

```python
frontend_knowledge = store.index.search_by_category("frontend")
```

## Integration with Agentic Workflows

### Automatic Suggestion on Code Changes

The file monitor can automatically suggest knowledge entries when significant patterns are detected:

```python
from .roo.skills.knowledge import KnowledgeMonitor, FileChange

def on_change(change: FileChange):
    if change.change_type == "modified":
        print(f"File modified: {change.path}")
        # Suggestion engine automatically analyzes and logs suggestions

monitor = KnowledgeMonitor(root_path=".")
monitor.watcher.register_callback(on_change)
monitor.setup()
monitor.start(blocking=False)
```

### AI Context Enhancement

When the AI is working on a task, it can retrieve relevant knowledge:

```python
# Before implementing a feature, check for existing knowledge
context = get_knowledge_context("implementing user authentication")

# Use the context to inform implementation decisions
for entry in context:
    print(f"- {entry['title']}: {entry['solution']}")
```

## Configuration

### File Watcher Configuration

```python
from .roo.skills.knowledge import WatchConfig

config = WatchConfig(
    root_path=".",
    exclude_patterns=[".git", "node_modules", ".next", "__pycache__"],
    include_extensions=[".py", ".tsx", ".ts", ".md", ".json"],
    polling_interval=2.0,
    debounce_time=1.0
)
```

## File Structure

```
.roo/skills/knowledge/
├── SKILL.md              # Skill definition and documentation
├── README.md             # This file
├── __init__.py          # Package exports
├── data/
│   └── knowledge.md     # Main knowledge base
├── monitors/
│   ├── __init__.py
│   └── file_watcher.py  # File system monitoring
├── analyzers/
│   ├── __init__.py
│   └── knowledge_suggester.py  # Pattern detection
├── store/
│   ├── __init__.py
│   └── knowledge_store.py  # Storage and retrieval
└── logs/
    └── suggestions/     # Suggestion logs
```

## Best Practices

1. **Review Before Capturing**: Always review AI-suggested entries before saving
2. **Be Specific**: Use precise titles and code references
3. **Add Validation**: Document how the knowledge was verified
4. **Use Tags**: Tag entries with relevant keywords for discoverability
5. **Regular Maintenance**: Periodically review and update entries

## Troubleshooting

### Knowledge entries not being captured

- Ensure the knowledge.md file has write permissions
- Check that the parent directory exists
- Verify the entry format matches the expected schema

### File watcher not detecting changes

- Check that the root_path is correct
- Verify exclude patterns aren't filtering out the target files
- Increase polling_interval if changes are being missed

### Search returning no results

- Check the category spelling
- Verify tags match exactly (case-insensitive)
- Try broader search terms

## Example Entries

See [`data/knowledge.md`](data/knowledge.md) for example knowledge entries and the entry template.

## License

Part of the Torro Agentic Coding Standards ecosystem.
