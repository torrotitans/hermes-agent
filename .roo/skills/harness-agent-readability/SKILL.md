---
name: harness-agent-readability
description: Optimize codebases for AI agent readability including technology selection, code structure, and context management for agent reasoning
---

# Agent Readability Skill

## When to Use This Skill

Use this skill when:
- Designing systems for AI agent development
- Refactoring code for better agent comprehension
- Setting up development environments for agents
- Creating documentation for agent consumption

## When NOT to Use This Skill

Do NOT use this skill when:
- Project is purely human-driven development
- Team lacks AI agent infrastructure
- Creative/exploratory work requires flexible patterns

## Core Principle

**Optimize for agent reasoning, not just human reading.**

Anything not accessible in the agent's context window doesn't exist for the agent.

## Key Practices

### Choose "Boring" Technologies

Prioritize technologies with:
- Stable APIs (minimal breaking changes)
- Good training data coverage
- Strong type systems
- Comprehensive documentation

"Boring" technologies are easier for agents to model:
- Better composability
- Predictable behavior
- Extensive training examples

### Re-implement vs Wrap Decision

Sometimes re-implementing a subset is more cost-effective than wrapping opaque upstream behavior.

**Criteria for re-implementation:**
- Upstream behavior is opaque/unpredictable
- Need tight integration with own telemetry
- Require 100% test coverage
- Behavior must be fully predictable

### Enable Agent-Operable Applications

Make applications actionable for agents:

1. **Git Worktree Launch**: Enable per-change isolated instances
2. **DevTools Protocol Access**: DOM snapshots, screenshots, navigation
3. **Local Observability Stack**: LogQL for logs, PromQL for metrics
4. **Ephemeral Environments**: Task-complete cleanup

This enables prompts like:
- "Ensure service starts in <800ms"
- "No span exceeds 2 seconds for these 4 user journeys"

## Workflow

### Step 1: Audit Technology Stack

Evaluate technologies for agent readability:

1. List all major dependencies
2. Rate each for API stability (1-5)
3. Rate each for training coverage (1-5)
4. Identify candidates for re-implementation

Example audit:

```python
# Technology audit
technologies = {
    "Flask": {"api_stability": 5, "training_coverage": 5},
    "SQLModel": {"api_stability": 4, "training_coverage": 4},
    "CustomORM": {"api_stability": 2, "training_coverage": 1}
}
```

### Step 2: Implement FN: Docstring Convention

Add standardized docstring prefixes:

1. Every function/method starts with `FN:function_name`
2. Include purpose and behavior description
3. Document parameters and return values

Example:

```python
def process_user_data(user_id: int, data: dict) -> User:
    """FN:process_user_data Process user data and create user record.
    
    Args:
        user_id: Unique user identifier
        data: User data dictionary
        
    Returns:
        Created User object
    """
```

### Step 3: Structure Code for Agent Navigation

Organize code for easy agent parsing:

1. Use class-based organization (not standalone functions)
2. Keep files under 200 lines
3. Create clear entry points
4. Add type hints throughout

Example structure:

```python
class UserService:
    """FN:UserService Handle user-related operations."""
    
    def __init__(self, session: Session):
        """FN:__init__ Initialize service."""
        self.session = session
    
    def create_user(self, data: UserCreate) -> User:
        """FN:create_user Create new user."""
        # Implementation
```

### Step 4: Implement Context Management

Address Context Rot problem:

1. **Compaction**: Smart compression of context
2. **Tool Output Offloading**: Store full outputs in filesystem
3. **Progressive Disclosure**: Load tools on-demand

Example context management:

```python
class ContextManager:
    """FN:ContextManager Manage agent context window."""
    
    def compact_context(self, context: list) -> str:
        """FN:compact_context Compress context for efficiency."""
        # Keep headers and key info, truncate details
        
    def offload_output(self, output: str, path: str):
        """FN:offload_output Store large outputs to filesystem."""
        # Save to file, keep reference in context
```

### Step 5: Set Up Observability

Enable agent debugging:

1. Structured logging with FN: prefix
2. Metrics for key operations
3. Trace IDs for request tracking

Example logging setup:

```python
import logging

logger = logging.getLogger(__name__)

def process_request(request_id: str):
    """FN:process_request Handle incoming request."""
    logger.info(f"FN:process_request Starting request {request_id}")
    # Implementation
```

## Key Metrics

| Metric | Target |
|--------|--------|
| File size average | <200 lines |
| Type hint coverage | 100% |
| Docstring coverage | 100% |
| Context window usage | <80% |
| Agent task success rate | >90% |

## Related Skills

- [`harness-engineering-overview`](harness-engineering-overview/SKILL.md) - Overview of all Harness Engineering concepts
- [`harness-repo-as-truth`](harness-repo-as-truth/SKILL.md) - Documentation structure
- [`harness-entropy-management`](harness-entropy-management/SKILL.md) - Code quality maintenance

## Troubleshooting

### Problem: Agents can't understand complex code

**Solution:** Break into smaller functions. Add more docstrings. Use descriptive variable names.

### Problem: Context window fills up quickly

**Solution:** Implement context compaction. Use progressive disclosure. Offload large outputs.

### Problem: Agents make wrong assumptions

**Solution:** Add more explicit type hints. Improve documentation. Add inline comments for non-obvious logic.

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [LangChain Context Rot](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
