---
name: harness-repo-as-truth
description: Implement repo as system of record for AI agents including AGENTS.md entry point, documentation structure, and knowledge centralization
---

# Repo as System of Record Skill

## When to Use This Skill

Use this skill when:
- Setting up a new repository for AI agent development
- Migrating existing documentation into agent-accessible format
- Creating AGENTS.md navigation structure
- Establishing documentation conventions for agent consumption

## When NOT to Use This Skill

Do NOT use this skill when:
- Repository is for human-only development
- Documentation contains sensitive information not suitable for repository storage
- Team uses alternative knowledge management systems accessible to agents

## Core Principle

**Nothing exists for the agent outside the repository.**

Knowledge location determines agent accessibility:

| Location | For Humans | For Agents |
|----------|------------|------------|
| Google Docs | ✅ | ❌ |
| Slack discussions | ✅ | ❌ |
| Team member's brain | ✅ | ❌ |
| Repository Markdown | ✅ | ✅ |
| Code + comments | ✅ | ✅ |
| Lint rules | Indirect ✅ | Direct ✅ |

## Workflow

### Step 1: Create AGENTS.md Entry Point

Create `AGENTS.md` at repository root with these constraints:

1. Keep file under 100 lines
2. Structure as navigation directory, not encyclopedia
3. Include sections:
   - Repository purpose
   - Quick start guide
   - Link to ARCHITECTURE.md
   - Link to docs/ subdirectories
   - Key conventions summary

Example structure:

```markdown
# Repository Name

Brief description of what this repository contains.

## Quick Start

1. Read ARCHITECTURE.md for domain overview
2. Check docs/exec-plans/ for active plans
3. Run `make setup` to initialize environment

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Design Docs](docs/design-docs/)
- [Execution Plans](docs/exec-plans/)
- [References](docs/references/)
```

### Step 2: Create ARCHITECTURE.md

Create architecture documentation with:

1. Domain boundaries and layer definitions
2. Dependency flow diagrams
3. Key abstractions and their purposes
4. Technology choices and rationale

### Step 3: Establish docs/ Structure

Create the following directory structure:

```
docs/
├── design-docs/          # Design decisions with validation status
├── exec-plans/           # Execution plans with progress tracking
│   ├── active/           # Currently active plans
│   └── completed/        # Completed plans (archived)
├── product-specs/        # Product specifications
├── references/           # External references (llms.txt)
├── generated/            # Auto-generated content (DB schemas, etc.)
├── QUALITY_SCORE.md      # Quality metrics per domain
├── RELIABILITY.md        # Reliability standards
└── SECURITY.md           # Security guidelines
```

### Step 4: Implement Documentation Conventions

For each document type, establish conventions:

**Design Docs:**
- Title and problem statement
- Proposed solution
- Alternatives considered
- Validation criteria
- Status (Draft/Approved/Implemented)

**Execution Plans:**
- Goal and success criteria
- Step-by-step tasks
- Progress tracking format
- Decision log

### Step 5: Set Up Doc Gardening

Implement automated documentation maintenance:

1. Create script to detect outdated documents
2. Configure CI check for documentation freshness
3. Set up agent tasks to propose documentation updates

## Key Metrics

| Metric | Target |
|--------|--------|
| AGENTS.md line count | <100 |
| Time to find architecture | <30 seconds |
| Documentation coverage | 100% of domains |
| Doc freshness score | >90% |

## Related Skills

- [`harness-engineering-overview`](harness-engineering-overview/SKILL.md) - Overview of all Harness Engineering concepts
- [`harness-mechanical-enforcement`](harness-mechanical-enforcement/SKILL.md) - Implementing validation rules
- [`harness-agent-readability`](harness-agent-readability/SKILL.md) - Optimizing content for agents

## Troubleshooting

### Problem: AGENTS.md becomes too large

**Solution:** Move detailed content to referenced files. AGENTS.md should only contain navigation links.

### Problem: Documentation becomes outdated

**Solution:** Implement doc-gardening agent that scans for stale content and proposes updates.

### Problem: Agents can't find relevant documentation

**Solution:** Improve cross-referencing between documents. Add explicit "See Also" sections.

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
