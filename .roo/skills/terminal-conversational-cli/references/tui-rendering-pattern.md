# TUI Rendering Pattern

## Overview

Terminal UI rendering for conversational CLI requires handling streaming content, real-time status updates, and responsive layouts. This document covers patterns for both Python (prompt_toolkit) and TypeScript (Ink/React).

## Python: prompt_toolkit

### Basic Application Structure

```python
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.widgets import TextArea, Label
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings

# Create key bindings
kb = KeyBindings()

@kb.add('c-c')
def _(event):
    event.app.exit()

# Create text areas
output_buffer = TextArea(style="class:output")
input_buffer = TextArea(
    placeholder="Type your message...",
    accept_handler=lambda buff: handle_input(buff.text)
)

# Create status bar
status_bar = FormattedTextControl(
    text=lambda: f"Model: {model_name} | Tokens: {token_count}"
)

# Create layout
layout = Layout(
    HSplit([
        Window(content=output_buffer, height=Layout.DIM_PREFERRED),
        VSplit([
            Window(),
            Window(content=input_buffer, height=3),
            Window(),
        ]),
        Window(height=1, content=status_bar, style="class:status-bar"),
    ])
)

# Create application
app = Application(
    layout=layout,
    key_bindings=kb,
    full_screen=True,
    mouse_support=True
)

app.run()
```

### Streaming Output Buffer

```python
class OutputBuffer:
    def __init__(self):
        self.lines = []
        self.max_lines = 1000
    
    def write(self, text: str):
        """Append text to buffer, maintaining max lines."""
        self.lines.append(text)
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]
    
    def get_text(self) -> str:
        return '\n'.join(self.lines)
    
    def clear(self):
        self.lines = []
```

### Status Bar with Live Updates

```python
class StatusBar:
    def __init__(self, app: Application):
        self.app = app
        self.model_name = "unknown"
        self.token_count = 0
        self.context_percent = 0
    
    def get_text(self) -> str:
        return (
            f"⚕ {self.model_name} | "
            f"Context: {self.context_percent}% | "
            f"Tokens: {self.token_count}"
        )
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.app.invalidate()  # Trigger re-render
```

### Spinner/Progress Indicator

```python
import time
from prompt_toolkit.formatted_text import FormattedText

class Spinner:
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self):
        self.frame_index = 0
        self.start_time = None
        self.is_active = False
    
    def start(self):
        self.is_active = True
        self.start_time = time.time()
    
    def stop(self):
        self.is_active = False
        self.frame_index = 0
    
    def get_text(self) -> str:
        if not self.is_active:
            return ""
        
        elapsed = time.time() - self.start_time
        frame = self.FRAMES[self.frame_index % len(self.FRAMES)]
        self.frame_index += 1
        
        return f"{frame} Processing... ({elapsed:.1f}s)"
```

### Layout Management

```python
from prompt_toolkit.layout import Dimension

# Responsive layout based on terminal width
def get_layout_widths(terminal_width: int):
    if terminal_width < 60:
        return {"sidebar": 0, "main": None}
    elif terminal_width < 100:
        return {"sidebar": 30, "main": None}
    else:
        return {"sidebar": 40, "main": None}

# Conditional visibility
from prompt_toolkit.layout.containers import ConditionalContainer

sidebar = ConditionalContainer(
    content=Window(content=sidebar_content),
    filter=Condition(lambda: terminal_width >= 60)
)
```

## TypeScript: Ink/React

### Basic Component Structure

```typescript
import React, { useState, useEffect } from 'react'
import { Box, Text, useApp } from 'ink'

interface AppProps {
  messages: Message[]
  status: Status
}

export function App({ messages, status }: AppProps) {
  const { exit } = useApp()
  
  return (
    <Box flexDirection="column">
      <Box flexDirection="column" marginBottom={1}>
        {messages.map((msg, i) => (
          <Message key={i} message={msg} />
        ))}
      </Box>
      
      <Box marginTop={1}>
        <Text color="green">⚕ {status.model}</Text>
        <Text color="gray"> | </Text>
        <Text color="blue">{status.tokens} tokens</Text>
      </Box>
    </Box>
  )
}
```

### Streaming Message Component

```typescript
import { Text } from 'ink'
import { useEffect, useState } from 'react'

interface MessageProps {
  message: {
    role: 'user' | 'assistant'
    content: string
  }
}

export function Message({ message }: MessageProps) {
  const [displayed, setDisplayed] = useState('')
  
  useEffect(() => {
    // Typewriter effect
    let index = 0
    const interval = setInterval(() => {
      setDisplayed(message.content.slice(0, index + 1))
      index++
      if (index >= message.content.length) {
        clearInterval(interval)
      }
    }, 10)
    
    return () => clearInterval(interval)
  }, [message.content])
  
  return (
    <Box>
      <Text color={message.role === 'user' ? 'green' : 'white'}>
        {message.role === 'user' ? '> ' : '< '}
        {displayed}
      </Text>
    </Box>
  )
}
```

### Status Bar with Live Updates

```typescript
import { Box, Text, useApp } from 'ink'
import { useEffect, useState } from 'react'

interface StatusBarProps {
  model: string
  tokens: number
  contextPercent: number
}

export function StatusBar({ model, tokens, contextPercent }: StatusBarProps) {
  const [elapsed, setElapsed] = useState(0)
  
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed(t => t + 1)
    }, 1000)
    return () => clearInterval(timer)
  }, [])
  
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}m ${secs}s`
  }
  
  return (
    <Box marginTop={1} flexDirection="column">
      <Box>
        <Text color="cyan">⚕ {model}</Text>
        <Text> | </Text>
        <Text color="yellow">Context: {contextPercent}%</Text>
        <Text> | </Text>
        <Text color="green">Tokens: {tokens}</Text>
        <Text> | </Text>
        <Text color="gray">Elapsed: {formatTime(elapsed)}</Text>
      </Box>
    </Box>
  )
}
```

### Spinner Component

```typescript
import { Text } from 'ink'
import { useEffect, useState } from 'react'

const FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

interface SpinnerProps {
  label?: string
}

export function Spinner({ label = 'Processing' }: SpinnerProps) {
  const [frame, setFrame] = useState(0)
  const [elapsed, setElapsed] = useState(0)
  
  useEffect(() => {
    const timer = setInterval(() => {
      setFrame(f => (f + 1) % FRAMES.length)
      setElapsed(t => t + 1)
    }, 80)
    
    return () => clearInterval(timer)
  }, [])
  
  return (
    <Text>
      {FRAMES[frame]} {label} ({elapsed / 10}s)
    </Text>
  )
}
```

### Layout with Responsive Width

```typescript
import { Box, Text, useStdout } from 'ink'

interface ResponsiveLayoutProps {
  sidebar: React.ReactNode
  main: React.ReactNode
}

export function ResponsiveLayout({ sidebar, main }: ResponsiveLayoutProps) {
  const { stdout } = useStdout()
  const width = stdout.columns
  
  if (width < 60) {
    return (
      <Box flexDirection="column">
        {main}
      </Box>
    )
  }
  
  return (
    <Box>
      <Box width={40} marginRight={1}>
        {sidebar}
      </Box>
      <Box flexGrow={1}>
        {main}
      </Box>
    </Box>
  )
}
```

## Common Patterns

### 1. Output Truncation

```python
def truncate_output(output: str, max_lines: int = 100) -> str:
    """Truncate long output with ellipsis."""
    lines = output.split('\n')
    if len(lines) <= max_lines:
        return output
    
    half = max_lines // 2
    return '\n'.join([
        *lines[:half],
        f'\n... ({len(lines) - max_lines} lines truncated) ...\n',
        *lines[-half:]
    ])
```

### 2. Collapsible Sections

```typescript
import { Box, Text } from 'ink'

interface CollapsibleProps {
  title: string
  children: React.ReactNode
  defaultExpanded?: boolean
}

export function Collapsible({ 
  title, 
  children, 
  defaultExpanded = false 
}: CollapsibleProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)
  
  return (
    <Box flexDirection="column">
      <Box onClick={() => setExpanded(!expanded)}>
        <Text color="gray">{expanded ? '▼' : '▶'} {title}</Text>
      </Box>
      {expanded && (
        <Box marginLeft={2} flexDirection="column">
          {children}
        </Box>
      )}
    </Box>
  )
}
```

### 3. Progress Bar

```typescript
import { Box, Text } from 'ink'

interface ProgressBarProps {
  value: number
  max: number
  width?: number
}

export function ProgressBar({ 
  value, 
  max, 
  width = 30 
}: ProgressBarProps) {
  const percent = Math.min(100, Math.max(0, (value / max) * 100))
  const filled = Math.round((percent / 100) * width)
  
  return (
    <Box>
      <Text color="green">{'█'.repeat(filled)}</Text>
      <Text color="gray">{'░'.repeat(width - filled)}</Text>
      <Text color="gray"> {percent.toFixed(0)}%</Text>
    </Box>
  )
}
```

## Related Files

- [`legacy/hermes-agent/cli.py`](../../legacy/hermes-agent/cli.py) - Python prompt_toolkit implementation
- [`legacy/claude-code/src/ink.ts`](../../legacy/claude-code/src/ink.ts) - Ink/React utilities
- [`legacy/claude-code/src/main.tsx`](../../legacy/claude-code/src/main.tsx) - React CLI entry point
