---
name: nextjs-enterprise
description: Enterprise-grade Next.js development covering App Router architecture, Server/Client Components, caching strategies, performance optimization, security patterns, and production deployment best practices
---

# Enterprise Next.js Development Skill

## When to use this skill

Use this skill when:
- Building new Next.js applications with the App Router
- Implementing data fetching, caching, or revalidation strategies
- Designing component architecture with Server and Client Components
- Optimizing performance (Core Web Vitals, bundle size, rendering)
- Configuring Next.js for production deployment
- Implementing authentication, middleware, and route protection
- Creating Route Handlers, Server Actions, or API endpoints
- Working with metadata, images, fonts, or static assets

## When NOT to use this skill

- For Pages Router (legacy) development - use specific Pages Router documentation instead
- For backend Python/Flask development - use `backend-architecture` or `backend-coding-standards` skills
- For UI component library decisions - refer to project-specific design system documentation
- For basic React knowledge - assume familiarity with React hooks and components

## Core Architecture Patterns

### 1. App Router Fundamentals

The App Router uses a file-system based router based on React Server Components. Key concepts:

- **Layouts**: Persist UI across route changes and share data between routes
- **Pages**: Render specific routes and handle data fetching
- **Loading UI**: Streaming loading states with Suspense
- **Error Handling**: Boundaries for error recovery
- **Route Handlers**: Custom request handlers for API endpoints
- **Special Files**: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `template.tsx`

### 2. Server vs Client Components

**Server Components (default)**:
- Render on the server and send HTML to the client
- Can directly access backend resources and databases
- Zero bundle size impact
- Use for: data fetching, backend integration, markdown rendering, large libraries

**Client Components (use 'use client')**:
- Render on the client with JavaScript
- Required for browser APIs, state, effects, and event listeners
- Use for: interactivity, browser APIs, state management, side effects

### 3. Data Fetching Strategies

| Strategy | Use Case | Implementation |
|----------|----------|----------------|
| Direct Fetching | Server Components need data | `async/await` in Server Components |
| Server Actions | Form submissions, mutations | `'use server'` functions |
| Client Fetching | Dynamic user-specific data | `useEffect` in Client Components |
| SWR/React Query | Complex caching requirements | External data libraries |

## Core Workflow

### Step 1: Route Structure Setup

1. Create the route folder structure: `app/[feature]/page.tsx`
2. Add `layout.tsx` for persistent UI if needed
3. Add `loading.tsx` for streaming UI
4. Add `error.tsx` for error boundaries

### Step 2: Component Architecture

1. Determine if component needs interactivity (Client Component) or just rendering (Server Component)
2. Keep Server Components at the top of the tree
3. Push Client Components as low as possible
4. Use Props Drilling for Server-to-Server communication
5. Use Context only for Client Component state

### Step 3: Data Fetching Implementation

1. For Server Components: Fetch data directly in the component
2. For mutations: Use Server Actions with Zod validation
3. Configure caching based on data freshness requirements
4. Implement error handling and loading states

### Step 4: Performance Optimization

1. Use `next/image` for all images
2. Use `next/font` for font optimization
3. Implement proper caching headers
4. Configure route segment options for static/dynamic rendering

## Caching Strategy

### Data Cache (Data Fetching)

```typescript
// Force cache (default)
const data = await fetch('https://...') // Cached indefinitely

// No cache (dynamic)
const data = await fetch('https://...', { cache: 'no-store' })

// Revalidate after time
const data = await fetch('https://...', { next: { revalidate: 3600 } })
```

### Full Route Cache

- Stores rendered output (HTML + data)
- Cached per route path
- Revalidated on demand or time-based

### Route Worker Cache

- Cached per deployment
- Used for server actions and route handlers
- Cleared on new deployment

### Client-Side Cache

- Browser HTTP cache
- `fetch()` in Client Components uses HTTP cache by default
- Use `next: { revalidate }` to control

## Revalidation Strategies

### Time-Based Revalidation (ISR)

```typescript
export const revalidate = 3600 // Revalidate every hour
```

### On-Demand Revalidation

```typescript
import { revalidatePath } from 'next/cache'

revalidatePath('/dashboard') // Invalidate path
revalidatePath('/api/users', 'layout') // Invalidate layout
```

### Tag-Based Revalidation

```typescript
// Fetch with tag
fetch('https://...', { next: { tags: ['users'] } })

// Revalidate by tag
revalidateTag('users')
```

## Server Actions Security

### Required Security Patterns

1. **Treat Server Actions as Public Endpoints**
   - Always validate input with Zod or similar
   - Check authentication and authorization on every action
   - Never trust client-side data

2. **Input Validation Pattern**

```typescript
'use server'

import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
})

export async function createPost(prevState: unknown, formData: FormData) {
  const validatedFields = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors }
  }

  // Check authorization here
  const user = await getCurrentUser()
  if (!user) {
    return { error: 'Unauthorized' }
  }

  // Process mutation
  await db.post.create({ data: validatedFields.data })
}
```

## Route Handler Patterns

### RESTful Route Handler Structure

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET(request: Request) {
  try {
    const users = await db.user.findMany()
    return NextResponse.json(users)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const user = await db.user.create({ data: body })
    return NextResponse.json(user, { status: 201 })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 400 }
    )
  }
}
```

### Route Handler with Path Params

```typescript
// app/api/users/[id]/route.ts
import { NextResponse } from 'next/server'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  })

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  return NextResponse.json(user)
}
```

## Metadata and SEO

### Static Metadata

```typescript
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: {
    title: 'OG Title',
    description: 'OG description',
    images: ['/og-image.jpg'],
  },
}
```

### Dynamic Metadata

```typescript
export async function generateMetadata({
  params,
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Performance Optimization Checklist

### Core Web Vitals Targets

| Metric | Target | Next.js Feature |
|--------|--------|-----------------|
| LCP | < 2.5s | Server Components, optimized images |
| FID | < 100ms | Minimize client JS, code splitting |
| CLS | < 0.1 | Reserve space for images/fonts |
| INP | < 200ms | Optimize event handlers |

### Optimization Techniques

1. **Images**: Always use `next/image` with proper sizes
2. **Fonts**: Use `next/font` to eliminate layout shift
3. **Script Loading**: Use `next/script` with appropriate strategy
4. **Code Splitting**: Automatic by route; use dynamic imports for heavy components
5. **Streaming**: Use Suspense boundaries for progressive rendering

## Configuration Best Practices

### next.config.js Essential Settings

```typescript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
    ],
  },
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
```

### Environment Variables

- Prefix with `NEXT_PUBLIC_` for client-side exposure
- Keep sensitive variables server-only
- Use `.env.local` for local development
- Never commit `.env.local` to git

## Deployment Checklist

- [ ] Build succeeds with `next build`
- [ ] All routes pass static generation (unless dynamic)
- [ ] Environment variables are configured for production
- [ ] Image domains are configured for remote images
- [ ] Static assets are optimized
- [ ] Performance metrics meet targets
- [ ] Security headers are configured
- [ ] CORS is properly configured if needed

## Troubleshooting

| Issue | Common Cause | Resolution |
|-------|--------------|------------|
| Dynamic error on static page | Using `searchParams` or cookies | Add `dynamic: 'force-dynamic'` or restructure |
| Images not loading | Missing remote pattern | Add hostname to `next.config.js` images |
| Server Action not working | Missing `'use server'` directive | Add directive at top of file or function |
| Layout shifting | Missing image dimensions | Use `next/image` with proper `width/height` or `fill` |
| Route Handler 404 | Wrong file structure | Verify route is at `app/api/.../route.ts` |

## Migration Guidelines

### From Pages Router to App Router

1. Create parallel `app` directory alongside `pages`
2. Migrate routes gradually, one section at a time
3. Use `redirect` for compatibility during migration
4. Convert `getStaticProps` to Server Component data fetching
5. Convert `getServerSideProps` to Server Components or Route Handlers
6. Replace `useRouter` with `next/navigation` hooks for Client Components

### From Create React App

1. Initialize Next.js: `npx create-next-app@latest`
2. Move components to appropriate App Router structure
3. Replace CRA webpack config with `next.config.js`
4. Migrate API routes to `app/api/` Route Handlers

## Related Resources

- For testing strategies: Use `nextjs-agentic` skill for Vitest, Playwright, and security testing
- For backend patterns: Use `backend-architecture` skill for database and API design patterns
- For security: Refer to OWASP Top 10 and Next.js security documentation
