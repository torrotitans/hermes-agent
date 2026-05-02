#!/bin/bash
# NextAuth.js v5 Setup Script
# This script helps set up NextAuth.js v5 in a Next.js project

set -e

echo "=========================================="
echo "NextAuth.js v5 Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="${1:-.}"

echo -e "${GREEN}Step 1: Installing dependencies...${NC}"
npm install next-auth@beta

echo -e "${GREEN}Step 2: Creating directory structure...${NC}"
mkdir -p "${PROJECT_ROOT}/app/api/auth/[...nextauth]"
mkdir -p "${PROJECT_ROOT}/app/login"
mkdir -p "${PROJECT_ROOT}/app/dashboard"

echo -e "${GREEN}Step 3: Creating auth configuration files...${NC}"

# Create auth.config.ts
cat > "${PROJECT_ROOT}/auth.config.ts" << 'EOF'
import type { NextAuthConfig } from "next-auth"
import GitHub from "next-auth/providers/github"
import Credentials from "next-auth/providers/credentials"

export const authConfig: NextAuthConfig = {
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Credentials({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Implement your credential validation here
        // This is a placeholder - replace with your actual auth logic
        if (!credentials?.username || !credentials?.password) {
          return null
        }
        // Call your backend API to verify credentials
        const response = await fetch(`${process.env.API_URL}/auth/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(credentials),
        })
        const user = await response.json()
        if (response.ok && user) return user
        return null
      },
    }),
  ],
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
        token.role = user.role || "user"
      }
      return token
    },
    async session({ session, token }) {
      session.user.id = token.sub
      session.user.role = token.role as string
      return session
    },
  },
}
EOF

echo -e "${GREEN}Step 4: Creating main auth entry point...${NC}"

# Create auth.ts
cat > "${PROJECT_ROOT}/auth.ts" << 'EOF'
import NextAuth from "next-auth"
import { authConfig } from "./auth.config"

export const { handlers, signIn, signOut, auth } = NextAuth(authConfig)
EOF

echo -e "${GREEN}Step 5: Creating API route handler...${NC}"

# Create route handler
cat > "${PROJECT_ROOT}/app/api/auth/[...nextauth]/route.ts" << 'EOF'
import { handlers } from "@/auth"

export const { GET, POST } = handlers
EOF

echo -e "${GREEN}Step 6: Creating middleware...${NC}"

# Create middleware
cat > "${PROJECT_ROOT}/middleware.ts" << 'EOF'
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith("/dashboard")
  
  if (isOnDashboard && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl))
  }
  
  if (req.nextUrl.pathname === "/login" && isLoggedIn) {
    return Response.redirect(new URL("/dashboard", req.nextUrl))
  }
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
EOF

echo -e "${GREEN}Step 7: Creating login page...${NC}"

# Create login page
cat > "${PROJECT_ROOT}/app/login/page.tsx" << 'EOF'
"use client"

import { signIn } from "@/auth"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        
        <div className="mt-8 space-y-6">
          <form
            action={async () => {
              "use server"
              await signIn("github", { redirectTo: "/dashboard" })
            }}
            className="space-y-4"
          >
            <button
              type="submit"
              className="flex w-full justify-center rounded-md border border-transparent bg-gray-800 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Sign in with GitHub
            </button>
          </form>
          
          <form
            action={async () => {
              "use server"
              await signIn("credentials", { redirectTo: "/dashboard" })
            }}
            className="space-y-4"
          >
            <input name="username" type="text" placeholder="Username" className="w-full rounded-md border border-gray-300 px-4 py-2" />
            <input name="password" type="password" placeholder="Password" className="w-full rounded-md border border-gray-300 px-4 py-2" />
            <button
              type="submit"
              className="flex w-full justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Sign in with Credentials
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
EOF

echo -e "${GREEN}Step 8: Creating environment template...${NC}"

# Create .env.local.template
cat > "${PROJECT_ROOT}/.env.local.template" << 'EOF'
# NextAuth Secret (generate with: openssl rand -base64 32)
AUTH_SECRET=your-secret-key-here

# Trust proxy headers (for production behind reverse proxy)
AUTH_TRUST_HOST=true

# GitHub OAuth
AUTH_GITHUB_ID=your-github-client-id
AUTH_GITHUB_SECRET=your-github-client-secret

# API URL for credential verification
API_URL=http://localhost:3000
EOF

echo -e "${GREEN}Step 9: Creating TypeScript types...${NC}"

# Create type definitions
cat > "${PROJECT_ROOT}/types/next-auth.d.ts" << 'EOF'
import NextAuth from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
    } & Session["user"]
  }
  
  interface User {
    id: string
    role: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string
    role: string
  }
}
EOF

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Copy .env.local.template to .env.local and fill in your credentials"
echo "2. Generate a secret: openssl rand -base64 32"
echo "3. Run your Next.js development server: npm run dev"
echo "4. Visit http://localhost:3000/login to test authentication"
echo ""
echo "Documentation:"
echo "- Auth Config: ./auth.config.ts"
echo "- Middleware: ./middleware.ts"
echo "- Login Page: ./app/login/page.tsx"
echo ""
