# Theme Validation Checklist

Use this checklist to verify a theme has been correctly applied without breaking Torro's structural integrity.

## Visual Consistency Checks

### Color Verification
- [ ] Primary color is applied consistently across all interactive elements
- [ ] Accent color is used for highlights and calls-to-action
- [ ] Background colors have proper hierarchy (background > surface > overlay)
- [ ] Text colors maintain readability on all backgrounds
- [ ] Border colors provide subtle definition without visual noise
- [ ] Shadow colors create appropriate depth perception

### Typography Verification
- [ ] Font families are loaded correctly (check Network tab)
- [ ] Font size scale is consistent (20% ratio between adjacent sizes)
- [ ] Font weights provide clear hierarchy (400/500/600/700)
- [ ] Line heights are readable (1.5 for body, 1.2 for headings)
- [ ] Letter spacing enhances readability (not too tight or loose)

### Component Styling
- [ ] Cards use consistent border radius
- [ ] Buttons have uniform heights and padding
- [ ] Inputs match the theme's visual language
- [ ] Modals use appropriate backdrop blur
- [ ] Tables maintain readability with theme colors

## Structural Integrity Checks

### Preserved Torro Elements
- [ ] AppShell contains title, sessionBar, and roleSelector
- [ ] AppNav is visible and functional (collapsible sidebar)
- [ ] AnnouncementBar appears below header when active
- [ ] Breadcrumbs show current navigation path
- [ ] ErrorBoundary wraps feature routes

### Layer Hierarchy
- [ ] `app/` contains only routing, layouts, and data prefetching
- [ ] `src/features/` contains self-contained business logic
- [ ] `src/entities/` contains shared domain models
- [ ] `src/shared/` contains UI kit and theme tokens
- [ ] `src/lib/` contains API clients and utilities

### Import Constraints
- [ ] No deep imports (all imports go through `index.ts` entry points)
- [ ] DB layer does not import from API layer
- [ ] Features can import from entities and shared
- [ ] Entities can import from shared only

## Accessibility Checks

### Color Contrast
Run contrast checks for all text/color combinations:

| Element | Minimum Ratio | Target |
|---------|--------------|--------|
| Body text | 4.5:1 | 7:1 (AAA) |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | 4.5:1 |
| Focus indicators | 3:1 | 4.5:1 |

**Tools:**
- WebAIM Contrast Checker
- axe DevTools extension
- Chrome DevTools Accessibility panel

### Keyboard Navigation
- [ ] All interactive elements are focusable
- [ ] Focus indicators are visible and distinct
- [ ] Tab order follows logical sequence
- [ ] Skip links are present for main content
- [ ] Modal dialogs trap focus correctly

### Screen Reader
- [ ] All images have alt text
- [ ] Form inputs have associated labels
- [ ] Color is not the only means of conveying information
- [ ] ARIA labels used where needed
- [ ] Heading hierarchy is logical (h1 > h2 > h3)

## Theme-Specific Validation

### Vercel Style
- [ ] Black/white contrast is crisp
- [ ] Geist font (or Inter fallback) is applied
- [ ] Minimal shadows and borders
- [ ] High information density

### Linear Style
- [ ] Purple accent (#purple-500) is used consistently
- [ ] Spacing is precise and consistent
- [ ] Subtle depth effects
- [ ] Keyboard shortcuts are discoverable

### Notion Style
- [ ] Warm, paper-like backgrounds
- [ ] Serif headings with sans-serif body
- [ ] Soft shadows and rounded corners
- [ ] Emoji and icons used decoratively

### Stripe Style
- [ ] Gradient backgrounds are subtle
- [ ] Card-based layout with shadows
- [ ] Blue primary with orange/yellow accents
- [ ] Illustration-heavy design elements

## Performance Checks

- [ ] No layout shift on theme load
- [ ] Font files are optimized (woff2 format)
- [ ] CSS is minified in production
- [ ] Theme switches without full page reload
- [ ] No console errors on theme change

## Browser Compatibility

- [ ] Chrome (latest) - Full support
- [ ] Firefox (latest) - Full support
- [ ] Safari (latest) - Full support
- [ ] Edge (latest) - Full support
- [ ] Mobile Safari (iOS 15+) - Responsive
- [ ] Chrome Mobile (Android 10+) - Responsive

## Final Sign-off

Before deployment:
1. Review against [`agentic/UI.md`](../../../agentic/UI.md) to confirm structural elements intact
2. Test with real users or stakeholders for aesthetic approval
3. Document any theme-specific deviations from the source design
4. Update this checklist with new findings
