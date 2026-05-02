# Torro UI Standards: 03. Architecture & Patterns

<agent_instructions>
- Adhere to Feature-Sliced Design (FSD) principles.
- Use Next.js high-efficiency patterns for all data fetching and rendering.
- Prioritize Resilience (Loading/Error states) for every route.
</agent_instructions>

## 1. Architectural Layers

Torro follows a layered design system:
**Brand Layer** -> **Style Layer** -> **Token Layer** -> **Component Layer**.

### 1.1 Feature-Sliced Design (FSD) Boundaries

| Layer | Path | Responsibility |
|-------|------|----------------|
| **App** | `UI/app/` | Global providers, layout, and routing. |
| **Features** | `UI/src/features/` | Domain-specific logic and UI (e.g., Auth, Discovery). |
| **Shared** | `UI/src/shared/` | Reusable components, hooks, and utilities. |

**Import Rule**: Features MUST NOT import from other features. Use `shared` for common logic.

---

## 2. Next.js High-Efficiency Patterns

### 2.1 Controller-Atomic Hook Pattern
Decompose complex state into atomic hooks composed by a central controller.
- **Filter Hook**: Manages URL/UI filters.
- **Data Hook**: Manages async fetching.
- **Controller Hook**: Composes logic for the UI.

### 2.2 URL as "Source of Truth"
Any UI state influencing data (filters, pagination) MUST be synced with URL SearchParams.

### 2.3 Dynamic Payload Loading
Lazy-load heavy libraries (D3, Recharts) using `next/dynamic` with `ssr: false`.

### 2.4 Server-Side Hydration
Use `HydrationBoundary` with `dehydrate(queryClient)` for high-density data routes to eliminate waterfalls.

---

## 3. Platform Resilience Standards

Every top-level feature route MUST implement:

| Primitive | Requirement |
|-----------|-------------|
| **`loading.tsx`** | High-fidelity "Liquid Glass" skeletons. |
| **`error.tsx`** | Localized recovery boundary with "Retry" logic. |

### 3.1 Resilient Proxy Logic
All backend calls MUST implement **Exponential Backoff** (minimum 3 retries) for transient network failures (502, 503, 504).

---

## 4. Static Asset Serving
Static files MUST be served from the `public/` directory to avoid Turbopack NFT (Non-File-Trace) warnings.

```typescript
// CORRECT: Fetch from public URL
const response = await fetch(new URL(`/templates/${fileName}`, request.url));
```
