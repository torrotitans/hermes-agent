# Theme Extraction Guide

This guide explains how to extract design tokens from any brand's DESIGN.md to apply to Torro UI.

## Step 1: Get the Source Design.md

Visit `https://getdesign.md/<brand>/design-md` to view the full design specification for any brand.

## Step 2: Extract Key Design Tokens

### Color Palette
Look for and extract:
- **Primary color** - Main brand color for actions and highlights
- **Secondary/Accent color** - Supportive brand color
- **Background colors** - Primary, secondary, and surface colors
- **Text colors** - Primary, secondary, muted text
- **Border colors** - Default and hover states
- **Shadow colors** - Drop shadow and elevation colors

**Example Format:**
```css
/* Vercel-style tokens */
--color-primary: #000000;
--color-primary-soft: rgba(0, 0, 0, 0.08);
--color-secondary: #ffffff;
--color-accent: #0070f3;
--color-background: #ffffff;
--color-surface: rgba(0, 0, 0, 0.05);
--color-border: rgba(0, 0, 0, 0.1);
--color-text: #000000;
--color-text-muted: rgba(0, 0, 0, 0.6);
```

### Typography
Extract:
- **Font families** - Primary, secondary, monospace
- **Font sizes** - Scale (xs, sm, base, lg, xl, etc.)
- **Font weights** - Normal, medium, semibold, bold
- **Line heights** - Tight, normal, relaxed
- **Letter spacing** - Tighter, tight, normal, wide

**Example Format:**
```css
/* Vercel-style typography */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
--font-size-xs: 0.75rem;
--font-size-sm: 0.875rem;
--font-size-base: 1rem;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Spacing & Sizing
Extract:
- **Border radius** - sm, md, lg, xl, full
- **Spacing scale** - 1x, 2x, 4x, 8x, etc.
- **Component heights** - Button, input, card heights

### Visual Effects
Extract:
- **Shadow definitions** - Small, medium, large shadows
- **Blur effects** - Backdrop blur values
- **Gradients** - Any gradient patterns
- **Transitions** - Duration and easing functions

## Step 3: Map to Tailwind Config

Convert extracted tokens to Tailwind configuration:

```typescript
// UI/tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      colors: {
        'torro-primary': '#000000',      // Source: Vercel primary
        'torro-primarySoft': 'rgba(0, 0, 0, 0.08)',
        'torro-accent': '#0070f3',       // Source: Vercel accent
        'torro-surface': 'rgba(0, 0, 0, 0.05)',
      },
      fontFamily: {
        sans: ['Inter', 'var(--font-geist)'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
      },
      boxShadow: {
        'panel': '0 8px 32px 0 rgba(0, 0, 0, 0.08)',
      },
    },
  },
}
```

## Step 4: Update Theme Tokens File

Apply the mapped tokens to [`UI/src/shared/theme/tokens.ts`](../../../UI/src/shared/theme/tokens.ts):

```typescript
export const themeTokens = {
  colors: {
    primary: 'var(--color-torro-primary)',
    primarySoft: 'var(--color-torro-primarySoft)',
    accent: 'var(--color-torro-accent)',
    // ...
  },
  // ...
}
```

## Brand-Specific Extraction Tips

### Vercel
- Focus on black/white contrast
- Geist font family (or Inter fallback)
- Subtle gray surfaces

### Linear
- Purple accent (#purple-500)
- Precision spacing (0.5px increments)
- Subtle depth shadows

### Notion
- Warm beige/off-white backgrounds
- Serif headings (Georgia fallback)
- Soft, paper-like surfaces

### Stripe
- Vibrant gradients (blue-to-purple)
- Card-based layouts with shadows
- Blue primary with orange/yellow accents

## Quality Checklist

Before applying extracted tokens:
- [ ] All colors have sufficient contrast (WCAG AA minimum)
- [ ] Typography scale is consistent (20% ratio between sizes)
- [ ] Border radius values are harmonious
- [ ] Shadow values create clear depth hierarchy
- [ ] All referenced fonts are loaded in the project
