---
name: ui-style-skill
description: Premium UI style skill for world-class design outputs including pixel-perfect Figma translation, visual auditing, micro-interactions, accessibility compliance, and design system synchronization. USE FOR: Apple Liquid Glass aesthetic, Red Dot design grade, Figma MCP integration, design-code parity, WCAG accessibility, Framer Motion animations, dashboard visualizations, design token management.
---

# UI Style Skill (Red Dot / World-Class Design Grade)

## When to Use This Skill

Activate this skill when the task requires premium, award-winning UI quality that exceeds basic functional implementation:

- **Pixel-Perfect Translation**: Converting Figma designs to code without fidelity loss
- **Visual Auditing**: Ensuring coded UI matches design intent with scored parity reports
- **Premium Micro-Interactions**: Adding polished Framer Motion animations
- **Accessibility Compliance**: WCAG 2.1 AA/AAA compliance with automated auditing
- **Data Visualization**: Dashboard-grade charts with Tremor or D3.js
- **Design System Sync**: Managing design tokens across themes (Light, Dark, Brand)

## When NOT to Use This Skill

- Basic CRUD forms or admin panels without design requirements
- Internal tools where speed trumps visual polish
- Legacy code maintenance without redesign scope
- When using pre-approved Storybook components only

## Inputs Required

1. **Design Source**: Figma file URL or design token JSON
2. **Target Framework**: Next.js, React, or Vue component path
3. **Accessibility Target**: WCAG level (AA or AAA)
4. **Animation Requirements**: List of micro-interactions needed

## Two-Phase Lifecycle (UI Component Factory Pattern)

This skill follows the UI Component Factory template with two distinct phases:

### Phase 1: Component Design (Architecture)

Before writing any code, establish the design foundation:

1. **Extract Design Tokens** from Figma via MCP
2. **Define Component API** (props, variants, states)
3. **Plan Accessibility** (ARIA roles, keyboard navigation)
4. **Document Decisions** in component README

### Phase 2: Implementation (Code)

Execute the implementation with strict quality gates:

1. **Build with Primitives** (Radix UI, Headless UI)
2. **Add Micro-Interactions** (Framer Motion)
3. **Verify Parity** (Figma check)
4. **Run A11y Audit** (WCAG compliance)

## Workflow

### Phase 1: Design Context Extraction

1. **Connect Figma MCP Server**
   - Use `get_design_context` to extract design tokens, typography, spacing
   - Use `get_variable_defs` to retrieve design variables
   - Reference: [`references/01-figma-mcp.md`](references/01-figma-mcp.md)

2. **Extract Design Tokens**
   - Colors (primary, secondary, semantic)
   - Typography scale (font-family, sizes, weights)
   - Spacing system (4px grid, gaps, margins)
   - Border radius values (squircle patterns)

### Phase 2: Design-Code Parity Verification

1. **Run Fidelity Check**
   - Execute `figma_check_design_parity` tool
   - Generate scored diff report
   - Apply actionable fixes from report

2. **UI/UX Audit**
   - Run 12-dimension audit (color contrast, typography, layout)
   - Validate against OKLCH and APCA color spaces
   - Reference: [`references/02-audit-tools.md`](references/02-audit-tools.md)

### Phase 3: Component Implementation

1. **Headless Architecture**
   - Use Radix UI or Headix UI primitives
   - Ensure WAI-ARIA compliance by default
   - Implement strict focus management

2. **Micro-Interactions**
   - Add Framer Motion animations
   - Button press states, modal slides, tooltip fades
   - Reference: [`references/03-animation.md`](references/03-animation.md)

3. **Accessibility Audit**
   - Run `a11y-audit` or `accessibility-checker`
   - Fix missing ARIA attributes
   - Simulate color-blindness scorecards
   - Reference: [`references/04-accessibility.md`](references/04-accessibility.md)

### Phase 4: Data Visualization (If Applicable)

1. **Dashboard Components**
   - Use Tremor for KPI cards, sparklines
   - Follow dashboard-specific design patterns
   - Reference: [`references/05-data-viz.md`](references/05-data-viz.md)

2. **Custom Visualizations**
   - Use D3.js for bespoke data art
   - Implement interactive elements
   - Ensure responsive behavior

### Phase 5: Design System Synchronization

1. **Token Management**
   - Use `figma_create_variable_collection`
   - Use `figma_setup_design_tokens`
   - Architect multi-theme system (Light, Dark, Brand)

2. **Component Discovery**
   - Connect Storybook MCP Server
   - Reuse existing approved components
   - Reference: [`references/06-design-system.md`](references/06-design-system.md)

## Examples

### Example 1: Apple Liquid Glass Button

```tsx
// ✅ CORRECT: Apple Liquid Glass aesthetic
import { motion } from 'framer-motion';

export function PrimaryButton({ children, onClick }) {
  return (
    <motion.button
      className="bg-torro-primary rounded-[14px] h-[40px] px-6
                 backdrop-blur-xl bg-white/70 border border-black/5
                 shadow-panel hover:bg-torro-primary/90 transition-all"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}
```

### Example 2: Precision DataTable

```tsx
// ✅ CORRECT: Precision DataTable with design tokens
<DataTable
  columns={columns}
  data={data}
  className="border-[rgba(143,160,245,0.3)] shadow-panel"
  headerClassName="bg-torro-primary text-white font-brand"
  rowHoverClassName="hover:bg-torro-primarySoft/50"
  serverPagination={{
    currentPage: page,
    totalRows: total,
    onPageChange: setPage
  }}
/>
```

## Troubleshooting

### Fidelity Issues

**Problem**: Coded UI doesn't match Figma spec
**Solution**: Run `figma_check_design_parity` and apply fixes from scored diff

**Problem**: Color contrast fails WCAG
**Solution**: Use OKLCH color space validation; adjust luminance

### Animation Issues

**Problem**: Animations feel janky
**Solution**: Add `will-change` CSS property; use GPU-accelerated transforms

**Problem**: Motion conflicts with React hydration
**Solution**: Wrap with `<MotionConfig skipAnimations={true}>` for SSR

### Accessibility Issues

**Problem**: Missing ARIA labels
**Solution**: Run `a11y-audit`; add `aria-label` to interactive elements

**Problem**: Focus management broken
**Solution**: Use Radix UI FocusScope; implement focus traps for modals

## Files

- [`references/01-figma-mcp.md`](references/01-figma-mcp.md) - Figma MCP server tools and commands
- [`references/02-audit-tools.md`](references/02-audit-tools.md) - UI/UX audit and parity checking
- [`references/03-animation.md`](references/03-animation.md) - Framer Motion micro-interactions
- [`references/04-accessibility.md`](references/04-accessibility.md) - WCAG compliance and auditing
- [`references/05-data-viz.md`](references/05-data-viz.md) - Dashboard and D3.js visualization
- [`references/06-design-system.md`](references/06-design-system.md) - Design token management
- [`scripts/validate-visual-parity.sh`](scripts/validate-visual-parity.sh) - Automated parity validation
