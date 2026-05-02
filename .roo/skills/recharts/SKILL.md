---
name: recharts
description: Create interactive data visualizations using Recharts including charts, graphs, and custom components with React and TypeScript support
license: MIT
compatibility:
  - react-16.8+
  - recharts-2.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/recharts
---

# Recharts Skill

## When to Use This Skill

Use this skill when you need to:
- Create interactive charts and data visualizations in React
- Build line charts, bar charts, pie charts, scatter plots, and more
- Implement responsive charts that adapt to container size
- Add tooltips, legends, and customization to charts
- Animate chart data changes with transitions
- Create custom shapes and markers for charts
- Handle responsive design with ResponsiveContainer
- Implement dashboard-style data displays
- Use TypeScript with Recharts for type safety
- Create custom chart components with composable API

## When NOT to Use This Skill

Do NOT use this skill when:
- Building complex 3D visualizations (use Three.js)
- Creating geographic maps (use Mapbox/Leaflet)
- Building real-time streaming charts (use D3.js with Canvas)
- Creating highly customized scientific visualizations (use Plotly)

## Inputs Required

Before starting, ensure you have:
1. React version (default: 16.8+)
2. Chart type (line, bar, pie, area, scatter, etc.)
3. Data structure and fields
4. Responsive requirements

## Workflow

### Step 1: Basic Line Chart

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

const data = [
  { name: 'Jan', uv: 4000, pv: 2400, amt: 2400 },
  { name: 'Feb', uv: 3000, pv: 1398, amt: 2210 },
  { name: 'Mar', uv: 2000, pv: 9800, amt: 2290 },
  { name: 'Apr', uv: 2780, pv: 3908, amt: 2000 },
  { name: 'May', uv: 1890, pv: 4800, amt: 2181 },
  { name: 'Jun', uv: 2390, pv: 3800, amt: 2500 },
  { name: 'Jul', uv: 3490, pv: 4300, amt: 2100 },
]

function BasicLineChart() {
  return (
    <LineChart
      width={600}
      height={300}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="pv" stroke="#8884d8" />
      <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
    </LineChart>
  )
}
```

### Step 2: Responsive Chart

```typescript
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

const data = [
  { name: 'Page A', uv: 4000, pv: 2400, amt: 2400 },
  { name: 'Page B', uv: 3000, pv: 1398, amt: 2210 },
  { name: 'Page C', uv: 2000, pv: 9800, amt: 2290 },
  { name: 'Page D', uv: 2780, pv: 3908, amt: 2000 },
  { name: 'Page E', uv: 1890, pv: 4800, amt: 2181 },
  { name: 'Page F', uv: 2390, pv: 3800, amt: 2500 },
  { name: 'Page G', uv: 3490, pv: 4300, amt: 2100 },
]

function ResponsiveBarChart() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="pv" fill="#8884d8" />
          <Bar dataKey="uv" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 3: Area Chart with Gradient

```typescript
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { name: 'Jan', value: 4000 },
  { name: 'Feb', value: 3000 },
  { name: 'Mar', value: 5000 },
  { name: 'Apr', value: 4500 },
  { name: 'May', value: 6000 },
  { name: 'Jun', value: 5500 },
  { name: 'Jul', value: 7000 },
]

function GradientAreaChart() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            fillOpacity={1}
            fill="url(#colorValue)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 4: Pie Chart

```typescript
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { name: 'Group A', value: 400 },
  { name: 'Group B', value: 300 },
  { name: 'Group C', value: 300 },
  { name: 'Group D', value: 200 },
]

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

function PieChartComponent() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 5: Scatter Plot

```typescript
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { x: 100, y: 200, z: 200 },
  { x: 120, y: 100, z: 260 },
  { x: 170, y: 300, z: 400 },
  { x: 140, y: 250, z: 280 },
  { x: 150, y: 400, z: 500 },
  { x: 110, y: 280, z: 200 },
]

function ScatterPlot() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <ScatterChart>
          <CartesianGrid />
          <XAxis type="number" dataKey="x" name="stature" unit="cm" />
          <YAxis type="number" dataKey="y" name="weight" unit="kg" />
          <ZAxis type="number" dataKey="z" range={[50, 400]} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter data={data} fill="#8884d8" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 6: Custom Tooltip

```typescript
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { name: 'Jan', sales: 4000, profit: 2400 },
  { name: 'Feb', sales: 3000, profit: 1398 },
  { name: 'Mar', sales: 2000, profit: 980 },
]

function CustomTooltip({ active, payload }: any) {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: '#fff',
        padding: '10px',
        border: '1px solid #ccc',
      }}>
        <p>{`Month: ${payload[0].payload.name}`}</p>
        <p>{`Sales: $${payload[0].value.toLocaleString()}`}</p>
        <p>{`Profit: $${payload[1].value.toLocaleString()}`}</p>
      </div>
    )
  }
  return null
}

function ChartWithCustomTooltip() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Line dataKey="sales" stroke="#8884d8" />
          <Line dataKey="profit" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 7: Bar Chart with Custom Shapes

```typescript
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'

const data = [
  { name: 'Jan', value: 4000 },
  { name: 'Feb', value: 3000 },
  { name: 'Mar', value: 2000 },
  { name: 'Apr', value: 2780 },
  { name: 'May', value: 1890 },
]

function CustomBarChart() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={index % 2 === 0 ? '#8884d8' : '#82ca9d'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 8: Combined Chart Types

```typescript
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { name: 'Jan', uv: 4000, pv: 2400, amt: 2400 },
  { name: 'Feb', uv: 3000, pv: 1398, amt: 2210 },
  { name: 'Mar', uv: 2000, pv: 9800, amt: 2290 },
  { name: 'Apr', uv: 2780, pv: 3908, amt: 2000 },
  { name: 'May', uv: 1890, pv: 4800, amt: 2181 },
]

function CombinedChart() {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <ComposedChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="pv" barSize={20} fill="#413ea0" />
          <Line type="monotone" dataKey="uv" stroke="#ff7300" />
          <Line type="monotone" dataKey="amt" stroke="#387906" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 9: Dynamic Data with Animations

```typescript
import { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

function DynamicChart() {
  const [data, setData] = useState([
    { name: '0s', value: 0 },
  ])

  useEffect(() => {
    const timer = setInterval(() => {
      setData((prev) => {
        const nextValue = prev[prev.length - 1].value + Math.random() * 100 - 50
        const newData = [
          ...prev.slice(1),
          { name: `${prev.length}s`, value: Math.max(0, nextValue) },
        ]
        return newData
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            animationDuration={300}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Step 10: TypeScript Types

```typescript
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  TooltipProps,
} from 'recharts'

interface DataItem {
  name: string
  value: number
  count?: number
}

interface CustomTooltipProps extends TooltipProps<number, string> {
  label?: string
}

function TypedChart() {
  const data: DataItem[] = [
    { name: 'Jan', value: 4000 },
    { name: 'Feb', value: 3000 },
  ]

  const CustomTooltip: React.FC<CustomTooltipProps> = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ background: '#fff', padding: '10px', border: '1px solid #ccc' }}>
          <p>{`Month: ${label}`}</p>
          <p>{`Value: $${payload[0].value.toLocaleString()}`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `src/chart/generateAllCategoricalChart.tsx` | Chart generation logic |
| `src/component/` | Reusable components |
| `src/shape/` | Shape components |
| `src/util/` | Utility functions |

## Troubleshooting

### Issue: Chart Not Rendering

**Symptom**: Empty chart area

**Solution**:
- Ensure data array is not empty
- Check `dataKey` matches data object keys
- Verify container has explicit width/height or use ResponsiveContainer

### Issue: ResponsiveContainer Not Working

**Symptom**: Chart doesn't resize

**Solution**:
- Parent container must have explicit width/height
- Wrap ResponsiveContainer in div with dimensions
- Check for CSS `display: none` blocking resize

### Issue: Animations Not Smooth

**Symptom**: Janky chart animations

**Solution**:
- Reduce `animationDuration` for faster updates
- Use `isAnimationActive={false}` for real-time data
- Check for excessive re-renders

## Examples

### Example 1: Dashboard Chart

```typescript
function DashboardChart() {
  const data = [
    { month: 'Jan', revenue: 4000 },
    { month: 'Feb', revenue: 3000 },
    { month: 'Mar', revenue: 5000 },
  ]

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip formatter={(value: number) => `$${value.toLocaleString()}`} />
          <Bar dataKey="revenue" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### Example 2: Multi-line Chart

```typescript
function MultiLineChart() {
  const data = [
    { name: 'Jan', desktop: 4000, mobile: 2400 },
    { name: 'Feb', desktop: 3000, mobile: 1398 },
    { name: 'Mar', desktop: 2000, mobile: 980 },
  ]

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="desktop" stroke="#8884d8" />
          <Line type="monotone" dataKey="mobile" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

## Related Resources

- [Recharts Documentation](https://recharts.org/)
- [Recharts Examples](https://recharts.org/en-US/examples)
- [Recharts API Reference](https://recharts.org/en-US/api)
