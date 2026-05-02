---
name: design-theme-selector
description: Select and apply visual style themes from getdesign.md brand collection to Torro UI without overriding the brand structure in agentic/UI.md
---

# Design Theme Selector

## When to use this skill
Use this skill when you need to:
- **Adopt a visual style** from popular brands (Vercel, Linear, Notion, Stripe, etc.) for the Torro UI
- **Mix style elements** from multiple brands while preserving Torro's structural foundation
- **Choose a design aesthetic** for a specific feature or page without changing the core brand identity

This skill **only affects the style layer** (colors, typography, shadows, borders) and **does NOT override** the brand theme defined in [`agentic/UI.md`](../../../agentic/UI.md).

## When NOT to use this skill
- **Do NOT use** when you want to change Torro's core brand identity (logo, primary/secondary colors, brand values)
- **Do NOT use** when modifying structural components (AppShell, navigation patterns, layout hierarchy)
- **Use `agentic/UI.md` directly** when changing the "Apple Liquid Glass" aesthetic itself

## Inputs required
- `style-source`: Brand name from getdesign.md (e.g., "vercel", "linear", "notion", "stripe")
- `scope`: Where to apply the style - "global" (entire app) or "feature" (specific section)
- `intensity`: "full" (complete style match) or "hybrid" (blend with Torro's aesthetic)

## Available Design Themes

### AI & Developer Platforms
| Brand | Style Profile | Best For |
|-------|---------------|----------|
| **Vercel** | Black/white precision, Geist font, minimal accents | Developer documentation, clean dashboards |
| **Linear** | Ultra-minimal, purple accent (#purple-500), precise spacing | Project management, task interfaces |
| **Notion** | Warm minimalism, serif headings, soft surfaces | Content-heavy pages, wikis |
| **Stripe** | Vibrant gradients, data-rich, blue-primary | Payment flows, financial dashboards |
| **Raycast** | Sleek dark chrome, vibrant gradient accents | Productivity tools, command palettes |
| **Cursor** | Sleek dark interface, gradient accents | Code editors, development tools |
| **Supabase** | Dark emerald theme, code-first | Database tools, API documentation |

### Enterprise & SaaS
| Brand | Style Profile | Best For |
|-------|---------------|----------|
| **Airtable** | Clean structured tables, green accent | Data grids, spreadsheet interfaces |
| **Intercom** | Friendly blue palette, conversational | Chat interfaces, support tools |
| **Mintlify** | Clean green-accented, reading-optimized | Documentation, knowledge bases |
| **PostHog** | Playful hedgehog branding, dark UI | Analytics dashboards, data visualization |

### Dark Mode Specialists
| Brand | Style Profile | Best For |
|-------|---------------|----------|
| **Vercel** | Monochrome precision, high contrast | Technical documentation |
| **Linear** | Dark minimal, subtle depth | Professional tools |
| **Superhuman** | Dark premium, purple glow | Premium experiences |
| **Warp** | Dark terminal-native, block-based | Command interfaces |

## Workflow

### Step 1: Select a Style Source
Choose a brand style that matches your UI goal:
- **For precision/technical**: Vercel, Linear, Raycast
- **For friendly/approachable**: Notion, Intercom, Zapier
- **For data-heavy dashboards**: PostHog, Airtable, Stripe
- **For premium experiences**: Superhuman, Linear

### Step 2: Extract Theme Tokens
Read the [`references/theme-extraction-guide.md`](references/theme-extraction-guide.md) to understand how to extract color, typography, and component tokens from the source brand.

### Step 3: Apply to Torro UI Structure
Follow the [`references/apply-theme.md`](references/apply-theme.md) guide to:
1. Map style tokens to Tailwind classes in [`UI/tailwind.config.ts`](../../../UI/tailwind.config.ts)
2. Update theme tokens in [`UI/src/shared/theme/tokens.ts`](../../../UI/src/shared/theme/tokens.ts)
3. **Preserve** the structural components defined in [`agentic/UI.md`](../../../agentic/UI.md) (AppShell, AppNav, etc.)

### Step 4: Validate the Hybrid Design
Run the validation checklist from [`references/theme-validation.md`](references/theme-validation.md) to ensure:
- Torro brand structure remains intact
- New style tokens are properly applied
- Accessibility contrast requirements are met

## Examples

### Example 1: Apply Linear-style to Task Management
```
Style Source: linear
Scope: feature (features/tasks/)
Intensity: hybrid

Result: Tasks section uses Linear's purple accents and precision spacing,
but retains Torro's AppShell layout and Liquid Glass depth effects
```

### Example 2: Apply Vercel-style to Documentation
```
Style Source: vercel
Scope: feature (app/docs/)
Intensity: full

Result: Documentation pages use Vercel's black/white precision and Geist font,
while keeping Torro's navigation structure and error boundaries
```

## File References
- [`references/theme-extraction-guide.md`](references/theme-extraction-guide.md) - How to extract style tokens from any brand
- [`references/apply-theme.md`](references/apply-theme.md) - Step-by-step theme application
- [`references/theme-validation.md`](references/theme-validation.md) - Pre-deployment checklist
- [`references/brand-directory.md`](references/brand-directory.md) - Complete list of available design sources

## Troubleshooting

### Style conflicts with Torro structure
If the applied style breaks UI components, revert to [`agentic/UI.md`](../../../agentic/UI.md) defaults and reduce intensity to "hybrid".

### Accessibility failures
Check contrast ratios in [`references/theme-validation.md`](references/theme-validation.md). Some light themes need dark text adjustments.

### Font rendering issues
Ensure the selected font is available. Vercel requires Geist fonts; Notion requires serif fallback.
