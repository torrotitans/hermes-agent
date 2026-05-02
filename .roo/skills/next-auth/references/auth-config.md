# NextAuth.js v5 Configuration Reference

## Complete auth.config.ts Structure

```typescript
import type { NextAuthConfig } from "next-auth"
import GitHub from "next-auth/providers/github"
import Google from "next-auth/providers/google"
import AzureAD from "next-auth/providers/azure-ad"
import Okta from "next-auth/providers/okta"
import Credentials from "next-auth/providers/credentials"
import Email from "next-auth/providers/nodemailer"

export const authConfig: NextAuthConfig = {
  // ============================================================================
  // PROVIDERS
  // ============================================================================
  providers: [
    // OAuth Providers
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
      // Custom scopes
      authorization: { params: { scope: "read:user user:email" } },
    }),
    
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    
    AzureAD({
      clientId: process.env.AUTH_AZURE_AD_ID,
      clientSecret: process.env.AUTH_AZURE_AD_SECRET,
      tenantId: process.env.AUTH_AZURE_AD_TENANT_ID,
    }),
    
    // Credentials Provider (username/password)
    Credentials({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text", placeholder: "jsmith" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Validate against your backend API
        if (!credentials?.username || !credentials?.password) {
          throw new Error("Missing credentials")
        }
        
        const response = await fetch(`${process.env.API_URL}/auth/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(credentials),
        })
        
        const user = await response.json()
        
        if (response.ok && user) {
          return {
            id: user.id.toString(),
            name: user.username,
            email: user.email,
            image: user.avatar,
            role: user.role,
          }
        }
        return null
      },
    }),
    
    // Email/Passwordless
    Email({
      server: {
        host: process.env.EMAIL_SERVER_HOST,
        port: Number(process.env.EMAIL_SERVER_PORT),
        auth: {
          user: process.env.EMAIL_SERVER_USER,
          pass: process.env.EMAIL_SERVER_PASSWORD,
        },
      },
      from: process.env.EMAIL_FROM,
    }),
  ],
  
  // ============================================================================
  // SESSION CONFIGURATION
  // ============================================================================
  session: {
    // Strategy: "jwt" (default) or "database"
    strategy: "jwt",
    
    // Maximum age of the session (in seconds)
    maxAge: 30 * 24 * 60 * 60, // 30 days
    
    // Update age: how often to update the session expiration
    updateAge: 24 * 60 * 60, // 24 hours
    
    // Generate session ID function (for database strategy)
    // generateSessionToken: () => crypto.randomBytes(32).toString("hex"),
  },
  
  // ============================================================================
  // DATABASE ADAPTER (Optional - for database sessions)
  // ============================================================================
  // adapter: PrismaAdapter(prisma),
  // See: https://authjs.dev/getting-started/adapters
  
  // ============================================================================
  // CALLBACKS
  // ============================================================================
  callbacks: {
    // JWT Callback: Called when a JWT is created or updated
    async jwt({ token, user, trigger, session, account }) {
      // Initial sign in
      if (user) {
        token.id = user.id
        token.role = user.role || "user"
        token.avatar = user.image
      }
      
      // Handle session updates
      if (trigger === "update" && session) {
        token.name = session.user.name
        token.email = session.user.email
      }
      
      // Store OAuth access token
      if (account?.access_token) {
        token.accessToken = account.access_token
        token.refreshToken = account.refresh_token
        token.expiresAt = account.expires_at
      }
      
      return token
    },
    
    // Session Callback: Called when accessing the session
    async session({ session, token, user }) {
      // Add custom fields to session
      session.user.id = token.sub
      session.user.role = token.role as string
      session.user.avatar = token.avatar as string
      session.accessToken = token.accessToken as string
      
      return session
    },
    
    // Authorization Callback: Control access to routes
    async authorized({ auth, request }) {
      const isOnDashboard = request.nextUrl.pathname.startsWith("/dashboard")
      if (isOnDashboard) {
        if (auth?.user) return true
        return false
      }
      return true
    },
    
    // Sign In Callback: Validate sign in before redirect
    async signIn({ user, account, profile, email, credentials }) {
      // Allow all OAuth sign-ins
      if (account?.provider === "credentials") {
        // Custom validation for credentials
        return true
      }
      
      // Block sign in for certain email domains
      if (user.email?.endsWith("@blocked.com")) {
        return false
      }
      
      return true
    },
  },
  
  // ============================================================================
  // EVENTS
  // ============================================================================
  events: {
    async createUser({ user }) {
      console.log("New user created:", user.email)
      // Send welcome email, create default workspace, etc.
    },
    
    async signIn({ user, account, isNewUser }) {
      console.log("User signed in:", user.email, "isNewUser:", isNewUser)
      // Update last login timestamp
    },
    
    async signOut({ token }) {
      console.log("User signed out:", token.email)
      // Invalidate tokens, cleanup sessions, etc.
    },
  },
  
  // ============================================================================
  // EVENTS & HOOKS
  // ============================================================================
  // These are called at specific points in the auth flow
  
  // ============================================================================
  // COOKIE CONFIGURATION
  // ============================================================================
  cookies: {
    sessionToken: {
      name: `next-auth.session-token`,
      options: {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax" as const,
        path: "/",
        maxAge: 30 * 24 * 60 * 60, // 30 days
      },
    },
    callbackUrl: {
      name: `next-auth.callback-url`,
      options: {
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax" as const,
        path: "/",
        maxAge: 24 * 60 * 60, // 24 hours
      },
    },
    csrfToken: {
      name: `next-auth.csrf-token`,
      options: {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax" as const,
        path: "/",
        maxAge: 120, // 2 minutes
      },
    },
  },
  
  // ============================================================================
  // PAGE CUSTOMIZATION
  // ============================================================================
  pages: {
    signIn: "/login",
    signOut: "/logout",
    error: "/auth/error",
    verifyRequest: "/auth/verify",
    newUser: "/onboarding",
  },
  
  // ============================================================================
  // DEBUGGING
  // ============================================================================
  debug: process.env.NODE_ENV === "development",
}
```

## Provider-Specific Configurations

### GitHub OAuth

```typescript
// Environment variables
AUTH_GITHUB_ID=your-client-id
AUTH_GITHUB_SECRET=your-client-secret

// Setup: https://github.com/settings/developers
// Callback URL: http://localhost:3000/api/auth/callback/github
```

### Google OAuth

```typescript
// Environment variables
AUTH_GOOGLE_ID=your-client-id.apps.googleusercontent.com
AUTH_GOOGLE_SECRET=your-client-secret

// Setup: https://console.cloud.google.com/apis/credentials
// Authorized redirect URIs: http://localhost:3000/api/auth/callback/google
```

### Azure AD

```typescript
// Environment variables
AUTH_AZURE_AD_ID=your-client-id
AUTH_AZURE_AD_SECRET=your-client-secret
AUTH_AZURE_AD_TENANT_ID=your-tenant-id

// Setup: Azure Portal > App Registrations
// Reply URL: http://localhost:3000/api/auth/callback/azure-ad
```

### Credentials Provider

```typescript
// Custom validation against your backend
Credentials({
  name: "Credentials",
  credentials: {
    username: { label: "Username", type: "text" },
    password: { label: "Password", type: "password" },
  },
  async authorize(credentials) {
    // Call your backend API to verify credentials
    const response = await fetch(`${process.env.API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    })
    
    if (!response.ok) {
      throw new Error("Invalid credentials")
    }
    
    const user = await response.json()
    return {
      id: user.id,
      name: user.username,
      email: user.email,
      role: user.role,
    }
  },
})
```

### Email Provider

```typescript
// Environment variables
EMAIL_SERVER_HOST=smtp.gmail.com
EMAIL_SERVER_PORT=587
EMAIL_SERVER_USER=your-email@gmail.com
EMAIL_SERVER_PASSWORD=your-app-password
EMAIL_FROM=noreply@yourdomain.com

// Setup: Configure SMTP server
Email({
  server: {
    host: process.env.EMAIL_SERVER_HOST,
    port: Number(process.env.EMAIL_SERVER_PORT),
    auth: {
      user: process.env.EMAIL_SERVER_USER,
      pass: process.env.EMAIL_SERVER_PASSWORD,
    },
  },
  from: process.env.EMAIL_FROM,
})
```
