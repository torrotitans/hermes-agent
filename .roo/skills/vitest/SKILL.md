---
name: vitest
description: Write, maintain, and improve Vitest tests including unit tests, integration tests, component tests, mocking, coverage, and Browser Mode for end-to-end testing using the Vitest framework
license: MIT
compatibility:
  - node-20.0+
  - vite-6.0+
  - vitest-2.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://github.com/vitest-dev/vitest
---

# Vitest Testing Skill

## When to Use This Skill

Use this skill when you need to:
- Write unit tests with Vitest (`describe`, `it`, `test`, `expect`)
- Configure Vitest in `vitest.config.ts`
- Implement mocking with `vi.fn()`, `vi.mock()`, `vi.spyOn()`
- Use Chai assertions (built-in) or Jest-compatible `expect` APIs
- Set up code coverage with V8 or Istanbul
- Write snapshot tests
- Run component tests in the browser (Browser Mode)
- Configure test environments (jsdom, happy-dom, node)
- Implement watch mode and test filtering
- Write integration tests with real dependencies
- Benchmark tests with `bench`

## When NOT to Use This Skill

Do NOT use this skill when:
- Writing Playwright/E2E tests (use `playwright-test-generator` skill)
- Writing Jest tests without Vitest (use Jest skill)
- Setting up CI/CD pipelines (use DevOps skill)
- Writing backend API tests without Vitest framework

## Inputs Required

Before starting, ensure you have:
1. Vitest version (default: v2.x+)
2. Test type (unit, integration, component, E2E)
3. Test environment (node, jsdom, happy-dom, browser)
4. Coverage requirements (V8, Istanbul)

## Workflow

### Step 1: Basic Test Structure

```typescript
import { describe, expect, it, vi } from 'vitest'
import { add, multiply } from './math'

describe('math module', () => {
  it('should add two numbers', () => {
    expect(add(1, 2)).toBe(3)
    expect(add(-1, 1)).toBe(0)
  })

  it('should multiply two numbers', () => {
    expect(multiply(2, 3)).toBe(6)
    expect(multiply(0, 5)).toBe(0)
  })
})
```

### Step 2: Use Chai Assertions

Vitest includes Chai with Jest-compatible APIs:

```typescript
import { describe, expect, it } from 'vitest'

describe('assertions', () => {
  it('should use Chai style', () => {
    const user = { name: 'John', age: 30 }
    
    // Jest-style
    expect(user.name).toBe('John')
    expect(user.age).toBeGreaterThan(25)
    
    // Chai-style
    expect(user).toHaveProperty('name')
    expect([1, 2, 3]).to.include.members([1, 2])
    expect({ foo: 'bar' }).to.deep.equal({ foo: 'bar' })
  })
})
```

### Step 3: Mocking with vi

```typescript
import { describe, expect, it, vi } from 'vitest'
import { fetchData } from './api'

describe('fetchData', () => {
  it('should mock a function', async () => {
    const mockFn = vi.fn(() => Promise.resolve({ data: 'test' }))
    vi.mock('./api', () => ({ fetchData: mockFn }))
    
    const result = await fetchData()
    expect(mockFn).toHaveBeenCalledTimes(1)
    expect(result).toEqual({ data: 'test' })
  })

  it('should spy on a method', () => {
    const obj = {
      getValue: () => 42,
    }
    const spy = vi.spyOn(obj, 'getValue')
    
    obj.getValue()
    expect(spy).toHaveBeenCalledTimes(1)
    expect(spy).toHaveReturnedWith(42)
  })

  it('should mock timers', () => {
    vi.useFakeTimers()
    const callback = vi.fn()
    
    setTimeout(callback, 1000)
    vi.advanceTimersByTime(1000)
    
    expect(callback).toHaveBeenCalledTimes(1)
    vi.useRealTimers()
  })
})
```

### Step 4: Async Tests

```typescript
import { describe, expect, it } from 'vitest'
import { delay } from './utils'

describe('async tests', () => {
  it('should handle promises', async () => {
    const result = await delay(100).then(() => 'done')
    expect(result).toBe('done')
  })

  it('should reject', async () => {
    await expect(delay(100).then(() => { throw new Error('fail') }))
      .rejects.toThrow('fail')
  })

  it('should use top-level await', async () => {
    const result = await delay(50).then(() => 'resolved')
    expect(result).toBe('resolved')
  })
})
```

### Step 5: Snapshot Testing

```typescript
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import Component from './Component'

describe('Component', () => {
  it('should match snapshot', () => {
    const { container } = render(<Component />)
    expect(container.innerHTML).toMatchSnapshot()
  })

  it('should update snapshot', () => {
    const { container } = render(<Component updated={true} />)
    expect(container.innerHTML).toMatchSnapshot({ timestamp: expect.any(Number) })
  })
})
```

### Step 6: Test Hooks

```typescript
import { describe, expect, it, vi, beforeEach, afterEach, beforeAll, afterAll } from 'vitest'

describe('hooks', () => {
  beforeAll(() => {
    // Run once before all tests
    console.log('Setup all tests')
  })

  afterAll(() => {
    // Run once after all tests
    console.log('Cleanup all tests')
  })

  beforeEach(() => {
    // Run before each test
    vi.clearAllMocks()
  })

  afterEach(() => {
    // Run after each test
    vi.restoreAllMocks()
  })

  it('test 1', () => {
    expect(true).toBe(true)
  })
})
```

### Step 7: Test Filtering and Concurrency

```typescript
import { describe, expect, it } from 'vitest'

describe('filtering', () => {
  it.skip('should be skipped', () => {
    // This test is skipped
  })

  it.only('should run only this', () => {
    // Only this test runs
  })

  it('should run with timeout', { timeout: 5000 }, () => {
    // Custom timeout for this test
    expect(true).toBe(true)
  })

  it('should run in sequence', { sequential: true }, () => {
    // Runs after previous sequential tests
  })
})
```

### Step 8: Coverage Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/main.ts',
        '**/*.d.ts',
      ],
    },
  },
})
```

### Step 9: Browser Mode (Component Tests)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      name: 'chromium', // or 'firefox', 'webkit'
      provider: 'playwright',
      headless: true,
    },
  },
})
```

```typescript
// Component.test.tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import Component from './Component'

describe('Component', () => {
  it('should render', () => {
    render(<Component />)
    expect(screen.getByRole('button')).toBeInTheDocument()
  })
})
```

### Step 10: Benchmarking

```typescript
import { bench, describe, expect } from 'vitest'

describe('benchmarks', () => {
  bench('string concat', () => {
    'hello' + ' ' + 'world'
  })

  bench('template literal', () => {
    `hello world`
  })

  bench('Array.join', () => {
    ['hello', 'world'].join(' ')
  })
})
```

## Files Reference

| File | Purpose |
|------|---------|
| `vitest.config.ts` | Test configuration |
| `packages/vitest/src/public/index.ts` | Public API exports |
| `packages/expect/src/` | Assertion library |
| `packages/runner/src/` | Test runner |

## Troubleshooting

### Issue: Module Not Found

**Symptom**: `Cannot find module 'vitest'`

**Solution**:
- Install Vitest: `npm install -D vitest`
- Verify `vitest` is in devDependencies
- Check `package.json` scripts include `"test": "vitest"`

### Issue: Tests Not Running

**Symptom**: `No test files found`

**Solution**:
- Check file naming: `*.test.ts` or `*.spec.ts`
- Verify `test.include` in config
- Run with explicit path: `vitest src/components/Button.test.ts`

### Issue: Mock Not Working

**Symptom**: `vi.mock() not hoisting`

**Solution**:
- Use `vi.mock()` at top level (auto-hoisted)
- Or use `vi.hoisted()` for runtime mocks
- Ensure module path is relative to test file

## Examples

### Example 1: Testing React Component

```typescript
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import Button from './Button'

describe('Button', () => {
  it('should call onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Example 2: Testing API Service

```typescript
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { apiService } from './api'

describe('apiService', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('should fetch data', async () => {
    const mockData = [{ id: 1, name: 'Test' }]
    vi.spyOn(global, 'fetch').mockResolvedValue({
      json: () => Promise.resolve(mockData),
    } as Response)
    
    const result = await apiService.getData()
    expect(result).toEqual(mockData)
  })
})
```

## Related Resources

- [Vitest Documentation](https://vitest.dev/)
- [Vitest API Reference](https://vitest.dev/api/)
- [Vitest Examples](https://github.com/vitest-dev/vitest/tree/main/examples)
