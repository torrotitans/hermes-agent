# Accessibility (A11y) Compliance

## Purpose

This reference document details the tools, patterns, and workflows for achieving WCAG 2.1 AA/AAA compliance through automated auditing and headless UI primitives.

## WCAG Compliance Levels

| Level | Minimum Contrast | Use Case |
|-------|------------------|----------|
| AA | 4.5:1 (text), 3:1 (UI) | Standard compliance |
| AAA | 7:1 (text), 4.5:1 (UI) | Enhanced accessibility |

## Headless UI Primitives

### Radix UI

**Website**: https://www.radix-ui.com

**Why Radix UI**:
- Full WAI-ARIA compliance out of the box
- Strict focus management
- Keyboard navigation built-in
- Unstyled (complete design freedom)

**Installation**:

```bash
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
```

**Example: Accessible Modal**:

```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function AccessibleModal({ isOpen, onClose, children }) {
  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Trigger asChild>
        <button>Open Modal</button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg">
          <Dialog.Title>Modal Title</Dialog.Title>
          <Dialog.Description>
            This modal is fully accessible with keyboard navigation and focus trapping.
          </Dialog.Description>
          {children}
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Headless UI

**Website**: https://headlessui.com

**Installation**:

```bash
npm install @headlessui/react
```

**Example: Accessible Dropdown**:

```tsx
import { Menu } from '@headlessui/react';

export function AccessibleDropdown({ items }) {
  return (
    <Menu as="div" className="relative">
      <Menu.Button className="btn-primary">
        Options
      </Menu.Button>
      <Menu.Items className="absolute right-0 mt-2 bg-white rounded-lg shadow-lg">
        {items.map((item) => (
          <Menu.Item key={item.id}>
            <a href={item.href} className="block px-4 py-2 hover:bg-gray-100">
              {item.label}
            </a>
          </Menu.Item>
        ))}
      </Menu.Items>
    </Menu>
  );
}
```

## Automated A11y Auditing

### Tool: `a11y-audit`

**Repository**: https://github.com/rohitg00/awesome-claude-code-toolkit

**Installation**:

```bash
npm install --save-dev a11y-audit
```

**Usage**:

```bash
npx a11y-audit --url http://localhost:3000 --output report.json
```

**Sample Output**:

```json
{
  "score": 92,
  "issues": [
    {
      "id": "color-contrast",
      "severity": "critical",
      "element": ".btn-primary",
      "message": "Text color contrast ratio is 3.2:1, expected 4.5:1",
      "fix": "Darken text color to #595959 or lighter"
    },
    {
      "id": "missing-alt",
      "severity": "serious",
      "element": "img.hero-image",
      "message": "Image missing alt attribute",
      "fix": "Add descriptive alt text"
    }
  ]
}
```

### Tool: `accessibility-checker`

**Installation**:

```bash
npm install --save-dev accessibility-checker
```

**Usage**:

```bash
npx a11y --ruleset WCAG21 --level AA --failOnViolation src/
```

## Color Blindness Simulation

### Tool: `color-blindness-simulator`

**Installation**:

```bash
npm install --save-dev color-blindness-simulator
```

**Usage**:

```tsx
import { simulateColorBlindness } from 'color-blindness-simulator';

// Simulate protanopia (red-blind)
const simulatedColor = simulateColorBlindness('#8fa0f5', 'protanopia');
// Returns simulated color value
```

### Browser DevTools

Chrome DevTools has built-in color blindness simulation:

1. Open DevTools (F12)
2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
3. Type "Rendering"
4. Select "Emulate vision deficiencies"
5. Choose type (Protanopia, Deuteranopia, Tritanopia)

## ARIA Attributes Reference

### Common ARIA Roles

| Role | Purpose | Example |
|------|---------|---------|
| `button` | Clickable element | `<div role="button">` |
| `dialog` | Modal window | `<div role="dialog">` |
| `navigation` | Navigation links | `<nav role="navigation">` |
| `alert` | Important message | `<div role="alert">` |
| `progressbar` | Progress indicator | `<div role="progressbar">` |

### ARIA States

| State | Purpose | Example |
|-------|---------|---------|
| `aria-expanded` | Expandable element | `aria-expanded="true"` |
| `aria-hidden` | Hidden from screen readers | `aria-hidden="true"` |
| `aria-disabled` | Disabled element | `aria-disabled="true"` |
| `aria-selected` | Selected item | `aria-selected="false"` |
| `aria-pressed` | Toggle button | `aria-pressed="true"` |

### ARIA Labels

```tsx
// Icon-only button
<button aria-label="Close modal">
  <XIcon />
</button>

// Form field with error
<input
  type="email"
  aria-label="Email address"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error">Invalid email format</span>
```

## Focus Management

### Focus Trap

```tsx
import { FocusScope } from '@radix-ui/react-focus-scope';

export function Modal({ children }) {
  return (
    <FocusScope trapped>
      {children}
    </FocusScope>
  );
}
```

### Focus Visible

```css
/* Custom focus indicator */
:focus-visible {
  outline: 2px solid #8fa0f5;
  outline-offset: 2px;
}

/* Remove default focus for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

## Keyboard Navigation

### Tab Order

```tsx
// Correct tab order
<div>
  <button tabIndex={0}>First</button>
  <button tabIndex={0}>Second</button>
  <button tabIndex={0}>Third</button>
</div>

// Avoid negative tabIndex
<button tabIndex={-1}>Not in tab order</button>
```

### Keyboard Event Handlers

```tsx
function handleKeyDown(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}

<button onKeyDown={handleKeyDown}>
  Clickable with Enter and Space
</button>
```

## Audit Checklist

### Pre-Launch A11y Checklist

- [ ] All images have alt text
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible
- [ ] Form fields have labels
- [ ] Error messages are announced to screen readers
- [ ] Modal dialogs trap focus
- [ ] Page has proper heading hierarchy (H1-H6)
- [ ] Skip links for main content
- [ ] ARIA landmarks used correctly

### Automated Audit Command

```bash
# Run full accessibility audit
npm run audit:accessibility

# Generate HTML report
npx a11y-audit --url http://localhost:3000 --output report.html
```

## Related Files

- [`03-animation.md`](03-animation.md) - Framer Motion micro-interactions
- [`02-audit-tools.md`](02-audit-tools.md) - UI/UX audit and parity checking
