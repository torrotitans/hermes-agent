# D3.js Patterns and Code Snippets

## Table of Contents

1. [Setup and Boilerplate](#setup-and-boilerplate)
2. [Scales](#scales)
3. [Axes](#axes)
4. [Data Binding](#data-binding)
5. [Transitions](#transitions)
6. [Interactivity](#interactivity)
7. [Common Chart Patterns](#common-chart-patterns)

---

## Setup and Boilerplate

### Basic SVG Setup

```javascript
import * as d3 from 'd3';

const svg = d3.select('#chart')
  .attr('width', 800)
  .attr('height', 600);

// Add margins convention
const margin = { top: 20, right: 30, bottom: 40, left: 50 };
const width = 800 - margin.left - margin.right;
const height = 600 - margin.top - margin.bottom;

const g = svg.append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
```

### Responsive Container

```javascript
import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export default function ResponsiveChart({ data }) {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        const { width } = containerRef.current.getBoundingClientRect();
        setDimensions({ width, height: width * 0.75 });
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div ref={containerRef}>
      <svg width={dimensions.width} height={dimensions.height} />
    </div>
  );
}
```

---

## Scales

### Linear Scale

```javascript
const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, width]);
```

### Band Scale (Categorical)

```javascript
const xScale = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, width])
  .padding(0.1);
```

### Time Scale

```javascript
const xScale = d3.scaleTime()
  .domain(d3.extent(data, d => new Date(d.date)))
  .range([0, width]);
```

### Ordinal Scale (Colors)

```javascript
const colorScale = d3.scaleOrdinal()
  .domain([...new Set(data.map(d => d.category))])
  .range(d3.schemeCategory10);
```

### Sequential Scale (Gradient)

```javascript
const colorScale = d3.scaleSequential(d3.interpolateViridis)
  .domain([0, d3.max(data, d => d.value)]);
```

---

## Axes

### Basic Axis

```javascript
// X axis
svg.append('g')
  .attr('transform', `translate(0,${height})`)
  .call(d3.axisBottom(xScale));

// Y axis
svg.append('g')
  .call(d3.axisLeft(yScale));
```

### Custom Tick Format

```javascript
// Format as currency
const yAxis = d3.axisLeft(yScale)
  .tickFormat(d => `$${d.toLocaleString()}`);

// Format as percentage
const yAxis = d3.axisLeft(yScale)
  .tickFormat(d => `${(d * 100).toFixed(0)}%`);

// Format dates
const xAxis = d3.axisBottom(xScale)
  .tickFormat(d3.timeFormat('%b %Y'));
```

### Grid Lines

```javascript
// Y grid lines
svg.append('g')
  .attr('class', 'grid')
  .call(d3.axisLeft(yScale)
    .tickSize(-width)
    .tickFormat('')
  )
  .style('stroke-dasharray', '3,3')
  .style('opacity', 0.3);
```

### Axis Labels

```javascript
// X axis label
svg.append('text')
  .attr('class', 'axis-label')
  .attr('x', width / 2)
  .attr('y', height + 40)
  .attr('text-anchor', 'middle')
  .text('Category');

// Y axis label
svg.append('text')
  .attr('class', 'axis-label')
  .attr('transform', 'rotate(-90)')
  .attr('x', -height / 2)
  .attr('y', -40)
  .attr('text-anchor', 'middle')
  .text('Value');
```

---

## Data Binding

### Enter/Update/Exit Pattern

```javascript
// SELECT
const circles = svg.selectAll('.circle')
  .data(data, d => d.id);

// EXIT
circles.exit()
  .transition()
  .duration(300)
  .attr('r', 0)
  .remove();

// UPDATE
circles
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y));

// ENTER
circles.enter()
  .append('circle')
  .attr('class', 'circle')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', 0)
  .merge(circles)
  .transition()
  .duration(300)
  .attr('r', 5);
```

### Key Function for Stable Identity

```javascript
// Use unique ID as key
svg.selectAll('.row')
  .data(data, d => d.id)
  .join('rect')
  .attr('x', d => xScale(d.category));
```

---

## Transitions

### Basic Transition

```javascript
svg.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .attr('x', d => xScale(d.category))
  .attr('width', xScale.bandwidth())
  .attr('y', height)
  .attr('height', 0)
  .transition()
  .duration(800)
  .attr('y', d => yScale(d.value))
  .attr('height', d => height - yScale(d.value));
```

### Staggered Transition

```javascript
svg.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .attr('x', d => xScale(d.category))
  .attr('width', xScale.bandwidth())
  .attr('y', d => yScale(d.value))
  .attr('height', d => height - yScale(d.value))
  .transition()
  .duration(800)
  .delay((d, i) => i * 50);
```

### Chained Transitions

```javascript
svg.selectAll('.dot')
  .data(data)
  .enter()
  .append('circle')
  .attr('r', 0)
  .transition()
  .duration(500)
  .attr('r', 5)
  .transition()
  .duration(500)
  .attr('fill', '#4A90D9');
```

### Easing Functions

```javascript
// Different easing options
.transition()
  .duration(1000)
  .ease(d3.easeCubicInOut);

// Available easings:
// d3.easeLinear, d3.easePolyIn, d3.easeQuadOut, 
// d3.easeCubicInOut, d3.easeBounce, d3.easeElastic
```

---

## Interactivity

### Tooltip Pattern

```javascript
// Create tooltip div
const tooltip = d3.select('body')
  .append('div')
  .attr('class', 'tooltip')
  .style('position', 'absolute')
  .style('visibility', 'hidden')
  .style('background', '#fff')
  .style('padding', '8px')
  .style('border', '1px solid #ccc')
  .style('border-radius', '4px');

// Add hover events
svg.selectAll('.dot')
  .data(data)
  .enter()
  .append('circle')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', 6)
  .on('mouseover', function(event, d) {
    tooltip.style('visibility', 'visible')
      .html(`Value: ${d.value}`);
  })
  .on('mousemove', function(event) {
    tooltip.style('top', `${event.pageY - 10}px`)
      .style('left', `${event.pageX + 10}px`);
  })
  .on('mouseout', function() {
    tooltip.style('visibility', 'hidden');
  });
```

### Click Handler

```javascript
svg.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .on('click', function(event, d) {
    console.log('Clicked:', d);
    // Handle click event
  });
```

### Brush Selection

```javascript
const brush = d3.brushX()
  .extent([[0, 0], [width, height]])
  .on('end', handleBrushEnd);

svg.append('g')
  .attr('class', 'brush')
  .call(brush);

function handleBrushEnd(event) {
  if (!event.selection) return;
  const [x0, x1] = event.selection.map(xScale.invert);
  console.log('Selected range:', x0, x1);
}
```

### Zoom Behavior

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 5])
  .on('zoom', handleZoom);

svg.call(zoom);

function handleZoom(event) {
  g.attr('transform', event.transform);
}
```

---

## Common Chart Patterns

### Grouped Bar Chart

```javascript
const subgroups = ['2020', '2021', '2022'];
const groups = data.map(d => d.category);

const x0 = d3.scaleBand()
  .domain(groups)
  .range([0, width])
  .padding(0.2);

const x1 = d3.scaleBand()
  .domain(subgroups)
  .range([0, x0.bandwidth()])
  .padding(0.05);

const colorScale = d3.scaleOrdinal()
  .domain(subgroups)
  .range(d3.schemeCategory10);

data.forEach(d => {
  subgroups.forEach(subgroup => {
    g.append('rect')
      .attr('x', x0(d.category) + x1(subgroup))
      .attr('y', d => yScale(d[subgroup]))
      .attr('width', x1.bandwidth())
      .attr('height', d => height - yScale(d[subgroup]))
      .attr('fill', colorScale(subgroup));
  });
});
```

### Stacked Area Chart

```javascript
const stack = d3.stack()
  .keys(['series1', 'series2', 'series3']);

const stackedData = stack(data);

const area = d3.area()
  .x(d => xScale(d.date))
  .y0(d => yScale(d[0]))
  .y1(d => yScale(d[1]))
  .curve(d3.curveMonotoneX);

const colorScale = d3.scaleOrdinal()
  .domain(['series1', 'series2', 'series3'])
  .range(d3.schemeCategory10);

g.selectAll('.layer')
  .data(stackedData)
  .enter()
  .append('path')
  .attr('class', 'layer')
  .attr('d', area)
  .attr('fill', (d, i) => colorScale(d.key));
```

### Donut Chart with Labels

```javascript
const radius = Math.min(width, height) / 2;

const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(radius * 0.5)
  .outerRadius(radius);

const labelArc = d3.arc()
  .innerRadius(radius * 0.6)
  .outerRadius(radius * 0.6);

const colorScale = d3.scaleOrdinal()
  .domain(data.map(d => d.label))
  .range(d3.schemeCategory10);

const slices = g.selectAll('.slice')
  .data(pie(data))
  .enter()
  .append('path')
  .attr('class', 'slice')
  .attr('d', arc)
  .attr('fill', d => colorScale(d.data.label));

// Add labels
g.selectAll('.label')
  .data(pie(data))
  .enter()
  .append('text')
  .attr('class', 'label')
  .attr('transform', d => `translate(${labelArc.centroid(d)})`)
  .attr('text-anchor', 'middle')
  .text(d => d.data.label);
```

### Histogram

```javascript
const histogram = d3.histogram()
  .value(d => d.value)
  .domain(xScale.domain())
  .thresholds(xScale.ticks(20));

const bins = histogram(data);

const barWidth = xScale(bins[0].x1) - xScale(bins[0].x0);

g.selectAll('.bar')
  .data(bins)
  .enter()
  .append('rect')
  .attr('x', d => xScale(d.x0))
  .attr('y', d => yScale(d.length))
  .attr('width', d => xScale(d.x1) - xScale(d.x0))
  .attr('height', d => height - yScale(d.length));
```

### Line with Gradient Fill

```javascript
// Define gradient
const gradient = svg.append('defs')
  .append('linearGradient')
  .attr('id', 'area-gradient')
  .attr('x1', '0%')
  .attr('y1', '0%')
  .attr('x2', '0%')
  .attr('y2', '100%');

gradient.append('stop')
  .attr('offset', '0%')
  .attr('stop-color', '#4A90D9')
  .attr('stop-opacity', 0.8);

gradient.append('stop')
  .attr('offset', '100%')
  .attr('stop-color', '#4A90D9')
  .attr('stop-opacity', 0);

// Create area
const area = d3.area()
  .x(d => xScale(d.date))
  .y0(height)
  .y1(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

g.append('path')
  .datum(data)
  .attr('class', 'area')
  .attr('d', area)
  .attr('fill', 'url(#area-gradient)');

// Add line on top
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

g.append('path')
  .datum(data)
  .attr('class', 'line')
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', '#4A90D9')
  .attr('stroke-width', 2);
```
