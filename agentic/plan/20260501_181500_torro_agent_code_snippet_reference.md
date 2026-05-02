---
Create Date: 2026-05-01
Update Date: 2026-05-01
IDE: Roo Code
Agent: Qwen3.6-35B-A3B-FP8
GitHub committer: User
Sprint: Sprint #24
---

# Torro Agent Enterprise Architecture — Code Snippet Reference

## 1. Executive Summary

This document provides a comprehensive mapping of code snippets from the four industry reference frameworks (**Claude Code [CC]**, **Roo Code [RC]**, **Hermes Agent [HA]**, **Everything Claude Code [ECC]**) to each of the seven Torro Agent layers (0-6). Each entry includes the exact file path, a code excerpt, and the Torro layer it maps to.

---

## 2. Layer 0: Presentation Layer (Omni-Channel Gateway)

The Presentation Layer handles all user-facing interfaces — CLI, Web UI, and enterprise messaging adapters.

### 2.1 Conversational UI Manager

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **CC** | [`legacy/claude-code/src/QueryEngine.ts`](legacy/claude-code/src/QueryEngine.ts:1) | Core query engine managing LLM interaction, tool calls, and streaming execution | Base for Torro's `QueryEngine` abstraction |
| **CC** | [`legacy/claude-code/src/ink.ts`](legacy/claude-code/src/ink.ts) | Terminal UI rendering using React/Ink | Torro's TUI foundation |
| **CC** | [`legacy/claude-code/src/interactiveHelpers.tsx`](legacy/claude-code/src/interactiveHelpers.tsx) | Interactive back-and-forth logic clarification | Torro's Mode Selection Menu |

```typescript
// CC: QueryEngine.ts — Core LLM interaction entry point
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs'
import type { SDKMessage, SDKStatus } from 'src/entrypoints/agentSdkTypes.js'

// Manages the full query chain: user input → system prompt → tool calls → response
// Torro maps this to Layer 1's Orchestrator with Layer 0's UI abstraction
```

### 2.2 Enterprise Messaging Adapters (Slack, Email)

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/gateway/platforms/base.py`](legacy/hermes-agent/gateway/platforms/base.py:1) | `BasePlatformAdapter` — abstract interface for all platform adapters | Torro's Layer 0 gateway adapter pattern |
| **HA** | [`legacy/hermes-agent/gateway/platforms/slack.py`](legacy/hermes-agent/gateway/platforms/slack.py:1) | Slack Socket Mode adapter with thread context caching | Torro's Slack integration |
| **HA** | [`legacy/hermes-agent/gateway/platforms/email.py`](legacy/hermes-agent/gateway/platforms/email.py:1) | IMAP/SMTP email adapter with automated sender filtering | Torro's Outlook/Email integration |

```python
# HA: gateway/platforms/base.py — Base platform adapter
class BasePlatformAdapter(ABC):
    """All platform adapters (Telegram, Discord, WhatsApp) inherit from this."""
    
    @abstractmethod
    async def process_message(self, event: MessageEvent) -> ProcessingOutcome:
        """Process incoming message and return outcome."""
    
    @abstractmethod
    async def send_message(self, event: MessageEvent, text: str) -> SendResult:
        """Send response back to the platform."""
```

```python
# HA: gateway/platforms/slack.py — Slack adapter with Block Kit parsing
def _extract_text_from_slack_blocks(blocks: list) -> str:
    """Extract readable text from Slack Block Kit blocks, including quoted/forwarded content."""
    # Handles rich_text elements, links, channels, users, emoji
    # Torro maps this to Layer 0's Enterprise API Gateway
```

### 2.3 Gateway Configuration & Session Management

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/gateway/session.py`](legacy/hermes-agent/gateway/session.py) | Session lifecycle management | Torro's headless cognitive core |
| **HA** | [`legacy/hermes-agent/gateway/config.py`](legacy/hermes-agent/gateway/config.py) | Platform configuration loading | Torro's `config.ini` master broker |

---

## 3. Layer 1: Autonomous Layer (The Brain)

The Autonomous Layer handles high-level reasoning, workflow dispatch, and cognitive retention.

### 3.1 Agentic Orchestrator

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **CC** | [`legacy/claude-code/src/coordinator/`](legacy/claude-code/src/coordinator/) | Coordinator module managing multi-agent handoffs | Torro's Agentic Orchestrator |
| **CC** | [`legacy/claude-code/src/QueryEngine.ts`](legacy/claude-code/src/QueryEngine.ts:39) | `Tool` type definition and tool call context | Torro's tool execution contract |
| **HA** | [`legacy/hermes-agent/agent/context_engine.py`](legacy/hermes-agent/agent/context_engine.py:32) | `ContextEngine` base class for pluggable context management | Torro's context compression |

```typescript
// CC: Tool.ts — Tool contract interface
export type ToolInputJSONSchema = {
  [x: string]: unknown
  type: 'object'
  properties?: { [x: string]: unknown }
}

// Every tool must implement: checkPermissions(), validateInput(), call()
// Torro maps this to Layer 3's Execution Layer tool contract
```

```python
# HA: agent/context_engine.py — Context compression base class
class ContextEngine(ABC):
    """Base class all context engines must implement."""
    
    @abstractmethod
    def should_compress(self, prompt_tokens: int = None) -> bool:
        """Return True if compaction should fire this turn."""
    
    @abstractmethod
    def compress(self, messages: List[Dict[str, Any]], ...) -> List[Dict[str, Any]]:
        """Compact the message list and return the new message list."""
```

### 3.2 Agentic Planner (Airflow Integration)

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/cron/scheduler.py`](legacy/hermes-agent/cron/scheduler.py) | Task scheduling and dependency management | Torro's Airflow DAG integration |
| **HA** | [`legacy/hermes-agent/cron/jobs.py`](legacy/hermes-agent/cron/jobs.py) | Background job definitions | Torro's scheduled agent tasks |

### 3.3 Agentic Function Factory

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/tools/skill_commands.py`](legacy/hermes-agent/tools/skill_commands.py) | Dynamic skill command generation | Torro's Function Factory |
| **HA** | [`legacy/hermes-agent/tools/skill_usage.py`](legacy/hermes-agent/tools/skill_usage.py) | Skill usage tracking and frequency analysis | Torro's command frequency monitoring |

---

## 4. Layer 2: Reporting Layer

The Reporting Layer tracks, translates, and communicates progress across the enterprise.

### 4.1 Project Manager & Jira Integration

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/gateway/platforms/`](legacy/hermes-agent/gateway/platforms/) | Platform registry for multi-channel status reporting | Torro's bi-directional Jira sync |

### 4.2 Business Analyst & Executive Reporting

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **ECC** | [`legacy/everything-claude-code/agents/planner.md`](legacy/everything-claude-code/agents/planner.md) | Structured planning agent definition | Torro's BA agent output format |
| **ECC** | [`legacy/everything-claude-code/agents/code-reviewer.md`](legacy/everything-claude-code/agents/code-reviewer.md) | YAML frontmatter agent schema | Torro's agent persona definitions |

```markdown
# ECC: agents/code-reviewer.md — Agent persona definition
---
name: code-reviewer
description: Reviews code for quality, security, and best practices
tools: [read, grep, edit, bash]
---

You are a senior code reviewer...
```

---

## 5. Layer 3: Execution Layer

The Execution Layer executes concrete tasks with strict validation and sandboxing.

### 5.1 Tool Execution Contract

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **CC** | [`legacy/claude-code/src/Tool.ts`](legacy/claude-code/src/Tool.ts:15) | `ToolInputJSONSchema` and validation types | Torro's tool contract |
| **CC** | [`legacy/claude-code/src/tools/`](legacy/claude-code/src/tools/) | Tool implementations (Bash, FileEdit, Grep, etc.) | Torro's Execution Layer tools |
| **HA** | [`legacy/hermes-agent/tools/registry.py`](legacy/hermes-agent/tools/registry.py) | AST-based tool registration and dependency resolution | Torro's auto-discovery |
| **HA** | [`legacy/hermes-agent/tools/file_tools.py`](legacy/hermes-agent/tools/file_tools.py) | File operation tools with safety checks | Torro's file execution |
| **HA** | [`legacy/hermes-agent/tools/terminal_tool.py`](legacy/hermes-agent/tools/terminal_tool.py) | Terminal execution with sandboxing | Torro's Docker sandboxing |

```python
# HA: tools/registry.py — Tool registration pattern
# Auto-discovers tools from tools/ directory
# Prevents circular imports via AST analysis
# Torro maps this to Layer 3's tool registry
```

### 5.2 Security & Path Safety

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/tools/path_security.py`](legacy/hermes-agent/tools/path_security.py) | Path traversal prevention | Torro's security validation |
| **HA** | [`legacy/hermes-agent/tools/file_safety.py`](legacy/hermes-agent/agent/file_safety.py) | File operation safety checks | Torro's compliance police |

### 5.3 Error Classification & Recovery

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/agent/error_classifier.py`](legacy/hermes-agent/agent/error_classifier.py:24) | `FailoverReason` enum and `ClassifiedError` dataclass | Torro's feedback circuit |

```python
# HA: agent/error_classifier.py — Error taxonomy
class FailoverReason(enum.Enum):
    auth = "auth"                        # Transient auth (401/403)
    billing = "billing"                  # 402 or credit exhaustion
    rate_limit = "rate_limit"            # 429 or quota throttling
    context_overflow = "context_overflow"  # Context too large
    # Torro maps this to Layer 3's Mistake Analysis trigger
```

---

## 6. Layer 4: Innovation & Cognitive Layer

The Innovation Layer focuses on continuous self-improvement and structural optimization.

### 6.1 autoDream Service (Memory Consolidation)

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **CC** | [`legacy/claude-code/src/services/autoDream/autoDream.ts`](legacy/claude-code/src/services/autoDream/autoDream.ts:1) | Background memory consolidation service | Torro's AI Researcher Agent |
| **CC** | [`legacy/claude-code/src/services/autoDream/consolidationPrompt.ts`](legacy/claude-code/src/services/autoDream/consolidationPrompt.ts) | Consolidation prompt generation | Torro's skill generation |

```typescript
// CC: autoDream.ts — Background memory consolidation
// Gate order (cheapest first):
//   1. Time: hours since lastConsolidatedAt >= minHours
//   2. Sessions: transcript count with mtime > lastConsolidatedAt >= minSessions
//   3. Lock: no other process mid-consolidation
// Torro maps this to Layer 4's Data Scientist Diagnostic
```

### 6.2 Skill Management & Evolution

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/agent/curator.py`](legacy/hermes-agent/agent/curator.py:1) | Background skill maintenance orchestrator | Torro's AI Engineer Agent |
| **HA** | [`legacy/hermes-agent/tools/skills_hub.py`](legacy/hermes-agent/tools/skills_hub.py) | Skill hub management and sync | Torro's SKILL.md generation |
| **ECC** | [`legacy/everything-claude-code/agents/`](legacy/everything-claude-code/agents/) | 48 specialized agent definitions | Torro's agent persona library |

```python
# HA: agent/curator.py — Skill maintenance orchestrator
"""
The curator is an auxiliary-model task that periodically reviews agent-created
skills and maintains the collection. It runs inactivity-triggered.

Responsibilities:
  - Auto-transition lifecycle states based on last_used_at timestamps
  - Spawn a background review agent that can pin / archive / consolidate
  - Persist curator state (last_run_at, paused, etc.) in .curator_state
"""
# Torro maps this to Layer 4's AI Engineer Agent
```

---

## 7. Layer 5: Memory Layer (The Continuity)

The Memory Layer provides persistent state and long-term intelligence.

### 7.1 Vector & Graph Memory

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **CC** | [`legacy/claude-code/src/memdir/memdir.ts`](legacy/claude-code/src/memdir/memdir.ts:34) | `MEMORY.md` entrypoint with line/byte truncation | Torro's Knowledge DB |
| **CC** | [`legacy/claude-code/src/memdir/memoryTypes.ts`](legacy/claude-code/src/memdir/memoryTypes.ts) | Memory type definitions and categorization | Torro's vector schema |
| **HA** | [`legacy/hermes-agent/agent/memory_manager.py`](legacy/hermes-agent/agent/memory_manager.py:1) | MemoryManager orchestrating builtin + external providers | Torro's memory abstraction |
| **HA** | [`legacy/hermes-agent/agent/memory_provider.py`](legacy/hermes-agent/agent/memory_provider.py) | MemoryProvider interface for pluggable backends | Torro's pgvector/AGE integration |

```typescript
// CC: memdir/memdir.ts — Memory entrypoint management
export const ENTRYPOINT_NAME = 'MEMORY.md'
export const MAX_ENTRYPOINT_LINES = 200
export const MAX_ENTRYPOINT_BYTES = 25_000

function truncateEntrypointContent(raw: string): EntrypointTruncation {
  // Truncate to line AND byte caps
  // Torro maps this to Layer 5's Knowledge DB with pgvector
}
```

```python
# HA: agent/memory_manager.py — Memory orchestration
"""
MemoryManager — orchestrates the built-in memory provider plus at most
ONE external plugin memory provider.

Usage:
    self._memory_manager = MemoryManager()
    self._memory_manager.add_provider(BuiltinMemoryProvider(...))
    prompt_parts.append(self._memory_manager.build_system_prompt())
    context = self._memory_manager.prefetch_all(user_message)
"""
# Torro maps this to Layer 5's hybrid vector-graph memory
```

### 7.2 Context Compression & Condensing

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/agent/context_compressor.py`](legacy/hermes-agent/agent/context_compressor.py) | Message list compression with DAG construction | Torro's context condensing |
| **HA** | [`legacy/hermes-agent/agent/trajectory.py`](legacy/hermes-agent/agent/trajectory.py) | Conversation trajectory tracking | Torro's past plan trajectories |

---

## 8. Layer 6: AI SRE Layer (Operational Reliability)

The SRE Layer ensures system health, performance monitoring, and secure routing.

### 8.1 Credential Isolation & Security

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/agent/credential_pool.py`](legacy/hermes-agent/agent/credential_pool.py:1) | Multi-credential pool with failover strategies | Torro's Layer 6 security envelope |
| **HA** | [`legacy/hermes-agent/tools/credential_files.py`](legacy/hermes-agent/tools/credential_files.py) | Credential file management | Torro's credential isolation |

```python
# HA: agent/credential_pool.py — Multi-credential pool
@dataclass
class PooledCredential:
    provider: str
    id: str
    label: str
    auth_type: str  # oauth | api_key
    priority: int
    source: str
    access_token: str
    last_status: Optional[str]  # ok | exhausted
    # Strategies: fill_first, round_robin, random, least_used
    # Torro maps this to Layer 6's Deterministic ABAC
```

### 8.2 Error Classification & Circuit Breakers

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/agent/error_classifier.py`](legacy/hermes-agent/agent/error_classifier.py:65) | `ClassifiedError` with recovery hints | Torro's circuit breaker |

```python
# HA: agent/error_classifier.py — Recovery action hints
@dataclass
class ClassifiedError:
    reason: FailoverReason
    retryable: bool = True
    should_compress: bool = False
    should_rotate_credential: bool = False
    should_fallback: bool = False
    # Torro maps this to Layer 6's SRE Agent heartbeat monitoring
```

### 8.3 Security Auditing

| Framework | File | Snippet | Purpose |
|-----------|------|---------|---------|
| **HA** | [`legacy/hermes-agent/tools/tirith_security.py`](legacy/hermes-agent/tools/tirith_security.py) | Tirith-based security policy evaluation | Torro's Security Agent |

---

## 9. Cross-Framework Pattern Mapping

### 9.1 Agent Definition Patterns

| Pattern | CC | RC | HA | ECC | Torro Layer |
|---------|----|----|----|-----|-------------|
| YAML Frontmatter Agents | ❌ | ❌ | ❌ | ✅ `agents/*.md` | Layer 1 |
| SKILL.md Paradigm | ❌ | ✅ `skills/` | ✅ `skills/` | ✅ `skills/` | Layer 3 |
| Tool Contract Interface | ✅ `Tool.ts` | ✅ `Tool.ts` | ✅ `tools/registry.py` | ❌ | Layer 3 |
| Platform Adapters | ❌ | ❌ | ✅ `gateway/platforms/` | ❌ | Layer 0 |
| Memory Providers | ✅ `memdir/` | ❌ | ✅ `agent/memory_*.py` | ❌ | Layer 5 |
| Context Compression | ❌ | ❌ | ✅ `context_engine.py` | ❌ | Layer 5 |
| Credential Pooling | ❌ | ❌ | ✅ `credential_pool.py` | ❌ | Layer 6 |
| Error Classification | ❌ | ❌ | ✅ `error_classifier.py` | ❌ | Layer 3/6 |
| autoDream Consolidation | ✅ `autoDream/` | ❌ | ❌ | ❌ | Layer 4 |
| Curator Maintenance | ❌ | ❌ | ✅ `curator.py` | ❌ | Layer 4 |

### 9.2 Technology Stack Mapping

| Component | CC | RC | HA | ECC | Torro Target |
|-----------|----|----|----|-----|--------------|
| Language | TypeScript (Bun) | TypeScript (Node) | Python | Python/TS | Python |
| AI Interface | Anthropic SDK | OpenAI SDK | OpenAI-compatible | OpenAI SDK | OpenAI-compatible |
| MCP Support | ✅ | ✅ | ✅ | ✅ | ✅ |
| Memory | File-based (memdir) | VSCode Memento | Pluggable providers | File-based | PostgreSQL + pgvector + AGE |
| Scheduling | Internal | VSCode Tasks | cron/ | Internal | Apache Airflow |
| UI | React/Ink | VSCode Extension | CLI + Gateway | VSCode Extension | React/Ink + Web |
| Security | Permission modes | VSCode permissions | Credential pool | Config-based | YAML entitlements |

---

## 10. Implementation Priority Matrix

| Torro Layer | Primary Reference | Secondary Reference | Implementation Complexity |
|-------------|-------------------|---------------------|--------------------------|
| **Layer 0** | HA `gateway/platforms/base.py` | CC `src/ink.ts` | Medium |
| **Layer 1** | CC `src/QueryEngine.ts` | HA `agent/context_engine.py` | High |
| **Layer 2** | ECC `agents/*.md` | HA `gateway/platforms/slack.py` | Medium |
| **Layer 3** | CC `src/Tool.ts` | HA `tools/registry.py` | High |
| **Layer 4** | CC `src/services/autoDream/` | HA `agent/curator.py` | Medium |
| **Layer 5** | CC `src/memdir/` | HA `agent/memory_manager.py` | High |
| **Layer 6** | HA `agent/credential_pool.py` | HA `agent/error_classifier.py` | Medium |

---

## 11. File Index by Layer

### Layer 0 Files
- [`legacy/hermes-agent/gateway/platforms/base.py`](legacy/hermes-agent/gateway/platforms/base.py)
- [`legacy/hermes-agent/gateway/platforms/slack.py`](legacy/hermes-agent/gateway/platforms/slack.py)
- [`legacy/hermes-agent/gateway/platforms/email.py`](legacy/hermes-agent/gateway/platforms/email.py)
- [`legacy/claude-code/src/ink.ts`](legacy/claude-code/src/ink.ts)

### Layer 1 Files
- [`legacy/claude-code/src/QueryEngine.ts`](legacy/claude-code/src/QueryEngine.ts)
- [`legacy/claude-code/src/coordinator/`](legacy/claude-code/src/coordinator/)
- [`legacy/hermes-agent/agent/context_engine.py`](legacy/hermes-agent/agent/context_engine.py)
- [`legacy/hermes-agent/cron/scheduler.py`](legacy/hermes-agent/cron/scheduler.py)

### Layer 2 Files
- [`legacy/everything-claude-code/agents/planner.md`](legacy/everything-claude-code/agents/planner.md)
- [`legacy/everything-claude-code/agents/code-reviewer.md`](legacy/everything-claude-code/agents/code-reviewer.md)

### Layer 3 Files
- [`legacy/claude-code/src/Tool.ts`](legacy/claude-code/src/Tool.ts)
- [`legacy/claude-code/src/tools/`](legacy/claude-code/src/tools/)
- [`legacy/hermes-agent/tools/registry.py`](legacy/hermes-agent/tools/registry.py)
- [`legacy/hermes-agent/tools/file_tools.py`](legacy/hermes-agent/tools/file_tools.py)
- [`legacy/hermes-agent/tools/terminal_tool.py`](legacy/hermes-agent/tools/terminal_tool.py)

### Layer 4 Files
- [`legacy/claude-code/src/services/autoDream/autoDream.ts`](legacy/claude-code/src/services/autoDream/autoDream.ts)
- [`legacy/hermes-agent/agent/curator.py`](legacy/hermes-agent/agent/curator.py)
- [`legacy/hermes-agent/tools/skills_hub.py`](legacy/hermes-agent/tools/skills_hub.py)

### Layer 5 Files
- [`legacy/claude-code/src/memdir/memdir.ts`](legacy/claude-code/src/memdir/memdir.ts)
- [`legacy/claude-code/src/memdir/memoryTypes.ts`](legacy/claude-code/src/memdir/memoryTypes.ts)
- [`legacy/hermes-agent/agent/memory_manager.py`](legacy/hermes-agent/agent/memory_manager.py)
- [`legacy/hermes-agent/agent/context_compressor.py`](legacy/hermes-agent/agent/context_compressor.py)

### Layer 6 Files
- [`legacy/hermes-agent/agent/credential_pool.py`](legacy/hermes-agent/agent/credential_pool.py)
- [`legacy/hermes-agent/agent/error_classifier.py`](legacy/hermes-agent/agent/error_classifier.py)
- [`legacy/hermes-agent/tools/tirith_security.py`](legacy/hermes-agent/tools/tirith_security.py)

---

## 12. Usage Instructions

This reference document serves as the authoritative mapping between industry reference implementations and the Torro Agent architecture. When implementing any Torro layer:

1. **Identify the target layer** from the architecture plan
2. **Find the primary reference** in Section 9's Implementation Priority Matrix
3. **Read the referenced files** using the exact paths provided
4. **Adapt the pattern** to Torro's Python/SQLModel/Airflow stack
5. **Cross-reference secondary patterns** from other frameworks for completeness
