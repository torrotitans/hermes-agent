---
name: harness-engineering-overview
description: Implement Harness Engineering practices for AI agent-driven development including repo as source of truth, mechanical enforcement, agent readability, entropy management, and throughput-optimized merging
---

# Harness Engineering Overview Skill

## When to Use This Skill

Use this skill when:
- Starting a new AI agent-driven development project
- Optimizing existing workflows for AI agent productivity
- Implementing constraint-based development environments
- Designing feedback loops for autonomous agent work
- Managing technical debt in high-throughput agent environments

## When NOT to Use This Skill

Do NOT use this skill when:
- Working on traditional human-coded projects without AI agents
- Projects require creative/exploratory coding without constraints
- Team lacks AI coding agent infrastructure (Claude Code, Cursor, etc.)

## Core Concepts

Harness Engineering is an engineering paradigm where engineers **design environments, articulate intent, and build feedback loops** that enable AI agents to reliably complete work.

### The Six Core Concepts

1. **Repo as System of Record** - Nothing exists for the agent outside the repository
2. **Map, Not Manual** - AGENTS.md as a ~100-line navigation entry point
3. **Mechanical Enforcement** - Lint rules and CI checks as invariant guardians
4. **Agent Readability** - Optimize for agent reasoning, not just human reading
5. **Entropy Management** - Automated garbage collection for code drift
6. **Throughput Changes Merge** - Fast iteration with backpressure mechanisms

## Workflow

### Step 1: Establish Repo as System of Record

Create the foundational documentation structure:

1. Create `AGENTS.md` at repository root (~100 lines max)
2. Create `ARCHITECTURE.md` with domain and layer mappings
3. Create `docs/` directory with subdirectories:
   - `design-docs/` - Design decisions with validation status
   - `exec-plans/` - Execution plans with progress tracking
   - `product-specs/` - Product specifications
   - `references/` - External references (llms.txt)
   - `generated/` - Auto-generated content

### Step 2: Implement Mechanical Enforcement

Set up automated validation:

1. Create custom linter rules for:
   - File size limits
   - Naming conventions
   - Logging standards
   - Architecture boundaries
2. Configure CI to block on lint violations
3. Embed fix instructions in error messages

### Step 3: Design for Agent Readability

Optimize codebase for agent consumption:

1. Choose "boring" technologies (stable APIs, good training coverage)
2. Implement self-contained utilities with 100% test coverage
3. Enable git worktree-based application launching
4. Provide clear entry points with FN: docstring prefixes

### Step 4: Implement Entropy Management

Set up automated code quality maintenance:

1. Define "Golden Rules" for code quality
2. Create background agent tasks for:
   - Scanning code drift
   - Updating quality scores
   - Filing refactoring PRs
3. Configure auto-merge for trusted refactoring PRs

### Step 5: Optimize for Throughput

Design for high-velocity agent work:

1. Minimize blocking merge gates
2. Implement agent-to-agent code review
3. Configure flaky test retry mechanisms
4. Set up Ralph Loop for long-running tasks

## Key Metrics

| Metric | Target |
|--------|--------|
| PRs per developer per day | 3.5+ |
| AGENTS.md line count | <100 |
| Lint rule coverage | 100% of critical paths |
| Test coverage for utilities | 100% |
| Auto-merge rate for refactoring | >80% |

## Related Skills

- [`harness-repo-as-truth`](harness-repo-as-truth/SKILL.md) - Deep dive on repo as system of record
- [`harness-mechanical-enforcement`](harness-mechanical-enforcement/SKILL.md) - Implementing lint rules and CI checks
- [`harness-agent-readability`](harness-agent-readability/SKILL.md) - Optimizing for agent reasoning
- [`harness-entropy-management`](harness-entropy-management/SKILL.md) - Automated code quality maintenance
- [`harness-throughput-merge`](harness-throughput-merge/SKILL.md) - High-velocity agent workflows

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [Ralph Wiggum Loop](https://github.com/snarktank/ralph)
