# Torro UI Standards: 05. Development Workflow

<agent_instructions>
- Follow this workflow before committing any UI code.
- Ensure all "Definition of Done" items are checked.
</agent_instructions>

## 1. Code Governance & Encapsulation

### 1.1 Public API Enforcement
- Every feature/shared directory MUST have an `index.ts`.
- **Deep imports are prohibited.** Only import from top-level entry points.

### 1.2 TypeScript Resolution Rules
- **JSX Extension**: MUST use `.tsx` for files containing JSX.
- **No Duplicate Modules**: Never create both `.ts` and `.tsx` for the same logic.
- **React Hooks**: MUST import hooks explicitly (`import { useState } from 'react'`).

### 1.3 Styling Authority
- `UI/app/globals.css` is the consolidated source for all CSS.
- Use `@/shared/theme/tokens.ts` for JS-level tokens.

---

## 2. Dependency & Build Protocol

Before committing, developers MUST ensure a clean build.

| Step | Command | Goal |
|------|---------|------|
| **Install** | `npm install` | Clean, conflict-free dependencies. |
| **Audit** | `npm audit` | Zero HIGH/CRITICAL vulnerabilities. |
| **Type Check** | `npx tsc --noEmit` | Zero type errors. |
| **Build** | `npm run build` | Successful production bundle. |

---

## 3. Master Definition of Done (DoD)

<agent_instructions>
Every UI task is considered INCOMPLETE until the following constraints are verified. 
If any check fails, the agent MUST remediate before concluding.
</agent_instructions>

### ✅ Visual Compliance
- [ ] **Colors**: All hex codes MUST be replaced with `torroTokens.colors` or `@/shared/theme/tokens`.
- [ ] **Aesthetics**: Containers MUST use `backdrop-blur-xl` and `rounded-[20px]` (Radius XL).
- [ ] **Icons**: SVG icons MUST use `stroke='currentColor'` to inherit theme colors.
- [ ] **Layout**: Grids MUST use `gap-6` (24px) for consistent vertical/horizontal rhythm.

### ✅ Architectural Compliance
- [ ] **FSD Boundaries**: Feature components MUST NOT import from other features.
- [ ] **Encapsulation**: Imports MUST only reference the feature's `index.ts` (Public API).
- [ ] **State**: Data influencing UI (filters/page) MUST be persistent in URL SearchParams.
- [ ] **Performance**: Non-critical heavy libraries MUST be lazy-loaded with `ssr: false`.

### ✅ Reliability & Security
- [ ] **Tests**: Every new component MUST have a `.test.tsx` file using React Testing Library.
- [ ] **Resilience**: Every route MUST have a `loading.tsx` and `error.tsx` in its directory.
- [ ] **Validation**: All form inputs MUST be validated with a Zod schema.
- [ ] **Security**: No user-facing strings are hardcoded (MUST use `t()` from i18n).
- [ ] **Accessibility**: All interactive elements MUST have an `aria-label` or discernible text.

### ✅ Build Health
- [ ] **Types**: `npx tsc --noEmit` returns zero errors.
- [ ] **Vulnerabilities**: `npm audit` returns zero HIGH/CRITICAL vulnerabilities.
- [ ] **Build**: `npm run build` completes successfully.
