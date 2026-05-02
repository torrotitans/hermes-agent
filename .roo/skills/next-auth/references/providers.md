# NextAuth.js v5 Provider Configuration Guide

## OAuth Provider Setup

### GitHub

**1. Create OAuth App**
- Go to: https://github.com/settings/developers
- New OAuth App
- Application name: Your App Name
- Homepage URL: https://yourdomain.com
- Authorization callback URL: https://yourdomain.com/api/auth/callback/github

**2. Environment Variables**
```bash
AUTH_GITHUB_ID=your-client-id
AUTH_GITHUB_SECRET=your-client-secret
```

**3. Configuration**
```typescript
import GitHub from "next-auth/providers/github"

providers: [
  GitHub({
    clientId: process.env.AUTH_GITHUB_ID,
    clientSecret: process.env.AUTH_GITHUB_SECRET,
    // Optional: Custom scopes
    authorization: { params: { scope: "read:user user:email" } },
  }),
]
```

---

### Google

**1. Create OAuth 2.0 Credentials**
- Go to: https://console.cloud.google.com/apis/credentials
- Create Credentials > OAuth 2.0 Client ID
- Application type: Web application
- Authorized JavaScript origins: https://yourdomain.com
- Authorized redirect URIs: https://yourdomain.com/api/auth/callback/google

**2. Environment Variables**
```bash
AUTH_GOOGLE_ID=your-client-id.apps.googleusercontent.com
AUTH_GOOGLE_SECRET=your-client-secret
```

**3. Configuration**
```typescript
import Google from "next-auth/providers/google"

providers: [
  Google({
    clientId: process.env.AUTH_GOOGLE_ID,
    clientSecret: process.env.AUTH_GOOGLE_SECRET,
  }),
]
```

---

### Azure Active Directory

**1. Register Application**
- Go to: https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps
- New registration
- Supported account types: Choose appropriate option
- Redirect URI: Platform configurations > Web > https://yourdomain.com/api/auth/callback/azure-ad

**2. Create Client Secret**
- Certificates & secrets > New client secret
- Copy the secret value (shown only once)

**3. Environment Variables**
```bash
AUTH_AZURE_AD_ID=your-application-id
AUTH_AZURE_AD_SECRET=your-client-secret
AUTH_AZURE_AD_TENANT_ID=your-tenant-id
```

**4. Configuration**
```typescript
import AzureAD from "next-auth/providers/azure-ad"

providers: [
  AzureAD({
    clientId: process.env.AUTH_AZURE_AD_ID,
    clientSecret: process.env.AUTH_AZURE_AD_SECRET,
    tenantId: process.env.AUTH_AZURE_AD_TENANT_ID,
  }),
]
```

---

### Okta

**1. Create OAuth 2.0 Application**
- Go to: https://developer.okta.com/
- Applications > New Application
- Platform: Web
- Sign-in redirect URI: https://yourdomain.com/api/auth/callback/okta
- Sign-out redirect URI: https://yourdomain.com/logout

**2. Environment Variables**
```bash
AUTH_OKATA_ID=your-client-id
AUTH_OKATA_SECRET=your-client-secret
AUTH_OKATA_ISSUER=https://your-domain.okta.com/oauth2/default
```

**3. Configuration**
```typescript
import Okta from "next-auth/providers/okta"

providers: [
  Okta({
    clientId: process.env.AUTH_OKATA_ID,
    clientSecret: process.env.AUTH_OKATA_SECRET,
    issuer: process.env.AUTH_OKATA_ISSUER,
  }),
]
```

---

### Auth0

**1. Create Application**
- Go to: https://manage.auth0.com/
- Applications > Create Application
- Application type: Regular Web Application
- Settings:
  - Allowed Callback URLs: https://yourdomain.com/api/auth/callback/auth0
  - Allowed Logout URLs: https://yourdomain.com

**2. Environment Variables**
```bash
AUTH_AUTH0_ID=your-client-id
AUTH_AUTH0_SECRET=your-client-secret
AUTH_AUTH0_ISSUER=https://your-domain.auth0.com/
```

**3. Configuration**
```typescript
import Auth0 from "next-auth/providers/auth0"

providers: [
  Auth0({
    clientId: process.env.AUTH_AUTH0_ID,
    clientSecret: process.env.AUTH_AUTH0_SECRET,
    issuer: process.env.AUTH_AUTH0_ISSUER,
  }),
]
```

---

## Credentials Provider

**1. Configuration**
```typescript
import Credentials from "next-auth/providers/credentials"
import { z } from "zod"

const LoginSchema = z.object({
  username: z.string(),
  password: z.string().min(1, "Password is required"),
})

providers: [
  Credentials({
    name: "Credentials",
    credentials: {
      username: { label: "Username", type: "text", placeholder: "jsmith" },
      password: { label: "Password", type: "password" },
    },
    async authorize(credentials) {
      // Validate schema
      const validated = LoginSchema.safeParse(credentials)
      
      if (!validated.success) {
        throw new Error("Invalid credentials format")
      }
      
      // Call your backend API to verify credentials
      const response = await fetch(`${process.env.API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(validated.data),
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || "Invalid credentials")
      }
      
      const user = await response.json()
      
      return {
        id: user.id.toString(),
        name: user.username,
        email: user.email,
        role: user.role,
        image: user.avatar,
      }
    },
  }),
]
```

**2. Login Form Component**
```typescript
"use client"

import { signIn } from "@/auth"
import { useFormStatus } from "react-dom"

export function LoginForm() {
  async function handleSubmit(formData: FormData) {
    try {
      await signIn("credentials", {
        username: formData.get("username"),
        password: formData.get("password"),
        redirectTo: "/dashboard",
      })
    } catch (error) {
      // Handle error
      console.error("Login failed:", error)
    }
  }

  return (
    <form action={handleSubmit}>
      <input name="username" type="text" placeholder="Username" required />
      <input name="password" type="password" placeholder="Password" required />
      <button type="submit">Sign In</button>
    </form>
  )
}
```

---

## Email Provider (Passwordless)

**1. SMTP Configuration**
```bash
EMAIL_SERVER_HOST=smtp.gmail.com
EMAIL_SERVER_PORT=587
EMAIL_SERVER_USER=your-email@gmail.com
EMAIL_SERVER_PASSWORD=your-app-password
EMAIL_FROM=noreply@yourdomain.com
```

**2. Configuration**
```typescript
import Email from "next-auth/providers/nodemailer"

providers: [
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
]
```

**3. Custom Email Template**
```typescript
import Email from "next-auth/providers/nodemailer"

providers: [
  Email({
    // ... SMTP config
    sendVerificationRequest: async ({ identifier, url, provider }) => {
      // Custom email logic
      await sendEmail({
        to: identifier,
        subject: "Sign in to Your App",
        html: `
          <h1>Sign In</h1>
          <p>Click <a href="${url}">here</a> to sign in.</p>
          <p>This link expires in 24 hours.</p>
        `,
      })
    },
  }),
]
```

---

## Custom OAuth Provider

```typescript
import { OAuthConfig, OAuthConfigBase } from "next-auth"

interface CustomProviderConfig extends OAuthConfigBase {
  // Custom fields
  customField?: string
}

const CustomProvider = (options: CustomProviderConfig) => {
  return {
    id: "custom",
    name: "Custom Provider",
    type: "oauth" as const,
    authorization: {
      url: "https://custom-provider.com/oauth/authorize",
      params: { scope: "read write" },
    },
    token: "https://custom-provider.com/oauth/token",
    userinfo: "https://custom-provider.com/api/user",
    clientId: options.clientId,
    clientSecret: options.clientSecret,
    async profile(profile) {
      return {
        id: profile.id,
        name: profile.name,
        email: profile.email,
        image: profile.avatar_url,
      }
    },
    ...options,
  }
}
```

---

## Provider Ordering and Priority

```typescript
providers: [
  // Order matters! First provider is shown first in default UI
  GitHub({ /* config */ }),
  Google({ /* config */ }),
  Credentials({ /* config */ }),
  Email({ /* config */ }),
]
```

## Provider-Specific Features

### GitHub
- Organization membership check
- Team-based access control
- Repository permissions

### Google
- Google Workspace (G Suite) support
- Domain restriction
- Google Drive/Calendar integration

### Azure AD
- Group membership
- Custom security claims
- Conditional access policies

### Okta
- Group-based authorization
- Lifecycle management
- MFA enforcement

### Auth0
- Rules and actions
- Custom database connections
- Social connection management
