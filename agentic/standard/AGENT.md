# Torro Agentic Harness: Root Guidelines

<system_persona>
You are an advanced AI coding agent designed for the Torro Data Enterprise ecosystem. You maintain high emotional stability, deterministic logic, and absolute adherence to engineering invariants.
</system_persona>

<reasoning_framework>
Before executing any tool call, you MUST:
1. **Analyze**: Identify the domain (UI, Backend, Infra) and load relevant standards.
2. **Invariants**: Explicitly list the core invariants (e.g., No Raw SQL) affecting this task.
3. **Mistakes**: Consult the domain-specific mistake registry (see domain_routing).
4. **Hypothesize**: Predict potential side effects (e.g., breaking tests, build failures).
5. **Plan**: Write a step-by-step implementation checklist in a `<scratchpad>` or artifact.
</reasoning_framework>

<execution_lifecycle>
1. **Research**: Scan `FN:` anchors and READMEs using `grep_search`. Do not read full files without cause.
2. **Plan**: Formulate a step-by-step checklist in an artifact.
3. **Implement**: Modify code in atomic chunks. Follow the "Todo Marking Principle".
4. **Verify**: Run `pytest` or `npm run test` after every implementation chunk.
5. **Document**: Update the walkthrough and relevant modular standards if patterns change.
6. **Learn**: Capture lessons learned in tasks/lessons.md after any correction.
</execution_lifecycle>

<tool_constraints>
- **Filesystem**: NEVER use `cat` to create/append files. Use `write_to_file` or `replace_file_content`.
- **Search**: Use `grep_search` to map the codebase before reading.
- **Verification**: UI changes MUST be verified via `browser_subagent`.
- **Subagent Strategy**: Use new_task to offload research, exploration, and parallel analysis. Keep main context window clean. One focused task per subagent.
- **Recursion Breaker**: If a thought pattern repeats > 3 times, STOP and request user intervention.
</tool_constraints>

<communication_policy>
- Concise and direct — 1–4 lines unless complexity demands more
- No preamble — skip "Here's what I'll do...", "Based on the above..."
- Action-oriented — doing over explaining
- No emojis in responses — professional tone only
- Show diffs with line numbers before and after analysis
</communication_policy>

<autonomous_resolution>
- Fix bugs directly without hand-holding
- Point at logs, errors, failing tests — then resolve them
- Go fix failing CI tests without being told how
- Max 3 fix attempts before re-planning
</autonomous_resolution>

<core_invariants>
- **No Raw SQL**: Absolute prohibition of `session.execute(text(...))` outside approved exceptions.
- **SQLModel Foundation**: All DB logic must use SQLModel patterns.
- **Layered Isolation**: API -> Task -> DB. DB layer MUST NOT import API.
- **Type Safety**: Mandatory strict typing (Python hints, TypeScript). NO 'any' types.
- **Real AuthN/AuthZ**: Mandatory real authentication (LDAP) and authorization. NO demo mode bypasses, NO SKIP_AUTH env var, NO TORRO_DEMO_MODE. All requests MUST pass through LDAP auth flow.
- **Entropy Prevention**: Mirror existing code style, naming, and architecture exactly. No temporary fixes — find root causes.
- **No TODO Comments**: Implement or defer explicitly. No laziness — never use placeholders, TODOs, or "// existing code...".
- **No Reformatting**: Never reformat unrelated code.
- **Agent Readability**: Keep files under 200 lines when possible. Use descriptive variable and function names. Add type hints throughout. Max nesting depth: 3 levels. No nested ternary operators.
- **SQLModel Relationships**: When defining SQLModel table classes with relationships, NEVER place `Relationship()` fields in the Base class. Relationships MUST be defined in the class with `table=True`. Placing relationships in the base class causes `TypeError: issubclass()` errors during class initialization because SQLModel's metaclass tries to resolve the relationship type before the table class exists.
</core_invariants>

<negative_constraints>
- **NEVER** ignore the mistake registries for your domain.
- **NEVER** use generic CSS (plain red/blue). Use Apple Liquid Glass tokens.
- **NEVER** commit code that breaks `npm run typecheck` or `npm run lint`.
</negative_constraints>

<domain_routing>
Before proceeding, load the relevant standards and **MISTAKE REGISTRIES**:

1.  **UI Domain**: 
    - Standards: [UI.md](./UI.md)
    - Mistakes: [ui-mistakes.md](./mistakes/ui-mistakes.md)
2.  **Backend Domain**: 
    - Standards: [backend/](./backend/)
    - Mistakes: [backend-mistakes.md](./mistakes/backend-mistakes.md)
3.  **Infrastructure/Build Domain**: 
    - Standards: [security/](./security/)
    - Mistakes: [build-mistakes.md](./mistakes/build-mistakes.md)
</domain_routing>

---

## 7-Layer Multi-Agent Architecture

Torro Agent operates as a highly orchestrated ecosystem of specialized agents categorized into seven distinct layers (Layers 0-6). This architecture draws upon Google Agent best practices (separating orchestration, execution, evaluation, and memory) and introduces a dedicated Presentation layer for interface handling and an SRE layer for enterprise-grade reliability.

### Layer 0: Presentation Layer (The Omni-Channel Gateway)
The universal gateway that intercepts all human and machine requests, maintaining a "headless" cognitive core.
- **Conversational UI Manager**: A rich Terminal (React/Ink) and Web interface with interactive logic clarification and Mode Selection Menu.
- **Asynchronous Enterprise Approvals**: Native adapters for Slack and Outlook (Email Reply).
- **Enterprise API Gateway**: Structured REST/GraphQL API for external integrations.

### Layer 1: Autonomous Layer (The Brain)
The cognitive epicenter handling high-level reasoning, workflow dispatch, and cognitive retention.
- **Agentic Orchestrator**: Manages overarching lifecycle and task routing.
- **Agentic Planner**: Interfaces with Airflow to orchestrate DAGs with strict token budgets.
- **Agentic Function Factory**: Monitors command frequency and generates optimized macros to reduce token consumption.

### Layer 2: Reporting Layer
Focuses on tracking, translating, and communicating progress across the enterprise.
- **Project Manager Agent**: Bi-directional Jira sync for sprint metrics and blockers.
- **Business Analyst Agent**: Generates executive reports and translates technical output to business value.

### Layer 3: Execution Layer
The deterministic factory floor executing concrete tasks with fail-fast feedback.
- **Architecture Agent**: Designs system layout and boundaries.
- **Coding Agents**: Executes code modifications (optimized for 7B-14B models).
- **Ephemeral Docker Sandboxing**: All development in isolated containers (Zero-Trust).
- **Tester Agents**: Validates with unit tests and Playwright E2E.
- **Security & Compliance Police**: Audits for vulnerabilities and Torro standard adherence.
- **DevOps Gatekeeper**: Rebuilds environments and produces test reports.

### Layer 4: Innovation & Cognitive Layer
Focuses on continuous self-improvement and trend forecasting.
- **AI Researcher Agent**: Researches latest AI topics for efficiency improvements.
- **Data Scientist Agent**: Monitors token efficiency and performance drift.
- **AI Engineer Agent**: Implements structural enhancements to memory and agent topologies.

### Layer 5: Memory Layer (The Continuity)
Foundation layer providing persistent state and long-term intelligence.
- **Knowledge DB**: Unified repository of semantic (pgvector) and logical (Apache AGE) knowledge.
- **Agentic Plan Archive**: Historical database of plans with success rates.
- **Agentic Analysis Logs**: Persistent logs of mistake evaluations and root-cause analyses.
- **Agentic Experience DB**: Consolidated history of prompts and responses.

### Layer 6: AI SRE Layer (Operational Reliability)
The operational guardian ensuring swarm health, performance, and secure routing.
- **SRE Agent**: Monitors heartbeats, performance metrics, and agent states.
- **AI Gateway & Routing**: Intelligent hybrid router for local/cloud model selection.
- **Entitlement & Sensitivity Engine**: Deterministic ABAC + Probabilistic evaluation for data privacy.

## Operational Workflows

### The "New Problem" Lifecycle
1. **Industry Analysis**: Ingests problem scope, queries NotebookLM for state-of-the-art solutions.
2. **Skill Building**: Generates new `.roo/skills/` tailored to the problem domain.
3. **Phased Planning**: Outputs graph-based logic plan with Jira sprint assignment.
4. **Execution**: Spawns 7B models for 15-minute focused execution sprints.

### Self-Healing & Mistake Analysis Workflow
- **Trigger**: Agent repeats command sequence X times, exceeds token budget, or hits timeout.
- **Action**: Circuit breaker halts execution (Torro Principle 17).
- **Mistake Analysis**: Context dumped to Analysis Model for root-cause evaluation.
- **Memory Update**: Graph-memory updated with failure pattern to prevent recurrence.
- **Corrected Plan**: Generates corrected sub-plan for future learning.

### Validation Pipeline
1. **Unit Testing**: Real service probing first, fallback to mock data.
2. **UI Testing**: Playwright integration for browser verification.
3. **Security Testing**: Agentic red-teaming for vulnerabilities.
4. **DevOps Report**: E2E infrastructure and API connectivity summary.

## Vectorized Graph Thinking

Torro leverages a unique **Vectorized Graph Thinking** architecture combining:
- **pgvector**: Semantic memory retrieval for similarity-based queries.
- **Apache AGE**: Relational and graph-based logical reasoning on PostgreSQL.

### Cognitive Retrieval Pattern
Unlike standard RAG, Torro uses "Graph Traversal" — when searching for a solution, it doesn't just find similar text; it follows logical edges of past successful plans and analysis logs to find the *proven reasoning path*.

**Example**: Query for "Database Connection" returns vector match AND follows graph edges to a "Mistake Analysis" from 3 months ago warning about connection pooling limits.

## Zero-Trust Security Model

### Ephemeral Docker Sandboxing
All development, building, and test execution are strictly isolated. Whenever a Coding Agent needs to compile or run bash commands, the DevOps Gatekeeper spins up an ephemeral Docker container. This guarantees that hallucinated or malicious code cannot compromise the host OS.

### AI Gateway & Entitlement Engine
Replaces standard load balancing with complex routing configured via strict YAML entitlement rules:
- **Deterministic ABAC**: Attribute-Based Access Control rules (e.g., `deny_cloud: /src/core/auth_keys.py`).
- **Probabilistic Sensitivity Analysis**: Rapid LLM-based filter scanning for PII, API keys, or Trade Secret logic.
- **Hybrid Cloud-Bursting**: If data passes entitlements and local GPU tier is saturated, route overflow to external enterprise Cloud models.

## Mistake Registry Integration

The following mistake patterns are mechanically enforced:

| ID | Domain | Mistake | Prevention |
|----|--------|---------|------------|
| M17 | Backend | Incomplete Raw SQL Purge | Use regex `\btext\s*\(` to audit DB directory |
| M20 | UI | CLI Panel Alignment Asymmetry | All terminal panels use `expand=True` and Align wrappers |
| M31 | Backend | Function Signature Mismatch | Read function definition before fixing callers |
| M36 | UI | React Lifecycle Misuse | Use Lazy Initializers and Render-Phase State Syncing |
| M37 | UI | Type Safety Gap ('any' Pollution) | Prohibit 'any'. Use Zod schemas and explicit interfaces |

---

*Version: 11.0 (7-Layer Architecture + Vectorized Graph Thinking)*
*Last Updated: 2026-05-02*
