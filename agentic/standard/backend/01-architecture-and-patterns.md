# Backend Architecture & Patterns

## Layered Architecture (3-Tier)

Torro follows a strict 3-tier layered architecture to ensure separation of concerns and testability.

### 1. API Layer (engine/api)
- **Role**: Handles HTTP entry points, request validation, and response formatting.
- **Rules**:
  - Thin handlers only.
  - MUST use `Pydantic V2` for validation.
  - All logic MUST be decoupled into a `tasks/` sub-directory.
  - Dependency: Calls Task Layer.

### 2. Task Layer (engine/api/*/tasks)
- **Role**: Orchestrates business logic.
- **Rules**:
  - Framework-agnostic (no `request` or `flask` objects).
  - If a task exceeds 200 lines, it MUST be split (Principle 1).
  - Dependency: Calls DB Layer.

### 3. DB Layer (engine/db)
- **Role**: Data persistence and retrieval.
- **Rules**:
  - Use `SQLModel` exclusively.
  - CRUD operations in `utils/`.
  - Dependency: Calls Common/Utils.

## Dependency Direction
API -> Task -> DB -> Common/Utils. **DB should NEVER import API.**

```mermaid
graph TD
    Client["Client / Agent"] -->|HTTP Request| API["API Layer (engine/api)"]
    API -->|Validation & Auth| DB["DB Layer (engine/db)"]
    DB -->|SQL/Data| Store[(Database)]
    DB -->|Logic| Common["Common / Utils (engine/common)"]
    
    %% Forbidden Paths
    DB -.->|❌ Forbidden| API
    
    style API fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000000
    style DB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000000
    style Store fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000000
    style Common fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000000
```
