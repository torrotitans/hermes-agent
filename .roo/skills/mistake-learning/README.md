# Mistake Learning Skill

A comprehensive system for capturing, analyzing, and learning from mistakes encountered during agent task execution.

## Overview

This skill provides a structured approach to mistake management that:
1. **Captures** mistakes in real-time during task execution
2. **Analyzes** patterns and relationships between issues
3. **Summarizes** findings into the central `agentic/mistakes.md` registry
4. **Enables** future agents to consult past mistakes for prevention

## Files

| File | Purpose |
|------|---------|
| [`SKILL.md`](SKILL.md) | Main skill instructions and guidelines |
| [`../agentic/mistake_collector.py`](../agentic/mistake_collector.py) | Real-time mistake tracking utility |
| [`../agentic/mistake_summary.py`](../agentic/mistake_summary.py) | Summary generation and analysis tools |
| [`../agentic/mistakes.md`](../agentic/mistakes.md) | Central mistake registry (target destination) |

## Quick Start

### 1. Initialize at Task Start

```python
from agentic.mistake_collector import MistakeCollector

collector = MistakeCollector(task_name="Your Task Name")
```

### 2. Log Mistakes During Execution

```python
collector.log_mistake(
    issue="Brief description of the mistake",
    context="What was being attempted when error occurred",
    resolution="How the mistake was fixed",
    category="Category Name",
    severity="High",
    affected_files=["file1.py", "file2.js"],
    root_cause="Why the mistake happened",
    preventive_measures=["Action to avoid recurrence"]
)
```

### 3. Log Observations (Optional)

```python
collector.log_observation(
    content="Important learning point",
    category="Category"
)
```

### 4. Generate Summary at Task End

```python
from agentic.mistake_summary import generate_summary

generate_summary(
    collector=collector,
    mistakes_file="agentic/mistakes.md"
)
```

## CLI Usage

```bash
# Demo mode - shows example usage
python3 agentic/mistake_collector.py --demo

# Search existing mistakes
python3 agentic/mistake_summary.py --search "Next.js standalone"

# Analyze session for patterns
python3 agentic/mistake_summary.py --analyze --session-file session.json
```

## Mistake Categories

Use these standardized categories:
- **Build Configuration** - Build scripts, Makefile, webpack, Next.js config
- **Database** - SQLModel, migrations, connection issues
- **API Integration** - REST/GraphQL endpoints, authentication
- **UI/UX** - Frontend components, styling, layout
- **Testing** - Test failures, mock issues, coverage
- **Docker/Container** - Containerization, Docker Compose, k8s
- **Environment** - Environment variables, config files
- **Dependencies** - Package conflicts, version issues
- **Security** - Auth, permissions, vulnerabilities
- **Performance** - Slow queries, memory leaks, optimization

## Severity Levels

| Level | Description |
|-------|-------------|
| **Low** | Minor inconvenience, cosmetic issues |
| **Medium** | Functional but requires workaround |
| **High** | Blocks feature or causes significant issues |
| **Critical** | System-breaking or data-loss scenarios |

## Integration with Torro Standards

This skill enforces:
- **Principle 16 (Resiliency)**: Learning from failures to improve future performance
- **Principle 7 (Agentic Best Practices)**: Explicit error handling and schema validation
- **Principle 14 (Modular Design)**: Observable, diagnostic-friendly systems

## Example Workflow

1. **Task Start**: `collector = MistakeCollector(task_name="Next.js Build")`
2. **During Execution**: Log mistakes as they occur
3. **Task Complete**: `generate_summary(collector, "agentic/mistakes.md")`
4. **Next Task**: Read `mistakes.md` to check for related past issues

## Best Practices

1. **Be Specific**: Include exact error messages and file paths
2. **Document Root Cause**: Don't just note the symptom - explain why it happened
3. **Add Prevention Steps**: Clear actions to avoid recurrence
4. **Link Related Mistakes**: Connect to existing entries when applicable
5. **Consult Before Starting**: Always check `mistakes.md` for similar past issues

## Maintenance

### Adding New Categories

Edit [`mistake_collector.py`](../agentic/mistake_collector.py) and add to `MistakeCategory` enum:

```python
class MistakeCategory(Enum):
    # ... existing categories ...
    NEW_CATEGORY = "New Category Name"
```

### Updating Mistake Registry Format

Edit [`mistake_summary.py`](../agentic/mistake_summary.py) and update the `to_markdown()` method in the `Mistake` class.
