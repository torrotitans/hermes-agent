# NextAuth.js v5 Middleware Patterns

## Basic Middleware Setup

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  // req.auth contains the session information
  const isLoggedIn = !!req.auth
  
  // Redirect logic
  if (!isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
})

export const config = {
  matcher: ["/dashboard/:path*"],
}
```

## Multiple Route Protection

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith("/dashboard")
  const isOnSettings = req.nextUrl.pathname.startsWith("/settings")
  const isOnAdmin = req.nextUrl.pathname.startsWith("/admin")
  
  // Protected routes require login
  const protectedRoutes = [isOnDashboard, isOnSettings, isOnAdmin]
  
  if (protectedRoutes.some(Boolean) && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
  
  // Logged-in users should not access login page
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

## Role-Based Access Control (RBAC)

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const userRole = req.auth?.user?.role
  const isOnAdmin = req.nextUrl.pathname.startsWith("/admin")
  const isOnPremium = req.nextUrl.pathname.startsWith("/premium")
  
  // Admin routes require admin role
  if (isOnAdmin && userRole !== "admin") {
    return Response.redirect(new URL("/unauthorized", req.nextUrl))
  }
  
  // Premium routes require premium or admin role
  if (isOnPremium && !["premium", "admin"].includes(userRole || "")) {
    return Response.redirect(new URL("/unauthorized", req.nextUrl))
  }
  
  // All protected routes require login
  if ((isOnAdmin || isOnPremium) && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
})

export const config = {
  matcher: ["/admin/:path*", "/premium/:path*"],
}
```

## Public Routes Exception

```typescript
// middleware.ts
import { auth } from "@/auth"

// Routes that don't require authentication
const publicRoutes = ["/", "/login", "/register", "/forgot-password", "/api/auth"]

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isPublicRoute = publicRoutes.some(route => 
    req.nextUrl.pathname.startsWith(route)
  )
  
  // Skip middleware for public routes
  if (isPublicRoute) {
    return
  }
  
  // Redirect unauthenticated users to login
  if (!isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|public).*)"],
}
```

## API Route Protection

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  // Check if request is for API routes
  if (req.nextUrl.pathname.startsWith("/api/")) {
    const isLoggedIn = !!req.auth
    
    if (!isLoggedIn) {
      return Response.json(
        { error: "Unauthorized" },
        { status: 401 }
      )
    }
    
    // Check for specific API permissions
    const isAdmin = req.auth.user?.role === "admin"
    const isApiAdmin = req.nextUrl.pathname.startsWith("/api/admin")
    
    if (isApiAdmin && !isAdmin) {
      return Response.json(
        { error: "Forbidden" },
        { status: 403 }
      )
    }
  }
})

export const config = {
  matcher: ["/api/:path*"],
}
```

## Multi-Tenant Protection

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const tenantId = req.auth?.user?.tenantId
  const pathname = req.nextUrl.pathname
  
  // Extract tenant from URL: /tenant/{tenantId}/dashboard
  const tenantMatch = pathname.match(/^\/tenant\/([^/]+)/)
  
  if (tenantMatch) {
    const requestedTenant = tenantMatch[1]
    
    // Check if user has access to this tenant
    if (tenantId !== requestedTenant && req.auth?.user?.role !== "admin") {
      return Response.redirect(new URL("/unauthorized", req.nextUrl))
    }
  }
  
  // Require login for tenant routes
  if (pathname.startsWith("/tenant/") && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
})

export const config = {
  matcher: ["/tenant/:path*"],
}
```

## Performance Optimization

```typescript
// middleware.ts
import { auth } from "@/auth"

// Only run auth check on specific routes
export default auth((req) => {
  // Your auth logic here
})

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     * - static files
     */
    "/((?!_next/static|_next/image|favicon.ico|public|static).*)",
  ],
}
```

## Custom Session Validation

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth(async (req) => {
  const isLoggedIn = !!req.auth
  
  if (!isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
  
  // Additional session validation
  const session = req.auth
  
  // Check if session is expired
  if (session?.expires && new Date(session.expires) < new Date()) {
    return Response.redirect(new URL("/login?expired=true", req.nextUrl))
  }
  
  // Check for required permissions
  const requiredPermission = req.nextUrl.searchParams.get("permission")
  if (requiredPermission) {
    const userPermissions = session.user?.permissions || []
    if (!userPermissions.includes(requiredPermission)) {
      return Response.redirect(new URL("/unauthorized", req.nextUrl))
    }
  }
})

export const config = {
  matcher: ["/dashboard/:path*"],
}
```

## Environment-Specific Middleware

```typescript
// middleware.ts
import { auth } from "@/auth"

const isDevelopment = process.env.NODE_ENV === "development"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  
  // In development, allow bypass for testing
  if (isDevelopment && req.headers.get("x-dev-bypass") === "true") {
    return
  }
  
  // Production: enforce authentication
  if (!isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

## Middleware with Custom Headers

```typescript
// middleware.ts
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  
  if (!isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
  
  // Add custom headers for authenticated requests
  const response = Response.next()
  response.headers.set("X-User-Id", req.auth?.user?.id || "")
  response.headers.set("X-User-Role", req.auth?.user?.role || "")
  
  return response
})

export const config = {
  matcher: ["/dashboard/:path*"],
}
```
