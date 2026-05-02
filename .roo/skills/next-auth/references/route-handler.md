# NextAuth.js v5 Route Handler Patterns

## App Router Pattern

### Standard Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth" // Re-export from auth.ts

export const { GET, POST } = handlers
```

### Custom Route Handler with Middleware

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth"
import { authConfig } from "@/auth.config"

const handler = NextAuth(authConfig)

export async function GET(request: Request) {
  return handler(request)
}

export async function POST(request: Request) {
  return handler(request)
}
```

## Pages Router Pattern

```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from "next-auth"
import { authConfig } from "../../auth.config"

export default NextAuth(authConfig)
```

## Custom API Routes

### Get Current User

```typescript
// app/api/me/route.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await auth()
  
  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    )
  }
  
  return NextResponse.json({
    user: {
      id: session.user.id,
      name: session.user.name,
      email: session.user.email,
      image: session.user.image,
    },
  })
}
```

### Protected Route with Role Check

```typescript
// app/api/admin/route.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await auth()
  
  // Check if user is admin
  if (session?.user?.role !== "admin") {
    return NextResponse.json(
      { error: "Forbidden: Admin access required" },
      { status: 403 }
    )
  }
  
  // Admin-only logic here
  return NextResponse.json({ data: "admin-only-data" })
}
```

### OAuth Callback with Custom Logic

```typescript
// app/api/auth/callback/github/route.ts
import { NextResponse } from "next/server"
import { auth } from "@/auth"

export async function GET(request: Request) {
  const session = await auth()
  
  if (!session?.user) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  
  // Custom post-authentication logic
  // e.g., create user profile, sync data, etc.
  
  return NextResponse.redirect(new URL("/dashboard", request.url))
}
```

## Route Grouping Pattern

```typescript
// app/api/auth/route.ts (handles all auth routes)
import { handlers } from "@/auth"

export const { GET, POST } = handlers

// Or for more control:
export async function GET(request: Request) {
  const url = new URL(request.url)
  const pathname = url.pathname
  
  // Handle different auth paths
  switch (pathname) {
    case "/api/auth/signin":
      // Custom sign-in page
      break
    case "/api/auth/callback":
      // Handle callback
      break
    case "/api/auth/signout":
      // Handle sign-out
      break
    default:
      return handlers.GET(request)
  }
}
```

## Middleware-Based Protection

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith("/dashboard")
  const isOnAdmin = req.nextUrl.pathname.startsWith("/admin")
  
  // Redirect to login if not logged in and accessing protected routes
  if ((isOnDashboard || isOnAdmin) && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
  
  // Redirect to dashboard if logged in and accessing login
  if (req.nextUrl.pathname === "/login" && isLoggedIn) {
    return Response.redirect(new URL("/dashboard", req.nextUrl))
  }
})

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico|public).*)",
  ],
}
```

## Server Actions Pattern

```typescript
// app/actions/auth.ts
"use server"

import { signIn, signOut } from "@/auth"
import { AuthError } from "next-auth"

export async function authenticate(
  prevState: string | undefined,
  formData: FormData
) {
  try {
    await signIn("credentials", formData)
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return "Invalid credentials"
        default:
          return "Something went wrong"
      }
    }
    throw error
  }
}

export async function handleSignOut() {
  await signOut({ redirectTo: "/" })
}
```

## Type-Safe Route Handlers

```typescript
// app/api/protected/route.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await auth()
  
  if (!session) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    )
  }
  
  // Type-safe access to user data
  const userId = session.user?.id
  const userEmail = session.user?.email
  
  return NextResponse.json({
    message: "Protected data",
    userId,
    userEmail,
  })
}
```

## Error Handling

```typescript
// app/api/auth/[...nextauth]/route.ts
import { NextResponse } from "next/server"
import { handlers } from "@/auth"

export async function GET(request: Request) {
  try {
    return await handlers.GET(request)
  } catch (error) {
    console.error("Auth error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    return await handlers.POST(request)
  } catch (error) {
    console.error("Auth error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
```
