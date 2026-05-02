---
name: react-query
description: Implement @tanstack/react-query for server-state management including data fetching, caching, mutations, pagination, and real-time updates with TypeScript support
license: MIT
compatibility:
  - react-18.0+
  - @tanstack/react-query-5.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://github.com/TanStack/query
---

# React Query (TanStack Query) Skill

## When to Use This Skill

Use this skill when you need to:
- Fetch data with `useQuery` and manage server state
- Implement mutations with `useMutation` for create/update/delete operations
- Set up QueryClient provider and configure caching
- Handle pagination and infinite scrolling with `useInfiniteQuery`
- Prefetch data for improved performance
- Synchronize multiple queries and mutations
- Implement optimistic updates
- Use React Suspense mode with `useSuspenseQuery`
- Configure retry, staleTime, and gcTime options
- Manage query keys and invalidation strategies

## When NOT to Use This Skill

Do NOT use this skill when:
- Managing client-side UI state (use React state/context instead)
- Building simple static data displays (no server state)
- Working with Vue, Angular, or Svelte (use respective Query libraries)
- Setting up backend APIs (use backend skills instead)

## Inputs Required

Before starting, ensure you have:
1. React version (default: 18.x+)
2. API endpoint URLs and methods
3. Data types and response shapes
4. Caching requirements (staleTime, gcTime)

## Workflow

### Step 1: Setup QueryClient Provider

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  )
}
```

### Step 2: Basic Data Fetching with useQuery

```typescript
import { useQuery } from '@tanstack/react-query'
import { apiGet } from '@/shared/api/api/client'

interface User {
  id: string
  name: string
  email: string
}

function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error, isSuccess } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => apiGet<User>(`/api/users/${userId}`),
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  if (isSuccess && data) {
    return (
      <div>
        <h1>{data.name}</h1>
        <p>{data.email}</p>
      </div>
    )
  }
  return null
}
```

### Step 3: Data Mutations with useMutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreateUserForm() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (newUser: { name: string; email: string }) =>
      apiPost('/api/users', newUser),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    mutation.mutate({ name: 'John', email: 'john@example.com' })
  }

  return (
    <form onSubmit={handleSubmit}>
      <button disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

### Step 4: Pagination with useInfiniteQuery

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

function AssetList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ['assets'],
    queryFn: ({ pageParam = 0 }) =>
      apiGet<{ data: Asset[]; meta: { total: number } }>('/api/assets', {
        params: { skip: pageParam, limit: 25 },
      }),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      const currentSkip = lastPage.meta.skip + lastPage.meta.limit
      return currentSkip < lastPage.meta.total ? currentSkip : undefined
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      {data.pages.map((page) =>
        page.data.map((asset) => (
          <div key={asset.id}>{asset.name}</div>
        ))
      )}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading more...' : 'Load more'}
        </button>
      )}
    </div>
  )
}
```

### Step 5: Query Options for Type Safety

```typescript
import { queryOptions, infiniteQueryOptions } from '@tanstack/react-query'

// Define query options
const userOptions = queryOptions({
  queryKey: ['user', '123'],
  queryFn: () => apiGet<User>('/api/users/123'),
})

// Use the options
function UserProfile() {
  const { data } = useQuery(userOptions)
  return <div>{data?.name}</div>
}

// Infinite query options
const assetsOptions = infiniteQueryOptions({
  queryKey: ['assets'],
  queryFn: ({ pageParam }) =>
    apiGet<AssetPage>('/api/assets', { params: { skip: pageParam } }),
  initialPageParam: 0,
  getNextPageParam: (lastPage) =>
    lastPage.meta.skip + lastPage.meta.limit < lastPage.meta.total
      ? lastPage.meta.skip + lastPage.meta.limit
      : undefined,
})
```

### Step 6: Prefetching Data

```typescript
import { usePrefetchQuery } from '@tanstack/react-query'

function Dashboard() {
  const prefetch = usePrefetchQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => apiGet<Stats>('/api/dashboard/stats'),
  })

  // Prefetch on hover or navigation
  return (
    <div onMouseEnter={() => prefetch()}>
      <StatsCard />
    </div>
  )
}
```

### Step 7: React Suspense Mode

```typescript
import { useSuspenseQuery } from '@tanstack/react-query'
import { Suspense } from 'react'

function SuspenseUserProfile({ userId }: { userId: string }) {
  const { data } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => apiGet<User>(`/api/users/${userId}`),
  })

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  )
}

// Wrap in Suspense boundary
function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SuspenseUserProfile userId="123" />
    </Suspense>
  )
}
```

### Step 8: Query Invalidation and Updates

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function UserManagement() {
  const queryClient = useQueryClient()

  const deleteMutation = useMutation({
    mutationFn: (userId: string) => apiDelete(`/api/users/${userId}`),
    onSuccess: (_data, variables) => {
      // Optimistic update
      queryClient.setQueryData(['user', variables], (old: User) => ({
        ...old,
        deleted: true,
      }))
      
      // Invalidate after mutation
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  return (
    <button onClick={() => deleteMutation.mutate('123')}>
      Delete User
    </button>
  )
}
```

### Step 9: Real-time Updates with Refetching

```typescript
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect } from 'react'

function RealTimeNotifications() {
  const queryClient = useQueryClient()

  const { data } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => apiGet<Notification[]>('/api/notifications'),
    refetchInterval: 5000, // Refetch every 5 seconds
    refetchIntervalInBackground: true,
  })

  // Or refetch on specific events
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:3000/notifications')
    ws.onmessage = () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
    }
    return () => ws.close()
  }, [queryClient])

  return <div>{data?.length || 0} notifications</div>
}
```

### Step 10: Custom Hooks Pattern

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Custom hook for workspaces
export function useWorkspaces() {
  return useQuery({
    queryKey: ['workspaces'],
    queryFn: () => apiGet<Workspace[]>('/api/workspaces'),
  })
}

export function useCreateWorkspace() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: CreateWorkspacePayload) =>
      apiPost('/api/workspaces', payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
    },
  })
}

// Usage in component
function WorkspaceManager() {
  const { data: workspaces } = useWorkspaces()
  const createWorkspace = useCreateWorkspace()

  return (
    <div>
      {workspaces?.map((ws) => <WorkspaceCard key={ws.id} workspace={ws} />)}
      <button onClick={() => createWorkspace.mutate({ name: 'New' })}>
        Create Workspace
      </button>
    </div>
  )
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `packages/react-query/src/index.ts` | Public API exports |
| `packages/query-core/src/` | Core query logic |
| `packages/react-query/src/useQuery.ts` | useQuery implementation |
| `packages/react-query/src/useMutation.ts` | useMutation implementation |

## Troubleshooting

### Issue: Stale Data

**Symptom**: Data not updating after mutation

**Solution**:
- Call `queryClient.invalidateQueries({ queryKey: ['key'] })` after mutation
- Set appropriate `staleTime` in QueryClient config
- Use `refetchOnMount: true` for critical data

### Issue: Too Many Refetches

**Symptom**: Excessive API calls

**Solution**:
- Increase `staleTime` to reduce refetches
- Set `refetchOnWindowFocus: false`
- Use `keepPreviousData: true` for pagination

### Issue: TypeScript Errors

**Symptom**: Type errors with query data

**Solution**:
- Use `queryOptions` for type inference
- Specify return types in `queryFn`
- Use `DefinedInitialDataOptions` or `UndefinedInitialDataOptions`

## Examples

### Example 1: Complete CRUD Pattern

```typescript
// API service
const userApi = {
  list: () => apiGet<User[]>('/api/users'),
  get: (id: string) => apiGet<User>(`/api/users/${id}`),
  create: (data: CreateUserDto) => apiPost('/api/users', data),
  update: (id: string, data: UpdateUserDto) => apiPut(`/api/users/${id}`, data),
  delete: (id: string) => apiDelete(`/api/users/${id}`),
}

// Custom hooks
function useUsers() {
  return useQuery({ queryKey: ['users'], queryFn: userApi.list })
}

function useCreateUser() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: userApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['users'] }),
  })
}
```

### Example 2: Dependent Queries

```typescript
function UserProjects({ userId }: { userId: string }) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => apiGet<User>(`/api/users/${userId}`),
  })

  const { data: projects } = useQuery({
    queryKey: ['projects', user?.workspaceId],
    queryFn: () => apiGet<Project[]>(`/api/projects?workspaceId=${user?.workspaceId}`),
    enabled: !!user?.workspaceId, // Only run if user exists
  })

  return <div>{projects?.length || 0} projects</div>
}
```

## Related Resources

- [TanStack Query Documentation](https://tanstack.com/query)
- [React Query API Reference](https://tanstack.com/query/latest/docs/react/reference/useQuery)
- [React Query DevTools](https://tanstack.com/query/latest/docs/react/devtools/overview)
