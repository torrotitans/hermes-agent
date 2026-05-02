# Torro UI Standards: 07. State Management

<agent_instructions>
- Minimize global state. Use local state by default.
- Use `React Query` for all server-side data fetching.
- Use `Zustand` for complex cross-component UI state.
</agent_instructions>

## 1. State Categorization

| Category | Tool | Scope |
|----------|------|-------|
| **Local UI State** | `useState` / `useReducer` | Single component or small tree. |
| **Server State** | `React Query` (`@tanstack/react-query`) | API data, caching, revalidation. |
| **Global UI State** | `Zustand` | Cross-feature state (e.g., Global Search, Session). |
| **Navigation State** | `URL SearchParams` | Filters, pagination, active IDs. |

---

## 2. Server State (React Query) Standards

### 2.1 Hook Placement
Queries MUST be wrapped in custom hooks co-located with the feature API.
- **Path**: `UI/src/features/feature-name/api/use-feature-data.ts`

### 2.2 Revalidation Rule
Default `staleTime` should be set to `5 * 1000` (5 seconds) unless the data is highly static.

---

## 3. Global State (Zustand) Standards

### 3.1 Store Location
- **Path**: `UI/src/shared/lib/store/my-store.ts`

### 3.2 Immutability
Always use the `set` function provided by Zustand. Never mutate state directly.

```typescript
const useUIStore = create<UIState>((set) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
}));
```

---

## 4. URL State Persistence
Any state that should survive a page refresh MUST be stored in the URL.
- **Hook**: `useSearchParams` from `next/navigation`.
- **Constraint**: Update the URL using `router.replace(url, { scroll: false })` to avoid jumping.
