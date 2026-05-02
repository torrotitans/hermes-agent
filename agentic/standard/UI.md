# Torro UI Engineering Standards (Harness Methodology)

<agent_instructions>
You are an AI coding assistant specialized in building high-end enterprise UI for the Torro platform.
Before writing any UI code, you MUST consult the modular standards and the **[UI Mistake Registry](./mistakes/ui-mistakes.md)**.
</agent_instructions>

<ui_invariants>
- **Aesthetic**: Apple Liquid Glass (backdrop-blur-xl, bg-white/80, border-black/5).
- **Typography**: Inter (UI), Outfit (Headers).
- **Layout**: Feature-Sliced Design (FSD) strict boundaries.
- **State**: Lazy initialization for localStorage. No set-state-in-effect.
- **Forms**: react-hook-form + Zod (Strict Schema).
- **API**: All API calls use `/api/` prefix. `/api/v1/` is deprecated and removed.
- **Authentication**: NextAuth.js v5 (Mandatory). Credentials provider for LDAP integration.
- **Session Data**: Server-side injection via `auth()` into client components. No client-side API fetch for session.
</ui_invariants>

## 📚 Standard Modules

1.  **[01. Brand & Aesthetic](./ui/01-brand-and-aesthetic.md)**: Logo, Typography, Color Palettes, and "Apple Liquid Glass" pillars.
2.  **[02. Design System Tokens](./ui/02-design-system-tokens.md)**: Centralized design tokens, spacing scales, and responsive grid standards.
3.  **[03. Architecture & Patterns](./ui/03-architecture-and-patterns.md)**: FSD boundaries, Next.js patterns, and platform resilience.
4.  **[04. Component Library](./ui/04-component-library.md)**: "Golden Path" implementation for cards, tables, search, and auth.
5.  **[05. Development Workflow](./ui/05-development-workflow.md)**: Code governance, NPM protocols, and the Master Definition of Done (DoD).

---

## 📚 Standard Modules (Continued)

12. **[12. Notification Popover](./ui/12-notification-popover.md)**: Mandatory styling for the notification dropdown, including layout rules, liquid glass footer, and scrollable notification list.

---

## 🏗️ FSD Architecture Structure (Updated 2026-04-27)

All new UI services MUST follow this Feature-Sliced Design structure:

### Directory Layout

```
UI/
├── app/                          # Route Layer (URL-organized)
│   ├── (auth)/                   # Unauthenticated routes → /login, /org-setting
│   │   ├── login/page.tsx
│   │   └── org-setting/page.tsx
│   ├── (secure)/                 # Authenticated routes → /dashboard, /admin, etc.
│   │   ├── layout.tsx            # Auth guard + AppShell wrapper
│   │   ├── dashboard/page.tsx    # → imports from widgets/dashboard
│   │   ├── governance/page.tsx   # → imports from widgets/governance
│   │   └── ...
│   └── api/                      # API route handlers → /api/auth/login, etc.
│       ├── auth/login/route.ts
│       ├── discovery/assets/route.ts
│       └── ...
├── src/                          # Source Layer (Concern-organized, FSD)
│   ├── features/                 # Business capabilities (self-contained)
│   │   ├── auth/                 # → ui/, model/, index.ts
│   │   ├── dashboard/            # → ui/, model/, index.ts
│   │   ├── discovery/            # → ui/, model/, api/, lib/
│   │   ├── governance/           # → ui/, model/, api/, lib/
│   │   ├── forms/                # → ui/, model/, api/
│   │   ├── workspace/            # → ui/, model/, api/
│   │   ├── workflow/             # → ui/, model/, api/
│   │   └── session/              # → ui/, model/
│   ├── entities/                 # Domain models (shared types)
│   │   ├── asset/                # → model/types.ts, model/index.ts, index.ts
│   │   ├── user/                 # → model/types.ts, model/index.ts, index.ts
│   │   ├── workspace/            # → model/types.ts, model/index.ts, index.ts
│   │   ├── form/                 # → model/types.ts, model/index.ts, index.ts
│   │   ├── policy/               # → model/types.ts, model/index.ts, index.ts
│   │   ├── tag/                  # → model/types.ts, model/index.ts, index.ts
│   │   ├── connector/            # → model/types.ts, model/index.ts, index.ts
│   │   ├── workflow/             # → model/types.ts, model/index.ts, index.ts
│   │   └── request/              # → model/types.ts, model/index.ts, index.ts
│   ├── widgets/                  # Page sections (aggregate features)
│   │   ├── dashboard/            # → dashboard-panel.tsx, index.ts
│   │   ├── discovery/            # → discovery-panel.tsx, index.ts
│   │   ├── governance/           # → governance-panel.tsx, index.ts
│   │   ├── workflow/             # → workflow-panel.tsx, index.ts
│   │   └── workspace/            # → workspace-panel.tsx, index.ts
│   ├── components/               # Reusable UI primitives
│   │   ├── FormDesign/
│   │   ├── WorkspaceForm/
│   │   └── ...
│   └── shared/                   # Cross-cutting utilities
│       ├── api/                  # API clients, auth utilities
│       ├── ui/                   # Primitives (Button, Card, Modal)
│       ├── layout/               # AppShell, ErrorBoundary
│       ├── config/               # navigation.json, etc.
│       ├── i18n/                 # Translation keys
│       └── lib/                  # Pure utilities (cn.ts, validation/)
└── test/                         # Test files
    ├── __shared__/               # Unit tests for entities, icons, etc.
    ├── e2e/                      # Playwright E2E tests
    └── integration/              # API route integration tests
```

### Decision Rules for New Code

| Code Type | Criteria | Destination |
|-----------|----------|-------------|
| **Route page** | Defines a URL path, composes widgets/features | `app/(auth)/` or `app/(secure)/` |
| **Route layout** | Wraps routes with shared shell, auth guard, session injection | `app/(secure)/layout.tsx` |
| **API endpoint** | Handles HTTP requests, returns JSON | `app/api/<domain>/route.ts` |
| **Feature UI** | Tied to a specific business domain | `src/features/<domain>/ui/` |
| **Feature model** | Business logic, schemas, types for a domain | `src/features/<domain>/model/` |
| **Feature API hooks** | React hooks/queries for a domain | `src/features/<domain>/api/` |
| **Entity type** | Core domain data structure used across features | `src/entities/<domain>/model/` |
| **Widget** | Composed page section aggregating multiple features | `src/widgets/<domain>/` |
| **Component** | Reusable UI element, no business logic | `src/components/<name>/` |
| **Shared UI** | Primitive UI elements (buttons, inputs, cards) | `src/shared/ui/` |
| **Shared API** | API clients, auth utilities, constants | `src/shared/api/` |

### Server Component Session Injection Rule

All authenticated route layouts (`app/(secure)/layout.tsx`) MUST fetch session data server-side and inject it into client components:

```tsx
// In app/(secure)/layout.tsx (Server Component)
import { auth } from '@/auth';

export default async function SecureLayout({ children }) {
  const session = await auth();
  const initialSession = transformSession(session);
  
  return (
    <AppShell sessionBar={<SessionBar initialSession={initialSession} />}>
      {children}
    </AppShell>
  );
}
```

This rule eliminates loading state flash in client components that depend on session data. Client components receiving session data MUST accept an `initialSession` prop and pass it to React Query as `initialData`.

### Feature Structure Standard

Every feature MUST have this structure:
```
features/<domain>/
├── index.ts          # Barrel exports
├── model/            # Domain types and schemas
│   ├── index.ts      # Re-exports from entities/<domain>
│   └── types.ts      # (Optional) Feature-specific types
├── ui/               # React components
│   ├── <component>.tsx
│   └── index.ts
├── api/              # API hooks and queries (if applicable)
│   ├── index.ts
│   └── <service>.ts
└── lib/              # Business logic utilities (optional)
    └── helpers.ts
```

### API Convention

- **All API calls use `/api/` prefix** — `/api/v1/` is deprecated and removed
- Frontend code MUST call `/api/auth/login`, `/api/discovery/assets`, etc.
- Backend proxy routes in `app/api/` forward to Flask backend at `http://127.0.0.1:3128/api/`

---

*Last Updated: 2026-04-29*
*Version: 11.0 (FSD Compliant + Server-Side Session Injection + Notification Popover Standard)*
