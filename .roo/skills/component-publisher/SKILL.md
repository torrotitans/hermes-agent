---
name: component-publisher
description: Update existing or publish new reusable UI components for the Torro design system following Apple Liquid Glass aesthetic, Torro brand identity, and enterprise-grade standards
---

# Component Publisher Skill

## When to Use

Use this skill when you need to:
- Create new reusable UI components in `UI/src/shared/ui/`
- Update existing component implementations or variants
- Ensure components follow Torro brand identity (colors, typography, spacing)
- Apply Apple Liquid Glass aesthetic (backdrop blur, aura borders, depth shadows, squircle roundness)
- Export components via the `UI/src/shared/ui/index.ts` barrel file
- Validate component compliance with design tokens and accessibility standards

## When NOT to Use

Do NOT use this skill for:
- Page-level or feature-specific components (these belong in `UI/src/features/`)
- One-off styling that won't be reused
- Components that don't follow the Torro design system
- Direct edits to `UI/src/shared/theme/tokens.ts` (use theme-update skill instead)

## Inputs Required

1. **Component Name**: The name of the component to create or update (e.g., `button`, `card`, `modal`)
2. **Component Type**: Whether this is a new component or an update to existing
3. **Design Requirements**: Specific visual or functional requirements

## Workflow

### Step 1: Check if Component Exists

Check if the component already exists in `UI/src/shared/ui/`:
- If exists: Read the current implementation at `UI/src/shared/ui/<component-name>.tsx`
- If new: Use the component template from [references/component-template.md](references/component-template.md)

### Step 2: Apply Torro Design System

Ensure the component follows these standards:

#### Colors
- Use design tokens from [`UI/src/shared/theme/tokens.ts`](UI/src/shared/theme/tokens.ts:1)
- Never hardcode hex values
- Reference: `bg-torro-primary`, `text-torro-text`, `border-torro-border`

#### Typography
- Headings/Brand: `font-brand` (Comfortaa)
- Body/Content: `font-content` (Roboto)
- Code/Mono: `font-mono` (Roboto Mono)

#### Apple Liquid Glass Effects
Apply these classes for the glass aesthetic:
- **Backdrop Blur**: `backdrop-blur-xl` or `backdrop-blur-2xl`
- **Aura Borders**: `border border-black/5` or `border-white/10`
- **Depth Shadows**: `shadow-panel` or `shadow-float`
- **Squircle Roundness**: `rounded-[20px]` for panels, `rounded-[14px]` for 40px items

### Step 3: Create or Update Component File

Write the component to `UI/src/shared/ui/<component-name>.tsx` with:
- TypeScript interface for props
- Proper JSDoc documentation
- Forward ref support if needed
- Class variance authority (cva) for variants (if applicable)
- Accessibility attributes (ARIA labels, roles)

### Step 4: Export from Barrel File

Update [`UI/src/shared/ui/index.ts`](UI/src/shared/ui/index.ts:1):
```typescript
export * from './<component-name>';
```

### Step 5: Validate Component

Run the validation script to ensure compliance:
```bash
cd UI && npm run type-check
```

## Examples

### Creating a New Component

To create a new `dropdown-menu` component:

1. Create `UI/src/shared/ui/dropdown-menu.tsx` using the template
2. Implement with Torro colors and Liquid Glass effects
3. Add export to `index.ts`
4. Run validation

### Updating an Existing Component

To update the `button` component with a new variant:

1. Read `UI/src/shared/ui/button.tsx`
2. Add new variant to `buttonVariants` cva
3. Update JSDoc documentation
4. Validate with type-check

## Files Reference

| File | Purpose |
|------|---------|
| [`UI/src/shared/ui/`](UI/src/shared/ui/) | Component directory |
| [`UI/src/shared/ui/index.ts`](UI/src/shared/ui/index.ts:1) | Barrel export file |
| [`UI/src/shared/theme/tokens.ts`](UI/src/shared/theme/tokens.ts:1) | Design tokens |
| [references/component-template.md](references/component-template.md) | Component template |
| [references/design-system-reference.md](references/design-system-reference.md) | Design system guide |

## Troubleshooting

### Component Not Exporting
- Check that `index.ts` has the export statement
- Verify the file is named correctly (lowercase, hyphenated)

### Styles Not Applying
- Ensure you're using token classes (not hardcoded values)
- Check that Tailwind config includes the custom shadows/blur classes

### TypeScript Errors
- Verify all props are properly typed
- Check that imports are using correct paths
