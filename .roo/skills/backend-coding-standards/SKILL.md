---
name: backend-coding-standards
description: Define core coding standards, agentic best practices, naming conventions, and structural rules for the Torro backend ecosystem
---

# Backend Coding Standards & Best Practices Skill

This skill defines the core coding standards, agentic best practices, and structural rules for the Torro backend ecosystem.

## When to use
- When writing new Python code for the Torro backend
- When refactoring existing code to improve readability and agent-friendliness
- When reviewing code for compliance with Torro standards
- When setting up new modules or packages

## When NOT to use
- For architecture/layering guidance (use `backend-architecture` skill instead)
- For testing-specific guidance (use `backend-testing` skill instead)
- For security/dependency management (use `backend-operations` skill instead)

## Inputs required
- Target file/module to create or modify
- Domain/entity being implemented

## Workflow

### 1. Radical Simplicity & Human Readability
Code must be aesthetically pleasing, logically fluid, and intentionally designed for both human and agent comprehension.

- **Intentional Logic:** Prioritize clear, linear logic. Refactor non-trivial blocks into smaller, named functions.
- **Literate Programming:** Every module, class, and function must include a descriptive docstring.
- **The "Why" Rule:** Comments must explain *why* a specific approach was taken, not *what* the code is doing.
- **Refactoring Rule:** If a `.py` file exceeds **200 lines**, it MUST be refactored into smaller, modular tasks and saved in a sub-`tasks/` folder within the same directory. The main file acts as an orchestrator.

### 2. Naming Conventions & Type Safety
Strict adherence to naming conventions and strong typing ensures clear interfaces for AI agents to analyze.

**Naming Rules:**
- **Classes:** `PascalCase` (e.g., `UserSubscriptionManager`).
- **Functions/Methods:** `snake_case` (e.g., `get_user_profile`).
- **Variables:** `snake_case`, verbose and descriptive (e.g., `is_active`, `user_id_list`).
- **Constants:** `UPPER_CASE` (e.g., `MAX_RETRY_COUNT`).
- **Files (Python):** `snake_case`.
  - DB managers MUST start with `db_` and end with `_mgr.py` (e.g., `db_user_mgr.py`).
  - API interfaces MUST start with `interface_` (e.g., `interface_user.py`).

**Type Safety:** Use strong typing (Type Hints in Python) to provide clear interfaces.

### 3. Agentic Documentation & Headers (MANDATORY)
Documentation is critical for agentic RAG (Retrieval-Augmented Generation) and codebase navigation.

- **`__init__.py` RAG Anchors:** Every package `__init__.py` MUST start with a structured docstring containing:
  - `FN:__init__.py`
  - `Package:` full package path
  - `Summary:` 1-2 sentence purpose
  - `Structure:` simple bullet list of files/folders
  - `Entry Points:` primary modules/classes to open first
  - `Flow:` one-line mapping of UI → API → DB or relevant path
  - `Read First:` ordered list of the most important files

- **Agentic Function Header:** All Python files MUST include a standardized header at the top containing:
  - File name/main function
  - Description (classes/purpose)
  - `Class.function` breakdown with line numbers

- **The FN: Tag:** Every method docstring **MUST** begin with `FN:method_name` (e.g., `"""FN:get_user Description..."""`). This allows agents to assume a "Headless" mode for scanning.

- **Documentation Mandate:** Every top-level folder and significant subsystem folder MUST include a concise `README.md` explaining: Purpose, Structure, Usage, and Dependencies.

### 4. Agentic Class Method Principle (Token Minimization)
Encapsulate logic to minimize token usage and improve agentic understanding.

- **Class-Based Encapsulation:** Standalone scripts and top-level functions are prohibited (except for `main.py` entry points and `__init__.py`). Logic MUST be encapsulated within descriptive Classes (e.g., `AssetIngestionTask`).
- **Method-Driven Execution:** All business logic MUST be contained within methods, not the global scope.

### 5. Resiliency & Task Planning
Ensure robust execution and systematic refactoring processes.

- **Pre-Refactor Marker:** BEFORE modifying code logic, agents MUST inject a `TODO` comment at the top of the target file: `# TODO: [Refactor] <Description> (Step ID: <CurrentStep>)`. Remove only after verification.
- **Mandatory Agentic Task Planning Protocol:** All agentic logs, task definitions, and markdown reports MUST be stored in the `agentic/tasks/` directory in `.md` format (e.g., `YYYYMMDD_HHMMSS_<tasks>.md`).
- **Idempotency:** Design data-modifying functions to be idempotent, allowing agents to safely retry actions without side effects.
- **Explicit Error Handling:** Avoid generic "catch-all" error blocks. Use specific exception handling to allow agents to diagnose and self-correct based on error types.

### 6. Agent Stability & Circuit Breakers
Maintain operational stability during agentic execution.

- **Emotional Stability:** Agents MUST maintain a constant, professional, and objective tone. Do not apologize excessively or simulate human distress.
- **Recursion Circuit Breaker:** If code or thought patterns repeat > 3 times without progress, **STOP immediately**. Request user intervention.
- **Flood Protection:** If output generation becomes repetitive or garbled, the agent MUST terminate the process and fail gracefully.

## Examples

**Agentic Function Header Format:**
```python
"""
FN:db_user_mgr.py
Database manager for user-related operations.

Classes:
- UserDatabaseManager: Handles user data persistence and retrieval
- UserValidator: Validates user data before database operations

Functions:
- FN:create_user: Creates a new user in the database (lines 45-78)
- FN:get_user_by_id: Retrieves user by ID (lines 80-95)
- FN:update_user: Updates user information (lines 97-120)
"""
```

**Agentic Class Method Pattern:**
```python
class AssetIngestionTask:
    """Task for ingesting assets from external sources."""

    def __init__(self, config: dict):
        """FN:__init__ Initialize the task with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)

    def execute(self) -> bool:
        """FN:execute Execute the asset ingestion task."""
        self.logger.info("FN:execute Starting asset ingestion...")
        # Implementation here
        return True
```

**Agentic `__init__.py` RAG Anchor:**
```python
"""
FN:__init__.py
Package: engine/api/user

Summary: User management APIs and interfaces.

Structure:
- interface_user_login.py
- interface_user_profile.py
- tasks/

Entry Points:
- interface_user_login.UserApi (main routes)
- interface_user_profile.UserProfileApi (profile routes)

Flow:
- UI -> engine/api/user/interface_*.py -> engine/db/user/db_user_mgr.py -> DB

Read First:
- interface_user_login.py
- engine/db/user/db_user_mgr.py
"""
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| File exceeds 200 lines | Refactor into `tasks/` subfolder; main file becomes orchestrator |
| Missing `FN:` tag in docstring | Add `FN:method_name` prefix to all method docstrings |
| Standalone functions at module level | Wrap in a descriptive class |
| Comments describe "what" not "why" | Rewrite comments to explain reasoning and business context |
| Missing agentic function header | Add standardized header listing classes and functions with line numbers |
