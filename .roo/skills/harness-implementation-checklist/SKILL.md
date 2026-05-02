---
name: harness-implementation-checklist
description: Practical implementation checklist for Harness Engineering adoption including setup steps, validation criteria, and troubleshooting guide
---

# Harness Implementation Checklist Skill

## When to Use This Skill

Use this skill when:
- Starting Harness Engineering adoption for a new project
- Assessing current project's Harness readiness
- Planning incremental implementation steps
- Validating implementation completeness

## When NOT to Use This Skill

Do NOT use this skill when:
- Project doesn't use AI coding agents
- Team is not committed to constraint-based development
- Timeline doesn't allow for infrastructure setup

## Implementation Phases

### Phase 1: Foundation Setup (Week 1-2)

**Goal:** Establish basic Harness Engineering infrastructure

#### Checklist

- [ ] **Create AGENTS.md**
  - Location: Repository root
  - Constraint: Under 100 lines
  - Content: Navigation only, not encyclopedia

- [ ] **Create ARCHITECTURE.md**
  - Document domain boundaries
  - Define layer structure
  - Show dependency flow

- [ ] **Set up docs/ directory**
  - Create `docs/design-docs/`
  - Create `docs/exec-plans/active/`
  - Create `docs/exec-plans/completed/`
  - Create `docs/references/`

- [ ] **Establish FN: docstring convention**
  - Add prefix to all functions
  - Document in style guide
  - Add lint rule

#### Validation

```bash
# Check AGENTS.md exists and is under 100 lines
test $(wc -l < AGENTS.md) -lt 100 && echo "PASS" || echo "FAIL"

# Check FN: prefix in Python files
grep -r "def.*FN:" src/ | wc -l
```

### Phase 2: Mechanical Enforcement (Week 2-3)

**Goal:** Implement automated quality enforcement

#### Checklist

- [ ] **Configure base linter**
  - Install ESLint/Pylint
  - Enable strict mode
  - Add project-specific rules

- [ ] **Create custom lint rules**
  - File size limits
  - Naming conventions
  - Logging standards
  - Architecture boundaries

- [ ] **Set up CI integration**
  - Add lint step to CI
  - Configure branch protection
  - Set up status checks

- [ ] **Embed fix instructions**
  - Review error messages
  - Add remediation guidance
  - Include file paths and examples

#### Validation

```bash
# Run lint check
npm run lint || echo "FAIL: Lint errors found"

# Check CI configuration
test -f .github/workflows/lint.yml && echo "PASS" || echo "FAIL"
```

### Phase 3: Agent Readability (Week 3-4)

**Goal:** Optimize codebase for agent consumption

#### Checklist

- [ ] **Audit technology stack**
  - Rate API stability
  - Rate training coverage
  - Identify re-implementation candidates

- [ ] **Implement class-based organization**
  - Convert standalone functions to methods
  - Add type hints
  - Keep files under 200 lines

- [ ] **Set up context management**
  - Implement context compaction
  - Configure output offloading
  - Enable progressive disclosure

- [ ] **Configure observability**
  - Structured logging with FN: prefix
  - Metrics for key operations
  - Trace IDs for requests

#### Validation

```bash
# Check file sizes
find src -name "*.py" -exec wc -l {} \; | awk '$1 > 200 {print "FAIL: " $2}'

# Check type hint coverage
pyright --stats src/ | grep "type annotations"
```

### Phase 4: Entropy Management (Week 4-5)

**Goal:** Implement automated code quality maintenance

#### Checklist

- [ ] **Define Golden Rules**
  - Document coding standards
  - Identify anti-patterns
  - Create enforcement rules

- [ ] **Create quality scoring**
  - Define metrics per domain
  - Implement scoring algorithm
  - Set up tracking dashboard

- [ ] **Set up background scanning**
  - Schedule regular scans
  - Configure report generation
  - Set up alerting

- [ ] **Configure auto-refactoring**
  - Create refactoring agent
  - Set up PR templates
  - Configure auto-merge

#### Validation

```bash
# Run quality scan
python scripts/scan_quality.py

# Check quality score trend
cat reports/quality_score.json | jq '.trend'
```

### Phase 5: Throughput Optimization (Week 5-6)

**Goal:** Enable high-velocity agent workflows

#### Checklist

- [ ] **Configure PR templates**
  - Create agent-friendly template
  - Add validation checklist
  - Include agent metadata fields

- [ ] **Minimize merge gates**
  - Audit branch protection
  - Remove non-critical checks
  - Configure parallel validation

- [ ] **Implement flaky test handling**
  - Identify flaky tests
  - Set up retry mechanism
  - Track flakiness metrics

- [ ] **Set up Ralph Loop**
  - Implement loop manager
  - Configure context refresh
  - Set up work persistence

#### Validation

```bash
# Check PR throughput
gh pr list --state merged | wc -l

# Check flaky test rate
cat reports/flaky_tests.json | jq '.retry_success_rate'
```

## Key Metrics Dashboard

| Metric | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|--------|---------|---------|---------|---------|---------|
| AGENTS.md lines | <100 | <100 | <100 | <100 | <100 |
| Lint coverage | - | 100% | 100% | 100% | 100% |
| Type hint coverage | - | - | 100% | 100% | 100% |
| Quality score | - | - | - | >80% | >90% |
| PRs per day | - | - | - | - | 3.5+ |

## Troubleshooting

### Problem: Phase 1 takes too long

**Solution:** Start with minimal AGENTS.md. Add detail gradually. Focus on navigation, not content.

### Problem: Lint rules block too many PRs

**Solution:** Start with critical rules only. Add rules incrementally. Use warnings before errors.

### Problem: Agents still make mistakes

**Solution:** Improve documentation. Add more examples. Strengthen validation rules.

### Problem: Quality scores don't improve

**Solution:** Review scoring algorithm. Add missing metrics. Calibrate with human review.

### Problem: Throughput decreases after implementation

**Solution:** Check for bottlenecks. Review merge gate configuration. Optimize CI pipeline.

## Related Skills

- [`harness-engineering-overview`](harness-engineering-overview/SKILL.md) - Overview of all concepts
- [`harness-repo-as-truth`](harness-repo-as-truth/SKILL.md) - Documentation structure
- [`harness-mechanical-enforcement`](harness-mechanical-enforcement/SKILL.md) - Quality enforcement
- [`harness-agent-readability`](harness-agent-readability/SKILL.md) - Agent optimization
- [`harness-entropy-management`](harness-entropy-management/SKILL.md) - Quality maintenance
- [`harness-throughput-merge`](harness-throughput-merge/SKILL.md) - High-velocity workflows

## References

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [Ralph Wiggum Loop](https://github.com/snarktank/ralph)
- [HumanLayer Harness Engineering](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)
