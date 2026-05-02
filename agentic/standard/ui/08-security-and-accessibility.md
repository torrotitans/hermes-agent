# Torro UI Standards: 08. Security & Accessibility

<agent_instructions>
- All interactive components MUST be keyboard accessible.
- Sanitize all user-generated content to prevent XSS.
- Never log or display PII in plain text unless explicitly required by a "Secure View" permission.
</agent_instructions>

## 1. Accessibility (A11y) Baseline

### 1.1 Semantic HTML
Use the correct HTML element for the job:
- `<button>` for actions.
- `<a>` for navigation.
- `<h1>`-`<h6>` for hierarchy.

### 1.2 ARIA Attributes
- **Labels**: Every icon-only button MUST have an `aria-label`.
- **States**: Use `aria-expanded`, `aria-hidden`, and `aria-selected` correctly.
- **Roles**: Use `role="alert"` for toasts and `role="dialog"` for modals.

### 1.3 Color Contrast
- Maintain WCAG AA (4.5:1) minimum contrast ratio.
- Use `text-torro-text` or `text-white` on brand backgrounds.

---

## 2. Frontend Security

### 2.1 Cross-Site Scripting (XSS) Prevention
- **Never** use `dangerouslySetInnerHTML` without a robust sanitizer (e.g., `dompurify`).
- Prefer standard React children/text nodes.

### 2.2 Sensitive Data (PII)
- Mask sensitive data (e.g., emails, IDs) by default.
- Use the `MaskedValue` component for consistent display.

### 2.3 Form Security
- Always validate payloads using **Zod** on the client before submission.
- Implement CSRF protection (handled by BFF/Proxy layer).

---

## 3. Compliance Checklist
- [ ] Tab order is logical and intuitive.
- [ ] Focus rings are visible on all interactive elements.
- [ ] No hardcoded sensitive strings in the source code.
- [ ] Input fields have proper `autoComplete` and `type` attributes.
