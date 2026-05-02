# Mistake Learning Skill

This skill enables agents to capture, analyze, and learn from mistakes and errors encountered during task execution. It provides automated tools to track issues, generate summaries, and maintain a living knowledge base of lessons learned.

## Overview

The Mistake Learning Skill consists of:
1. **Mistake Collector** (`agentic/mistake_collector.py`) - Tracks errors and observations during task execution
2. **Summary Generator** (`agentic/mistake_summary.py`) - Analyzes captured mistakes and generates structured reports
3. **Mistake Registry** (`agentic/mistakes.md`) - Central repository for documented mistakes and solutions

## Core Principles

### 1. Continuous Observation
- Agents MUST log significant decisions, errors, and corrections during task execution
- Use the `MistakeCollector` class to track observations in real-time
- Capture context: what was attempted, what went wrong, and how it was resolved

### 2. Structured Capture
- All mistakes MUST follow a standardized format:
  - **Issue**: Clear description of the problem
  - **Root Cause**: Why the mistake happened
  - **Solution**: How it was fixed
  - **Prevention**: How to avoid in the future

### 3. Post-Task Summarization
- At the end of each task, agents MUST call `generate_summary()` to compile all captured mistakes
- The summary should be appended to `agentic/mistakes.md`
- Each mistake receives a unique ID (M1, M2, M3, etc.)

### 4. Knowledge Reuse
- Before starting any task, agents SHOULD consult `mistakes.md` for related issues
- Use the `find_similar_mistakes()` method to search for relevant past incidents

## Usage

### During Task Execution

```python
from agentic.mistake_collector import MistakeCollector

# Initialize collector at task start
collector = MistakeCollector(task_name="Your Task Name")

# Log mistakes as they occur
collector.log_mistake(
    issue="Next.js standalone server path incorrect",
    context="Tried to run server at .next/standalone/server.js",
    resolution="Changed to .next/standalone/UI/server.js",
    category="Build Configuration"
)

# Log observations (non-critical learning points)
collector.log_observation(
    observation="Static assets need explicit copy command in standalone mode"
)
```

### Task Completion

```python
from agentic.mistake_summary import generate_summary

# Generate and append summary to mistakes.md
generate_summary(
    collector=collector,
    mistakes_file="agentic/mistakes.md",
    next_id=23  # Auto-determine from existing file
)
```

## Mistake Categories

Use these standardized categories for consistent tracking:

| Category | Description |
|----------|-------------|
| **Build Configuration** | Build scripts, Makefile, webpack, Next.js config |
| **Database** | SQLModel, migrations, connection issues |
| **API Integration** | REST/GraphQL endpoints, authentication |
| **UI/UX** | Frontend components, styling, layout |
| **Testing** | Test failures, mock issues, coverage |
| **Docker/Container** | Containerization, Docker Compose, k8s |
| **Environment** | Environment variables, config files |
| **Dependencies** | Package conflicts, version issues |
| **Security** | Auth, permissions, vulnerabilities |
| **Performance** | Slow queries, memory leaks, optimization |

## Mistake ID Assignment

- Mistakes are numbered sequentially (M1, M2, M3, ...)
- The next ID is determined by reading the existing `mistakes.md` file
- If no mistakes exist, start with M1
- IDs are permanent and should never be reused

## Template for New Mistakes

```markdown
### M##: [Short Descriptive Title]

**Date:** YYYY-MM-DD
**Severity:** Low | Medium | High | Critical
**Domain:** Category/Subcategory
**Affected Files:** `file1.py`, `file2.js`

#### Problem Statement
Clear description of what went wrong.

#### Root Cause Analysis
Explanation of why the mistake occurred.

#### Solution Applied
Step-by-step fix that was implemented.

#### Verification Steps
How to confirm the fix works.

#### Preventive Measures
Actions to avoid recurrence.

#### Related Mistakes
- **M##** - Related issue
- **M##** - Similar pattern
```

## Automated Workflow

1. **Task Start**: Initialize `MistakeCollector`
2. **During Execution**: Log all significant mistakes and observations
3. **Task End**: Call `generate_summary()` to append to `mistakes.md`
4. **Next Task**: Read `mistakes.md` to learn from past issues

## Skills Integration

This skill enforces the following Torro Agentic Coding Standards:
- **Principle 16 (Resiliency)**: Learning from failures to improve future performance
- **Principle 7 (Agentic Best Practices)**: Explicit error handling and schema validation
- **Principle 14 (Modular Design)**: Observable, diagnostic-friendly systems

## Example Output

After completing a task with mistakes, the agent generates:

```markdown
---

### M23: Task-Specific Mistake Title

**Date:** 2026-04-16
**Severity:** Medium
**Domain:** API Integration / Authentication
**Affected Files:** `engine/api/login/interface_login.py`

#### Problem Statement
Agent failed to handle expired token refresh correctly, causing 401 errors.

#### Root Cause Analysis
The token refresh logic did not check token expiration before use.

#### Solution Applied
Added pre-flight token validation before API calls.

#### Preventive Measures
Always validate token expiration before making authenticated requests.

#### Related Mistakes
- **M17** - Incomplete validation patterns
```

## Commands

| Command | Description |
|---------|-------------|
| `python3 agentic/mistake_collector.py --init` | Initialize new collector session |
| `python3 agentic/mistake_summary.py --generate` | Generate summary from current session |
| `python3 agentic/mistake_summary.py --search "keyword"` | Search mistakes by keyword |
| `python3 agentic/mistake_summary.py --simulate` | Show simulated mistake log |
