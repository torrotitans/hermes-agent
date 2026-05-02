# Mermaid Diagram Examples - Torro Brand

## Table of Contents

1. [Flowcharts](#flowcharts)
2. [Sequence Diagrams](#sequence-diagrams)
3. [Class Diagrams](#class-diagrams)
4. [ER Diagrams](#er-diagrams)
5. [State Diagrams](#state-diagrams)
6. [Gantt Charts](#gantt-charts)
7. [Pie Charts](#pie-charts)
8. [Quadrant Charts](#quadrant-charts)
9. [Requirement Diagrams](#requirement-diagrams)
10. [Architecture Diagrams](#architecture-diagrams)

---

## Flowcharts

### Example 1: API Authentication Flow

```mermaid
graph TD
    classDef primary fill:#8fa0f5,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef secondary fill:#f9bc60,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef error fill:#e16162,stroke:#5c6bb5,stroke-width:2px,color:#ffffff
    classDef success fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#ffffff
    
    Start([Start]):::primary --> Login[Login Page]:::primary
    Login --> Validate{Validate Credentials}:::secondary
    Validate -->|Valid| Auth[Generate JWT Token]:::primary
    Validate -->|Invalid| Error[Authentication Failed]:::error
    Error --> Login
    Auth --> Session[Create Session]:::success
    Session --> End([End]):::primary
```

### Example 2: Data Pipeline Flow

```mermaid
flowchart LR
    classDef source fill:#8fa0f5,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef process fill:#f9bc60,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef storage fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#ffffff
    
    subgraph Ingestion[Data Ingestion]
        A[API Source]:::source --> B[Validation]:::process
        B --> C[Transformation]:::process
    end
    
    subgraph Storage[Data Storage]
        C --> D[(PostgreSQL)]:::storage
        C --> E[(Redis Cache)]:::storage
    end
    
    subgraph Consumption[Data Consumption]
        D --> F[Analytics Dashboard]:::source
        E --> F
    end
```

### Example 3: User Journey Map

```mermaid
graph TD
    classDef awareness fill:#8fa0f5,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef consideration fill:#f9bc60,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef decision fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#ffffff
    classDef retention fill:#2196f3,stroke:#1976d2,stroke-width:2px,color:#ffffff
    
    A[Discover Product]:::awareness --> B[Visit Website]:::awareness
    B --> C[Read Documentation]:::consideration
    C --> D[Try Demo]:::consideration
    D --> E{Purchase Decision}:::consideration
    E -->|Yes| F[Complete Purchase]:::decision
    E -->|No| B
    F --> G[Onboarding]:::retention
    G --> H[Regular Usage]:::retention
```

---

## Sequence Diagrams

### Example 1: LDAP Authentication Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as UI Component
    participant API as API Layer
    participant LDAP as LDAP Service
    participant DB as Database
    
    rect rgb(143, 160, 245, 0.1)
        Note over User,DB: Authentication Sequence
        User->>UI: Enter credentials
        UI->>API: POST /api/login
        API->>LDAP: Bind request
        LDAP-->>API: Bind response
        alt Valid credentials
            API->>DB: Create session
            DB-->>API: Session ID
            API-->>UI: JWT token
            UI-->>User: Redirect to dashboard
        else Invalid credentials
            API-->>UI: 401 Unauthorized
            UI-->>User: Show error
        end
    end
```

### Example 2: Data Ingestion Pipeline

```mermaid
sequenceDiagram
    participant Source as Data Source
    participant Ingest as Ingestion Service
    participant Transform as Transform Service
    participant Store as Storage Layer
    
    Source->>Ingest: Raw data payload
    Ingest->>Ingest: Validate schema
    Ingest->>Transform: Send for transformation
    Transform->>Transform: Apply business rules
    Transform-->>Ingest: Transformed data
    Ingest->>Store: Persist to database
    Store-->>Ingest: Confirmation
    Ingest-->>Source: Acknowledgment
```

---

## Class Diagrams

### Example 1: User Management Domain

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String fullName
        +Boolean isActive
        +login()
        +logout()
    }
    
    class Session {
        +String token
        +Date expiresAt
        +User user
        +validate()
        +invalidate()
    }
    
    class Role {
        +String name
        +String[] permissions
        +hasPermission()
    }
    
    User "1" --> "0..*" Session : creates
    User "1" --> "1..*" Role : assigned
    Session "1" --> "1" User : references
```

### Example 2: Workspace Management

```mermaid
classDiagram
    class Workspace {
        +String id
        +String name
        +String description
        +Date createdAt
        +addMember()
        +removeMember()
    }
    
    class WorkspaceMember {
        +String userId
        +String role
        +Date joinedAt
        +updateRole()
    }
    
    class WorkspaceConfig {
        +String theme
        +String language
        +Boolean notifications
        +updateSettings()
    }
    
    Workspace "1" --> "0..*" WorkspaceMember : contains
    Workspace "1" --> "1" WorkspaceConfig : configures
```

---

## ER Diagrams

### Example 1: User and Workspace Schema

```mermaid
erDiagram
    USER ||--o{ SESSION : creates
    USER ||--o{ WORKSPACE_MEMBER : joins
    WORKSPACE ||--o{ WORKSPACE_MEMBER : contains
    WORKSPACE ||--|| WORKSPACE_CONFIG : configures
    
    USER {
        string id PK
        string email
        string full_name
        boolean is_active
        datetime created_at
    }
    
    SESSION {
        string id PK
        string user_id FK
        string token
        datetime expires_at
    }
    
    WORKSPACE {
        string id PK
        string name
        string description
        datetime created_at
    }
    
    WORKSPACE_MEMBER {
        string user_id FK
        string workspace_id FK
        string role
        datetime joined_at
    }
    
    WORKSPACE_CONFIG {
        string workspace_id FK
        string theme
        string language
    }
```

---

## State Diagrams

### Example 1: Document Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft : Create
    Draft --> Review : Submit for review
    Review --> Draft : Request changes
    Review --> Approved : Approve
    Approved --> Published : Publish
    Published --> Archived : Archive
    Archived --> [*]
    
    state Draft {
        [*] --> Editing
        Editing --> Pending : Save
    }
    
    state Review {
        [*] --> UnderReview
        UnderReview --> Reviewed : Complete
    }
```

### Example 2: Order Processing State Machine

```mermaid
stateDiagram-v2
    [*] --> Created : Place order
    Created --> Paid : Payment confirmed
    Paid --> Processing : Start processing
    Processing --> Shipped : Ship order
    Shipped --> Delivered : Delivery confirmed
    Delivered --> [*] : Complete
    
    state Processing {
        [*] --> Validating
        Validating --> Preparing
        Preparing --> Ready
    }
    
    Paid --> Cancelled : Cancel request
    Processing --> Cancelled
    Shipped --> Returned : Return request
```

---

## Gantt Charts

### Example 1: Project Timeline

```mermaid
gantt
    title Torro Platform Development Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Requirements Analysis     :a1, 2024-01-01, 14d
    Architecture Design       :a2, after a1, 10d
    section Development
    Backend API Development   :b1, 2024-01-25, 21d
    Frontend UI Development   :b2, 2024-01-25, 21d
    Integration Testing       :b3, after b1, 7d
    section Deployment
    UAT Environment Setup     :c1, after b3, 5d
    Production Deployment     :c2, after c1, 3d
```

### Example 2: Sprint Planning

```mermaid
gantt
    title Sprint 1 - Authentication Module
    dateFormat  YYYY-MM-DD
    section Sprint 1
    Sprint Planning           :done, 2024-02-01, 1d
    User Story Development    :active, 2024-02-02, 5d
    Code Review               :2024-02-07, 2d
    Testing                   :2024-02-09, 3d
    Sprint Review             :2024-02-12, 1d
```

---

## Pie Charts

### Example 1: User Role Distribution

```mermaid
pie title User Roles Distribution
    "Admin" : 15
    "Manager" : 25
    "Contributor" : 40
    "Viewer" : 20
```

### Example 2: Project Status Overview

```mermaid
pie title Project Status Overview
    "Completed" : 45
    "In Progress" : 30
    "On Hold" : 15
    "Cancelled" : 10
```

---

## Quadrant Charts

### Example 1: Feature Priority Matrix

```mermaid
quadrantChart
    title Feature Priority Matrix
    x-axis Low Impact --> High Impact
    y-axis Low Effort --> High Effort
    quadrant-1 Quick Wins
    quadrant-2 Major Projects
    quadrant-3 Fill-ins
    quadrant-4 Time Wasters
    "Feature A": [0.8, 0.3]
    "Feature B": [0.6, 0.7]
    "Feature C": [0.3, 0.4]
    "Feature D": [0.2, 0.8]
```

---

## Requirement Diagrams

### Example 1: Authentication Requirements

```mermaid
requirementDiagram
    requirement AuthRequirement {
        id: AUTH-001
        text: "System shall support LDAP authentication"
        risk: High
        verifymethod: Test
    }
    
    requirement SessionRequirement {
        id: AUTH-002
        text: "System shall implement JWT-based sessions"
        risk: Medium
        verifymethod: Inspection
    }
    
    functionalRequirement TokenRequirement {
        id: AUTH-003
        text: "Tokens shall expire after 24 hours"
        risk: Low
        verifymethod: Test
    }
    
    AuthRequirement - contains -> TokenRequirement
    SessionRequirement - contains -> TokenRequirement
```

---

## Architecture Diagrams

### Example 1: Torro Platform Architecture

```mermaid
flowchart TB
    subgraph Client[Client Layer]
        A[Web Browser]
        B[Mobile App]
    end
    
    subgraph Gateway[API Gateway]
        C[Load Balancer]
        D[Rate Limiter]
    end
    
    subgraph Services[Application Services]
        E[Auth Service]
        F[User Service]
        G[Workspace Service]
        H[Data Service]
    end
    
    subgraph Data[Data Layer]
        I[(PostgreSQL)]
        J[(Redis)]
        K[(Elasticsearch)]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    E --> I
    F --> I
    G --> I
    H --> J
    H --> K
```

### Example 2: Microservices Topology

```mermaid
flowchart LR
    subgraph Core[Core Services]
        A[User Service]
        B[Auth Service]
        C[Config Service]
    end
    
    subgraph Domain[Domain Services]
        D[Workspace Service]
        E[Data Service]
        F[Analytics Service]
    end
    
    subgraph Infra[Infrastructure]
        G[Message Queue]
        H[Cache Layer]
        I[Search Engine]
    end
    
    A --> G
    B --> G
    D --> G
    E --> G
    F --> G
    A --> H
    E --> H
    F --> I
```

---

## Color Reference

### Torro Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | `#8fa0f5` | Main nodes, active states |
| Secondary | `#f9bc60` | Secondary nodes, highlights |
| Accent | `#e16162` | Error states, warnings |
| Success | `#4caf50` | Success states, completion |
| Info | `#2196f3` | Information, tips |
| Text Dark | `#001e1d` | Primary text |
| Text Light | `#ffffff` | Text on dark backgrounds |

### Class Definitions

```mermaid
graph TD
    classDef primary fill:#8fa0f5,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef secondary fill:#f9bc60,stroke:#5c6bb5,stroke-width:2px,color:#001e1d
    classDef accent fill:#e16162,stroke:#5c6bb5,stroke-width:2px,color:#ffffff
    classDef success fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#ffffff
    classDef info fill:#2196f3,stroke:#1976d2,stroke-width:2px,color:#ffffff
```
