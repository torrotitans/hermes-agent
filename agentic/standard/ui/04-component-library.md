# Torro UI Standards: 04. Component Library

<agent_instructions>
- Reference these "Golden Path" patterns when building new components or pages.
- Ensure all components use the `variant="glass"` standard where applicable.
</agent_instructions>

## 1. Structural Components

### 1.1 The "Glass Panel" (Cards)
- **Constraint**: MUST use `rounded-[20px]`, `border-black/5`, and `backdrop-blur-xl`.
- **Implementation**: `<Card variant="glass">`

### 1.2 The "Precision DataTable"
- **Header**: MUST use `bg-torro-primary` (#8fa0f5) and `text-white`.
- **Row Hover**: MUST use `hover:bg-torro-primarySoft/50`.
- **Icons**: MUST use `stroke='currentColor'`.

### 1.3 The "Liquid Modal"
- **Constraint**: MUST use `backdrop-blur-2xl` and scale-in animation.

---

## 2. Page Patterns

### 2.1 Landing Dashboards
Used for "Centre" or "Hub" pages (Onboarding, Lineage Centre).
- **Structure**: Transparent Header + 4-column Action Card Grid.
- **Card Hover**: MUST transition icon background to solid `torro-primary`.

### 2.2 Navigation Sidebar
- **Z-Index**: MUST use `z-[1000]`.
- **Backdrop**: `backdrop-blur-xl bg-white/85`.

---

## 3. Torro Search Framework

### 3.1 Primary Header Search
- **Behavior**: Expanding liquid glass element (`w-96` on focus).
- **Persistence**: Query MUST persist in `search` URL parameter.

### 3.2 Global Search Modal
- **Trigger**: `Cmd+K` / `Ctrl+K`.
- **Style**: Heavy Blur (`backdrop-blur-2xl`) overlay.

---

## 4. Authentication Pages (Login Panel)
- **Canonical Pattern**: Glass panel centered on screen.
- **Form Spacing**: `space-y-4`.
- **Buttons**: `bg-torro-primary/50 hover:bg-torro-primary`.
- **Validation**: MUST use Zod schema validation before submission.

---

## 5. Component "Golden Paths" (Snippets)

### Glass Effect Container
```tsx
className='rounded-[20px] border border-white/40 bg-white/70 ring-1 ring-black/5 p-8 shadow-sm backdrop-blur-xl'
```

### Marketplace Filter Bar
Used for content-heavy pages with real-time filtering and pagination.
- **Reference**: `UI/src/features/marketplace/ui/marketplace-filter-bar.tsx`
