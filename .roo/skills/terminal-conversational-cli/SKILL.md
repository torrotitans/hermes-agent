---
name: terminal-conversational-cli
description: Build terminal conversational CLI interfaces with structured I/O, interactive TUI, tool permissions, and session management. USE FOR: terminal UI, conversational interface, REPL, interactive CLI, prompt_toolkit, Ink/React CLI, structured IO, tool permissions, session management, streaming responses. DO NOT USE FOR: web UI, GUI applications, non-interactive scripts.
---

# Terminal Conversational CLI

Build terminal-based conversational interfaces for AI agents with interactive TUI, structured I/O, tool permissions, and session management.

## When to Use

Use this skill when building:
- Interactive AI agent CLI with streaming responses
- Terminal UI with real-time status updates
- REPL interfaces for conversational interactions
- Tool-based command execution with permission prompts
- Session-aware conversations with history persistence

## When NOT to Use

- Web-based interfaces (use web UI patterns instead)
- Non-interactive batch scripts
- GUI applications requiring mouse interaction

## Core Architecture

### 1. Structured I/O Layer

Implement NDJSON (newline-delimited JSON) for stdin/stdout communication:

```typescript
// StructuredIO pattern from Claude Code
class StructuredIO {
  async write(message: StdoutMessage): Promise<void> {
    writeToStdout(ndjsonSafeStringify(message) + '\n')
  }
  
  async *read(): AsyncGenerator<StdinMessage> {
    // Parse NDJSON lines, handle control responses
    for await (const line of this.input) {
      const message = jsonParse(line)
      yield message
    }
  }
}
```

Key message types:
- `user`: User input messages
- `assistant`: AI response messages  
- `system`: System notifications
- `control_request`: Tool permission requests
- `control_response`: Permission decisions

### 2. Interactive TUI Layer

Choose rendering engine based on language:

**Python (prompt_toolkit):**
```python
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import TextArea

# Create interactive application with status bar
app = Application(
    layout=Layout(HSplit([
        Window(content=output_buffer),
        TextArea(name="input"),
        Window(content=status_bar)
    ])),
    full_screen=True
)
```

**TypeScript (Ink/React):**
```typescript
import { render, Box, Text } from 'ink'
import React from 'react'

function App() {
  return (
    <Box flexDirection="column">
      <Text>Assistant response</Text>
      <Text>⏱ 2m 30s</Text>
    </Box>
  )
}

render(<App />)
```

### 3. Tool Permission System

Implement permission prompts for dangerous operations:

```typescript
// Permission flow from Claude Code
async function hasPermissionsToUseTool(
  tool: Tool,
  input: Record<string, unknown>,
  toolUseID: string
): Promise<PermissionDecision> {
  // Check cached permissions
  // Run permission hooks
  // Send control_request for user approval
  const decision = await sendRequest(
    { subtype: 'can_use_tool', tool_name: tool.name },
    permissionToolOutputSchema
  )
  return decision
}
```

Permission modes:
- `default`: Ask for each dangerous command
- `auto`: Allow read-only, ask for writes
- `bypass`: Allow all (YOLO mode)

### 4. Session Management

Track conversation state with SQLite:

```python
# SessionDB pattern from Hermes Agent
class SessionDB:
    def __init__(self):
        self.db_path = get_hermes_home() / "state.db"
    
    def create_session(self, session_id: str, source: str):
        # Track session metadata
        pass
    
    def add_message(self, session_id: str, role: str, content: str):
        # Persist conversation history
        pass
    
    def get_session(self, session_id: str) -> dict:
        # Retrieve session with token counts
        pass
```

Session features:
- Unique session IDs with timestamps
- Message history persistence
- Token usage tracking
- Compression support for long sessions

### 5. Streaming Response Handler

Handle token-level streaming with progress indicators:

```python
# Streaming pattern from Hermes Agent
def _stream_response(self, response_stream):
    for chunk in response_stream:
        if chunk.type == "content":
            self._output_buffer.write(chunk.text)
            self._invalidate()  # Refresh TUI
        elif chunk.type == "tool_use":
            self._render_tool_call(chunk.tool_name, chunk.args)
```

## Key Components

### Status Bar

Display real-time session metrics:
- Model name and provider
- Context tokens / limit
- Session duration
- Token usage (input/output/cache)

### Spinner/Progress Indicator

Show activity during long operations:
```python
_SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

def _render_spinner(self, frame_index: int, elapsed: str) -> str:
    return f"{_SPINNER_FRAMES[frame_index]} Processing... ({elapsed})"
```

### Tool Call Display

Render tool invocations with collapsible output:
```
┌─ BashTool ─────────────────────────────┐
│ $ ls -la                               │
│ total 48                               │
│ drwxr-xr-x  1 user  staff   32 Oct 1  │
└─────────────────────────────────────────┘
```

### Slash Command Registry

Implement extensible commands:
```python
COMMAND_REGISTRY = [
    CommandDef("new", "Start new session", "Session"),
    CommandDef("model", "Switch model", "Configuration", 
               args_hint="[model]"),
    CommandDef("tools", "Manage tools", "Tools & Skills",
               subcommands=("list", "enable", "disable")),
]
```

## Implementation Checklist

- [ ] Structured I/O with NDJSON parsing
- [ ] Interactive TUI with status bar
- [ ] Tool permission system with control requests
- [ ] Session database for history persistence
- [ ] Streaming response handler
- [ ] Slash command registry
- [ ] Token usage tracking
- [ ] Context compression support

## References

- [`StructuredIO`](legacy/claude-code/src/cli/structuredIO.ts:135) - NDJSON I/O implementation
- [`BashTool`](legacy/claude-code/src/tools/BashTool/BashTool.tsx:1) - Tool permission pattern
- [`HermesCLI`](legacy/hermes-agent/cli.py:1837) - Python prompt_toolkit TUI
- [`COMMAND_REGISTRY`](legacy/hermes-agent/hermes_cli/commands.py:59) - Slash command definitions
