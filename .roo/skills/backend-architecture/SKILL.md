---
name: backend-architecture
description: Define and enforce layered backend architecture with SQLModel foundation, standardized folder structure, and configuration patterns for the Torro Python/Flask ecosystem
---

# Backend Architecture & Design Skill

This skill defines the core architectural principles for the Torro backend ecosystem, focusing on a robust, scalable, and agent-friendly Python/Flask/SQLModel foundation.

## When to use
- When creating new backend API endpoints or database models
- When refactoring existing code to align with Torro standards
- When reviewing code for architectural compliance
- When setting up new domain modules

## When NOT to use
- For frontend/Next.js development (use `nextjs-agentic` skill instead)
- For testing-specific guidance (use `backend-testing` skill instead)
- For security/dependency management (use `backend-operations` skill instead)

## Inputs required
- Target domain/module name
- Entity types to model (if creating new models)

## Workflow

### 1. Layered Architecture & Structural Consistency
Maintain strict separation of concerns to ensure UI, business logic, and data access layers remain decoupled.

**Standardized Folder Structure:**
- `engine/api`: Public-facing interfaces (Controllers/Routers). Handles HTTP requests, validation, and response formatting. Should NOT contain complex business logic.
- `engine/db`: Data access managers, repositories, and SQLModel definitions. Implements business logic related to data persistence.
- `engine/common`: Shared domain primitives, schemas, and enums.
- `engine/utils`: Pure utility functions (stateless).

**Dependency Direction:** `API -> DB -> Common/Utils`. **DB should NEVER import API.**

**Obsessive Structural Integrity:** Folder structures and file naming must rigidly follow established patterns. Deviations (e.g., casing, pluralization) are critical defects.

### 2. SQLModel Enterprise Foundation (MANDATORY)
SQLModel is the **EXCLUSIVE** standard for all database interactions. Zero tolerance for deviation.

**Required Project Layout:**
- `engine/db/models/<entity>.py`: Centralized SQLModel 3-tier models (Base/Create/Table/Public).
- `engine/db/utils/db_crud.py`: Centralized DB utilities and CRUD operations.
- `engine/db/<domain>/db_<domain>_mgr.py`: Domain-specific DB manager (orchestrator).

**CRUD Layer Rules:**
- **Session First:** Every CRUD function MUST have `session: Session` as the FIRST parameter.
- **Use `select()`:** Always use `session.exec(select(Model))`. Deprecated `session.query()` and raw SQL (`session.execute(text(...))`) are **STRICTLY FORBIDDEN**.
- **Use `model_validate()`:** Convert request schemas to table instances with `model_validate()`.
- **No Business Logic:** CRUD functions handle ONLY database operations.

**API Layer Rules (Thin Handlers):**
- For Flask API endpoint implementation details, use the `flask-api` skill.
- **Session Injection:** Every endpoint MUST use dependency injection (e.g., `Depends(get_session)`).
- **Call DB Manager:** Endpoints MUST call their `<domain>` DB Manager. Endpoints MUST NOT contain inline DB logic.
- **Return Public:** Always return `Public` schemas, NOT table models.

### 3. Agentic Module Design
Modules must be designed for GenAI readiness and deterministic execution.

- **Self-Contained Modules:** Every major functional directory (`engine`, `agentic`, `services`, `tests`) MUST be treated as a micro-application.
- **Unified Entry Point:** Executable modules MUST possess a `main.py` that serves as the CLI/Service entry point (e.g., `engine/main.py`, `tests/main.py`).
- **Deterministic Interfaces:** Functions MUST have explicit input types and return structured data. Avoid `*args` and `**kwargs` for core business logic.
- **Schema-Driven Validation:** Every API request MUST be validated against a strict schema (e.g., Pydantic/SQLModel) before processing.
- **Clear Failure Modes:** Return standardized error codes and verbose, actionable diagnostic messages.

### 4. Configuration Externalization
Ensure a zero-secret codebase and dynamic configuration management.

- **Zero-Secret Codebase:** No credentials, API keys, or platform-specific property IDs may exist in Python files.
- **The INI Standard:** Use a centralized `config.ini` as the master registry for all environment-specific settings.
- **Single Source of Truth:** The `config.py` module serves as the exclusive broker between the raw `config.ini` and the application logic. Code MUST NEVER read the INI file directly outside of this module.
- **Flask Native Integration:** Always use `app.config.from_object(config[config_name])` to inject settings into the Flask context.
- **Default Resilience:** Implement robust fallbacks to permit "graceful degradation" if specific INI sections are missing.

## Examples

**Correct CRUD Pattern:**
```python
from sqlmodel import select, Session
from engine.db.models.<entity> import <Entity>, <Entity>Create

def create_<entity>(session: Session, payload: <Entity>Create) -> <Entity>:
    """FN:create_<entity> Create a new entity in the database."""
    obj = <Entity>.model_validate(payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Raw SQL found in codebase | Refactor to SQLModel `select()` pattern immediately |
| DB layer imports API | Remove import; move logic to DB manager or common layer |
| Session not first parameter | Reorder function signature; session must be first |
| Missing `Public` schema return | Add `Public` schema class; return it instead of table model |
| Need to create Flask API endpoint | Use `flask-api` skill for endpoint implementation |
