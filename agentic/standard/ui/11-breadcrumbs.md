# Breadcrumb Standards

> **LOCKED**: Breadcrumb styling is frozen. All breadcrumb implementations MUST follow these standards.

## Structure

- Breadcrumbs consist of a "Home" link followed by path segments separated by chevron icons.
- The current page (last segment) is displayed as plain text; all intermediate segments are clickable links.
- **No sub-labels** (e.g., "Workspace", "Data Asset") are displayed beneath the current page label.

## Styling

### Container
- `<nav>` element with `aria-label='Breadcrumb'`
- `mb-2 flex items-center gap-2 text-sm font-medium`

### Home Link
- Uses `Home` icon from lucide-react with `stroke='currentColor' strokeWidth={2}`
- Icon: `h-4 w-4`
- Label: `text-torro-muted`
- Hover: `hover:text-torro-header`
- Link target: `/dashboard`

### Chevron Separator
- Uses `ChevronRight` icon from lucide-react
- Size: `h-3.5 w-3.5`
- Color: `text-torro-border`

### Intermediate Links (non-last segments)
- `text-sm font-medium text-torro-muted transition hover:text-torro-header`
- Styled identically to Home (same size, font weight, color)

### Current Page (last segment)
- `text-sm font-medium text-torro-header`
- Same size and font weight as Home and intermediate links
- Plain `<span>` (not a link)

## Decision Rules

| Element | Style |
|---------|-------|
| Home link | `text-sm font-medium text-torro-muted hover:text-torro-header` |
| Intermediate link | `text-sm font-medium text-torro-muted transition hover:text-torro-header` |
| Current page | `text-sm font-medium text-torro-header` |
| Chevron | `h-3.5 w-3.5 text-torro-border` |

---

*Last Updated: 2026-04-28*
*Version: 1.0 (Breadcrumbs LOCKED)*
