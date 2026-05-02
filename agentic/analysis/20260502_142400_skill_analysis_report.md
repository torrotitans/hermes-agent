---
Create Date: 2026-05-02
Update Date: 2026-05-02
IDE: Roo Code
Agent: Qwen3.5-397B-A17B-int4-AutoRound
GitHub committer: q4r00t
---

# Consolidated Skill Analysis Report

## Executive Summary

This report analyzes the skill systems across four legacy AI agent frameworks: **Roo-Code**, **Claude Code**, **Hermes Agent**, and **Everything Claude Code (ECC)**. The analysis identifies patterns, best practices, and architectural decisions that inform the Torro Agent Skills Library and Skill Registry design.

## 1. Skill System Overview

### 1.1 Roo-Code Skills

**Location:** `legacy/Roo-Code/src/core/tools/SkillTool.ts`

**Key Characteristics:**
- Integrated as a first-class tool in the core tool system
- Skills are discovered and loaded dynamically
- Skills follow a standardized interface with `checkPermissions()`, `validateInput()`, and `call()` methods
- Skills are organized by domain categories

**Skill Categories Found:**
- `accessMcpResourceTool.ts` - MCP resource access
- `ApplyDiffTool.ts` - Code diff application
- `ApplyPatchTool.ts` - Patch application
- `AskFollowupQuestionTool.ts` - Interactive questioning
- `AttemptCompletionTool.ts` - Task completion
- `CodebaseSearchTool.ts` - Code search
- `EditFileTool.ts` - File editing
- `ExecuteCommandTool.ts` - Command execution
- `GenerateImageTool.ts` - Image generation
- `ListFilesTool.ts` - File listing
- `NewTaskTool.ts` - Task creation
- `ReadCommandOutputTool.ts` - Command output reading
- `ReadFileTool.ts` - File reading
- `RunSlashCommandTool.ts` - Slash command execution
- `SearchAndReplaceTool.ts` - Search and replace
- `SearchFilesTool.ts` - File search
- `SkillTool.ts` - Skill execution (meta-skill)
- `SwitchModeTool.ts` - Mode switching
- `ToolRepetitionDetector.ts` - Repetition detection
- `UpdateTodoListTool.ts` - Todo management
- `UseMcpToolTool.ts` - MCP tool usage
- `WriteToFileTool.ts` - File writing

### 1.2 Claude Code Skills

**Location:** `legacy/claude-code/src/services/autoDream/autoDream.ts`

**Key Characteristics:**
- Skills are memory-based consolidation patterns
- `autoDream` service fires periodically to consolidate session learnings
- Skills are triggered by time-gates and session accumulation
- Skills focus on memory optimization and context management

**Skill Patterns:**
- `SESSION_SCAN_INTERVAL_MS = 10 * 60 * 1000` (10 minute intervals)
- `minHours: 24` - Minimum hours between consolidations
- `minSessions: 5` - Minimum sessions before consolidation
- Gate-based execution (cheapest checks first)

### 1.3 Hermes Agent Skills

**Location:** `legacy/hermes-agent/skills/`

**Key Characteristics:**
- Organized by domain categories (24 top-level categories)
- Each skill has a `SKILL.md` file with YAML frontmatter
- Skills follow a standardized template with description, usage, and examples
- Skills can have sub-categories and nested structures

**Skill Categories:**
- `apple/` - Apple ecosystem integration
- `autonomous-ai-agents/` - Autonomous agent patterns
- `creative/` - Creative workflows
- `data-science/` - Data science tools
- `devops/` - DevOps automation
- `diagramming/` - Diagram generation
- `dogfood/` - Internal tooling
- `domain/` - Domain-specific skills
- `email/` - Email integration
- `gaming/` - Gaming utilities
- `gifs/` - GIF creation/search
- `github/` - GitHub operations
- `index-cache/` - Caching strategies
- `inference-sh/` - Inference shell scripts
- `mcp/` - Model Context Protocol
- `media/` - Media processing
- `mlops/` - ML operations
- `note-taking/` - Note management
- `productivity/` - Productivity tools
- `red-teaming/` - Security testing
- `research/` - Research utilities
- `smart-home/` - Smart home integration
- `social-media/` - Social media automation
- `software-development/` - Development tools
- `yuanbao/` - Tencent Yuanbao integration

**Example Skill Structure:**
```
skills/mlops/inference/llama-cpp/SKILL.md
skills/mlops/inference/llama-cpp/references/advanced-usage.md
skills/mlops/inference/llama-cpp/references/hub-discovery.md
skills/mlops/inference/llama-cpp/references/optimization.md
skills/mlops/inference/llama-cpp/references/quantization.md
skills/mlops/inference/llama-cpp/references/server.md
skills/mlops/inference/llama-cpp/references/troubleshooting.md
```

### 1.4 Everything Claude Code (ECC) Skills

**Location:** `legacy/everything-claude-code/skills/`

**Key Characteristics:**
- Most extensive skill library (182+ skills)
- Organized by functional domains
- Each skill has detailed documentation and examples
- Skills include cross-references and dependency information

**Skill Categories (100+ categories):**
- `accessibility/` - Accessibility compliance
- `agent-eval/` - Agent evaluation
- `agent-harness-construction/` - Agent building
- `agent-introspection-debugging/` - Agent debugging
- `agentic-engineering/` - Agentic patterns
- `ai-first-engineering/` - AI-native development
- `ai-regression-testing/` - AI testing
- `android-clean-architecture/` - Android patterns
- `api-connector-builder/` - API integration
- `architecture-decision-records/` - ADRs
- `article-writing/` - Content creation
- `automation-audit-ops/` - Automation auditing
- `autonomous-agent-harness/` - Agent harnesses
- `autonomous-loops/` - Autonomous loops
- `backend-patterns/` - Backend development
- `benchmark/` - Performance benchmarking
- `blueprint/` - Blueprint generation
- `brand-voice/` - Brand consistency
- `browser-qa/` - Browser testing
- `bun-runtime/` - Bun runtime
- `canary-watch/` - Canary deployments
- ... (100+ more categories)

## 2. Skill System Comparison

| Feature | Roo-Code | Claude Code | Hermes Agent | ECC | Torro Target |
|---------|----------|-------------|--------------|-----|--------------|
| Skill Format | TypeScript classes | Memory patterns | SKILL.md | SKILL.md | SKILL.md + Registry |
| Discovery | Dynamic loading | Time-gated | Directory scan | Directory scan | Skill Registry |
| Organization | Tool-based | Consolidation | Domain categories | Functional domains | Vector + Graph |
| Version Tracking | Git-based | Session-based | Manual | Manual | Automated |
| Dependencies | Import-based | Implicit | Manual | Manual | Graph-based |
| Context Firewall | Runtime checks | Time gates | Manual | Manual | Automated |
| Lifecycle | Load/unload | Periodic | Manual | Manual | Automated |

## 3. Key Patterns Identified

### 3.1 Skill Discovery Patterns

**Roo-Code Pattern:**
```typescript
// Dynamic tool registration
const tools = [
  new SkillTool(),
  new ReadFileTool(),
  new WriteToFileTool(),
  // ... more tools
];
```

**Hermes Agent Pattern:**
```python
# Directory-based discovery
def discover_skills(skill_dir: Path) -> List[Skill]:
    skills = []
    for category in skill_dir.iterdir():
        if category.is_dir():
            skill_file = category / "SKILL.md"
            if skill_file.exists():
                skills.append(load_skill(skill_file))
    return skills
```

**ECC Pattern:**
```yaml
# YAML frontmatter discovery
---
name: api-connector-builder
description: Build API connectors with validation
tools: [read, write, bash]
---
```

### 3.2 Skill Execution Patterns

**Roo-Code Pattern:**
```typescript
class SkillTool {
  async call(input: SkillInput, context: ToolCallContext) {
    // Validate permissions
    await this.checkPermissions();
    // Validate input
    this.validateInput(input);
    // Execute skill
    return await this.execute(input, context);
  }
}
```

**Hermes Agent Pattern:**
```python
class SkillManager:
    def execute_skill(self, skill_name: str, context: Dict) -> Any:
        skill = self.load_skill(skill_name)
        skill.validate(context)
        return skill.run(context)
```

### 3.3 Skill Lifecycle Patterns

**Claude Code autoDream Pattern:**
```typescript
// Time-gated consolidation
function shouldConsolidate(): boolean {
  if (hoursSinceLastConsolidated >= minHours) {
    if (sessionCount >= minSessions) {
      return true;
    }
  }
  return false;
}
```

**Hermes Curator Pattern:**
```python
# Inactivity-triggered maintenance
DEFAULT_INTERVAL_HOURS = 24 * 7  # 7 days
DEFAULT_MIN_IDLE_HOURS = 2
DEFAULT_STALE_AFTER_DAYS = 30
DEFAULT_ARCHIVE_AFTER_DAYS = 90
```

## 4. Torro Agent Skill System Design

### 4.1 Skills Library Storage

Based on the analysis, Torro Agent Skills Library should:

1. **Store SKILL.md workflows** with complete metadata:
   - YAML frontmatter (name, description, version)
   - Context firewall definitions
   - Dependency graph
   - Usage analytics

2. **Organize by domain categories** mirroring Hermes/ECC patterns:
   - `mlops/` - ML operations
   - `research/` - Research utilities
   - `productivity/` - Productivity tools
   - `devops/` - DevOps automation
   - `security/` - Security auditing

3. **Implement version history**:
   - Track all refinements from Layer 4
   - Maintain changelog per skill
   - Support rollback to previous versions

### 4.2 Skill Registry Index

The Skill Registry should provide:

1. **Fast lookup** by:
   - Skill name
   - Description keywords
   - Usage patterns
   - Domain category

2. **Dependency graph** using Apache AGE:
   - Track skill-to-skill dependencies
   - Detect circular dependencies
   - Calculate load order

3. **Lifecycle state tracking**:
   - Active: Currently available
   - Deprecated: Scheduled for removal
   - Archived: Historical reference

4. **Cross-reference links**:
   - Related Agentic Plans
   - Analysis logs
   - Experience entries

### 4.3 Skill Refinement Engine

Based on Hermes Curator pattern:

```python
class SkillRefinementEngine:
    """Background skill maintenance orchestrator.
    
    Responsibilities:
    - Auto-transition lifecycle states based on usage
    - Spawn background refinement tasks
    - Persist refinement state
    """
    
    DEFAULT_INTERVAL_HOURS = 24 * 7
    DEFAULT_MIN_IDLE_HOURS = 2
    DEFAULT_STALE_AFTER_DAYS = 30
    DEFAULT_ARCHIVE_AFTER_DAYS = 90
```

## 5. Recommendations

### 5.1 Immediate Actions

1. **Implement Skill Discovery** - Directory-based scanning like Hermes/ECC
2. **Standardize SKILL.md Format** - YAML frontmatter with mandatory fields
3. **Build Skill Registry** - Apache AGE graph for dependencies
4. **Create Refinement Engine** - Time-gated maintenance like Claude Code autoDream

### 5.2 Long-term Enhancements

1. **Vector Search** - Semantic skill discovery beyond keyword matching
2. **Usage Analytics** - Track success rates, invocation frequency
3. **Automated Testing** - Test harness for skill validation
4. **Community Marketplace** - Share skills across Torro instances

## 6. Implementation Checklist

- [ ] Create `src/memory/skills_library.py` with SQLModel schemas
- [ ] Create `src/memory/skill_registry.py` for version tracking
- [ ] Implement skill discovery scanner
- [ ] Build dependency graph with Apache AGE
- [ ] Create skill refinement engine
- [ ] Implement lifecycle state transitions
- [ ] Add usage analytics tracking
- [ ] Build skill testing framework
- [ ] Create skill documentation generator
- [ ] Implement skill marketplace interface

## 7. References

- [`legacy/Roo-Code/src/core/tools/SkillTool.ts`](legacy/Roo-Code/src/core/tools/SkillTool.ts)
- [`legacy/claude-code/src/services/autoDream/autoDream.ts`](legacy/claude-code/src/services/autoDream/autoDream.ts)
- [`legacy/hermes-agent/agent/curator.py`](legacy/hermes-agent/agent/curator.py)
- [`legacy/hermes-agent/skills/`](legacy/hermes-agent/skills/)
- [`legacy/everything-claude-code/skills/`](legacy/everything-claude-code/skills/)

## 8. Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-02 | Initial skill analysis report | Agentic Planner |
