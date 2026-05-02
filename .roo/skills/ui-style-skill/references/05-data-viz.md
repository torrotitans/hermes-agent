# Data Visualization (Dashboard & D3.js)

## Purpose

This reference document details the implementation of world-class data visualizations using Tremor for dashboard components and D3.js for bespoke data art.

## Tremor Dashboard Components

**Website**: https://www.tremor.so

**Why Tremor**:
- Purpose-built for dashboards
- KPI cards, sparklines, charts
- Built on Recharts (React-friendly)
- Responsive by default

### Installation

```bash
npm install @tremor/react
```

### KPI Card

```tsx
import { Card, Metric, Text, Flex } from '@tremor/react';

export function KPICard({ title, value, change }) {
  return (
    <Card className="p-6">
      <Flex className="justify-between">
        <Text className="font-brand">{title}</Text>
        <span className={`text-sm ${change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          {change >= 0 ? '+' : ''}{change}%
        </span>
      </Flex>
      <Metric className="mt-2 text-3xl font-brand">{value}</Metric>
    </Card>
  );
}
```

### Sparkline Chart

```tsx
import { SparkLineChart } from '@tremor/react';

const data = [
  { date: '2024-01', value: 2400 },
  { date: '2024-02', value: 1398 },
  { date: '2024-03', value: 9800 },
  { date: '2024-04', value: 3908 },
  { date: '2024-05', value: 4800 }
];

export function RevenueSparkline() {
  return (
    <Card className="p-6">
      <Text className="font-brand mb-4">Revenue Trend</Text>
      <SparkLineChart
        data={data}
        index="date"
        categories={['value']}
        colors={['#8fa0f5']}
        showTooltip={true}
      />
    </Card>
  );
}
```

### Bar Chart

```tsx
import { BarChart, Card, Title } from '@tremor/react';

const data = [
  { name: 'Product A', sales: 4000 },
  { name: 'Product B', sales: 3000 },
  { name: 'Product C', sales: 2000 },
  { name: 'Product D', sales: 2780 }
];

export function SalesBarChart() {
  return (
    <Card className="p-6">
      <Title className="font-brand mb-4">Sales by Product</Title>
      <BarChart
        data={data}
        index="name"
        categories={['sales']}
        colors={['#8fa0f5']}
        yAxisWidth={60}
      />
    </Card>
  );
}
```

### Dashboard Layout

```tsx
import { Grid, Col } from '@tremor/react';

export function Dashboard() {
  return (
    <Grid numItemsSm={2} numItemsLg={4} className="gap-6">
      <Col numColSpan={1}>
        <KPICard title="Total Revenue" value="$45,231" change={12.5} />
      </Col>
      <Col numColSpan={1}>
        <KPICard title="Active Users" value="2,345" change={8.2} />
      </Col>
      <Col numColSpan={1}>
        <KPICard title="Orders" value="1,234" change={-3.1} />
      </Col>
      <Col numColSpan={1}>
        <KPICard title="Conversion" value="3.24%" change={5.7} />
      </Col>
    </Grid>
  );
}
```

## D3.js Custom Visualizations

**Website**: https://d3js.org

**Why D3.js**:
- Complete creative freedom
- Industry standard for data art
- Highly performant
- Rich ecosystem

### Installation

```bash
npm install d3 @types/d3
```

### Basic Line Chart

```tsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export function D3LineChart({ data }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Create scales
    const x = d3.scaleLinear()
      .domain([0, data.length - 1])
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data)])
      .range([height - margin.bottom, margin.top]);

    // Create line
    const line = d3.line<number>()
      .x((d, i) => x(i))
      .y(d => y(d))
      .curve(d3.curveMonotoneX);

    // Draw line
    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#8fa0f5')
      .attr('stroke-width', 2)
      .attr('d', line);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

  }, [data]);

  return <svg ref={svgRef} width={600} height={400} />;
}
```

### Interactive Scatter Plot

```tsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export function D3ScatterPlot({ data }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const x = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.x)])
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.y)])
      .range([height - margin.bottom, margin.top]);

    // Add dots
    svg.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.x))
      .attr('cy', d => y(d.y))
      .attr('r', 6)
      .attr('fill', '#8fa0f5')
      .attr('opacity', 0.7)
      .on('mouseover', function(event, d) {
        d3.select(this)
          .attr('r', 10)
          .attr('opacity', 1);
      })
      .on('mouseout', function() {
        d3.select(this)
          .attr('r', 6)
          .attr('opacity', 0.7);
      });

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

  }, [data]);

  return <svg ref={svgRef} width={600} height={400} />;
}
```

### Animated Bar Chart

```tsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export function D3AnimatedBarChart({ data }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const x = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([margin.left, width - margin.right])
      .padding(0.2);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([height - margin.bottom, margin.top]);

    // Add bars with animation
    svg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      .attr('x', d => x(d.name))
      .attr('y', height - margin.bottom)
      .attr('width', x.bandwidth())
      .attr('height', 0)
      .attr('fill', '#8fa0f5')
      .transition()
      .duration(800)
      .attr('y', d => y(d.value))
      .attr('height', d => height - margin.bottom - y(d.value));

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

  }, [data]);

  return <svg ref={svgRef} width={600} height={400} />;
}
```

## Responsive Design

### Container Queries

```css
.chart-container {
  container-type: inline-size;
}

@container (min-width: 600px) {
  .chart-container {
    height: 400px;
  }
}

@container (max-width: 599px) {
  .chart-container {
    height: 300px;
  }
}
```

### Responsive D3 Chart

```tsx
import { useContainerQuery } from '@use-it/container-query';

export function ResponsiveChart({ data }) {
  const [ref, { width }] = useContainerQuery();

  return (
    <div ref={ref}>
      <D3LineChart data={data} width={width} />
    </div>
  );
}
```

## Performance Optimization

### Lazy Loading

```tsx
import dynamic from 'next/dynamic';

const D3Chart = dynamic(() => import('./D3Chart'), {
  ssr: false,
  loading: () => <div className="h-64 bg-gray-100 animate-pulse" />
});

export function Dashboard() {
  return <D3Chart data={data} />;
}
```

### Data Sampling

```javascript
// Downsample large datasets
function downsample(data, maxPoints) {
  if (data.length <= maxPoints) return data;
  
  const step = Math.floor(data.length / maxPoints);
  return data.filter((_, i) => i % step === 0);
}
```

## Related Files

- [`01-figma-mcp.md`](01-figma-mcp.md) - Figma MCP server integration
