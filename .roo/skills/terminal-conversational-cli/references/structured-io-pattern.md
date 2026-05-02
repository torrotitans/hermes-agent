# Structured I/O Pattern

## Overview

The Structured I/O pattern implements newline-delimited JSON (NDJSON) for bidirectional communication between the CLI and AI agent. This enables streaming responses, tool permissions, and control messages.

## Message Types

### Stdin Messages (from host to CLI)

```typescript
type StdinMessage = 
  | { type: 'user'; message: { role: 'user'; content: string } }
  | { type: 'assistant'; message: { role: 'assistant'; content: string } }
  | { type: 'system'; message: { role: 'system'; content: string } }
  | { type: 'control_response'; response: ControlResponse }
```

### Stdout Messages (from CLI to host)

```typescript
type StdoutMessage =
  | { type: 'user'; message: { role: 'user'; content: string } }
  | { type: 'assistant'; message: { role: 'assistant'; content: string } }
  | { type: 'system'; message: { role: 'system'; content: string } }
  | { type: 'control_request'; request: ControlRequest }
```

### Control Request Types

```typescript
type ControlRequest = {
  subtype: 'can_use_tool' | 'hook_callback' | 'elicitation' | 'mcp_message'
  tool_name?: string
  input?: Record<string, unknown>
  permission_suggestions?: PermissionUpdate[]
  tool_use_id: string
  agent_id?: string
}
```

### Control Response Types

```typescript
type ControlResponse = {
  subtype: 'success' | 'error'
  response?: {
    behavior: 'allow' | 'deny'
    updatedInput?: Record<string, unknown>
    toolUseID: string
  }
  error?: string
}
```

## Implementation

### Core Class Structure

```typescript
export class StructuredIO {
  readonly structuredInput: AsyncGenerator<StdinMessage>
  private readonly pendingRequests = new Map<string, PendingRequest<unknown>>()
  private readonly resolvedToolUseIds = new Set<string>()
  readonly outbound = new Stream<StdoutMessage>()

  constructor(private readonly input: AsyncIterable<string>) {
    this.structuredInput = this.read()
  }

  private async *read() {
    let content = ''
    for await (const block of this.input) {
      content += block
      yield* this.splitAndProcess(content)
    }
  }

  private async processLine(line: string): Promise<StdinMessage | undefined> {
    const message = jsonParse(line)
    
    // Handle control responses
    if (message.type === 'control_response') {
      const request = this.pendingRequests.get(message.response.request_id)
      if (request) {
        this.pendingRequests.delete(message.response.request_id)
        request.resolve(message.response.response)
      }
      return undefined
    }
    
    return message
  }

  async write(message: StdoutMessage): Promise<void> {
    writeToStdout(ndjsonSafeStringify(message) + '\n')
  }
}
```

### Permission Request Flow

```typescript
async function hasPermissionsToUseTool(
  tool: Tool,
  input: Record<string, unknown>,
  toolUseID: string
): Promise<PermissionDecision> {
  const requestId = randomUUID()
  
  // Send control request to host
  const result = await this.sendRequest<PermissionToolOutput>(
    {
      subtype: 'can_use_tool',
      tool_name: tool.name,
      input,
      tool_use_id: toolUseID,
    },
    permissionToolOutputSchema,
    undefined,
    requestId
  )
  
  return permissionPromptToolResultToPermissionDecision(
    result,
    tool,
    input,
    toolUseContext
  )
}
```

### Request/Response Pattern

```typescript
private async sendRequest<Response>(
  request: SDKControlRequest['request'],
  schema: z.Schema,
  signal?: AbortSignal,
  requestId: string = randomUUID()
): Promise<Response> {
  const message: SDKControlRequest = {
    type: 'control_request',
    request_id: requestId,
    request,
  }
  
  this.outbound.enqueue(message)
  
  return await new Promise<Response>((resolve, reject) => {
    this.pendingRequests.set(requestId, {
      request: message,
      resolve,
      reject,
      schema,
    })
  })
}
```

## Key Design Decisions

### 1. NDJSON Format

Using newline-delimited JSON enables:
- Line-by-line streaming parsing
- Easy debugging with `jq` or `cat`
- Compatibility with Unix pipes
- Simple concatenation for session replay

### 2. Pending Request Map

Track outstanding permission requests with a Map:
- Prevents race conditions
- Enables timeout handling
- Supports concurrent tool executions

### 3. Resolved Tool Use ID Tracking

Track resolved tool_use IDs to prevent duplicate processing:
```typescript
private readonly resolvedToolUseIds = new Set<string>()

private trackResolvedToolUseId(request: SDKControlRequest): void {
  if (request.request.subtype === 'can_use_tool') {
    this.resolvedToolUseIds.add(request.request.tool_use_id)
    if (this.resolvedToolUseIds.size > MAX_RESOLVED_TOOL_USE_IDS) {
      const first = this.resolvedToolUseIds.values().next().value
      if (first !== undefined) {
        this.resolvedToolUseIds.delete(first)
      }
    }
  }
}
```

### 4. Abort Signal Support

Support cancellation via AbortSignal:
```typescript
const aborted = () => {
  this.outbound.enqueue({
    type: 'control_cancel_request',
    request_id: requestId,
  })
  const request = this.pendingRequests.get(requestId)
  if (request) {
    request.reject(new AbortError())
  }
}

if (signal) {
  signal.addEventListener('abort', aborted, { once: true })
}
```

## Error Handling

### Parse Errors

```typescript
try {
  const message = jsonParse(line)
  return message
} catch (error) {
  console.error(`Error parsing streaming input line: ${line}: ${error}`)
  process.exit(1)
}
```

### Timeout Handling

```typescript
const timeoutId = setTimeout(() => {
  request.reject(new Error('Permission request timeout'))
}, PERMISSION_TIMEOUT_MS)

try {
  return await promise
} finally {
  clearTimeout(timeoutId)
}
```

## Testing

### Unit Test Example

```typescript
describe('StructuredIO', () => {
  it('should parse user messages', async () => {
    const input = ['{"type":"user","message":{"role":"user","content":"hello"}}\n']
    const io = new StructuredIO(input)
    
    const messages = []
    for await (const msg of io.structuredInput) {
      messages.push(msg)
    }
    
    expect(messages[0].type).toBe('user')
    expect(messages[0].message.content).toBe('hello')
  })
})
```

## Related Files

- [`legacy/claude-code/src/cli/structuredIO.ts`](../../legacy/claude-code/src/cli/structuredIO.ts) - Full implementation
- [`legacy/claude-code/src/cli/ndjsonSafeStringify.ts`](../../legacy/claude-code/src/cli/ndjsonSafeStringify.ts) - JSON stringify utility
