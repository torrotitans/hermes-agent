# Tool Permission Pattern

## Overview

The tool permission pattern implements a security layer for AI agent tool execution. It provides:
- Permission prompts for dangerous operations
- Configurable permission modes (default, auto, bypass)
- Hook-based permission automation
- Session-level permission caching

## Permission Modes

### Default Mode
Ask user for each dangerous command:
```
┌─ Permission Required ──────────────────────────┐
│ Tool: BashTool                                 │
│ Command: rm -rf /tmp/cache                     │
│ Risk: Destructive file operation               │
│                                                │
│ [A] Allow once  [S] Always allow  [D] Deny    │
└─────────────────────────────────────────────────┘
```

### Auto Mode
Allow read-only operations, ask for writes:
```python
PERMISSION_MODES = {
    'default': 'ask_all',
    'auto': 'allow_read_ask_write',
    'bypass': 'allow_all'
}
```

### Bypass Mode (YOLO)
Allow all operations without prompts:
```python
if os.getenv('HERMES_YOLO_MODE') == '1':
    permission_mode = 'bypass'
```

## Core Implementation

### Permission Decision Types

```typescript
type PermissionDecision = 
  | { behavior: 'allow'; updatedInput?: Record<string, unknown> }
  | { behavior: 'deny'; message: string }

type PermissionDecisionReason = 
  | { type: 'rule'; rule: string }
  | { type: 'mode'; mode: string }
  | { type: 'hook'; hookName: string }
  | { type: 'classifier'; reason: string }
```

### Permission Check Flow

```typescript
async function hasPermissionsToUseTool(
  tool: Tool,
  input: Record<string, unknown>,
  toolUseContext: ToolUseContext,
  assistantMessage: AssistantMessage,
  toolUseID: string
): Promise<PermissionDecision> {
  // 1. Check cached permissions
  const cached = checkPermissionCache(tool.name, input)
  if (cached) return cached
  
  // 2. Run permission hooks
  const hookDecision = await executePermissionHooks(tool, input)
  if (hookDecision) return hookDecision
  
  // 3. Check mode-based rules
  const modeDecision = checkModePermissions(tool, input)
  if (modeDecision.behavior !== 'ask') return modeDecision
  
  // 4. Prompt user
  return promptUserForPermission(tool, input, toolUseID)
}
```

### Permission Hooks

Hooks allow programmatic permission decisions:

```typescript
async function executePermissionRequestHooks(
  toolName: string,
  toolUseID: string,
  input: Record<string, unknown>,
  toolUseContext: ToolUseContext,
  permissionMode: string,
  suggestions: PermissionUpdate[]
): AsyncGenerator<HookResult> {
  // Run all registered hooks
  for (const hook of registeredHooks) {
    const result = await hook({
      toolName,
      toolUseID,
      input,
      permissionMode,
    })
    
    if (result.decision) {
      yield { decision: result.decision }
    }
  }
}
```

### Permission Cache

Cache user decisions for the session:

```python
class PermissionCache:
    def __init__(self):
        self._cache = {}  # tool_name -> set of allowed inputs
        self._always_allow = set()  # tool names
    
    def add(self, tool_name: str, input_hash: str, always: bool):
        if always:
            self._always_allow.add(tool_name)
        else:
            if tool_name not in self._cache:
                self._cache[tool_name] = set()
            self._cache[tool_name].add(input_hash)
    
    def check(self, tool_name: str, input_hash: str) -> bool:
        if tool_name in self._always_allow:
            return True
        return input_hash in self._cache.get(tool_name, set())
```

## Tool Categories

### Read-Only Tools (Auto-allowed in auto mode)
- `FileReadTool` - Read file contents
- `ListDirectoryTool` - List directory contents
- `SearchTool` - Search files with grep/ripgrep

### Write Tools (Require permission)
- `FileEditTool` - Modify file contents
- `FileWriteTool` - Create/overwrite files
- `BashTool` - Execute shell commands

### Dangerous Tools (Always require permission)
- `RecursiveDeleteTool` - Delete directories
- `SystemCommandTool` - Execute system commands
- `NetworkTool` - Make network requests

## Permission Prompt UI

### Python (prompt_toolkit)

```python
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.formatted_text import HTML

def show_permission_prompt(tool_name: str, command: str, risk: str):
    result = radiolist_dialog(
        title="Permission Required",
        text=HTML(f"""
            <b>Tool:</b> {tool_name}<br/>
            <b>Command:</b> {command}<br/>
            <b>Risk:</b> {risk}<br/>
            <br/>
            Allow this operation?
        """),
        values=[
            ("allow_once", "Allow once"),
            ("always", "Always allow this tool"),
            ("deny", "Deny"),
        ]
    ).run()
    
    return result.result
```

### TypeScript (Ink)

```typescript
import { Box, Text, useInput } from 'ink'

interface PermissionPromptProps {
  toolName: string
  command: string
  risk: string
  onDecision: (decision: string) => void
}

export function PermissionPrompt({
  toolName,
  command,
  risk,
  onDecision
}: PermissionPromptProps) {
  useInput((input) => {
    if (input === 'a') onDecision('allow_once')
    if (input === 's') onDecision('always')
    if (input === 'd') onDecision('deny')
  })
  
  return (
    <Box flexDirection="column" borderStyle="round" borderColor="yellow">
      <Text bold>Permission Required</Text>
      <Text>Tool: {toolName}</Text>
      <Text>Command: {command}</Text>
      <Text color="red">Risk: {risk}</Text>
      <Box marginTop={1}>
        <Text color="green">[A]</Text>
        <Text> Allow once  </Text>
        <Text color="green">[S]</Text>
        <Text> Always allow  </Text>
        <Text color="red">[D]</Text>
        <Text> Deny</Text>
      </Box>
    </Box>
  )
}
```

## Security Considerations

### Path Traversal Protection

```python
def validate_path_safety(path: str, allowed_dirs: list) -> bool:
    """Prevent path traversal attacks."""
    resolved = os.path.realpath(path)
    for allowed in allowed_dirs:
        if resolved.startswith(allowed):
            return True
    return False
```

### Command Injection Prevention

```typescript
function sanitizeCommandInput(input: string): string {
  // Remove shell metacharacters
  const dangerous = [';', '|', '&', '$', '`', '>', '<', '(', ')']
  let sanitized = input
  for (const char of dangerous) {
    sanitized = sanitized.replace(new RegExp(char, 'g'), '')
  }
  return sanitized.trim()
}
```

### Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = []
    
    def check(self) -> bool:
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.window]
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True
```

## Testing

### Unit Test Example

```python
def test_permission_cache():
    cache = PermissionCache()
    
    # Test cache miss
    assert cache.check('BashTool', 'hash1') == False
    
    # Test single add
    cache.add('BashTool', 'hash1', False)
    assert cache.check('BashTool', 'hash1') == True
    assert cache.check('BashTool', 'hash2') == False
    
    # Test always allow
    cache.add('BashTool', 'hash3', True)
    assert cache.check('BashTool', 'hash3') == True
    assert cache.check('BashTool', 'hash4') == False
```

## Related Files

- [`legacy/claude-code/src/tools/BashTool/bashPermissions.ts`](../../legacy/claude-code/src/tools/BashTool/bashPermissions.ts) - Bash permission rules
- [`legacy/claude-code/src/utils/permissions/permissions.ts`](../../legacy/claude-code/src/utils/permissions/permissions.ts) - Permission utilities
- [`legacy/hermes-agent/tools/approval.py`](../../legacy/hermes-agent/tools/approval.py) - Python approval tool
