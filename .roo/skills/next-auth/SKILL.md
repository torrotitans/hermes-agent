---
name: next-auth
description: Implement NextAuth.js v5 (Auth.js) authentication in Next.js applications including OAuth providers, JWT sessions, middleware protection, and database adapters
---

# NextAuth.js v5 Implementation

## When to use

Use this skill when you need to:
- Add authentication to a Next.js application (App Router or Pages Router)
- Implement OAuth login (Google, GitHub, Azure AD, etc.)
- Configure email/passwordless authentication
- Set up JWT or database-backed session management
- Protect routes with middleware
- Integrate custom authentication providers
- Migrate from NextAuth.js v4 to v5

## When NOT to use

- **Do NOT use** for backend-only authentication (use Flask/Python session management instead)
- **Do NOT use** if you need LDAP/Active Directory integration (use the existing Torro LDAP system)
- **Do NOT use** for enterprise SSO requiring SAML 2.0 with custom IdP (consider custom OAuth2 provider)
- **Do NOT use** if the project uses Express.js instead of Next.js (use `@auth/express` instead)

## NextAuth.js v5 Key Changes from v4

NextAuth.js v5 (Auth.js) introduces significant architectural changes:

| Feature | v4 | v5 |
|---------|-----|-----|
| Package | `next-auth` | `next-auth@beta` or `authjs` |
| Core | Next.js-specific | Framework-agnostic (`@auth/core`) |
| Session Strategy | `jwt` or `database` | JWT by default (database via adapter) |
| Middleware | `next/middleware` | `auth.ts` with Next.js middleware |
| Provider Config | Inline in `NextAuth()` | Separate config files |
| TypeScript | Good support | First-class, stricter types |

## Inputs Required

Before starting, gather:
1. **Provider credentials**: OAuth client IDs/secrets from your identity providers
2. **Session strategy**: JWT (default) or database-backed sessions
3. **Database adapter**: Prisma, Drizzle, TypeORM, or custom adapter
4. **Environment variables**: `AUTH_SECRET`, `AUTH_TRUST_HOST`, provider-specific keys

## Workflow

### Step 1: Install Dependencies

```bash
npm install next-auth@beta
# Or for specific framework
npm install @auth/core @auth/nextjs
```

### Step 2: Create Authentication Configuration

Create [`auth.config.ts`](references/auth-config.md) with provider definitions:

```typescript
import { NextAuthConfig } from "next-auth"
import GitHub from "next-auth/providers/github"
import Google from "next-auth/providers/google"
import Credentials from "next-auth/providers/credentials"

export const authConfig: NextAuthConfig = {
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    Credentials({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Validate against your backend API
        const response = await fetch("https://your-api.com/auth/verify", {
          method: "POST",
          body: JSON.stringify(credentials),
        })
        const user = await response.json()
        if (response.ok && user) return user
        return null
      },
    }),
  ],
  session: {
    strategy: "jwt", // or "database" with adapter
  },
  callbacks: {
    async jwt({ token, user, trigger, session }) {
      // Handle session updates
      if (trigger === "update") {
        token.name = session.user.name
      }
      return token
    },
    async session({ session, token }) {
      session.user.id = token.sub
      return session
    },
  },
}
```

### Step 3: Create Auth Route Handler

For App Router, create [`app/api/auth/[...nextauth]/route.ts`](references/route-handler.md):

```typescript
import { handlers, auth } from "@/auth" // Re-export from auth.ts

export const { GET, POST } = handlers
```

### Step 4: Create Main Auth Entry Point

Create [`auth.ts`](references/auth-config.md) at project root:

```typescript
import NextAuth from "next-auth"
import { authConfig } from "./auth.config"

export const { handlers, signIn, signOut, auth } = NextAuth(authConfig)
```

### Step 5: Configure Middleware

Create [`middleware.ts`](references/middleware.md) for route protection:

```typescript
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith("/dashboard")
  
  if (isOnDashboard) {
    if (!isLoggedIn) {
      return Response.redirect(new URL("/login", req.nextUrl))
    }
  } else if (isLoggedIn) {
    return Response.redirect(new URL("/dashboard", req.nextUrl))
  }
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

### Step 6: Create Login/Logout UI Components

Create authentication UI components:

```typescript
// app/login/page.tsx
"use client"
import { signIn } from "@/auth"

export default function LoginPage() {
  return (
    <div>
      <form
        action={async () => {
          "use server"
          await signIn("github")
        }}
      >
        <button type="submit">Sign in with GitHub</button>
      </form>
      
      <form
        action={async () => {
          "use server"
          await signIn("google")
        }}
      >
        <button type="submit">Sign in with Google</button>
      </form>
    </div>
  )
}
```

### Step 7: Access Session in Components

```typescript
// Server Component
import { auth } from "@/auth"

export default async function Dashboard() {
  const session = await auth()
  return <div>Welcome, {session?.user?.name}</div>
}

// Client Component
"use client"
import { useSession } from "next-auth/react"

export function UserProfile() {
  const { data: session, status } = useSession()
  if (status === "loading") return <div>Loading...</div>
  return <div>{session?.user?.email}</div>
}
```

### Step 8: Add Database Adapter (Optional)

For database-backed sessions, install and configure an adapter:

```bash
npm install @auth/prisma-adapter prisma
```

```typescript
// auth.config.ts
import { PrismaAdapter } from "@auth/prisma-adapter"
import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

export const authConfig: NextAuthConfig = {
  adapter: PrismaAdapter(prisma),
  session: {
    strategy: "database",
  },
  // ... rest of config
}
```

## Environment Variables

Required environment variables in `.env.local`:

```bash
# Required: Secret key for signing tokens (generate with `openssl rand -base64 32`)
AUTH_SECRET=your-secret-key-here

# Required: Trust proxy headers (for production behind reverse proxy)
AUTH_TRUST_HOST=true

# OAuth Provider credentials
AUTH_GITHUB_ID=your-github-client-id
AUTH_GITHUB_SECRET=your-github-client-secret

AUTH_GOOGLE_ID=your-google-client-id
AUTH_GOOGLE_SECRET=your-google-client-secret

# Database URL (if using database sessions)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

## Common Providers Reference

| Provider | Package Import | Setup Guide |
|----------|---------------|-------------|
| GitHub | `next-auth/providers/github` | [GitHub OAuth App](https://github.com/settings/developers) |
| Google | `next-auth/providers/google` | [Google Cloud Console](https://console.cloud.google.com/) |
| Azure AD | `next-auth/providers/azure-ad` | [Azure Portal](https://portal.azure.com/) |
| Okta | `next-auth/providers/okta` | [Okta Developer](https://developer.okta.com/) |
| Auth0 | `next-auth/providers/auth0` | [Auth0 Dashboard](https://manage.auth0.com/) |
| Credentials | `next-auth/providers/credentials` | Custom implementation |
| Email | `next-auth/providers/nodemailer` | SMTP configuration |

## Troubleshooting

### Session Not Persisting

**Problem**: User logs in but session disappears on refresh.

**Solution**:
1. Verify `AUTH_SECRET` is set correctly
2. Check cookie settings in config:
```typescript
session: {
  maxAge: 30 * 24 * 60 * 60, // 30 days
}
```

### OAuth Callback Errors

**Problem**: "Invalid state" or callback URL mismatch.

**Solution**:
1. Ensure callback URL matches provider configuration exactly
2. Check `AUTH_TRUST_HOST=true` is set in production
3. Verify redirect URI in OAuth provider dashboard

### Middleware Not Triggering

**Problem**: Protected routes accessible without authentication.

**Solution**:
1. Verify `matcher` pattern in middleware config
2. Check that `auth.ts` is properly exported
3. Clear Next.js cache: `rm -rf .next`

### TypeScript Errors

**Problem**: Type errors with session/user types.

**Solution**:
1. Create `types/next-auth.d.ts` for module augmentation:
```typescript
import NextAuth from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
    } & Session["user"]
  }
}
```

## Security Best Practices

1. **Always use HTTPS** in production
2. **Rotate secrets regularly** and use environment variables
3. **Implement rate limiting** on credential providers
4. **Use secure cookie settings**:
```typescript
cookies: {
  sessionToken: {
    name: `next-auth.session-token`,
    options: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
    },
  },
}
```

5. **Validate OAuth state** to prevent CSRF attacks
6. **Implement account linking** carefully to prevent account takeover

## Related Files

- [`references/auth-config.md`](references/auth-config.md) - Complete configuration reference
- [`references/route-handler.md`](references/route-handler.md) - API route patterns
- [`references/middleware.md`](references/middleware.md) - Route protection patterns
- [`references/providers.md`](references/providers.md) - Provider-specific configurations
