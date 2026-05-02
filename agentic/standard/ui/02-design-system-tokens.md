# Torro UI Standards: 02. Design System Tokens

<agent_instructions>
- Use these tokens exclusively. NEVER use hardcoded pixel or hex values.
- If a token is missing, refer to `UI/src/shared/theme/tokens.ts` for the full registry.
</agent_instructions>

## 1. Core Design Tokens

Centralized in [`UI/src/shared/theme/tokens.ts`](file:///Users/q4r00t/Github/mark3/UI/src/shared/theme/tokens.ts).

### 1.1 Color Tokens

| Category | Reference |
|----------|-----------|
| **Primary** | `torroTokens.colors.primary` |
| **Secondary** | `torroTokens.colors.secondary` |
| **Accent** | `torroTokens.colors.accent` |
| **Neutral** | `torroTokens.colors.neutral` |
| **Status** | `torroTokens.colors.status` |

### 1.2 Spacing & Radius

| Token | Value | Tailwind Class |
|-------|-------|----------------|
| **Radius XL** | 20px | `rounded-[20px]` |
| **Radius LG** | 12px | `rounded-xl` |
| **Radius MD** | 8px | `rounded-lg` |
| **Radius SM** | 4px | `rounded-sm` |
| **Squircle** | 14px | `rounded-[14px]` (for 40px items) |

---

## 2. Spacing & Layout System

Based on a 4px baseline.

### 2.1 Standard Spacing Scale

| Class | Pixels | Usage |
|-------|--------|-------|
| `p-2` | 8px | Small padding |
| `p-4` | 16px | Standard padding |
| `p-6` | 24px | Medium padding |
| `p-8` | 32px | Large padding |
| `gap-6` | 24px | **Default gap** for grids and layouts |

### 2.2 Responsive Grid Standards

```tsx
// Standard 4-column responsive grid
<div className='grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 w-full'>
```

---

## 3. Quick Reference Combinations

| Effect | Tailwind Classes |
|--------|------------------|
| **Glass Card** | `backdrop-blur-xl bg-white/80 border border-black/5 rounded-[20px] shadow-panel` |
| **Floating Modal** | `backdrop-blur-2xl bg-white/90 border border-black/5 rounded-[20px] shadow-float` |
| **Hover State** | `hover:bg-torro-primarySoft/50 transition-colors duration-200` |
| **Primary Button** | `bg-torro-primary hover:bg-torro-primaryHover text-white rounded-[14px] px-6 py-3` |

<agent_instructions>
Always ensure `transition` classes are paired with `duration-200` or `duration-300` for smooth interactions.
</agent_instructions>
