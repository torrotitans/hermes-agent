---
name: reactflow
description: Build interactive node-based diagrams and workflow visualizations using ReactFlow including node/edge management, custom nodes, drag-and-drop, zoom/pan, and layout patterns
license: MIT
compatibility:
  - react-18.0+
  - reactflow-11.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/reactflow
---

# ReactFlow Skill

## When to Use This Skill

Use this skill when you need to:
- Build interactive node-based diagrams (flowcharts, workflows, org charts)
- Implement drag-and-drop node creation and manipulation
- Create custom node components with React
- Manage node and edge connections programmatically
- Handle zoom, pan, and viewport operations
- Implement minimap for large graphs
- Add context menus and selection handling
- Build workflow editors or data pipeline visualizations
- Use built-in node types (default, input, output, custom)
- Implement edge styling and connection logic

## When NOT to Use This Skill

Do NOT use this skill when:
- Building static diagrams (use SVG/Canvas directly)
- Creating 2D/3D games (use Phaser/Three.js instead)
- Building simple tree views (use react-tree instead)
- Creating GIS maps (use Leaflet/Mapbox instead)

## Inputs Required

Before starting, ensure you have:
1. React version (default: 18.x+)
2. Diagram type (flowchart, workflow, org chart, etc.)
3. Node complexity (simple text, custom components)
4. Interaction requirements (drag, connect, select)

## Workflow

### Step 1: Basic ReactFlow Setup

```typescript
import { useState, useCallback } from 'react'
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'

interface FlowData {
  nodes: Node[]
  edges: Edge[]
}

function BasicFlow() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  return (
    <div style={{ height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  )
}
```

### Step 2: Define Node and Edge Data

```typescript
import { Node, Edge, Position } from '@xyflow/react'

interface CustomNodeData {
  label: string
  description?: string
  status?: 'active' | 'inactive' | 'error'
  metadata?: Record<string, any>
}

const initialNodes: Node<CustomNodeData>[] = [
  {
    id: '1',
    type: 'default',
    position: { x: 250, y: 50 },
    data: { label: 'Start Node', status: 'active' },
  },
  {
    id: '2',
    type: 'input',
    position: { x: 100, y: 150 },
    data: { label: 'Input Data' },
  },
  {
    id: '3',
    type: 'output',
    position: { x: 400, y: 150 },
    data: { label: 'Output Result' },
  },
]

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e1-3', source: '1', target: '3', animated: true },
]
```

### Step 3: Custom Node Component

```typescript
import { memo } from 'react'
import { Handle, Position, NodeProps } from '@xyflow/react'

interface CustomNodeData {
  label: string
  count?: number
  color?: string
}

const CustomNode = memo(({ data }: NodeProps<CustomNodeData>) => {
  return (
    <div className="custom-node" style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ddd', background: data.color || '#fff' }}>
      <Handle type="target" position={Position.Top} />
      <div className="custom-node-inner">
        <h3>{data.label}</h3>
        {data.count !== undefined && <p>Count: {data.count}</p>}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
})

CustomNode.displayName = 'CustomNode'

export default CustomNode
```

### Step 4: Add Custom Nodes to Flow

```typescript
import { useState, useCallback } from 'react'
import ReactFlow, { addEdge, useNodesState, useEdgesState } from '@xyflow/react'
import CustomNode from './CustomNode'
import '@xyflow/react/dist/style.css'

const nodeTypes = {
  custom: CustomNode,
}

function FlowWithCustomNodes() {
  const [nodes, setNodes, onNodesChange] = useNodesState([
    {
      id: '1',
      type: 'custom',
      position: { x: 250, y: 50 },
      data: { label: 'Custom Node', count: 42, color: '#e3f2fd' },
    },
  ])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      nodeTypes={nodeTypes}
    >
      <Controls />
    </ReactFlow>
  )
}
```

### Step 5: Handle Node Selection and Deletion

```typescript
import { useState, useCallback } from 'react'
import ReactFlow, { useNodesState, useEdgesState, Panel } from '@xyflow/react'

function FlowWithSelection() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNodes, setSelectedNodes] = useState<Node[]>([])

  const onNodesChange = useCallback(
    (changes: any[]) => {
      setNodes(changes)
    },
    [setNodes]
  )

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      setSelectedNodes((prev) =>
        prev.find((n) => n.id === node.id)
          ? prev.filter((n) => n.id !== node.id)
          : [...prev, node]
      )
    },
    []
  )

  const deleteSelected = useCallback(() => {
    setNodes((nds) => nds.filter((n) => !selectedNodes.find((sn) => sn.id === n.id)))
    setEdges((eds) =>
      eds.filter(
        (e) => !selectedNodes.some((sn) => sn.id === e.source || sn.id === e.target)
      )
    )
    setSelectedNodes([])
  }, [selectedNodes, setNodes, setEdges])

  return (
    <>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        multiSelectionShift={true}
      />
      <Panel position="top-right">
        <button onClick={deleteSelected} disabled={selectedNodes.length === 0}>
          Delete Selected ({selectedNodes.length})
        </button>
      </Panel>
    </>
  )
}
```

### Step 6: Drag and Drop Node Creation

```typescript
import { useState, useCallback, DragEvent } from 'react'
import ReactFlow, { addEdge, useNodesState, useEdgesState, Panel } from '@xyflow/react'

function FlowWithDragDrop() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  const onDragOver = useCallback((event: DragEvent) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  const onDrop = useCallback(
    (event: DragEvent) => {
      event.preventDefault()
      const type = event.dataTransfer.getData('application/reactflow')
      if (typeof type === 'undefined' || !type) {
        return
      }

      const position = {
        x: (event as any).clientX - (event as any).target.getBoundingClientRect().x,
        y: (event as any).clientY - (event as any).target.getBoundingClientRect().y,
      }

      const newNode = {
        id: `${Date.now()}`,
        type,
        position,
        data: { label: `${type} node` },
      }

      setNodes((nds) => nds.concat(newNode))
    },
    [setNodes]
  )

  return (
    <>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onDragOver={onDragOver}
        onDrop={onDrop}
      />
      <Panel position="top-left">
        <div
          draggable
          onDragStart={(event) =>
            event.dataTransfer.setData('application/reactflow', 'default')
          }
          style={{
            background: '#fff',
            padding: '10px',
            border: '1px solid #ddd',
            cursor: 'grab',
          }}
        >
          Drag me to the canvas
        </div>
      </Panel>
    </>
  )
}
```

### Step 7: Viewport and Zoom Control

```typescript
import { useState, useCallback, useRef } from 'react'
import ReactFlow, { useReactFlow, Panel, Controls } from '@xyflow/react'

function FlowWithZoomControls() {
  const { zoomIn, zoomOut, fitView, setViewport } = useReactFlow()

  const handleZoomIn = useCallback(() => zoomIn(), [zoomIn])
  const handleZoomOut = useCallback(() => zoomOut(), [zoomOut])
  const handleFitView = useCallback(() => fitView(), [fitView])
  const handleResetView = useCallback(
    () => setViewport({ x: 0, y: 0, zoom: 1 }),
    [setViewport]
  )

  return (
    <>
      <ReactFlow fitView>
        <Controls />
        <Panel position="bottom-right">
          <button onClick={handleZoomIn}>Zoom In</button>
          <button onClick={handleZoomOut}>Zoom Out</button>
          <button onClick={handleFitView}>Fit View</button>
          <button onClick={handleResetView}>Reset</button>
        </Panel>
      </ReactFlow>
    </>
  )
}
```

### Step 8: Edge Styling and Types

```typescript
import { EdgeProps, getBezierPath, BaseEdge } from '@xyflow/react'

function CustomEdge({
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
}: EdgeProps) {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  })

  return (
    <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} />
  )
}

// Usage in ReactFlow
<ReactFlow
  edges={[
    {
      id: 'e1-2',
      source: '1',
      target: '2',
      type: 'custom',
      animated: true,
      style: { stroke: '#0066cc' },
    },
  ]}
  edgeTypes={{ custom: CustomEdge }}
/>
```

### Step 9: Keyboard Shortcuts

```typescript
import { useEffect, useCallback } from 'react'
import ReactFlow, { useReactFlow } from '@xyflow/react'

function FlowWithKeyboardShortcuts() {
  const { screenToFlowCoordinate } = useReactFlow()

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Delete' || event.key === 'Backspace') {
        // Delete selected nodes/edges
        console.log('Delete pressed')
      }
      if (event.key === 'z' && (event.ctrlKey || event.metaKey)) {
        // Undo
        console.log('Undo pressed')
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return <ReactFlow />
}
```

### Step 10: Save and Load Flow State

```typescript
import { useState, useCallback } from 'react'
import ReactFlow, { useNodesState, useEdgesState, Panel } from '@xyflow/react'

function FlowWithPersistence() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const saveFlow = useCallback(() => {
    const flowData = { nodes, edges }
    localStorage.setItem('flow-data', JSON.stringify(flowData))
    console.log('Flow saved', flowData)
  }, [nodes, edges])

  const loadFlow = useCallback(() => {
    const saved = localStorage.getItem('flow-data')
    if (saved) {
      const { nodes, edges } = JSON.parse(saved)
      setNodes(nodes)
      setEdges(edges)
    }
  }, [setNodes, setEdges])

  return (
    <>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
      />
      <Panel position="top-right">
        <button onClick={saveFlow}>Save</button>
        <button onClick={loadFlow}>Load</button>
      </Panel>
    </>
  )
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `src/index.ts` | Main ReactFlow exports |
| `src/components/` | Node and edge components |
| `src/hooks/` | Custom hooks |
| `src/utils/` | Utility functions |

## Troubleshooting

### Issue: Nodes Not Draggable

**Symptom**: Nodes stuck in place

**Solution**:
- Ensure `nodesConnectable` and `nodesDraggable` are true (default)
- Check for CSS `pointer-events: none` on nodes
- Verify no `onNodeDragStop` blocking movement

### Issue: Edges Not Connecting

**Symptom**: Can't drag connections between nodes

**Solution**:
- Ensure nodes have `Handle` components with correct `Position`
- Check `edgesConnectable` is true (default)
- Verify `onConnect` handler is set

### Issue: Performance with Many Nodes

**Symptom**: Lag with 100+ nodes

**Solution**:
- Use `React.memo` on custom nodes
- Enable `defaultEdgeOptions={{ animated: false }}`
- Consider virtualization for 1000+ nodes

## Examples

### Example 1: Workflow Editor

```typescript
function WorkflowEditor() {
  const [nodes, setNodes, onNodesChange] = useNodesState([
    { id: 'start', type: 'input', position: { x: 250, y: 0 }, data: { label: 'Start' } },
    { id: 'process', type: 'default', position: { x: 250, y: 100 }, data: { label: 'Process' } },
    { id: 'end', type: 'output', position: { x: 250, y: 200 }, data: { label: 'End' } },
  ])
  const [edges, setEdges] = useEdgesState([
    { id: 'e1', source: 'start', target: 'process' },
    { id: 'e2', source: 'process', target: 'end' },
  ])

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodesConnectable
      nodesDraggable
    >
      <Controls />
      <Background />
    </ReactFlow>
  )
}
```

### Example 2: Data Pipeline Visualization

```typescript
function DataPipeline() {
  const [nodes, setNodes] = useNodesState([
    { id: 'source', type: 'input', position: { x: 0, y: 50 }, data: { label: 'Data Source' } },
    { id: 'transform', type: 'default', position: { x: 200, y: 50 }, data: { label: 'Transform' } },
    { id: 'validate', type: 'default', position: { x: 400, y: 50 }, data: { label: 'Validate' } },
    { id: 'sink', type: 'output', position: { x: 600, y: 50 }, data: { label: 'Sink' } },
  ])
  const [edges] = useEdgesState([
    { id: 'e1', source: 'source', target: 'transform', animated: true },
    { id: 'e2', source: 'transform', target: 'validate', animated: true },
    { id: 'e3', source: 'validate', target: 'sink', animated: true },
  ])

  return (
    <ReactFlow nodes={nodes} edges={edges} fitView>
      <Controls />
      <MiniMap />
    </ReactFlow>
  )
}
```

## Related Resources

- [ReactFlow Documentation](https://reactflow.dev/)
- [ReactFlow Examples](https://reactflow.dev/examples/overview)
- [ReactFlow API Reference](https://reactflow.dev/api)
