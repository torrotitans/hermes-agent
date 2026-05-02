# Mermaid Syntax Reference

Complete syntax guide for all Mermaid diagram types.

## Table of Contents

- [Flowchart](#flowchart)
- [Sequence Diagram](#sequence-diagram)
- [Class Diagram](#class-diagram)
- [State Diagram](#state-diagram)
- [ER Diagram](#er-diagram)
- [Gantt Chart](#gantt-chart)
- [Pie Chart](#pie-chart)
- [Git Graph](#git-graph)
- [User Journey](#user-journey)
- [Mindmap](#mindmap)
- [Quadrant Chart](#quadrant-chart)
- [Timeline](#timeline)
- [Block Diagram](#block-diagram)
- [General Syntax Rules](#general-syntax-rules)

---

## Flowchart

### Syntax

```mermaid
flowchart TD
    A["Start"] --> B{"Decision"}
    B -->|Yes| C["Path A"]
    B -->|No| D["Path B"]
    C --> E["End"]
    D --> E
```

### Node types

| Syntax | Type |
|--------|------|
| `A["Label"]` | Rectangle (default) |
| `A{{"Label"}}` | Stadium/rounded |
| `A[["Label"]]` | Subroutine |
| `A[("Label")]` | Circle |
| `A[/"Label"/]` | Parallelogram |
| `A[(Label)]` | Database/cylinder |
| `A{{{"Label"}}}` | Hexagon |
| `A[("Label")]` | Diamond (decision) |

### Directions

- `TD` — Top to bottom
- `BT` — Bottom to top
- `LR` — Left to right
- `RL` — Right to left

### Links

| Syntax | Type |
|--------|------|
| `-->` | Solid line |
| `-.-` | Dashed line |
| `==>` | Thick line |
| `~~>` | Wavy line |
| `---` | No arrow |

### Styling

```mermaid
flowchart TD
    A["Start"] --> B["Process"]
    classDef success fill:#d4edda,stroke:#28a745
    classDef error fill:#f8d7da,stroke:#dc3545
    class A success
    class B error
```

### Subgraphs

```mermaid
flowchart TD
    subgraph Frontend
        A["UI"] --> B["API Client"]
    end
    subgraph Backend
        C["Auth"] --> D["Data"]
    end
    B --> C
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant D as Database

    U->>S: POST /login
    S->>D: SELECT * FROM users
    D-->>S: user record
    S-->>U: 200 OK + JWT
```

### Arrow types

| Syntax | Type |
|--------|------|
| `->>` | Solid arrow |
| `->` | Dashed arrow |
| `>>` | Solid (no tail) |
| `-->>` | Solid return |
| `--` | Dashed return |

### Notes and activations

```mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: Request
    activate B
    B-->>A: Response
    deactivate B
    Note over A,B: Important note
```

---

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +eat() void
        +sleep() void
    }
    class Dog {
        +String breed
        +bark() void
    }
    Animal <|-- Dog
```

### Relationships

| Syntax | Type |
|--------|------|
| `<|--` | Inheritance |
| *-- | Composition |
| o-- | Aggregation |
| ..> | Dependency |
| <-> | Association |

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : Start
    Processing --> Success : Done
    Processing --> Error : Fail
    Success --> [*]
    Error --> Idle : Retry
```

---

## ER Diagram

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ "LINE ITEM" : contains
    PRODUCT ||--o{ "LINE ITEM" : includes
    CUSTOMER {
        int id
        string name
        string email
    }
    ORDER {
        int id
        date created_at
        string status
    }
```

---

## Gantt Chart

```mermaid
gantt
    title Project Schedule
    dateFormat  YYYY-MM-DD
    section Planning
    Requirements    :a1, 2026-05-01, 14d
    Design          :a2, after a1, 10d
    section Development
    Backend         :b1, after a2, 20d
    Frontend        :b2, after a2, 20d
    section Testing
    QA              :c1, after b1, 10d
```

### Sections

- `section <name>` — Group tasks
- `dateFormat` — Date format (YYYY-MM-DD)
- `excludes` — Exclude weekends: `excludes weekends`

---

## Pie Chart

```mermaid
pie showData
    title Budget Distribution
    "Engineering" : 45
    "Marketing" : 25
    "Operations" : 20
    "Legal" : 10
```

---

## Git Graph

```mermaid
gitGraph
    commit id: "Initial"
    branch feature
    checkout feature
    commit id: "Add feature"
    checkout main
    merge feature
    commit id: "Update docs"
```

---

## User Journey

```mermaid
journey
    title Onboarding Flow
    section Sign Up
      Visit page: 5: User
      Create account: 4: User
    section Setup
      Verify email: 3: User
      Complete profile: 4: User
    section First Use
      Explore dashboard: 5: User
      Create first project: 3: User
```

---

## Mindmap

```mermaid
mindmap
    root((Project))
        Planning
            Requirements
            Design
            Timeline
        Development
            Backend
            Frontend
            Testing
        Deployment
            Staging
            Production
```

---

## Quadrant Chart

```mermaid
quadrantChart
    title Development Maturity
    x-axis Low Impact --> High Impact
    y-axis Low Maturity --> High Maturity
    "Quick Wins": [0.7, 0.3]
    "Major Projects": [0.8, 0.7]
    "Fill-ins": [0.3, 0.3]
    "Thankless Tasks": [0.4, 0.8]
```

---

## Timeline

```mermaid
timeline
    title Project History
    2024-01 : Kickoff
              : Team assembly
    2024-03 : Alpha release
    2024-06 : Beta release
    2024-09 : Production launch
```

---

## Block Diagram

```mermaid
block
    columns 3
    A["Database"] B["Cache"] C["API"]
    A --> B
    B --> C
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#ff9,stroke:#333
```

---

## General Syntax Rules

1. **Node labels with special characters** must be quoted: `A["Label (with parens)"]`
2. **Spaces in IDs** require quotes: `A["My Node"]`
3. **Comments**: `%% This is a comment`
4. **Theme**: `%%{init: {'theme': 'dark'}}%%` at the top
5. **Direction**: `flowchart TD` or `graph TD` (graph is legacy, flowchart is preferred)
6. **Styling**: Use `classDef` + `class` for consistent styling
7. **Links with labels**: `A -->|label| B`
