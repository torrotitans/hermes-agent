# Applying a Design Theme to Torro UI

This guide walks you through applying a selected brand style to the Torro UI while preserving the core brand structure.

## Important: What Changes vs What Stays

### ❌ Do NOT Change (Torro Brand Structure)
These elements in [`agentic/UI.md`](../../../agentic/UI.md) are **immutable** when applying a theme:
- **AppShell** - Root wrapper with title, sessionBar, roleSelector
- **AppNav** - System sidebar navigation pattern
- **AnnouncementBar** - Global notification layer
- **Breadcrumbs** - Navigation path component
- **ErrorBoundary** - Telemetry-backed failure tracking
- **Layer Hierarchy** - FSD-Lite architecture (app/, features/, entities/, shared/, lib/)

### ✅ DO Change (Visual Style Layer)
These elements can be modified to match the selected brand:
- **Color tokens** - Primary, secondary, accent, background colors
- **Typography** - Font families, sizes, weights (within Torro's structure)
- **Borders** - Color, width, transparency
- **Shadows** - Elevation and depth effects
- **Spacing** - Component padding and margin preferences
- **Border radius** - Corner rounding preferences
- **Transitions** - Animation durations and easing

## Step-by-Step Application

### Step 1: Read the Theme Source
1. Visit `https://getdesign.md/<brand>/design-md` to view the full design spec
2. Copy the color palette, typography, and visual effect definitions
3. Note the "best for" use cases to understand where the style excels

### Step 2: Update Tailwind Configuration

Edit [`UI/tailwind.config.ts`](../../../UI/tailwind.config.ts) to add or override theme colors:

```typescript
// Example: Applying Vercel-style theme
module.exports = {
  theme: {
    extend: {
      colors: {
        // Torro structural colors (keep these stable)
        'torro-header': '#1a1a1a',
        'torro-primary': '#8fa0f5',
        'torro-secondary': '#f9bc60',
        
        // Theme override colors (change these per brand)
        'theme-primary': '#000000',          // Vercel black
        'theme-primary-soft': 'rgba(0, 0, 0, 0.08)',
        'theme-accent': '#0070f3',           // Vercel blue
        'theme-surface': 'rgba(0, 0, 0, 0.05)',
      },
      fontFamily: {
        sans: ['Inter', 'var(--font-geist)', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
}
```

### Step 3: Update Theme Tokens

Edit [`UI/src/shared/theme/tokens.ts`](../../../UI/src/shared/theme/tokens.ts):

```typescript
// Map theme tokens to CSS variables
export const themeTokens = {
  colors: {
    // Preserve Torro brand colors
    torroPrimary: '#8fa0f5',
    torroSecondary: '#f9bc60',
    
    // Apply theme styles
    themePrimary: 'var(--color-theme-primary)',
    themePrimarySoft: 'var(--color-theme-primary-soft)',
    themeAccent: 'var(--color-theme-accent)',
    themeSurface: 'var(--color-theme-surface)',
    themeBackground: 'var(--color-theme-background)',
    themeBorder: 'var(--color-theme-border)',
    themeText: 'var(--color-theme-text)',
    themeTextMuted: 'var(--color-theme-text-muted)',
  },
  // ...
}
```

### Step 4: Update Global CSS Variables

Edit [`UI/src/styles/globals.css`](../../../UI/src/styles/globals.css) or create theme-specific overrides:

```css
/* Vercel-style theme override */
:root[data-theme="vercel"] {
  --color-theme-primary: #000000;
  --color-theme-primary-soft: rgba(0, 0, 0, 0.08);
  --color-theme-accent: #0070f3;
  --color-theme-surface: rgba(0, 0, 0, 0.05);
  --color-theme-background: #ffffff;
  --color-theme-border: rgba(0, 0, 0, 0.1);
  --color-theme-text: #000000;
  --color-theme-text-muted: rgba(0, 0, 0, 0.6);
  
  /* Typography */
  --font-theme-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-theme-mono: 'JetBrains Mono', monospace;
  
  /* Shadows */
  --shadow-theme-panel: 0 8px 32px 0 rgba(0, 0, 0, 0.08);
}
```

### Step 5: Apply Theme-Specific Component Styles

Update high-frequency components to use theme tokens:

**Card Component:**
```typescript
// UI/src/shared/ui/card.tsx
export function Card({ children, className }: CardProps) {
  return (
    <div className={`
      rounded-[20px]
      border border-[var(--color-theme-border)]
      bg-[var(--color-theme-surface)]
      shadow-[var(--shadow-theme-panel)]
      backdrop-blur-xl
      ${className}
    `}>
      {children}
    </div>
  );
}
```

**Button Component:**
```typescript
// UI/src/shared/ui/button.tsx
export function Button({ variant = 'primary', ...props }: ButtonProps) {
  const baseStyles = "rounded-lg px-4 py-2 font-medium transition-colors";
  const variants = {
    primary: "bg-[var(--color-theme-accent)] text-white hover:opacity-90",
    secondary: "bg-[var(--color-theme-surface)] text-[var(--color-theme-text)] border border-[var(--color-theme-border)]",
  };
  
  return <button className={`${baseStyles} ${variants[variant]}`} {...props} />;
}
```

### Step 6: Configure Theme Selection (Optional)

Add a theme switcher for user preference:

```typescript
// UI/src/shared/theme/theme-provider.tsx
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'torro' | 'vercel' | 'linear' | 'notion'>('torro');
  
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);
  
  return <>{children}</>;
}
```

## Hybrid Mode: Blending Styles

For "hybrid" intensity, blend the theme with Torro's Liquid Glass aesthetic:

```css
/* Hybrid mode: Vercel style + Torro structure */
:root[data-theme="vercel-hybrid"] {
  /* Use Vercel colors */
  --color-theme-primary: #000000;
  --color-theme-accent: #0070f3;
  
  BUT keep Torro's:
  --torro-glass-blur: backdrop-blur-xl;
  --torro-aura-border: border-white/10;
  --torro-depth-shadow: shadow-panel;
}
```

## Verification Steps

After applying the theme:
1. Run the app and check visual consistency across pages
2. Verify all structural components (AppShell, AppNav) remain intact
3. Test dark mode compatibility if applicable
4. Run accessibility contrast checks
5. Confirm navigation and layout hierarchy unchanged
