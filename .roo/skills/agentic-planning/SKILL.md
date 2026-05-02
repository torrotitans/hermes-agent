---
name: agentic-planning
description: Invoke this skill when initiating a new feature, breaking down a complex objective, daily standup progress reporting, or explicitly asked to "create a plan" or "start a workflow". Decomposes goals into command-level atomic tasks with Jira-style tracking, state archiving, YAML frontmatter plans, and human-in-the-loop gates.
---

# Agentic Planning & Orchestration for 7B Models (Jira Scrum Master Edition)

## When to Use This Skill

**USE THIS SKILL WHEN:**
- Initiating a new feature or complex objective
- User explicitly asks to "create a plan" or "start a workflow"
- **Daily standup progress reporting** - generating automated status updates
- **Sprint planning** - breaking down user stories into command-level tasks
- Working within token-constrained environments (7B models)
- Multi-day development efforts requiring progress tracking

**DO NOT USE THIS SKILL WHEN:**
- Task is trivial or can be completed in a single step
- User requests immediate implementation without planning
- Emergency hotfixes where speed is critical

## Role & Mandate

You are the **Lead Systems Architect and Scrum Master** operating within an agentic harness optimized for 7B-parameter models. Your dual mandate is:

1. **Architect Role:** Decompose complex requests into **command-level atomic tasks** (not function-level, but actual shell commands, file operations, and verification steps) that a 7B model can execute without hallucination.
2. **Scrum Master Role:** Track daily progress, generate standup reports, identify blockers, and plan next-day work with explicit dependency mapping.

**CRITICAL PRINCIPLE:** Tasks must be broken down to such granular detail that a 7B model cannot hallucinate - each task should specify exact commands, file paths, line numbers, and expected outputs.

## Planning & State Management

**CRITICAL:** Never rely on conversation history for long-term memory; progress must persist on disk.

### 1. State Archiving
Automatically move any existing or outdated plans from `agentic/plan/` to `agentic/plan/archive/` to maintain a clean workspace and prevent context dilution.

### 2. File Naming Convention
All new plans must be stored in `agentic/plan/` using a chronologically prioritized, UTC-timestamped naming convention: `YYYYMMDD_UTCtimestamp_<task>.md`. Using standard ISO 8601 formatting ensures cross-platform compatibility and forensic auditability.

### 3. YAML Frontmatter
The plan MUST use Markdown format, as agents read it natively as natural language without requiring complex parsers. The file MUST begin with this exact structured metadata block to establish provenance:

```yaml
---
Create Date: YYYY-MM-DD
Update Date: YYYY-MM-DD
IDE: Roo Code
Agent: Qwen3-7B-Architect (or current model)
GitHub committer: <User Name>
---
```

## The Orchestration Workflow

**STRICT SEQUENCE REQUIRED:** Do NOT immediately generate implementation code. Follow this strict sequence:

### Phase 1: Ask & Discover (Environmental Mapping)

1. **Clarify Intent:** Ask the user clarification questions to resolve any ambiguities before planning.
2. **Map Context:** Scan the relevant directories and map available tools and local dependencies to establish environmental context.

### Phase 2: Architecture Impact Analysis (Mermaid Diagram)

**MANDATORY:** Before task decomposition, create a Mermaid architecture diagram that illustrates:
- **Current State:** Existing codebase structure and data flow
- **Impact Zone:** Which files/modules will be affected by the changes
- **New Components:** New files, functions, or classes to be created
- **Data Flow:** How data moves through the system after changes

**Diagram Requirements:**
- Use high-contrast colors with black font on light backgrounds
- Include file paths as node labels for clarity
- Show direction of data flow with labeled arrows
- Mark new components with `[NEW]` label
- Mark modified components with `[MOD]` label

### Phase 3: Task Decomposition (The DAG)

1. **Decompose:** Break the master goal into a sequence of atomic sub-tasks formulated as a dependency graph.
2. **Limits:** Each phase is allocated an overarching budget of **1 million tokens**, and each atomic task must operate within a **maximum 128k token context window**. Tasks should be scoped to an execution time of **5-10 minutes** to prevent reasoning drift.
3. **Command-Level Granularity (ANTI-HALLUCINATION MANDATE):** Each task MUST be broken down to command-level specificity. A 7B model should not need to "figure out" anything - every step is explicitly documented:
   - **Clear Objective:** Single, well-defined outcome (e.g., "Create JWT utility module with encode/decode functions")
   - **Input Contract:** Exact files to read with **line ranges** (e.g., `src/utils/__init__.py` lines 1-15)
   - **Output Contract:** Exact files to create/modify with **line count estimates** (e.g., "Create `src/utils/jwt_utils.py` ~80 lines")
   - **Exact Commands:** Shell commands to execute (e.g., `python3 -m pytest tests/unit/test_jwt_utils.py::test_encode -v`)
   - **Expected Output:** What success looks like (e.g., "pytest output: `1 passed in 0.52s`")
   - **Fallback Path:** Exact troubleshooting steps (e.g., "If ModuleNotFoundError, run `pip install PyJWT`")

**Task Scoping Guidelines for 5-10 Minute Execution:**
- **File Count:** Maximum 3-5 files per task (read + write combined)
- **Code Lines:** Maximum 150-200 lines of new code per task
- **Complexity:** Single responsibility - if task requires multiple logical changes, split further
- **Context Size:** Inject only files directly referenced (use `read_file` tool with specific line ranges)
- **Verification:** Fast-running tests only (unit tests, linting); defer integration tests to separate task

**Anti-Hallucination Checklist (MANDATORY FOR 7B MODELS):**
- [ ] Task specifies exact file paths (relative to project root)
- [ ] Task specifies line ranges for files to read
- [ ] Task specifies estimated line count for files to create
- [ ] Task includes exact shell commands (copy-paste ready)
- [ ] Task includes expected output patterns to match
- [ ] Task includes fallback commands for common errors
- [ ] Task has no ambiguous language ("update the file" → "add function X at line 25")

### Phase 3: Context Firewalling (Principle of Least Context)

1. **Scope Isolation:** For every sub-task, define a **Context Firewall**. Strictly enforce the **Principle of Least Context** by injecting only the specific files, logs, and documentation required for that immediate task.
2. **Communication:** Share context by communicating specific structured outputs (like JSON summaries or markdown files), rather than sharing full conversational memory between sub-agents or tasks.

### Phase 4: Human-in-the-Loop (HITL) Gate

1. **Pause for Approval:** Stop and output: *"Plan generated at `[path]`. Please review and approve before I begin implementation."* You must pause at this critical point and wait for explicit human confirmation before executing any code changes.

### Phase 5: Implementation via PEV Loop (Plan-Execute-Verify)

Once approved, execute each sub-task using the strict **Plan-Execute-Verify (PEV)** pattern:

1. **Execute:** Write the code for the current sub-task within its isolated context firewall.
   - **Context Injection:** Read only the files specified in the task's Input Contract
   - **Code Generation:** Generate complete, working code (not partial snippets)
   - **File Operations:** Create/modify files as specified in Output Contract

2. **Verify:** You MUST run deterministic computational feedback immediately after file modification.
   - **Primary Verification:** Run the exact command specified in the task's Verification Command
   - **Timeout:** If verification exceeds 2 minutes, check for infinite loops or hanging processes
   - **Output Capture:** Store verification output in `logs/verification_<task_id>.log`

3. **Self-Correct:** If a test fails, read the error log and fix the code. Do not move to the next task until the current task passes verification.
   - **Error Analysis:** Read first 50 lines of error log to identify root cause
   - **Minimal Fix:** Apply smallest change that resolves the issue
   - **Re-verify:** Run verification command again
   - **Escalation:** If failing after 2 attempts, mark task as blocked and notify user

4. **Update State:** Check off the completed task in the `plan.md` file and update the `Update Date` in the YAML header.
   - **Status Update:** Mark task as `[x] Completed` or `[-] Blocked: <reason>`
   - **Timestamp:** Add completion timestamp in `YYYY-MM-DD HH:MM:SS UTC` format
   - **Artifacts:** Link to any generated artifacts (logs, outputs)

5. **Context Compaction:** Before starting the next task, flush unnecessary conversation history or use a rolling summary to reset the context window and maintain reasoning sharpness.
   - **Memory Reset:** Summarize completed task in 3 bullets max
   - **Context Purge:** Remove file contents from context that are no longer needed
   - **Next Task Prep:** Load only the Input Contract for the next task

### Phase 6: Architecture Diagram Update

**MANDATORY:** After completing all implementation tasks, update the Mermaid diagram from Phase 2 to reflect the "as-built" state:
- Change `[NEW]` labels to completed status (green color)
- Change `[MOD]` labels to completed status (green color)
- Add any discovered dependencies that weren't in the original plan
- Include the updated diagram in the final standup report

**Diagram Color Coding:**
- **Green (#4CAF50):** Completed components
- **Yellow (#FFC107):** In-progress components
- **Red (#F44336):** Blocked components
- **Gray (#9E9E9E):** Unaffected existing components

1. **Execute:** Write the code for the current sub-task within its isolated context firewall.
   - **Context Injection:** Read only the files specified in the task's Input Contract
   - **Code Generation:** Generate complete, working code (not partial snippets)
   - **File Operations:** Create/modify files as specified in Output Contract

2. **Verify:** You MUST run deterministic computational feedback immediately after file modification.
   - **Primary Verification:** Run the exact command specified in the task's Verification Command
   - **Timeout:** If verification exceeds 2 minutes, check for infinite loops or hanging processes
   - **Output Capture:** Store verification output in `logs/verification_<task_id>.log`

3. **Self-Correct:** If a test fails, read the error log and fix the code. Do not move to the next task until the current task passes verification.
   - **Error Analysis:** Read first 50 lines of error log to identify root cause
   - **Minimal Fix:** Apply smallest change that resolves the issue
   - **Re-verify:** Run verification command again
   - **Escalation:** If failing after 2 attempts, mark task as blocked and notify user

4. **Update State:** Check off the completed task in the `plan.md` file and update the `Update Date` in the YAML header.
   - **Status Update:** Mark task as `[x] Completed` or `[-] Blocked: <reason>`
   - **Timestamp:** Add completion timestamp in `YYYY-MM-DD HH:MM:SS UTC` format
   - **Artifacts:** Link to any generated artifacts (logs, outputs)

5. **Context Compaction:** Before starting the next task, flush unnecessary conversation history or use a rolling summary to reset the context window and maintain reasoning sharpness.
   - **Memory Reset:** Summarize completed task in 3 bullets max
   - **Context Purge:** Remove file contents from context that are no longer needed
   - **Next Task Prep:** Load only the Input Contract for the next task

### Phase 7: Daily Standup Report Generation (Jira Scrum Master)

**TRIGGER:** At the end of each work day OR when user requests "daily progress report" or "standup update".

**OUTPUT:** Generate a structured standup report in `agentic/plan/standup_YYYYMMDD.md` with the following sections:

```markdown
---
Date: YYYY-MM-DD
Sprint: Sprint #<N>
Plan File: agentic/plan/YYYYMMDD_<task>.md
---

# Daily Standup Report - YYYY-MM-DD

## Yesterday's Progress (Completed Tasks)

| Task ID | Task Name | Status | Time Taken | Verification |
|---------|-----------|--------|------------|--------------|
| T1 | Create JWT utility module | ✅ DONE | 8 min | pytest passed |
| T2 | Update login interface | ✅ DONE | 12 min | pytest passed |

## Today's Plan (Pending Tasks)

| Task ID | Task Name | Priority | Dependencies | Est. Time |
|---------|-----------|----------|--------------|-----------|
| T3 | Add unit tests for JWT | High | T1 | 10 min |
| T4 | Update documentation | Medium | T1, T3 | 5 min |

## Blockers

- [ ] None / Describe blocker and who can help

## Next Day Plan

- Complete Task T3: Add unit tests for JWT
  - Command: `python3 -m pytest tests/unit/test_jwt_utils.py -v`
  - Expected: All tests pass with 100% coverage
- Complete Task T4: Update README with JWT usage examples
  - Command: `grep -n "JWT" docs/README.md` to verify additions

## Metrics

- Tasks Completed: 2
- Tasks Pending: 2
- Blockers: 0
- Total Time Spent: 20 min

## Architecture Diagram (As-Built)

```mermaid
flowchart TD
    Client["Client / Agent"] -->|HTTP Request| API["API Layer (engine/api)"]
    API -->|Validation & Auth| DB["DB Layer (engine/db)"]
    DB -->|SQL/Data| Store["(Database)"]
    DB -->|Logic| Common["Common / Utils (engine/common)"]
    
    %% New Components (Completed)
    API -->|JWT Encode| JWT["jwt_utils.py [NEW] ✅"]
    JWT -->|Token| Client
    
    %% Styling
    style API fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000000
    style DB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000000
    style Store fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000000
    style Common fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000000
    style JWT fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px,color:#000000
```
```

**AUTOMATION:** After generating the standup report:
1. Archive the current day's plan to `agentic/plan/archive/`
2. Create a new plan file for the next day with remaining tasks
3. Update the main plan's `Update Date` in YAML frontmatter

## Examples

### Example Plan Structure

```markdown
---
Create Date: 2026-04-24
Update Date: 2026-04-24
IDE: Roo Code
Agent: Qwen3-7B-Architect
GitHub committer: John Doe
Sprint: Sprint #24
---

# Plan: Implement User Authentication Feature

## Objective
Implement JWT-based authentication for the user login flow.

## Constraints
- Max context per task: 128k tokens
- Max execution time per task: 10 minutes
- Max files per task: 3-5 files
- Anti-hallucination: All tasks must specify exact commands and line numbers

## Architecture Diagram

```mermaid
flowchart TD
    Client["Client / Agent"] -->|HTTP Request| API["API Layer (login/interface_login.py) [MOD]"]
    API -->|JWT Encode| JWT["utils/jwt_utils.py [NEW]"]
    JWT -->|Token| Client
    API -->|Auth Check| DB["DB Layer (db_user_mgr.py)"]
    
    %% Styling
    style API fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000000
    style JWT fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px,color:#000000
    style DB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000000
```

**Legend:**
- `[NEW]` = New file to be created
- `[MOD]` = Existing file to be modified
- Green = Completed, Yellow = Planned

## Tasks (DAG)

### Task 1: Create JWT Utility Module
- [ ] Status: Pending
- **Objective:** Create `src/utils/jwt_utils.py` with `encode_token()` and `decode_token()` functions
- **Input Contract:**
  - Read: `requirements.txt` (lines 1-20 for dependencies)
  - Read: `src/utils/__init__.py` (lines 1-15 for export pattern)
- **Output Contract:**
  - Create: `src/utils/jwt_utils.py` (~80 lines)
  - Modify: `src/utils/__init__.py` (add `jwt_utils` exports at line 5)
- **Exact Commands:**
  ```bash
  # Step 1: Create the file
  touch src/utils/jwt_utils.py
  
  # Step 2: Verify file exists
  ls -la src/utils/jwt_utils.py
  
  # Step 3: Run verification
  python3 -m pytest tests/unit/test_jwt_utils.py::test_encode_token -v
  ```
- **Expected Output:** `1 passed in 0.52s`
- **Fallback Path:** If ModuleNotFoundError, run `pip install PyJWT==2.8.0`
- **Dependencies:** None
- **Estimated Time:** 5 minutes

### Task 2: Update Login Interface
- [ ] Status: Pending
- **Objective:** Modify `src/api/login/interface_login.py` to use JWT utility
- **Input Contract:**
  - Read: `src/utils/jwt_utils.py` (lines 1-80, complete file)
  - Read: `src/api/login/interface_login.py` (lines 1-50)
- **Output Contract:**
  - Modify: `src/api/login/interface_login.py` (add import at line 5, add JWT encoding at line 35)
- **Exact Commands:**
  ```bash
  # Step 1: Verify the import was added
  grep -n "from src.utils.jwt_utils import" src/api/login/interface_login.py
  
  # Step 2: Run verification
  python3 -m pytest tests/unit/test_login.py::test_login_returns_jwt -v
  ```
- **Expected Output:** `1 passed in 0.68s`
- **Fallback Path:** If test fails, check line 35 has `token = encode_token(user_id)`
- **Dependencies:** Task 1
- **Estimated Time:** 7 minutes

### Task 3: Add Unit Tests for JWT
- [ ] Status: Pending
- **Objective:** Create comprehensive unit tests for JWT utilities
- **Input Contract:**
  - Read: `src/utils/jwt_utils.py` (lines 1-80, complete file)
  - Read: `tests/unit/test_auth.py` (lines 1-40 for test patterns)
- **Output Contract:**
  - Create: `tests/unit/test_jwt_utils.py` (~60 lines)
- **Exact Commands:**
  ```bash
  # Step 1: Create test file
  touch tests/unit/test_jwt_utils.py
  
  # Step 2: Run verification with coverage
  python3 -m pytest tests/unit/test_jwt_utils.py -v --cov=src/utils/jwt_utils --cov-report=term-missing
  ```
- **Expected Output:** `2 passed in 0.45s` with 100% coverage
- **Fallback Path:** If coverage < 100%, add test cases for missing lines shown in output
- **Dependencies:** Task 1
- **Estimated Time:** 8 minutes
```

### Example Daily Standup Report

```markdown
---
Date: 2026-04-24
Sprint: Sprint #24
Plan File: agentic/plan/20260424_jwt_auth.md
---

# Daily Standup Report - 2026-04-24

## Yesterday's Progress (Completed Tasks)

| Task ID | Task Name | Status | Time Taken | Verification |
|---------|-----------|--------|------------|--------------|
| T1 | Create JWT utility module | ✅ DONE | 8 min | pytest passed |
| T2 | Update login interface | ✅ DONE | 12 min | pytest passed |

## Today's Plan (Pending Tasks)

| Task ID | Task Name | Priority | Dependencies | Est. Time |
|---------|-----------|----------|--------------|-----------|
| T3 | Add unit tests for JWT | High | T1 | 10 min |
| T4 | Update documentation | Medium | T1, T3 | 5 min |

## Blockers

- [ ] None

## Next Day Plan

- Complete Task T3: Add unit tests for JWT
  - Command: `python3 -m pytest tests/unit/test_jwt_utils.py -v --cov=src/utils/jwt_utils`
  - Expected: `2 passed in 0.45s` with 100% coverage
- Complete Task T4: Update README with JWT usage examples
  - Command: `grep -n "JWT" docs/README.md` to verify additions at line 25-40

## Metrics

- Tasks Completed: 2
- Tasks Pending: 2
- Blockers: 0
- Total Time Spent: 20 min
- Sprint Progress: 2/10 tasks (20%)

## Architecture Diagram (As-Built)

```mermaid
flowchart TD
    Client["Client / Agent"] -->|HTTP Request| API["API Layer (login/interface_login.py) [MOD] ✅"]
    API -->|JWT Encode| JWT["utils/jwt_utils.py [NEW] ✅"]
    JWT -->|Token| Client
    API -->|Auth Check| DB["DB Layer (db_user_mgr.py)"]
    
    %% Styling
    style API fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000000
    style JWT fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px,color:#000000
    style DB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000000
```
```

## Troubleshooting

### Context Window Exhaustion
If approaching token limits:
1. Archive completed task context to `agentic/plan/archive/`
2. Use rolling summaries instead of full conversation history
3. Reduce context firewall scope to minimum required files

### Verification Failures
If a task fails verification:
1. Read the error log completely
2. Identify the root cause (not just symptoms)
3. Apply minimal fix
4. Re-run verification
5. If still failing after 2 attempts, escalate to user

### Plan Drift
If the plan becomes outdated due to changing requirements:
1. Update the `Update Date` in YAML frontmatter
2. Add a "Change Log" section documenting what changed
3. Adjust remaining tasks accordingly

## Related Files

- `agentic/plan/` - Active plans directory
- `agentic/plan/archive/` - Archived plans directory
- `agentic/functions/plan/` - Plan utility functions
