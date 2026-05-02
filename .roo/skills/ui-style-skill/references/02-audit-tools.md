# UI/UX Audit Tools

## Purpose

This reference document details the tools and methodologies for conducting comprehensive UI/UX audits, including design-code parity verification and 12-dimension quality scoring.

## Audit Dimensions

### 12-Dimension Audit Framework

| Dimension | Tool | Metric | Target |
|-----------|------|--------|--------|
| Color Contrast | ui-ux-suite | OKLCH delta | ΔE < 3 |
| Typography | ui-ux-suite | Scale ratio | 1.25 (Major Third) |
| Layout | ui-ux-suite | Grid alignment | 95%+ |
| Spacing | ui-ux-suite | 4px grid compliance | 100% |
| Border Radius | ui-ux-suite | Consistency | ±2px |
| Shadow | ui-ux-suite | Elevation hierarchy | 5 levels |
| Iconography | ui-ux-suite | Stroke width | 2px consistent |
| Animation | ui-ux-suite | Duration | 200-400ms |
| Accessibility | a11y-audit | WCAG score | AA minimum |
| Performance | Lighthouse | FCP | < 1.5s |
| Responsiveness | BrowserStack | Breakpoint coverage | 100% |
| Brand Consistency | Custom | Token usage | 100% |

## Figma Design Parity Check

### Tool: `figma_check_design_parity`

**Purpose**: Compare Figma component specifications against coded implementation.

**Input**:

```json
{
  "figmaSpec": {
    "width": "320px",
    "height": "48px",
    "backgroundColor": "#8fa0f5",
    "borderRadius": "14px",
    "fontSize": "16px",
    "fontWeight": "600"
  },
  "codeSpec": {
    "width": "320px",
    "height": "48px",
    "backgroundColor": "#8fa0f5",
    "borderRadius": "14px",
    "fontSize": "16px",
    "fontWeight": "600"
  }
}
```

**Output**:

```json
{
  "score": 95,
  "diffs": [
    {
      "property": "fontWeight",
      "figma": "600",
      "code": "400",
      "severity": "medium",
      "fix": "Update fontWeight to 600 in component CSS"
    }
  ],
  "passed": false
}
```

### Parity Check Workflow

1. **Extract Figma Spec**
   - Use `get_design_context` from Figma MCP
   - Export component properties as JSON

2. **Extract Code Spec**
   - Parse component CSS/styled-components
   - Extract computed styles

3. **Generate Diff Report**
   - Run `figma_check_design_parity`
   - Review scored differences

4. **Apply Fixes**
   - Update component styles
   - Re-run parity check

## Color Space Validation

### OKLCH Color Space

OKLCH (Oklab Lightness Chroma Hue) is the preferred color space for accessibility validation.

**Why OKLCH**:
- Perceptually uniform (unlike RGB/HSL)
- Direct luminance measurement
- Better for contrast calculations

**Usage**:

```javascript
import { oklch } from 'culori';

// Convert hex to OKLCH
const color = oklch("#8fa0f5");
// { l: 0.72, c: 0.12, h: 260 }

// Check contrast ratio
const contrast = calculateContrast(color1, color2);
// Pass if contrast >= 4.5 (WCAG AA)
```

### APCA (Advanced Perceptual Contrast Algorithm)

APCA is the next-generation contrast metric for modern displays.

**APCA Scores**:

| Use Case | Minimum Lc |
|----------|------------|
| Large text (24px+) | 45 |
| Body text (16-24px) | 60 |
| UI elements | 60 |
| Decorative | 30 |

**Tool**: `apca-contrast` npm package

```javascript
import { APCAcontrast } from 'apca-w3';

const score = APCAcontrast(
  { r: 255, g: 255, b: 255 }, // Background
  { r: 0, g: 0, b: 0 }         // Text
);
// Returns Lc score (e.g., "Lc85")
```

## UI/UX Suite Integration

### Installation

```bash
npm install --save-dev ui-ux-suite
```

### Configuration

```javascript
// ui-ux.config.js
module.exports = {
  dimensions: [
    'color-contrast',
    'typography-scale',
    'layout-grid',
    'spacing-consistency',
    'border-radius',
    'shadow-hierarchy',
    'iconography',
    'animation-timing',
    'accessibility',
    'performance',
    'responsiveness',
    'brand-consistency'
  ],
  thresholds: {
    colorContrast: 4.5,
    typographyRatio: 1.25,
    gridAlignment: 0.95
  },
  output: {
    format: 'json',
    path: './reports/ui-ux-audit.json'
  }
};
```

### Running Audit

```bash
npx ui-ux-suite audit --config ui-ux.config.js
```

### Sample Report

```json
{
  "timestamp": "2026-04-24T18:00:00Z",
  "overallScore": 87,
  "dimensions": {
    "color-contrast": {
      "score": 92,
      "status": "pass",
      "issues": []
    },
    "typography-scale": {
      "score": 78,
      "status": "warning",
      "issues": [
        {
          "element": ".btn-primary",
          "expected": "16px",
          "actual": "14px",
          "fix": "Update font-size to 16px"
        }
      ]
    }
  }
}
```

## Related Files

- [`01-figma-mcp.md`](01-figma-mcp.md) - Figma MCP server integration
- [`04-accessibility.md`](04-accessibility.md) - WCAG compliance and auditing
