# Component Template

Use this template when creating new UI components for the Torro design system.

## Template Structure

```tsx
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils/cn';
import { torroTokens } from '@/shared/theme/tokens';

// 1. Define variants using cva
const componentVariants = cva(
  // Base classes (always applied)
  'transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-torro-primary/50',
  {
    variants: {
      // Variant definitions
      variant: {
        default: 'bg-torro-primary text-white',
        secondary: 'bg-torro-secondary text-torro-text',
      },
      size: {
        default: 'h-10 px-4',
        sm: 'h-8 px-2',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

// 2. Define props interface
export interface ComponentProps
  extends React.HTMLAttributes<HTMLElement>,
  VariantProps<typeof componentVariants> {
  // Additional props
  asChild?: boolean;
}

// 3. Create component with forwardRef
const Component = React.forwardRef<HTMLElement, ComponentProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <div
        className={cn(componentVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Component.displayName = 'ComponentName';

export { Component, componentVariants };
```

## Required Elements

### 1. Imports
- Always import React
- Import `cva` and `VariantProps` from `class-variance-authority`
- Import `cn` from `@/lib/utils/cn`
- Import `torroTokens` from `@/shared/theme/tokens` when needed

### 2. Variants Definition
- Use `cva` for all variant definitions
- Include base classes for transitions and focus states
- Define all visual variants (color, size, etc.)
- Set sensible defaults

### 3. Props Interface
- Extend appropriate React HTML attributes
- Include `VariantProps` for variant support
- Add `asChild` prop if component should support Slot pattern

### 4. Component Implementation
- Use `React.forwardRef` for ref forwarding
- Destructure className, variants, and other props
- Merge classes with `cn()` utility
- Set `displayName` for debugging

## Apple Liquid Glass Styling

Apply these classes for the signature look:

### Backdrop Blur
```tsx
'backdrop-blur-xl'  // Medium blur (24px)
'backdrop-blur-2xl' // Heavy blur (40px)
```

### Aura Borders
```tsx
'border border-black/5'    // Light backgrounds
'border border-white/10'   // Dark backgrounds
```

### Depth Shadows
```tsx
'shadow-panel'  // Panel shadow
'shadow-float'  // Floating element shadow
```

### Squircle Roundness
```tsx
'rounded-[14px]' // For 40px items (buttons, icons)
'rounded-[20px]' // For cards/panels
'rounded-xl'     // For smaller containers
```

## Example: Complete Component

```tsx
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils/cn';

const cardVariants = cva(
  'relative backdrop-blur-xl border border-black/5 rounded-[20px] shadow-panel p-6 transition-all duration-200',
  {
    variants: {
      elevation: {
        low: 'shadow-panel',
        high: 'shadow-float',
      },
    },
    defaultVariants: {
      elevation: 'low',
    },
  }
);

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
  VariantProps<typeof cardVariants> {
  title?: string;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, elevation, title, ...props }, ref) => {
    return (
      <div
        className={cn(cardVariants({ elevation, className }))}
        ref={ref}
        {...props}
      >
        {title && (
          <h2 className="font-brand font-bold text-xl mb-4 text-torro-text">
            {title}
          </h2>
        )}
        {props.children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card, cardVariants };
```

## Accessibility Checklist

- [ ] Include proper ARIA attributes when needed
- [ ] Ensure focus states are visible (`focus-visible:ring-2`)
- [ ] Use semantic HTML elements
- [ ] Include `aria-label` for icon-only components
- [ ] Ensure color contrast meets WCAG AA

## Export Pattern

Always export both the component and its variants:
```tsx
export { Component, componentVariants };
```
