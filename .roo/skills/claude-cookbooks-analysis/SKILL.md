---
name: claude-cookbooks-analysis
description: Analyze the Anthropic Claude Cookbooks repository and derive actionable Agent Skills based on documented patterns, capabilities, and workflows.
---

# Claude Cookbooks Skill Derivation Analysis

## Purpose
This skill provides a systematic analysis of the [Anthropic Claude Cookbooks repository](https://github.com/anthropics/claude-cookbooks) to identify and derive actionable Agent Skills (SKILL.md format) that can be implemented in the Torro ecosystem.

## When to Use
- When evaluating external repositories for skill derivation opportunities
- When planning skill implementation roadmap based on proven patterns
- When onboarding team members to available AI capability patterns
- When conducting competitive analysis of AI agent frameworks

## When NOT to Use
- When implementing actual skills (use individual derived skills instead)
- When the analysis scope is limited to a single capability
- When the repository structure differs significantly from cookbooks format

## Repository Overview

**Source:** https://github.com/anthropics/claude-cookbooks
**Total Markdown Files:** 62
**Analysis Date:** 2026-04-24

### Directory Structure
```
claude-cookbooks/
├── .claude/                    # Claude-specific configuration
│   ├── commands/               # 7 command files (skill candidates)
│   └── skills/                 # 1 existing skill (cookbook-audit)
├── capabilities/               # 6 capability guides (HIGH priority)
├── patterns/                   # Agent patterns (HIGH priority)
├── tool_use/                   # Tool implementations (MEDIUM priority)
├── managed_agents/             # Managed agent examples (MEDIUM priority)
├── coding/                     # Coding examples
├── extended_thinking/          # Reasoning patterns
├── multimodal/                 # Vision/image processing
├── finetuning/                 # Dataset preparation
└── third_party/                # Integration examples
```

## Skill Derivation Summary

### Priority Matrix

| Priority | Category | Skills | Implementation Window |
|----------|----------|--------|----------------------|
| HIGH | Capabilities | 6 | Week 1-2 |
| HIGH | Patterns | 5 | Week 3-4 |
| MEDIUM | Tool Use | 4 | Week 5-6 |
| MEDIUM | Managed Agents | 4 | Week 7-8 |
| LOW | Commands | 7 | Week 9-10 |

**Total Derivable Skills:** 26

---

## Phase 1: Core Capabilities (HIGH PRIORITY)

### 1.1 Retrieval Augmented Generation
**Proposed Skill:** `rag-implementation`
**Source:** `/capabilities/retrieval_augmented_generation/`

**Description:** Implement RAG systems using summary indexing, re-ranking, and evaluation frameworks.

**Derivable Sub-Skills:**
- `rag-summary-indexing` - Build RAG with summary indexing for improved precision/recall
- `rag-re-ranking` - Implement re-ranking for RAG accuracy optimization  
- `rag-evaluation` - Evaluate RAG systems using promptfoo and custom metrics

**Key Files:**
- [`guide.ipynb`](/tmp/claude-cookbooks/capabilities/retrieval_augmented_generation/guide.ipynb)
- [`evaluation/eval_retrieval.py`](/tmp/claude-cookbooks/capabilities/retrieval_augmented_generation/evaluation/eval_retrieval.py)

---

### 1.2 Text-to-SQL Generation
**Proposed Skill:** `text-to-sql-generation`
**Source:** `/capabilities/text_to_sql/`

**Description:** Generate complex SQL queries from natural language using prompting, self-improvement, and RAG.

**Derivable Sub-Skills:**
- `sql-query-generation` - Convert natural language to SQL with schema context
- `sql-self-improvement` - Iterative SQL refinement with feedback
- `sql-evaluation-suite` - Evaluate SQL for syntax, data correctness, row count

**Test Cases:**
- Simple query generation
- Employee count queries  
- Hierarchical queries
- Budget allocation queries

---

### 1.3 Multi-Document Summarization
**Proposed Skill:** `multi-document-summarization`
**Source:** `/capabilities/summarization/`

**Description:** Summarize and synthesize information from multiple sources using multi-shot, domain-based, and chunking methods.

**Derivable Sub-Skills:**
- `lease-document-summarization` - Summarize legal lease documents
- `multi-shot-summarization` - Use few-shot prompting for consistent summaries
- `chunking-summarization` - Handle long-form content with chunking strategies
- `summarization-evaluation` - Evaluate summaries using ROUGE, BLEU, and LLM judges

---

### 1.4 LLM Text Classification
**Proposed Skill:** `llm-text-classification`
**Source:** `/capabilities/classification/`

**Description:** Perform text classification with complex business rules and limited training data using Claude and RAG-enhanced prompts.

**Derivable Sub-Skills:**
- `rule-based-classification` - Classify using business rules without training data
- `classification-with-rag` - Enhance classification with retrieval-augmented prompts
- `classification-evaluation` - Evaluate classification accuracy with custom metrics

---

### 1.5 Knowledge Graph Construction
**Proposed Skill:** `knowledge-graph-extraction`
**Source:** `/capabilities/knowledge_graph/`

**Description:** Build knowledge graphs from unstructured text using NER, relation extraction, and entity resolution.

**Derivable Sub-Skills:**
- `named-entity-recognition` - Extract entities from unstructured text
- `relation-extraction` - Extract relationships between entities
- `entity-resolution` - Resolve and deduplicate entities
- `entity-summarization` - Summarize entity relationships
- `knowledge-graph-querying` - Query knowledge graphs with multi-hop queries

---

### 1.6 Contextual Embeddings
**Proposed Skill:** `contextual-embeddings-rag`
**Source:** `/capabilities/contextual-embeddings/`

**Description:** Improve RAG performance using contextual embeddings that add relevant context to each chunk before embedding.

**Derivable Sub-Skills:**
- `contextual-chunk-embedding` - Add context to chunks before embedding
- `semantic-search-with-context` - Combine semantic search with contextual embeddings
- `bm25-contextual-hybrid` - Hybrid search with BM25 and contextual reranking

---

## Phase 2: Agent Patterns (HIGH PRIORITY)

### 2.1 Building Effective Agents
**Source:** `/patterns/agents/`
**Reference:** [Building Effective Agents](https://anthropic.com/research/building-effective-agents)

**Derivable Skills:**

#### Basic Building Blocks:
1. **`prompt-chaining-pattern`** - Chain multiple LLM calls for complex tasks
2. **`routing-pattern`** - Route inputs to specialized handlers
3. **`parallel-llm-pattern`** - Run multiple LLM calls in parallel for comparison

#### Advanced Workflows:
4. **`orchestrator-subagent-pattern`** - Implement orchestrator that delegates to subagents
5. **`evaluator-optimizer-pattern`** - Iterative improvement with evaluator feedback

**Key Files:**
- [`basic_workflows.ipynb`](/tmp/claude-cookbooks/patterns/agents/basic_workflows.ipynb)
- [`evaluator_optimizer.ipynb`](/tmp/claude-cookbooks/patterns/agents/evaluator_optimizer.ipynb)
- [`orchestrator_workers.ipynb`](/tmp/claude-cookbooks/patterns/agents/orchestrator_workers.ipynb)
- [`prompts/research_subagent.md`](/tmp/claude-cookbooks/patterns/agents/prompts/research_subagent.md)
- [`prompts/research_lead_agent.md`](/tmp/claude-cookbooks/patterns/agents/prompts/research_lead_agent.md)

---

## Phase 3: Tool Use (MEDIUM PRIORITY)

### 3.1 Memory Tools
**Proposed Skill:** `memory-tool-implementation`
**Source:** `/tool_use/memory_demo/`

**Description:** Implement memory tools for AI agents including cache management, state persistence, and version tracking.

**Derivable Sub-Skills:**
- `cache-manager-tool` - Implement caching for API responses
- `code-review-memory` - Track code review state across sessions
- `sql-query-cache` - Cache and reuse SQL query results

---

### 3.2 Customer Service Tools
**Proposed Skill:** `customer-service-automation`
**Source:** `/tool_use/utils/customer_service_tools.py`

**Description:** Build customer service automation tools with ticket management, escalation handling, and response generation.

---

### 3.3 Team Expense API
**Proposed Skill:** `expense-approval-workflow`
**Source:** `/tool_use/utils/team_expense_api.py`

**Description:** Implement expense approval workflows with policy enforcement, human-in-the-loop escalation, and audit trails.

---

### 3.4 Visualization Tools
**Proposed Skill:** `data-visualization-generator`
**Source:** `/tool_use/utils/visualize.py`

**Description:** Generate visualizations from structured data with automatic chart selection and formatting.

---

## Phase 4: Managed Agents (MEDIUM PRIORITY)

### 4.1 Data Analyst Agent
**Proposed Skill:** `data-analysis-agent`
**Source:** `/managed_agents/example_data/data_analyst_agent/`

**Description:** Implement data analysis agents that can interpret datasets, generate insights, and create reports.

---

### 4.2 Policy-Based Approver
**Proposed Skill:** `policy-based-approver`
**Source:** `/managed_agents/example_data/gate/`

**Description:** Build approval agents that classify requests against policies and escalate ambiguous cases.

**Key Pattern:**
- `decide()` for clear approves/rejects
- `escalate()` for ambiguous cases
- Policy YAML configuration

---

### 4.3 Issue-to-PR Orchestrator
**Proposed Skill:** `issue-to-pr-orchestrator`
**Source:** `/managed_agents/example_data/orchestrate/`

**Description:** Orchestrate the full workflow from GitHub issue to merged PR with automated tool calls.

**Key Components:**
- Mock GitHub CLI (`gh-mock`)
- State persistence (`.gh-state/`)
- Issue triage → PR creation → Review → Merge

---

### 4.4 SRE Incident Responder
**Proposed Skill:** `sre-incident-responder`
**Source:** `/managed_agents/example_data/sre/runbooks/`

**Description:** Implement SRE incident response agents that follow runbooks for common issues like OOMKilled errors.

**Example Runbooks:**
- OOMKilled / OutOfMemoryError handling
- Pod crash diagnosis
- Resource exhaustion mitigation

---

## Phase 5: Commands & Utilities (LOW PRIORITY)

### 5.1 PR Review Skills
**Source:** `/.claude/commands/review-pr.md`, `review-pr-ci.md`

**Proposed Skills:**
- `pr-code-review` - Review pull requests with allowed tools
- `pr-ci-verification` - Verify CI/CD status before merge

---

### 5.2 Registry Management
**Proposed Skill:** `container-registry-management`
**Source:** `/.claude/commands/add-registry.md`

**Description:** Add and manage container registries with proper authentication and configuration.

---

### 5.3 Model Verification
**Proposed Skill:** `llm-model-verification`
**Source:** `/.claude/commands/model-check.md`

**Description:** Verify Claude model usage against current public models and deprecation schedules.

---

### 5.4 Notebook Review
**Proposed Skill:** `jupyter-notebook-review`
**Source:** `/.claude/commands/notebook-review.md`

**Description:** Comprehensive review of Jupyter notebooks for code quality, documentation, and best practices.

---

### 5.5 Link Quality Audit
**Proposed Skill:** `link-quality-audit`
**Source:** `/.claude/commands/link-review.md`

**Description:** Review links in documentation for quality, security, and accessibility issues.

---

### 5.6 GitHub Issue Triage
**Proposed Skill:** `github-issue-triage`
**Source:** `/.claude/commands/review-issue.md`

**Description:** Review and respond to GitHub issues with proper categorization and assignment.

---

## Existing Skill Reference

### cookbook-audit
**Source:** `/.claude/skills/cookbook-audit/SKILL.md`

This is the ONLY complete skill in the repository, serving as a reference pattern.

**Structure:**
```
.claude/skills/cookbook-audit/
├── SKILL.md (184 lines)
└── style_guide.md
```

**Frontmatter:**
```yaml
name: cookbook-audit
description: Audit an Anthropic Cookbook notebook based on a rubric. Use whenever a notebook review or audit is requested.
```

**Key Sections:**
1. Instructions
2. Workflow (8 steps)
3. Audit Report Format
4. Quick Reference Checklist
5. Content Philosophy
6. Style Guidelines
7. Structural Requirements
8. Common Anti-Patterns

**Takeaway:** This skill demonstrates proper SKILL.md structure with clear triggers, workflows, and evaluation criteria.

---

## Recommended Skill Template

Based on the existing `cookbook-audit` skill, each derived skill should follow:

```markdown
---
name: skill-name
description: Clear, actionable description with keywords
---

# Skill Title

## When to Use
- Trigger condition 1
- Trigger condition 2

## When NOT to Use
- Alternative approach 1
- Alternative approach 2

## Inputs Required
- Input 1 description
- Input 2 description

## Workflow
1. Step 1 with specific action
2. Step 2 with expected output
3. ...

## Examples
- Example 1 with context
- Example 2 with expected result

## Troubleshooting
- Common issue 1 and resolution
- Common issue 2 and resolution

## Related Files
- [Reference](path/to/reference.md)
- [Script](path/to/script.py)
```

---

## Implementation Roadmap

### Week 1-2: Core Capabilities
- [ ] `rag-implementation`
- [ ] `text-to-sql-generation`
- [ ] `multi-document-summarization`
- [ ] `llm-text-classification`

### Week 3-4: Agent Patterns
- [ ] `prompt-chaining-pattern`
- [ ] `orchestrator-subagent-pattern`
- [ ] `evaluator-optimizer-pattern`

### Week 5-6: Tool Use
- [ ] `memory-tool-implementation`
- [ ] `expense-approval-workflow`
- [ ] `data-visualization-generator`

### Week 7-8: Managed Agents
- [ ] `policy-based-approver`
- [ ] `issue-to-pr-orchestrator`
- [ ] `sre-incident-responder`

### Week 9-10: Specialized Skills
- [ ] `knowledge-graph-extraction`
- [ ] `contextual-embeddings-rag`
- [ ] `jupyter-notebook-review`

---

## File Organization Template

```
.roo/skills/
├── rag-implementation/
│   ├── SKILL.md
│   ├── references/
│   │   ├── evaluation-metrics.md
│   │   └── troubleshooting.md
│   └── scripts/
│       └── evaluate-rag.py
├── text-to-sql-generation/
│   ├── SKILL.md
│   └── examples/
│       └── sample-queries.json
└── ...
```

---

## Cross-References

### Related Skills
- [`rag-implementation`](../rag-implementation/SKILL.md) → [`contextual-embeddings-rag`](../contextual-embeddings-rag/SKILL.md)
- [`text-to-sql-generation`](../text-to-sql-generation/SKILL.md) → [`knowledge-graph-extraction`](../knowledge-graph-extraction/SKILL.md)
- [`orchestrator-subagent-pattern`](../orchestrator-subagent-pattern/SKILL.md) → [`issue-to-pr-orchestrator`](../issue-to-pr-orchestrator/SKILL.md)

### Common Utilities
- Evaluation scripts: `/assets/test_data/evaluation/`
- Test datasets: `/assets/test_data/`
- Reference prompts: `/agentic/functions/`

---

## Conclusion

The claude-cookbooks repository provides **26 derivable skills** across 8 categories. Priority should be given to:

1. **Core capabilities** (RAG, summarization, classification) - Most universally applicable
2. **Agent patterns** (prompt chaining, orchestration) - Foundation for complex workflows
3. **Tool use** (memory, visualization) - Practical automation

Each skill should follow the established SKILL.md format with clear triggers, workflows, and examples.

---

**Document Version:** 1.0
**Last Updated:** 2026-04-24
**Next Review:** After Phase 1 implementation
