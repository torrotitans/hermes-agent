# Header & Session Bar Standards

> **LOCKED**: The session bar visual styling is frozen. Do NOT modify button styling, icon sizing, or hover animations in `UI/src/features/session/ui/session-bar.tsx` without explicit approval.
> **Server-Side Injection**: Session data MUST be injected from server components to eliminate loading delay. See [Session Data Injection](#session-data-injection).

## Header Action Bar

### Liquid Glass Container
- The header action bar uses a rounded container with backdrop blur and glass styling.
- Search input, session bar buttons, and logout button share the same vertical height (`h-8`).
- **No vertical separators** between session bar buttons (user, workspace, notification, logout).

### Session Bar Buttons (LOCKED)
All session bar buttons (user profile, workspace selector, notification, logout) MUST follow this exact styling:

```tsx
className='group flex items-center gap-2 rounded-lg p-1.5 text-torro-header/70 hover:bg-torro-primary/10 hover:text-torro-header transition-all duration-200 focus:ring-2 focus:ring-torro-primary/50 focus:outline-none'
```

### Icon Sizing (LOCKED)
- All icons within session bar buttons MUST use `h-4 w-4` sizing for uniform alignment.
- Exception: Notification icon uses `h-6 w-6` with `style={{ transform: 'translateY(-1px)' }}` to visually center the bell shape.

### Text Styling (LOCKED)
- Primary label: `text-[11px] font-bold text-torro-header leading-none`
- Subtitle (e.g., "DEFAULT", "4 UNREAD"): `text-[8px] font-black uppercase tracking-[0.1em] text-torro-header/60 mt-0.5`

### Hover Expansion (LOCKED)
- Text panels use `max-w-0 overflow-hidden opacity-0` by default.
- On hover/focus: `group-hover:max-w-[140px] group-hover:opacity-100 group-focus-within:max-w-[140px] group-focus-within:opacity-100`.
- Transition: `duration-200 ease-out`.
- Left padding: `pl-1`.

### Logout Button (LOCKED)
- Uses `h-auto` to match button height with session bar.
- Text panel hover expansion: `group-hover:max-w-[60px] group-focus-within:max-w-[60px]`.

### Vertical Separators (LOCKED)
- **No vertical separators** (`h-8 w-px bg-torro-header/20`) between session bar buttons.
- Separators are only used between the search input and the session bar group in the header.

## Session Data Injection

### Server-Side Session Injection (MANDATORY)

The SessionBar component MUST receive session data from its parent server component via the `initialSession` prop. This eliminates the loading delay caused by client-side API fetch.

**Pattern**:

```tsx
// app/(secure)/layout.tsx — Server Component
import { auth } from '@/auth';
import { SessionBar } from '@/features/session';

export default async function SecureLayout({ children }) {
  const session = await auth(); // Server-side, zero network delay

  const initialSession = session?.user ? {
    authenticated: true,
    user: {
      username: session.user.name || session.user.email || 'User',
      staffId: (session.user as any).staffId,
      role: (session.user as any).role || 'user',
      workspaceId: (session.user as any).workspaceId,
      workspaceList: (session.user as any).workspaceList,
    },
  } : null;

  return (
    <AppShell
      sessionBar={
        <Suspense fallback={<SessionBarSkeleton />}>
          <SessionBar initialSession={initialSession} />
        </Suspense>
      }
    >
      {children}
    </AppShell>
  );
}
```

**SessionBar Component** (`UI/src/features/session/ui/session-bar.tsx`):

```tsx
// Client Component
type SessionBarProps = {
  initialSession?: SessionResponse | null;
};

export function SessionBar({ initialSession }: SessionBarProps) {
  const sessionQuery = useQuery({
    queryKey: ['session-me'],
    queryFn: () => apiGet<SessionResponse>('/api/session/me'),
    initialData: initialSession ?? undefined,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    retry: 1,
  });
  // ...
}
```

### Why Server-Side Injection

| Approach | Loading State | Network Latency | First Content |
|----------|--------------|-----------------|---------------|
| Client-side API call only | Always shown | + API roundtrip | Delayed |
| Server-side injection | Never shown | None (injected) | Immediate |

1. **Eliminates loading skeleton flash** — `initialData` in React Query means `isLoading` is `false` on mount
2. **Zero network latency** — session data is available at render time from server
3. **Better CLS** — no layout shift from skeleton → content transition
4. **Background refetch** — React Query still fetches in background, caches for 5 minutes

### SessionResponse Type

```typescript
type SessionResponse = {
  authenticated: boolean;
  user?: {
    username: string;
    staffId?: string;
    role: string;
    workspaceId?: string;
    workspaceList?: Array<{ value: string | number; label: string }>;
  };
};
```

### Fallback Behavior

When `initialSession` is `null` or `undefined`:
- React Query fetches from `/api/session/me` (shows brief loading skeleton)
- If API fails or returns unauthenticated, shows fallback icons with "User" / "Workspace" labels

---

*Last Updated: 2026-04-29*
*Version: 2.0 (Session Bar LOCKED + Server-Side Injection)*
