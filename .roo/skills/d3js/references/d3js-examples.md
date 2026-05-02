# D3.js Complete Examples

## Table of Contents

1. [Bar Chart with Tooltip](#bar-chart-with-tooltip)
2. [Multi-Line Chart with Legend](#multi-line-chart-with-legend)
3. [Scatter Plot with Regression Line](#scatter-plot-with-regression-line)
4. [Animated Bubble Chart](#animated-bubble-chart)
5. [Choropleth Map](#choropleth-map)
6. [Tree Diagram](#tree-diagram)

---

## Bar Chart with Tooltip

```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function BarChart({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Clear previous chart
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create scales
    const xScale = d3.scaleBand()
      .domain(data.map(d => d.category))
      .range([0, innerWidth])
      .padding(0.3);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([innerHeight, 0]);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end');

    svg.append('g')
      .call(d3.axisLeft(yScale).tickFormat(d => d3.format(',.0f')(d)));

    // Create tooltip
    const tooltip = d3.select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('visibility', 'hidden')
      .style('background', '#fff')
      .style('padding', '10px')
      .style('border', '1px solid #ccc')
      .style('border-radius', '4px')
      .style('box-shadow', '0 2px 4px rgba(0,0,0,0.1)');

    // Create bars
    svg.selectAll('.bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => xScale(d.category))
      .attr('y', d => yScale(d.value))
      .attr('width', xScale.bandwidth())
      .attr('height', d => innerHeight - yScale(d.value))
      .attr('fill', '#4A90D9')
      .on('mouseover', function(event, d) {
        tooltip.style('visibility', 'visible')
          .html(`
            <strong>${d.category}</strong><br/>
            Value: ${d.value.toLocaleString()}
          `);
      })
      .on('mousemove', function(event) {
        tooltip.style('top', `${event.pageY - 10}px`)
          .style('left', `${event.pageX + 10}px`);
      })
      .on('mouseout', function() {
        tooltip.style('visibility', 'hidden');
      });

    // Add axis labels
    svg.append('text')
      .attr('class', 'axis-label')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .attr('text-anchor', 'middle')
      .text('Category');

    svg.append('text')
      .attr('class', 'axis-label')
      .attr('transform', 'rotate(-90)')
      .attr('x', -innerHeight / 2)
      .attr('y', -45)
      .attr('text-anchor', 'middle')
      .text('Value');

  }, [data]);

  return <svg ref={svgRef} />;
}
```

---

## Multi-Line Chart with Legend

```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function MultiLineChart({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const margin = { top: 40, right: 120, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Parse dates
    const parseDate = d3.timeParse('%Y-%m-%d');
    data.forEach(d => {
      d.date = parseDate(d.date);
    });

    // Get unique series
    const series = [...new Set(data.map(d => d.series))];
    const colorScale = d3.scaleOrdinal()
      .domain(series)
      .range(d3.schemeCategory10);

    // Create scales
    const xScale = d3.scaleTime()
      .domain(d3.extent(data, d => d.date))
      .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([innerHeight, 0]);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat('%Y-%m')));

    svg.append('g')
      .call(d3.axisLeft(yScale).tickFormat(d => d3.format(',.0f')(d)));

    // Create lines
    const line = d3.line()
      .x(d => xScale(d.date))
      .y(d => yScale(d.value))
      .curve(d3.curveMonotoneX);

    series.forEach(seriesName => {
      const seriesData = data.filter(d => d.series === seriesName);
      
      svg.append('path')
        .datum(seriesData)
        .attr('class', 'line')
        .attr('d', line)
        .attr('fill', 'none')
        .attr('stroke', colorScale(seriesName))
        .attr('stroke-width', 2);
    });

    // Create legend
    const legend = svg.selectAll('.legend')
      .data(series)
      .enter()
      .append('g')
      .attr('class', 'legend')
      .attr('transform', (d, i) => `translate(${innerWidth + 20},${i * 25})`);

    legend.append('rect')
      .attr('width', 18)
      .attr('height', 18)
      .attr('fill', colorScale);

    legend.append('text')
      .attr('x', 24)
      .attr('y', 9)
      .attr('dy', '.35em')
      .text(d => d);

  }, [data]);

  return <svg ref={svgRef} />;
}
```

---

## Scatter Plot with Regression Line

```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function ScatterPlot({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create scales
    const xScale = d3.scaleLinear()
      .domain([d3.min(data, d => d.x) * 0.9, d3.max(data, d => d.x) * 1.1])
      .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
      .domain([d3.min(data, d => d.y) * 0.9, d3.max(data, d => d.y) * 1.1])
      .range([innerHeight, 0]);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale));

    svg.append('g')
      .call(d3.axisLeft(yScale));

    // Calculate regression line
    const n = data.length;
    const sumX = d3.sum(data, d => d.x);
    const sumY = d3.sum(data, d => d.y);
    const sumXY = d3.sum(data, d => d.x * d.y);
    const sumX2 = d3.sum(data, d => d.x * d.x);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const regressionLine = [
      { x: xScale.domain()[0], y: slope * xScale.domain()[0] + intercept },
      { x: xScale.domain()[1], y: slope * xScale.domain()[1] + intercept }
    ];

    // Add regression line
    const line = d3.line()
      .x(d => xScale(d.x))
      .y(d => yScale(d.y));

    svg.append('path')
      .datum(regressionLine)
      .attr('class', 'regression-line')
      .attr('d', line)
      .attr('stroke', '#ff6b6b')
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '5,5');

    // Add points
    const colorScale = d3.scaleOrdinal()
      .domain([...new Set(data.map(d => d.category))])
      .range(d3.schemeCategory10);

    svg.selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => xScale(d.x))
      .attr('cy', d => yScale(d.y))
      .attr('r', 6)
      .attr('fill', d => colorScale(d.category))
      .attr('opacity', 0.6);

    // Add axis labels
    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .attr('text-anchor', 'middle')
      .text('X Value');

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -innerHeight / 2)
      .attr('y', -45)
      .attr('text-anchor', 'middle')
      .text('Y Value');

  }, [data]);

  return <svg ref={svgRef} />;
}
```

---

## Animated Bubble Chart

```javascript
import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export default function AnimatedBubbleChart({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);
  const [animationState, setAnimationState] = useState('idle');

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create scales
    const xScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.x)])
      .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.y)])
      .range([innerHeight, 0]);

    const sizeScale = d3.scaleSqrt()
      .domain([0, d3.max(data, d => d.size)])
      .range([5, 40]);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale));

    svg.append('g')
      .call(d3.axisLeft(yScale));

    // Add bubbles
    const colorScale = d3.scaleOrdinal()
      .domain([...new Set(data.map(d => d.category))])
      .range(d3.schemeCategory10);

    svg.selectAll('.bubble')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'bubble')
      .attr('cx', d => xScale(d.x))
      .attr('cy', d => yScale(d.y))
      .attr('r', d => sizeScale(d.size))
      .attr('fill', d => colorScale(d.category))
      .attr('opacity', 0.6)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('click', function(event, d) {
        d3.select(this)
          .transition()
          .duration(300)
          .attr('r', sizeScale(d.size) * 1.5)
          .transition()
          .duration(300)
          .attr('r', sizeScale(d.size));
      });

  }, [data]);

  return (
    <div>
      <svg ref={svgRef} />
      <button onClick={() => setAnimationState('animating')}>
        Animate
      </button>
    </div>
  );
}
```

---

## Choropleth Map

```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { geoPath, geoMercator } from 'd3-geo';
import { json } from 'd3-fetch';

export default function ChoroplethMap({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Load GeoJSON
    json('path/to/geojson.json').then(geoData => {
      // Create color scale
      const colorScale = d3.scaleQuantize()
        .domain([d3.min(data, d => d.value), d3.max(data, d => d.value)])
        .range(d3.schemeBlues[9]);

      // Create projection and path
      const projection = geoMercator()
        .fitSize([innerWidth, innerHeight], geoData);

      const path = geoPath().projection(projection);

      // Create data map
      const dataMap = new Map(data.map(d => [d.id, d.value]));

      // Draw map
      svg.selectAll('.region')
        .data(geoData.features)
        .enter()
        .append('path')
        .attr('class', 'region')
        .attr('d', path)
        .attr('fill', d => {
          const value = dataMap.get(d.id) || 0;
          return colorScale(value);
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', 0.5)
        .on('mouseover', function(event, d) {
          d3.select(this)
            .attr('opacity', 0.8)
            .attr('stroke', '#333')
            .attr('stroke-width', 1);
        })
        .on('mouseout', function() {
          d3.select(this)
            .attr('opacity', 1)
            .attr('stroke', '#fff')
            .attr('stroke-width', 0.5);
        });
    });

  }, [data]);

  return <svg ref={svgRef} />;
}
```

---

## Tree Diagram

```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function TreeDiagram({ data, width = 800, height = 600 }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', 'translate(40,20)');

    // Create tree layout
    const root = d3.hierarchy(data);
    const treeLayout = d3.tree()
      .size([height - 40, width - 80]);

    treeLayout(root);

    // Create links
    const linkGenerator = d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x);

    svg.selectAll('.link')
      .data(root.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', linkGenerator)
      .attr('fill', 'none')
      .attr('stroke', '#999')
      .attr('stroke-width', 2);

    // Create nodes
    const colorScale = d3.scaleOrdinal()
      .domain([...new Set(root.descendants().map(d => d.depth))])
      .range(d3.schemeCategory10);

    svg.selectAll('.node')
      .data(root.descendants())
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('cx', d => d.y)
      .attr('cy', d => d.x)
      .attr('r', 6)
      .attr('fill', d => colorScale(d.depth))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);

    // Add labels
    svg.selectAll('.label')
      .data(root.descendants())
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', d => d.y + 10)
      .attr('y', d => d.x)
      .attr('dy', '.35em')
      .text(d => d.data.name);

  }, [data]);

  return <svg ref={svgRef} />;
}
```
