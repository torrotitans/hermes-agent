---
name: harness-entropy-management
description: Implement entropy management and automated garbage collection for AI agent codebases including golden rules, quality scoring, and automated refactoring
---

# Entropy Management Skill

## When to Use This Skill

Use this skill when:
- Managing technical debt in high-throughput agent environments
- Setting up automated code quality maintenance
- Implementing continuous refactoring workflows
- Preventing code drift and pattern degradation

## When NOT to Use This Skill

Do NOT use this skill when:
- Codebase is stable with minimal agent activity
- Team prefers scheduled refactoring sprints
- Automated refactoring risks are too high for the domain

## Core Principle

**Agents reproduce patterns that exist in the repository—including bad patterns.**

Technical debt is a high-interest loan. Pay it down continuously, not in crisis-driven rewrites.

## The Problem: Code Entropy

As agents work, inevitable drift occurs:

- Duplicate utility functions scattered across files
- Inconsistent error handling patterns
- Guess-based data structures (YOLO probing)
- Outdated documentation vs actual code

## Failed Approach: Manual Cleanup

> "Team spends 20% of Friday cleaning AI residue. Not scalable."

Manual cleanup doesn't scale and creates bottlenecks.

## Successful Approach: Encode + Automate

### Golden Rules

Encode subjective preferences as mechanical rules:

1. **Shared Utility Packages > Hand-Rolled Helpers**
   - Centralize invariants
   - Single source of truth
   - Easier to update

2. **No YOLO Probing**
   - Validate data at boundaries
   - Use typed SDKs
   - Fail fast on schema violations

3. **Prefer Owned Implementations of Critical Subsets**
   - Integrate with own telemetry
   - 100% test coverage
   - Fully predictable behavior

### Garbage Collection Flow

```
Scheduled Background Agent Task
  → Scan for code drift
  → Update quality scores
  → File refactoring PRs
  → Auto-merge trusted changes
```

## Workflow

### Step 1: Define Golden Rules

Document the golden rules for your codebase:

1. Identify recurring anti-patterns
2. Define preferred patterns
3. Encode as lint rules or documentation

Example golden rules:

```markdown
# Golden Rules

1. All database queries must use SQLModel
2. All API responses must be typed
3. No nested ternary operators
4. Functions must have docstrings with FN: prefix
```

### Step 2: Implement Quality Scoring

Create a quality scoring system:

1. Define quality metrics per domain
2. Create scoring algorithm
3. Track scores over time

Example quality metrics:

```python
# Quality score components
- Test coverage: 40%
- Documentation coverage: 20%
- Lint compliance: 20%
- Code complexity: 20%
```

### Step 3: Create Background Agent Tasks

Set up automated scanning:

1. Schedule regular scans (daily/weekly)
2. Define scan scope and depth
3. Configure report generation

Example scan task:

```python
# Scheduled task: scan_code_drift.py
def scan_codebase():
    issues = []
    for file in get_python_files():
        if not has_fn_prefix(file):
            issues.append(f"Missing FN: prefix in {file}")
        if get_complexity(file) > 10:
            issues.append(f"High complexity in {file}")
    return issues
```

### Step 4: Set Up Auto-Refactoring PRs

Configure automated fix proposals:

1. Create refactoring agent workflow
2. Define PR template with before/after
3. Set up auto-merge for trusted changes

Example PR template:

```markdown
# Automated Refactoring

## Issue
Duplicate utility function found in 3 files.

## Fix
Extract to shared utility module.

## Files Changed
- src/utils/common.py (new)
- src/service/a.py
- src/service/b.py
```

### Step 5: Configure Auto-Merge

Set up trusted auto-merge:

1. Define merge criteria (tests pass, lint passes)
2. Set up branch protection exceptions
3. Configure notification on merge

## Key Metrics

| Metric | Target |
|--------|--------|
| Code drift detection time | <24 hours |
| Quality score trend | Improving |
| Auto-merge success rate | >90% |
| Technical debt ratio | Decreasing |

## Related Skills

- [`harness-engineering-overview`](harness-engineering-overview/SKILL.md) - Overview of all Harness Engineering concepts
- [`harness-mechanical-enforcement`](harness-mechanical-enforcement/SKILL.md) - Implementing enforcement rules
- [`harness-agent-readability`](harness-agent-readability/SKILL.md) - Code optimization for agents

## Troubleshooting

### Problem: Too many refactoring PRs

**Solution:** Adjust scan frequency. Batch related changes. Prioritize by impact.

### Problem: Auto-merge introduces bugs

**Solution:** Strengthen test requirements. Add smoke tests to merge criteria.

### Problem: Quality scores don't reflect reality

**Solution:** Review scoring algorithm. Add missing metrics. Calibrate with human review.

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [Technical Debt Quadrants](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
