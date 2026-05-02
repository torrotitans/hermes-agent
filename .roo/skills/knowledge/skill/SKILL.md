# Dynamic Knowledge Acquisition Skill

This skill provides an event-driven system that automatically records new patterns, discoveries, and lessons learned during coding sessions and makes them available for AI reference in future tasks.

## Core Components

### 1. Knowledge Store (`knowledge.md`)
Central repository for structured knowledge entries that the AI can reference during development.

### 2. File Monitor (`monitors/file_watcher.py`)
Event-driven script that watches for file changes and triggers knowledge capture.

### 3. Suggestion Engine (`analyzers/knowledge_suggester.py`)
Analyzes code changes and proposes knowledge entries based on patterns.

### 4. Knowledge Index (`index/knowledge_index.json`)
Searchable index for fast AI lookups and references.

## Usage Pattern

```
Agent monitors code changes → Analyzes patterns → Suggests knowledge entry → 
Human approves/rejects → Stores in knowledge.md → Updates index
```

## Knowledge Entry Format

```markdown
## [Entry Title]
- **Type:** pattern|pattern-anti|best-practice|lesson-learned|discovery
- **Category:** backend|frontend|architecture|security|testing|devops
- **Date:** YYYY-MM-DD
- **Context:** Brief description of the situation
- **Problem:** What challenge was encountered
- **Solution:** How it was resolved
- **Code Reference:** File paths or code snippets
- **Tags:** [tag1, tag2, ...]
- **Validation:** How this knowledge was confirmed
```

## Functions

- `capture_knowledge_entry(entry: KnowledgeEntry) -> bool`
- `search_knowledge(query: str, category: str = None) -> List[KnowledgeEntry]`
- `suggest_knowledge_from_changes(changes: List[FileChange]) -> List[Suggestion]`
- `build_knowledge_index() -> dict`

## Integration Points

- **Agentic Compliance**: Records insights about coding standard adherence
- **Testing**: Captures test patterns and common failure modes
- **Architecture**: Documents design decisions and trade-offs
- **Security**: Logs security patterns and vulnerability fixes

## Automated Trigger Conditions

The system triggers knowledge capture when:
1. A new pattern is detected across multiple files
2. A bug fix reveals a systemic issue
3. A novel solution is implemented
4. A configuration change resolves a persistent issue
5. A performance optimization is applied

## Example Entry

```markdown
## Next.js 14 Server Action Caching Pattern
- **Type:** best-practice
- **Category:** frontend
- **Date:** 2026-04-16
- **Context:** Implementing data fetching with Next.js 14 Server Actions
- **Problem:** Client components were re-rendering unnecessarily on each action call
- **Solution:** Use `react.cache()` to memoize expensive computations and ensure stable references across renders
- **Code Reference:** UI/src/features/dashboard/ui/analytics-charts.tsx
- **Tags:** [nextjs, caching, performance, server-actions]
- **Validation:** Measured 40% reduction in unnecessary re-renders
```
