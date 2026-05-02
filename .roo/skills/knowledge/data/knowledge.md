# Torro Knowledge Base

This file contains curated knowledge entries discovered during development.
Entries are automatically suggested by the knowledge monitoring system.

---

## Index
- [Component Patterns](#component-patterns)
- [Architecture Decisions](#architecture-decisions)
- [Best Practices](#best-practices)
- [Lessons Learned](#lessons-learned)
- [Troubleshooting](#troubleshooting)

---

## Component Patterns

### Next.js App Router Navigation Pattern
- **Type:** best-practice
- **Category:** frontend
- **Date:** YYYY-MM-DD
- **Context:** Client-side navigation in Next.js 14+ App Router
- **Problem:** Standard `<a>` tags cause full page reloads instead of client-side transitions
- **Solution:** Use Next.js `Link` component with `href` prop for client-side navigation
- **Code Reference:** UI/src/shared/layout/app-nav.tsx
- **Tags:** [nextjs, navigation, link]
- **Validation:** Tested with navigation flow and browser history

---

## Architecture Decisions

### Data Table Component Abstraction
- **Type:** pattern
- **Category:** frontend
- **Date:** YYYY-MM-DD
- **Context:** Consistent data presentation across the application
- **Problem:** Multiple components implementing similar table logic with different styles
- **Solution:** Create reusable `data-table.tsx` component with column definition pattern
- **Code Reference:** UI/src/shared/ui/data-table.tsx
- **Tags:** [react, component, data-table]
- **Validation:** Used in 5+ features with consistent behavior

---

## Best Practices

### Error Boundary Implementation
- **Type:** best-practice
- **Category:** frontend
- **Date:** YYYY-MM-DD
- **Context:** React error handling in production
- **Problem:** Unhandled React errors crash the entire application
- **Solution:** Implement error boundary component to isolate failures
- **Code Reference:** UI/src/shared/layout/error-boundary.tsx
- **Tags:** [react, error-handling, stability]
- **Validation:** Tested with intentional React errors

---

## Lessons Learned

### Tailwind Configuration Scope
- **Type:** lesson-learned
- **Category:** frontend
- **Date:** YYYY-MM-DD
- **Context:** Design token customization in Tailwind
- **Problem:** Custom tokens not applying due to config path issues
- **Solution:** Ensure tailwind.config.ts includes all content paths
- **Code Reference:** UI/tailwind.config.ts
- **Tags:** [tailwind, configuration, styling]
- **Validation:** All custom tokens now apply correctly

---

## Troubleshooting

### TypeScript Path Resolution
- **Type:** lesson-learned
- **Category:** development
- **Date:** YYYY-MM-DD
- **Context:** Module imports across project boundaries
- **Problem:** TSConfig path aliases not resolving in certain IDEs
- **Solution:** Add both `paths` and explicit `include` patterns
- **Code Reference:** UI/tsconfig.json
- **Tags:** [typescript, paths, configuration]
- **Validation:** Imports resolve correctly in all editors

---

## Entry Template

Copy this template for new entries:

```markdown
## [Entry Title]
- **Type:** pattern | best-practice | lesson-learned | discovery | anti-pattern
- **Category:** frontend | backend | architecture | security | testing | devops | development
- **Date:** YYYY-MM-DD
- **Context:** Brief description of the situation
- **Problem:** What challenge was encountered
- **Solution:** How it was resolved
- **Code Reference:** File paths or code snippets
- **Tags:** [tag1, tag2, ...]
- **Validation:** How this knowledge was confirmed
```
