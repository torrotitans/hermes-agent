---
name: tailwindcss
description: >
  Create, configure, and extend TailwindCSS v4 stylesheets including utility classes,
  theme customization, plugin development, variants, and responsive design. Covers
  the new CSS-first configuration, @theme directive, @apply, @utility, and the
  design system API. USE FOR: utility classes, theme customization, plugins,
  responsive design, dark mode, variants, @apply, @utility, @theme, @slot.
  DO NOT USE FOR: Tailwind v3 config.js patterns (use documentation), component
  libraries (use storybook skill), CSS-in-JS patterns.
location: .roo/skills/tailwindcss/SKILL.md
metadata:
  created: "2026-04-27"
  version: "4.0.0"
  compatibility:
    - tailwindcss>=4.0.0
    - postcss>=8.4.0
---

# TailwindCSS v4 Skill

## When to Use This Skill

- Creating TailwindCSS stylesheets with utility classes
- Customizing the TailwindCSS theme
- Building responsive layouts
- Implementing dark mode
- Creating custom utilities and plugins
- Configuring variants and responsive breakpoints
- Using @apply, @utility, @slot directives
- Migrating from TailwindCSS v3 to v4

## When NOT to Use This Skill

- TailwindCSS v3 configuration (tailwind.config.js) → use v3 documentation
- Creating React/Vue components → use component-publisher skill
- Custom CSS without Tailwind → write raw CSS

## Inputs Required

1. Design requirements (colors, spacing, typography)
2. Breakpoint configuration
3. Custom utilities needed
4. Plugin requirements

## Workflow

### Step 1: Basic Stylesheet Setup

TailwindCSS v4 uses CSS-first configuration:

```css
@import "tailwindcss";

/* Import the full TailwindCSS v4 package */
@import "tailwindcss";

/* Or import specific parts */
@import "tailwindcss/preflight"; /* Base styles only */
@import "tailwindcss/utilities"; /* Utilities only */
```

### Step 2: Theme Customization

From [`/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts):

```css
@import "tailwindcss";

/* Define custom theme values using @theme */
@theme {
  /* Colors */
  --color-primary: #6366f1;
  --color-primary-50: #eef2ff;
  --color-primary-100: #e0e7ff;
  --color-primary-200: #c7d2fe;
  --color-primary-300: #a5b4fc;
  --color-primary-400: #818cf8;
  --color-primary-500: #6366f1;
  --color-primary-600: #4f46e5;
  --color-primary-700: #4338ca;
  --color-primary-800: #3730a3;
  --color-primary-900: #312e81;
  --color-primary-950: #1e1b4b;

  /* Spacing scale */
  --spacing-2xs: 0.125rem;
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --spacing-3xl: 4rem;

  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);

  /* Fonts */
  --font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --font-serif: 'Georgia', ui-serif, serif;

  /* Z-index scale */
  --z-index-base: 0;
  --z-index-dropdown: 1000;
  --z-index-sticky: 1020;
  --z-index-fixed: 1030;
  --z-index-modal-backdrop: 1040;
  --z-index-overlay: 1050;
  --z-index-modal: 1060;
  --z-index-popover: 1070;
  --z-index-tooltip: 1080;
}
```

### Step 3: Reference Theme Values

From [`/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts) lines 17-33:

```css
/* Theme keys that are ignored by nested keys */
/* --font ignores --font-weight, --font-size */
/* --inset ignores --inset-shadow, --inset-ring */
/* --text ignores --text-color, --text-decoration-color, etc. */
/* --grid-column ignores --grid-column-start, --grid-column-end */
/* --grid-row ignores --grid-row-start, --grid-row-end */

/* Clear all theme values */
@theme {
  --*: initial; /* Clears all custom theme values */
}

/* Clear specific namespace */
@theme {
  --colors-primary: initial; /* Clears all --color-primary-* values */
}
```

### Step 4: Responsive Design

```css
@import "tailwindcss";

@theme {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Usage in components */
.component {
  grid-template-columns: 1fr; /* Mobile first */
}

@media (min-width: 640px) {
  .component {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .component {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Step 5: Dark Mode

```css
@import "tailwindcss";

@theme {
  --color-dark-bg: #1a1a2e;
  --color-dark-fg: #e0e0e0;
}

/* Class-based dark mode */
.dark {
  --color-bg: var(--color-dark-bg);
  --color-fg: var(--color-dark-fg);
}

/* Usage */
.card {
  background-color: var(--color-bg);
  color: var(--color-fg);
}

/* Or use dark: variant */
.card {
  background-color: white;
  color: black;
}

.dark .card {
  background-color: var(--color-dark-bg);
  color: var(--color-dark-fg);
}
```

### Step 6: @apply Directive

```css
@import "tailwindcss";

/* Extract repeated utility combinations */
.btn {
  @apply px-4 py-2 font-medium rounded-lg transition-colors;
}

.btn-primary {
  @apply btn bg-primary-600 text-white hover:bg-primary-700;
}

.btn-secondary {
  @apply btn bg-gray-200 text-gray-800 hover:bg-gray-300;
}

/* Nested @apply */
.card {
  @apply rounded-xl shadow-md p-6 bg-white;
}

.card-header {
  @apply card border-b border-gray-200 pb-4;
}
```

### Step 7: Custom Utilities with @utility

From [`/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts):

```css
@import "tailwindcss";

@theme {
  --spacing-gutter: 1.5rem;
  --color-brand: #0066ff;
}

/* Define custom utilities */
@utility container-fluid {
  width: 100%;
  max-width: none;
  padding-left: var(--spacing-gutter);
  padding-right: var(--spacing-gutter);
}

@utility prose {
  max-width: 65ch;
  line-height: 1.75;
  
  p {
    margin-top: 1.25em;
    margin-bottom: 1.25em;
  }
  
  h2 {
    margin-top: 2em;
    margin-bottom: 0.75em;
    font-size: 1.5rem;
    font-weight: 600;
  }
}

/* Gradient utilities */
@utility bg-gradient-radial {
  background: radial-gradient(var(--tw-gradient-stops));
}

@utility bg-gradient-conic {
  background: conic-gradient(var(--tw-gradient-stops));
}
```

### Step 8: Custom Plugins

From [`/tmp/tailwindcss-repo/packages/tailwindcss/src/plugin.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/plugin.ts):

```typescript
import plugin from 'tailwindcss/plugin';

// Simple plugin
const myPlugin = plugin(function({ addUtilities, theme }) {
  addUtilities({
    '.custom-utility': {
      padding: theme('spacing.sm'),
      color: theme('colors.primary.500'),
    },
  });
});

// Plugin with options
const spacingPlugin = plugin.withOptions(
  (options = {}) => {
    const { scale = 1 } = options;
    return function({ addUtilities, theme }) {
      addUtilities({
        [`.scale-${scale}`]: {
          transform: `scale(${scale})`,
        },
      });
    };
  },
  (options = {}) => ({
    theme: {
      scale: options.scale ? [options.scale] : [],
    },
  })
);

// Export for use in CSS
export default myPlugin;
```

### Step 9: @slot Directive

```css
@import "tailwindcss";

@theme {
  --color-surface: #ffffff;
  --color-text: #1a1a1a;
}

/* Define reusable component slots */
@slot card {
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
}

@slot card-header {
  border-bottom: 1px solid var(--color-gray-200);
  padding-bottom: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

@slot card-body {
  padding: var(--spacing-md) 0;
}

@slot card-footer {
  border-top: 1px solid var(--color-gray-200);
  padding-top: var(--spacing-md);
  margin-top: var(--spacing-md);
}
```

### Step 10: Variants

```css
@import "tailwindcss";

/* Built-in variants */
.hover\:bg-blue-500:hover { background-color: rgb(59 130 246); }
.focus\:ring-2:focus { outline: 2px solid transparent; outline-offset: 2px; }
.group-hover\:opacity-100 .group:hover & { opacity: 1; }
.peer-checked\:block ~ .peer:checked + & { display: block; }

/* Custom variants */
@variant dark (&:is(.dark *));
@variant hover-focus (:hover, :focus);

/* Variant ordering */
@variant before { &::before { @contents }; }
@variant after { &::after { @contents }; }
```

### Step 11: Container Component

```css
@import "tailwindcss";

@theme {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Container utility */
@utility container {
  margin-inline: auto;
  padding-inline: var(--spacing-md);
  
  @media (min-width: 640px) {
    max-width: 640px;
  }
  @media (min-width: 768px) {
    max-width: 768px;
  }
  @media (min-width: 1024px) {
    max-width: 1024px;
  }
  @media (min-width: 1280px) {
    max-width: 1280px;
  }
  @media (min-width: 1536px) {
    max-width: 1536px;
  }
}
```

### Step 12: Common Utility Classes Reference

From [`/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts):

```css
/* Layout */
.block, .inline-block, .inline, .flex, .inline-flex, .grid, .inline-grid
.flex-row, .flex-col, .flex-wrap, .flex-nowrap
.justify-start, .justify-end, .justify-center, .justify-between, .justify-around, .justify-evenly
.items-start, .items-end, .items-center, .items-baseline, .items-stretch
.gap-0, .gap-1, .gap-2, .gap-4, .gap-8
.col-span-1, .col-span-2, .col-span-full
.row-span-1, .row-span-2, .row-span-full

/* Sizing */
.w-full, .w-screen, .w-min, .w-max, .w-fit
.h-full, .h-screen, .h-min, .h-max, .h-fit
.min-w-0, .min-w-full, .min-w-min, .min-w-max
.max-w-xs, .max-w-sm, .max-w-md, .max-w-lg, .max-w-xl
.w-0, .w-1, .w-2, .w-4, .w-8, .w-16, .w-20, .w-24, .w-32
.w-1\/2, .w-1\/3, .w-2\/3, .w-1\/4, .w-2\/4, .w-3\/4
.w-auto, .w-px, .w-prose

/* Spacing */
.p-0, .p-1, .p-2, .p-4, .p-8 /* padding */
.px-0, .px-4, .px-8 /* padding-x */
.py-0, .py-4, .py-8 /* padding-y */
.pt-0, .pt-4, .pt-8 /* padding-top */
.m-0, .m-1, .m-2, .m-4, .m-8 /* margin */
.mx-auto /* margin-x: auto */

/* Typography */
.text-xs, .text-sm, .text-base, .text-lg, .text-xl, .text-2xl
.font-thin, .font-light, .font-normal, .font-medium, .font-semibold, .font-bold
.text-left, .text-center, .text-right, .text-justify
.tracking-tight, .tracking-tighter, .tracking-normal
.leading-none, .leading-tight, .leading-snug, .leading-normal

/* Colors */
.text-white, .text-black
.text-primary, .text-primary-50, .text-primary-100, ...
.bg-primary, .bg-primary-500, .bg-primary-600
.text-opacity-50, .text-opacity-75, .text-opacity-100
.bg-opacity-50, .bg-opacity-75, .bg-opacity-100

/* Borders */
.border, .border-0, .border-2, .border-4, .border-8
.border-solid, .border-dashed, .border-dotted, .border-double, .border-none
.rounded, .rounded-sm, .rounded, .rounded-md, .rounded-lg, .rounded-xl, .rounded-full
.rounded-t, .rounded-r, .rounded-b, .rounded-l
.rounded-tl, .rounded-tr, .rounded-br, .rounded-bl

/* Shadows */
.shadow-sm, .shadow, .shadow-md, .shadow-lg, .shadow-xl, .shadow-2xl
.shadow-inner, .shadow-none

/* Effects */
.opacity-0, .opacity-25, .opacity-50, .opacity-75, .opacity-100
.blend-normal, .blend-multiply, .blend-screen, .blend-overlay
.backdrop-blur-none, .backdrop-blur-sm, .backdrop-blur, .backdrop-blur-lg
```

## Troubleshooting

### Theme Values Not Working

```css
/* Ensure theme values use CSS custom properties */
@theme {
  --color-primary: #6366f1; /* Correct */
  /* NOT: color-primary: #6366f1; */
}
```

### @apply Conflicts

```css
/* Avoid conflicting utilities */
.btn {
  @apply px-4 py-2; /* OK */
  @apply px-6 py-3; /* Conflicts with above */
}

/* Use inheritance instead */
.btn-base {
  @apply px-4 py-2;
}
.btn-lg {
  @apply btn-base px-6 py-3;
}
```

### Plugin Not Loading

```typescript
// Ensure plugin is exported correctly
import plugin from 'tailwindcss/plugin';

const myPlugin = plugin(function({ addUtilities }) {
  addUtilities({ /* ... */ });
});

export default myPlugin;
```

## Related Files

- [`/tmp/tailwindcss-repo/packages/tailwindcss/src/index.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/index.ts)
- [`/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/utilities.ts)
- [`/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/theme.ts)
- [`/tmp/tailwindcss-repo/packages/tailwindcss/src/plugin.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/plugin.ts)
- [`/tmp/tailwindcss-repo/packages/tailwindcss/src/compat/plugin-api.ts`](/tmp/tailwindcss-repo/packages/tailwindcss/src/compat/plugin-api.ts)
