---
name: turborepo-nextjs
description: Configure and use Turborepo for monorepo build orchestration with Next.js projects, including task caching, remote caching, and workspace management
---

# Turborepo for Next.js Monorepos

## When to use this skill

Use this skill when:
- Setting up a **monorepo** with multiple Next.js applications or packages
- Needing **faster builds** through task caching and parallel execution
- Managing **shared dependencies** across multiple Next.js projects
- Configuring **remote caching** for CI/CD pipelines
- Orchestrating build tasks across Next.js, backend services, and libraries
- Working with **pnpm workspaces**, npm workspaces, or Yarn workspaces

## When NOT to use this skill

- For **single Next.js projects** without monorepo needs (use `nextjs-enterprise` instead)
- For **Next.js-specific features** like App Router, Server Components, or Next.js configuration (use `nextjs-agentic` or `nextjs-enterprise`)
- For **deployment** of Next.js apps (use appropriate deployment skill)

## Inputs required

- Monorepo root directory path
- Package manager preference (pnpm, npm, or yarn)
- List of Next.js apps and shared packages in the monorepo
- Remote caching preference (Vercel or self-hosted)

## Workflow

### 1. Initialize Turborepo in existing monorepo

```bash
# Install Turborepo as dev dependency
pnpm add -D turborepo
# or
npm install -D turborepo
# or
yarn add -D turborepo

# Initialize Turborepo configuration
npx turborepo init
```

This creates:
- `turbo.json` - Turborepo pipeline configuration
- Updates `package.json` with turbo scripts

### 2. Configure turbo.json pipeline

Define task dependencies and caching behavior:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"],
      "env": ["NEXT_PUBLIC_*"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

Key configuration options:
- `dependsOn`: Task dependencies (`^` prefix = dependencies in other packages)
- `outputs`: Cached build artifacts
- `env`: Environment variables that affect task output
- `cache`: Enable/disable caching for specific tasks

### 3. Configure workspace packages

For pnpm workspaces (recommended):

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

For npm workspaces:

```json
// package.json
{
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}
```

### 4. Structure Next.js apps and shared packages

Recommended monorepo structure:

```
monorepo/
├── apps/
│   ├── web/              # Next.js application
│   │   ├── package.json
│   │   ├── next.config.js
│   │   └── src/
│   └── admin/            # Another Next.js app
│       ├── package.json
│       └── src/
├── packages/
│   ├── ui/               # Shared React components
│   │   └── package.json
│   ├── config/           # Shared ESLint, TypeScript configs
│   │   └── package.json
│   └── utils/            # Shared utilities
│       └── package.json
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

### 5. Run Turborepo commands

```bash
# Build all Next.js apps and their dependencies
pnpm turbo build

# Build specific app with dependencies
pnpm turbo build --filter=web

# Build with remote cache
pnpm turbo build --remote-cache

# Development mode (parallel across packages)
pnpm turbo dev

# Run lint across all packages
pnpm turbo lint

# Run tests with build dependency
pnpm turbo test

# View task graph
pnpm turbo run build --graph

# Clean cache
pnpm turbo daemon clean
```

### 6. Configure remote caching (Vercel)

```bash
# Link to Vercel for remote caching
npx turbo login
npx turbo link

# Or configure via environment variables
# TURBO_TEAM=your-team
# TURBO_TOKEN=your-token
```

Alternative: Self-hosted remote cache using HTTP endpoint.

### 7. Optimize for Next.js specific needs

Configure Next.js build outputs in `turbo.json`:

```json
{
  "tasks": {
    "build": {
      "outputs": [
        ".next/**",
        "!.next/cache/**",
        "out/**"
      ],
      "env": [
        "NEXT_PUBLIC_*",
        "NODE_ENV",
        "VERCEL_*"
      ]
    }
  }
}
```

## Examples

### Example 1: Basic Next.js monorepo setup

```bash
# Create monorepo structure
mkdir my-turborepo && cd my-turborepo
pnpm init
pnpm add -D turborepo

# Create workspace config
echo 'packages:
  - "apps/*"
  - "packages/*"' > pnpm-workspace.yaml

# Create turbo.json
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
EOF

# Create Next.js app
pnpm dlx create-next-app@latest apps/web
```

### Example 2: Shared UI package with Next.js

```bash
# Create shared UI package
mkdir -p packages/ui/src
cat > packages/ui/package.json << 'EOF'
{
  "name": "@myorg/ui",
  "version": "1.0.0",
  "main": "./src/index.tsx",
  "peerDependencies": {
    "react": "^18.0.0"
  }
}
EOF
```

## Troubleshooting

### Cache not working for Next.js builds

**Problem**: Next.js builds not being cached properly

**Solution**: Ensure `.next` outputs are correctly specified:
```json
"outputs": [".next/**", "!.next/cache/**"]
```

The `!.next/cache/**` exclusion prevents caching the webpack cache which can cause issues.

### Environment variables not picked up

**Problem**: `NEXT_PUBLIC_*` variables not available during build

**Solution**: Add to `turbo.json`:
```json
"env": ["NEXT_PUBLIC_*", "NODE_ENV"]
```

### Circular dependency errors

**Problem**: Turborepo detects circular dependencies between packages

**Solution**: Restructure packages to eliminate circular dependencies. Use `^` prefix correctly in `dependsOn`.

### Remote cache authentication failed

**Problem**: Unable to connect to Vercel remote cache

**Solution**:
```bash
npx turbo login
npx turbo link
# Or set environment variables
export TURBO_TEAM=your-team
export TURBO_TOKEN=your-token
```

## Related skills

- [`nextjs-enterprise`](../nextjs-enterprise/SKILL.md) - Next.js best practices and configuration
- [`nextjs-agentic`](../nextjs-agentic/SKILL.md) - Next.js security and testing
