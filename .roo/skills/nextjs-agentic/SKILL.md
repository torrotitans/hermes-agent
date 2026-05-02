---
name: nextjs-agentic
description: Next.js agentic skills for security, testing, and AI-assisted development including Server Actions security, Vitest/RTL unit testing, Playwright E2E, and AI coding agent guardrails
---

# Next.js Agentic Skills (Security + Testing Focus)

Goal: maximize ease of build, security, and low maintenance while preserving innovation speed.

## When to use
- When developing Next.js applications with security requirements
- When implementing Server Actions or Route Handlers
- When setting up unit tests with Vitest + React Testing Library
- When implementing E2E tests with Playwright
- When configuring AI coding agent guardrails and quality gates

## When NOT to use
- For backend Python/Flask development (use `backend-architecture` or `backend-coding-standards` skills instead)
- For backend testing (use `backend-testing` skill instead)

## Inputs required
- Next.js feature or component to implement
- Security requirements (if applicable)
- Test coverage goals

## Testing Stack Decision

- **Unit/Integration tests:** use **Vitest + React Testing Library** as the default.
- **E2E and browser-flow tests:** use **Playwright**.
- **Answer to "is Playwright best fit?":** best fit for **E2E** in Next.js, not as the primary unit test runner.

## Tier 1 Security Skills (Highest Priority)

### 1. Server-First Trust Boundary Design
- Keep sensitive logic in Server Components, Route Handlers, and Server Actions.
- Enforce strict client/server data boundaries to prevent secret leakage.

### 2. Server Actions Endpoint Security
- Treat every Server Action as a public endpoint.
- Validate authz on every mutation and configure `serverActions.allowedOrigins` where needed.

### 3. Authentication, Session, and Authorization Layering
- Centralize auth checks in a Data Access Layer and session utilities.
- Use optimistic route checks plus secure data-source checks for privileged operations.

### 4. CSP and Response Header Hardening
- Deploy strict CSP with nonce strategy where required.
- Standardize headers for clickjacking/XSS/injection mitigation.

### 5. Input Validation and Output Minimization
- Validate all external input with schemas (Zod or equivalent).
- Return least-privilege DTOs to minimize exposed data.

### 6. Secure Cookies and CSRF Defense
- Enforce `httpOnly`, `secure`, and `sameSite` cookie policies.
- Preserve POST-only mutation patterns and origin checks for anti-CSRF protection.

### 7. Dependency and Supply Chain Security
- Pin dependencies, scan CVEs in CI, and fail builds for critical issues.
- Require signed releases and controlled upgrade playbooks.

### 8. Security Regression Testing
- Add automated tests for authz bypass, direct API access, and privilege escalation paths.
- Keep a security test checklist for every feature touching sensitive data.

## Tier 1.5 Unit Testing Skills (Highest Priority)

### 9. Unit Test Architecture (Vitest-First)
- Separate pure domain logic from framework plumbing for fast deterministic tests.
- Target high coverage on business rules, parsers, and permission logic.

### 10. Component Testing with RTL
- Test user-observable behavior, not implementation details.
- Cover loading/error/empty states and accessibility semantics.

### 11. Async Server Component Test Strategy
- Unit test synchronous logic directly.
- For async Server Component flows, prefer E2E validation to avoid unsupported edges.

### 12. Contract Tests for Route Handlers and Server Actions
- Validate status codes, auth checks, schema failures, and payload contracts.
- Ensure idempotency and predictable error mapping.

### 13. Fast Feedback Test Pipeline
- Run unit tests in pre-commit and full suites in CI.
- Quarantine flaky tests with owner and expiry metadata.

## Tier 2 Agent-Native Productivity Skills

### 14. AI Coding Agent Guardrails
- Maintain `AGENTS.md` with mandatory checks: lint, typecheck, unit, E2E, security scan.
- Provide reusable prompt templates for feature, refactor, and hotfix tasks.

### 15. MCP-Enabled Debug and Runtime Introspection
- Configure Next.js MCP for docs/runtime error lookup and safe diagnostics.
- Default to read-only diagnostic flows unless mutation is required.

### 16. Code Generation Quality Gates
- Reject generated code that bypasses auth checks or test coverage requirements.
- Enforce duplication controls and architecture boundaries.

## Tier 3 Delivery and Innovation Skills

### 17. Playwright E2E Coverage by Risk
- Use Playwright for login, checkout, permissions, and critical workflows.
- Run smoke tests on every PR and broader matrix tests nightly.

### 18. Performance and Rendering Controls
- Use streaming, suspense boundaries, and caching intentionally.
- Track route-level budgets and regressions in CI.

### 19. Safe Experimentation and Rollback
- Use feature flags and staged rollouts.
- Keep one-click rollback paths and observable blast-radius controls.

### 20. Upgrade Automation and Maintenance Discipline
- Use `@next/codemod` for framework upgrades.
- Schedule recurring dependency, runtime, and security baseline refreshes.

## Recommended Adoption Order

1. Skills 1-8 (security baseline)
2. Skills 9-13 (unit testing baseline)
3. Skills 14-16 (agent productivity controls)
4. Skills 17-20 (E2E scale and innovation)

## Examples

**Secure Server Action Pattern:**
```typescript
// app/actions/secure-action.ts
'use server'

import { z } from 'zod'
import { getCurrentUser } from '@/lib/auth'

const ActionSchema = z.object({
  data: z.string().min(1),
})

export async function secureAction(input: z.infer<typeof ActionSchema>) {
  // Validate input
  const validated = ActionSchema.parse(input)
  
  // Check authorization
  const user = await getCurrentUser()
  if (!user) {
    throw new Error('Unauthorized')
  }
  
  // Process securely on server
  return { success: true }
}
```

**Vitest + RTL Component Test:**
```typescript
// __tests__/component.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('renders loading state', () => {
    render(<MyComponent loading={true} />)
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    render(<MyComponent />)
    const button = screen.getByRole('button')
    await fireEvent.click(button)
    expect(screen.getByText(/clicked/i)).toBeInTheDocument()
  })
})
```

**Playwright E2E Test:**
```typescript
// e2e/login.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Login Flow', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    
    await expect(page).toHaveURL('/dashboard')
  })
})
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Server Action exposes secrets | Move sensitive logic to server-only code; validate on server |
| Playwright used for unit tests | Switch to Vitest + RTL for unit tests; reserve Playwright for E2E |
| Missing CSP headers | Configure CSP with nonce strategy in Next.js config |
| Flaky tests in CI | Quarantine with owner/expiry metadata; investigate root cause |
| Generated code bypasses auth | Add quality gate to reject code without auth checks |
| Server Component async issues | Use E2E validation for async flows instead of unit tests |
