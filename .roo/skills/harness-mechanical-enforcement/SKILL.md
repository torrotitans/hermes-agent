---
name: harness-mechanical-enforcement
description: Implement mechanical enforcement for AI agent development including custom linter rules, structure tests, and embedded fix instructions
---

# Mechanical Enforcement Skill

## When to Use This Skill

Use this skill when:
- Setting up automated code quality enforcement
- Creating self-correcting feedback loops for agents
- Establishing architectural boundaries
- Implementing coding standards that agents must follow

## When NOT to Use This Skill

Do NOT use this skill when:
- Project is exploratory with evolving requirements
- Team prefers human code review over automated checks
- Enforcement would block legitimate experimentation

## Core Principle

**Documentation decays. Lint rules do not.**

Mechanical enforcement provides invariant guardians that execute consistently, unlike human memory or written documentation.

## Two Categories of Constraints

### Architecture Constraints (Structure Tests)

Enforce structural boundaries:

1. **Domain Layering**: Types → Config → Repo → Service → Runtime → UI
2. **Dependency Direction**: Dependencies flow forward only
3. **Cross-Cutting Concerns**: Must enter through Providers
4. **Violation Response**: Block CI/CD merge

### Taste Invariants (Custom Linter)

Enforce coding standards:

1. **Structured Logging**: Prohibit bare `console.log` output
2. **Naming Conventions**: Schema/type naming standards
3. **File Size Limits**: Maximum lines per file
4. **Platform Requirements**: Platform-specific reliability needs

## Workflow

### Step 1: Design Lint Rules

Create rules that enforce taste invariants:

1. Identify recurring code patterns that need standardization
2. Define clear pass/fail criteria for each rule
3. Document the rationale behind each rule

Example rules:

```javascript
// Rule: No bare console.log
// Rationale: Structured logging enables agent-readable telemetry
// Error: "Use logger.info() instead of console.log()"

// Rule: File size limit 500 lines
// Rationale: Files >500 lines are hard for agents to parse
// Error: "File exceeds 500 lines. Split into domain modules."
```

### Step 2: Implement Lint Rules

Create custom linter configuration:

1. Install required linting tools (ESLint, Pylint, etc.)
2. Create custom rules for domain-specific constraints
3. Configure rule severity (error vs warning)

Example ESLint configuration:

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'no-console': 'error',
    'max-lines': ['error', { max: 500 }],
    'require-logger-prefix': 'error'
  }
};
```

### Step 3: Embed Fix Instructions

Design error messages that enable self-correction:

**Bad Error Message:**
```
Error: File exceeds 500 lines.
```

**Good Error Message:**
```
Error: File exceeds 500 lines.
Fix: Split into domain-specific modules following docs/ARCHITECTURE.md#splitting-guide.
Consider extracting types to <domain>/types/ and service logic to <domain>/service/.
```

### Step 4: Configure CI Integration

Set up automated enforcement:

1. Add lint step to CI pipeline
2. Configure branch protection rules
3. Set up status checks for merge requirements

Example GitHub Actions:

```yaml
# .github/workflows/lint.yml
name: Lint Check
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm run lint
```

### Step 5: Implement Structure Tests

Create tests for architectural constraints:

1. Use tools like `dependency-cruiser` or `archunit`
2. Define allowed dependency patterns
3. Fail build on violation

Example dependency-cruiser config:

```javascript
// dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: 'no-service-to-ui',
      severity: 'error',
      from: { path: 'service/' },
      to: { path: 'ui/' }
    }
  ]
};
```

### Step 6: Set Up Auto-Fix

Configure automated fixing where possible:

1. Enable `--fix` flag for auto-fixable issues
2. Create agent tasks to handle complex fixes
3. Set up scheduled lint-fix runs

## Key Metrics

| Metric | Target |
|--------|--------|
| Lint rule coverage | 100% of critical paths |
| Auto-fix rate | >80% of violations |
| CI lint time | <2 minutes |
| False positive rate | <1% |

## Related Skills

- [`harness-engineering-overview`](harness-engineering-overview/SKILL.md) - Overview of all Harness Engineering concepts
- [`harness-repo-as-truth`](harness-repo-as-truth/SKILL.md) - Documentation structure
- [`harness-agent-readability`](harness-agent-readability/SKILL.md) - Code optimization for agents

## Troubleshooting

### Problem: Too many lint rules slow down development

**Solution:** Prioritize rules by impact. Start with critical architecture rules, add taste rules gradually.

### Problem: Agents can't understand error messages

**Solution:** Simplify error language. Include file paths and line numbers. Provide concrete fix examples.

### Problem: CI becomes bottleneck

**Solution:** Run lint locally before commit. Use incremental linting. Parallelize independent checks.

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [ESLint Custom Rules](https://eslint.org/docs/developer-guide/working-with-rules)
