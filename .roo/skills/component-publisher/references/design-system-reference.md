# Torro Design System Reference

This reference documents the complete design system for Torro UI components.

## Table of Contents

1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Spacing](#spacing)
4. [Effects](#effects)
5. [Component Patterns](#component-patterns)

---

## Color Palette

All colors are defined in [`UI/src/shared/theme/tokens.ts`](UI/src/shared/theme/tokens.ts:1).

### Primary Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.primary` | `#8fa0f5` | Primary actions, active states |
| `torro.primaryHover` | `#7d8ce0` | Hover states |
| `torro.primaryActive` | `#6c7ac9` | Active/pressed states |
| `torro.primarySoft` | `rgba(143, 160, 245, 0.15)` | Background accents |

### Secondary Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.secondary` | `#f9bc60` | Highlights, CTAs, warnings |
| `torro.secondaryHover` | `#f5b04b` | Hover states |
| `torro.secondaryActive` | `#ee9e33` | Active states |

### Accent Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.accent` | `#e16162` | Errors, deletions, urgent alerts |
| `torro.accentHover` | `#cc5556` | Hover states |
| `torro.accentActive` | `#b54a4b` | Active states |

### Neutral Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.header` | `#5c6bb5` | Headers, navigation bars |
| `torro.background` | `#ffffff` | Page backgrounds |
| `torro.panel` | `#ffffff` | Card/panel backgrounds |
| `torro.text` | `#001e1d` | Primary text |
| `torro.muted` | `#9fa7ae` | Secondary text, placeholders |
| `torro.border` | `#cccccc` | Borders, dividers |
| `torro.overlay` | `rgba(0, 0, 0, 0.4)` | Modal overlays |

### Semantic Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.success` | `#10b981` | Success states |
| `torro.warning` | `#f59e0b` | Warning states |
| `torro.danger` | `#ef4444` | Error states |
| `torro.info` | `#3b82f6` | Informational messages |

---

## Typography

### Font Families

| Font | Use Case | Source |
|------|----------|--------|
| `font-brand` | Comfortaa | Headings, brand elements |
| `font-content` | Roboto | Body text, data displays |
| `font-mono` | Roboto Mono | Code, technical data |

### Font Sizes

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Comfortaa | 2.5rem | 700 |
| H2 | Comfortaa | 2.0rem | 700 |
| H3 | Comfortaa | 1.5rem | 600 |
| H4 | Comfortaa | 1.25rem | 600 |
| Body | Roboto | 1.0rem | 400 |
| Small | Roboto | 0.875rem | 400 |
| Code | Roboto Mono | 0.875rem | 400 |

---

## Spacing

### Padding & Margin Scale

| Class | Value | Usage |
|-------|-------|-------|
| `p-2` | 0.5rem | Tight spacing |
| `p-4` | 1rem | Default spacing |
| `p-6` | 1.5rem | Comfortable spacing |
| `p-8` | 2rem | Large sections |
| `p-12` | 3rem | Hero sections |

### Gap Scale

| Class | Value | Usage |
|-------|-------|-------|
| `gap-1` | 0.25rem | Icon + text |
| `gap-2` | 0.5rem | Related items |
| `gap-4` | 1rem | Card content |
| `gap-6` | 1.5rem | Section elements |
| `gap-8` | 2rem | Major sections |

---

## Effects

### Backdrop Blur

| Class | Blur | Usage |
|-------|------|-------|
| `backdrop-blur-lg` | 16px | Subtle depth |
| `backdrop-blur-xl` | 24px | Headers, panels |
| `backdrop-blur-2xl` | 40px | Modals, overlays |

### Border Radius (Squircle)

| Element | Class | Value |
|---------|-------|-------|
| 40px items | `rounded-[14px]` | 0.875rem |
| Cards | `rounded-[20px]` | 1.25rem |
| Small containers | `rounded-xl` | 0.75rem |
| Inputs | `rounded-lg` | 0.5rem |

### Shadows

| Class | Effect | Usage |
|-------|--------|-------|
| `shadow-panel` | 3px 6px blur | Cards, panels |
| `shadow-float` | 8px 32px blur | Floating modals |
| `shadow-sm` | 2px 4px blur | Subtle elevation |

### Aura Borders

```tsx
// Light background
'border border-white/10'

// Dark background
'border border-black/5'

// Interactive element
'border border-black/10'
```

---

## Component Patterns

### Glass Panel Recipe

```tsx
<div className={`
  relative
  backdrop-blur-xl
  bg-white/70
  border border-black/5
  rounded-[20px]
  shadow-panel
  p-6
`}>
  {/* Content */}
</div>
```

### Floating Modal Recipe

```tsx
<div className={`
  fixed inset-0
  backdrop-blur-2xl
  bg-torro-overlay
  flex items-center justify-center
`}>
  <div className={`
    bg-white/90
    border border-black/5
    rounded-[20px]
    shadow-float
    p-8
    max-w-2xl
    w-full
  `}>
    {/* Modal content */}
  </div>
</div>
```

### Button Variants

```tsx
// Primary button
<button className="bg-torro-primary text-white rounded-[14px] px-6 py-3 hover:bg-torro-primaryHover transition-colors">
  Click Me
</button>

// Secondary button
<button className="bg-torro-primary/10 text-torro-primary rounded-[14px] px-6 py-3 hover:bg-torro-primary/20 transition-colors">
  Secondary
</button>

// Glass button
<button className="bg-white/20 backdrop-blur-md text-white rounded-[14px] px-6 py-3 ring-1 ring-white/30 hover:bg-white/30 transition-colors">
  Glass
</button>
```

### Input Field Pattern

```tsx
<input
  className="w-full px-4 py-3 rounded-lg border border-torro-border bg-white/50 backdrop-blur-md focus:outline-none focus:ring-2 focus:ring-torro-primary/50 transition-all"
  placeholder="Enter text..."
/>
```

---

## Accessibility Requirements

### Color Contrast

All color combinations must meet WCAG AA standards:
- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio

### Focus States

All interactive elements must have visible focus states:
```tsx
'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-torro-primary/50'
```

### ARIA Attributes

- Include `aria-label` for icon-only buttons
- Use `role` attributes for custom components
- Ensure proper heading hierarchy

### Keyboard Navigation

- All interactive elements must be keyboard accessible
- Use `tabIndex` for custom focusable elements
- Implement proper focus trapping for modals
