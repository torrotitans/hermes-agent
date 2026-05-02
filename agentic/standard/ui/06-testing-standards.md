# Torro UI Standards: 06. Testing Standards

<agent_instructions>
- Every new UI component MUST have an associated test file.
- Use `Vitest` + `React Testing Library` for unit/component tests.
- Use `Playwright` for high-criticality E2E flows.
</agent_instructions>

## 1. Testing Philosophy
Torro follows **Agent-Led Testing**. The AI agent is responsible for generating both the implementation AND the test suite simultaneously.

## 2. Component Testing (React Testing Library)

### 2.1 File Location
Test files MUST be co-located with the component:
`UI/src/features/feature-name/ui/my-component.test.tsx`

### 2.2 Selection Strategy
Avoid brittle CSS selectors. Prioritize:
1. `getByRole` (Accessibility-first)
2. `getByLabelText`
3. `getByPlaceholderText`
4. `getByTestId` (Only as a last resort)

### 2.3 Example Test Boilerplate
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './my-component';

describe('MyComponent', () => {
  it('renders correctly with default props', () => {
    render(<MyComponent title="Test Title" />);
    expect(screen.getByRole('heading', { name: /test title/i })).toBeInTheDocument();
  });

  it('triggers callback on click', () => {
    const handler = vi.fn();
    render(<MyComponent onClick={handler} />);
    fireEvent.click(screen.getByRole('button'));
    expect(handler).toHaveBeenCalledTimes(1);
  });
});
```

---

## 3. Unit Testing (Vitest)
Used for hooks, utilities, and pure functions.
- **Location**: `UI/src/features/feature-name/lib/my-utility.test.ts`

---

## 4. End-to-End Testing (Playwright)
Used for critical user journeys (Login, Data Onboarding, Lineage Workspace).
- **Location**: `UI/test/e2e/my-flow.spec.ts`

---

## 5. Testing DoD
- [ ] No `any` types in test files.
- [ ] Mocks are used for external API calls (`msw` or `vi.mock`).
- [ ] Test coverage includes happy paths AND edge cases (loading, error).
