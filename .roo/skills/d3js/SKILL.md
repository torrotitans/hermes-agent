---
name: d3js
description: Create interactive data visualizations using D3.js (Data-Driven Documents) library. Includes bar charts, line charts, scatter plots, pie charts, and custom SVG graphics with data binding, scales, axes, and transitions.
---

# D3.js Visualization Skill

## When to Use This Skill

Use this skill when you need to:
- Create interactive, data-driven visualizations for web applications
- Build custom charts (bar, line, scatter, pie, area, etc.)
- Implement data binding with SVG elements
- Add animations and transitions to visualizations
- Create responsive charts that adapt to container size
- Build dashboards with multiple coordinated views

## When NOT to Use This Skill

Do NOT use this skill when:
- You need simple static charts (use Chart.js or similar instead)
- The visualization doesn't require custom SVG manipulation
- You need quick, template-based charts without customization
- The project doesn't have D3.js as a dependency

## Inputs Required

1. **Data**: The dataset to visualize (array of objects, nested data, or time-series)
2. **Container**: HTML element selector or D3 selection for mounting
3. **Chart Type**: Bar, line, scatter, pie, area, or custom
4. **Dimensions**: Width, height, and margins
5. **Styling**: Color scheme, fonts, and visual preferences (optional)

## Workflow

### Step 1: Verify D3.js Installation

Check if D3.js is installed in the project:

```bash
npm list d3
```

If not installed, add it:

```bash
npm install d3
```

### Step 2: Create Base Visualization Structure

Create a new component file following the project structure:

```javascript
// UI/components/visualization/MyChart.jsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * FN: MyChart component
 * Creates a D3.js-powered data visualization
 */
export default function MyChart({ data, width, height }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;
    
    // D3.js visualization code here
  }, [data]);

  return <svg ref={svgRef} width={width} height={height} />;
}
```

### Step 3: Implement Data Binding Pattern

Follow the D3.js data binding pattern:

```javascript
// Select the SVG container
const svg = d3.select(svgRef.current);

// Clear any existing content
svg.selectAll('*').remove();

// Create a group for the chart with margins
const margin = { top: 20, right: 30, bottom: 40, left: 50 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const g = svg.append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
```

### Step 4: Create Scales

Define scales to map data to visual properties:

```javascript
// X scale (linear or band for categorical)
const xScale = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, innerWidth])
  .padding(0.1);

// Y scale (linear for numeric)
const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([innerHeight, 0]);
```

### Step 5: Add Axes

```javascript
// X axis
svg.append('g')
  .attr('transform', `translate(0,${innerHeight})`)
  .call(d3.axisBottom(xScale));

// Y axis
svg.append('g')
  .call(d3.axisLeft(yScale));
```

### Step 6: Render Data Elements

```javascript
// Create bars (for bar chart)
g.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .attr('class', 'bar')
  .attr('x', d => xScale(d.category))
  .attr('y', d => yScale(d.value))
  .attr('width', xScale.bandwidth())
  .attr('height', d => innerHeight - yScale(d.value))
  .attr('fill', '#4A90D9');
```

### Step 7: Add Interactivity (Optional)

```javascript
// Add hover effects
g.selectAll('.bar')
  .on('mouseover', function(event, d) {
    d3.select(this).attr('opacity', 0.7);
  })
  .on('mouseout', function(event, d) {
    d3.select(this).attr('opacity', 1);
  });
```

### Step 8: Add Transitions

```javascript
// Animate bars on mount
g.selectAll('.bar')
  .attr('height', 0)
  .attr('y', innerHeight)
  .transition()
  .duration(800)
  .attr('height', d => innerHeight - yScale(d.value))
  .attr('y', d => yScale(d.value));
```

## Chart Type Examples

### Bar Chart

```javascript
// Horizontal bar chart
const yScale = d3.scaleBand()
  .domain(data.map(d => d.name))
  .range([0, innerHeight])
  .padding(0.1);

const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, innerWidth]);

g.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .attr('y', d => yScale(d.name))
  .attr('x', 0)
  .attr('width', d => xScale(d.value))
  .attr('height', yScale.bandwidth())
  .attr('fill', '#4A90D9');
```

### Line Chart

```javascript
// Line generator
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

// Draw the line
g.append('path')
  .datum(data)
  .attr('fill', 'none')
  .attr('stroke', '#4A90D9')
  .attr('stroke-width', 2)
  .attr('d', line);

// Add data points
g.selectAll('.dot')
  .data(data)
  .enter()
  .append('circle')
  .attr('class', 'dot')
  .attr('cx', d => xScale(d.date))
  .attr('cy', d => yScale(d.value))
  .attr('r', 4)
  .attr('fill', '#4A90D9');
```

### Scatter Plot

```javascript
// Color scale for categories
const colorScale = d3.scaleOrdinal()
  .domain([...new Set(data.map(d => d.category))])
  .range(d3.schemeCategory10);

g.selectAll('.dot')
  .data(data)
  .enter()
  .append('circle')
  .attr('class', 'dot')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', 6)
  .attr('fill', d => colorScale(d.category))
  .attr('opacity', 0.7);
```

### Pie Chart

```javascript
// Pie generator
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

// Arc generator
const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2);

// Color scale
const color = d3.scaleOrdinal()
  .domain(data.map(d => d.label))
  .range(d3.schemeCategory10);

// Draw slices
g.selectAll('.slice')
  .data(pie(data))
  .enter()
  .append('path')
  .attr('class', 'slice')
  .attr('d', arc)
  .attr('fill', d => color(d.data.label));
```

## Files

- [`references/d3js-patterns.md`](references/d3js-patterns.md) - Common D3.js patterns and code snippets
- [`references/d3js-examples.md`](references/d3js-examples.md) - Complete chart examples with various data types

## Troubleshooting

### Chart Not Rendering

1. Check if D3.js is properly imported
2. Verify the container element exists
3. Ensure data is in the correct format
4. Check console for D3.js errors

### Data Not Binding

1. Verify data array structure
2. Check key function in `.data(data, keyFn)`
3. Ensure enter/update/exit pattern is correct

### Axes Not Showing

1. Verify scales are defined before axes
2. Check scale domains and ranges
3. Ensure axis groups are appended to SVG

### Responsive Issues

1. Use `useEffect` to handle window resize
2. Recalculate dimensions and redraw on resize
3. Consider using D3's `resizeObserver` pattern

## Related Resources

- [D3.js Official Documentation](https://d3js.org/)
- [D3.js Getting Started](https://d3js.org/getting-started)
- [Observable D3 Gallery](https://observablehq.com/@d3/gallery)
