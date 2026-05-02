# Torro UI Standards: 01. Brand & Aesthetic

<agent_instructions>
- Use these standards to validate the visual identity of any generated UI components.
- Ensure all typography and colors match the defined tokens precisely.
- Follow the "Apple Liquid Glass" pillars for all layout and surface designs.
</agent_instructions>

## 1. Torro Brand Identity

The Torro Enterprise UI combines professional enterprise aesthetics with modern consumer-grade polish.

### 1.1 Logo Specification

| Context | Size | Clear Space | File Format |
|---------|------|-------------|-------------|
| Application Header | 40px height | 16px minimum | SVG |
| Favicon | 32px x 32px | N/A | ICO/PNG |

**SVG Component Location**: `UI/src/shared/ui/torro-logo.svg`

### 1.2 Typography

Torro uses a dual-font system.

| Font Family | Use Case | Weight Range | Load Source |
|-------------|----------|--------------|-------------|
| **Comfortaa** | Brand headings, logos, accent text | 400, 700 | Google Fonts |
| **Roboto** | Body text, data displays, forms | 300, 400, 500 | Google Fonts |
| **Inter** (fallback) | UI elements, tables, code | 400, 500, 600 | System |

#### Font Hierarchy

| Element | Font | Weight | Size (rem) | Line Height |
|---------|------|--------|------------|-------------|
| H1 (Page Title) | Comfortaa | 700 | 2.5 | 1.2 |
| H2 (Section) | Comfortaa | 700 | 2.0 | 1.25 |
| Body | Roboto | 400 | 1.0 | 1.5 |

### 1.3 Color Palette (Torro Standard)

All colors MUST be referenced from `@/shared/theme/tokens.ts`, never hardcoded.

#### Primary & Semantic

| Token | Hex | Usage |
|-------|-----|-------|
| `torro.primary` | `#8fa0f5` | Primary actions, active states |
| `torro.secondary` | `#f9bc60` | Highlights, warnings |
| `torro.accent` | `#e16162` | Errors, deletions |
| `torro.header` | `#5c6bb5` | Headers, navigation bars |
| `torro.text` | `#001e1d` | Primary text |
| `torro.muted` | `#9fa7ae` | Secondary text, placeholders |

i#### Contrast Compliance Rules (MUST FOLLOW)

| Scenario | Background | Text/Icon Color | Class/Constraint |
|----------|------------|-----------------|------------------|
| Header Default | Purple (#5c6bb5) | White/70% | `text-white/70` |
| Header Hover | Purple (#5c6bb5) | White | `text-white` |
| Selected Item | White (#ffffff) | Dark Purple (#5c6bb5) | `text-torro-header` |
| Inactive Item | White (#ffffff) | Grey (#9fa7ae) | `text-torro-muted` |

---

## 2. Apple Liquid Glass Aesthetic

Inspired by high-end consumer technology, featuring frosted glass, soft depth, and fluid interactions.

### 2.1 Visual Pillars

| Pillar | Description | Implementation |
|--------|-------------|----------------|
| **High-Refraction Surfaces** | Frosted glass effect | `backdrop-blur-xl` or `backdrop-blur-2xl` |
| **Aura Borders** | Semi-transparent borders | `border-white/10` or `border-black/5` |
| **Depth Perception** | Multi-layered shadows | `shadow-panel`, `shadow-float` |
| **Squircle Roundness** | Apple-style corners | `rounded-[14px]` (40px items), `rounded-[20px]` (Cards) |

### 2.2 Backdrop Blur Matrix

| Level | Tailwind Class | Use Case |
|-------|----------------|----------|
| **Heavy** | `backdrop-blur-2xl` | Modals, full-screen overlays |
| **Medium** | `backdrop-blur-xl` | Headers, navigation panels |
| **Light** | `backdrop-blur-lg` | Subtle depth, card hover states |

### 2.3 Animation & Motion Standards

| Effect | Tailwind Class | Usage |
|-------|--------|-------|
| Pulse | `animate-pulse` | Icon emphasis, loading indicators |
| Spin | `animate-spin` | Rotating loaders |
| Transition | `transition-all duration-300 ease-out` | Standard for all hover/interactions |

<agent_instructions>
When animating width, use `transition-[width]`. When animating colors, use `transition-colors`. Default to `duration-300`.
</agent_instructions>
