# Torro UI Standards: 09. Internationalization (i18n)

<agent_instructions>
- Never hardcode user-facing strings.
- Use the `useTranslation()` hook for all text.
- Follow the dot-notation key naming convention.
</agent_instructions>

## 1. Key Naming Convention

Keys MUST be lowercase and structured by feature and context:
`<feature>.<component>.<element>`

**Example**:
- `auth.login.title`
- `discovery.table.header.name`
- `common.actions.cancel`

---

## 2. Translation File Structure

Translations are stored in JSON files within the `shared/i18n` feature or co-located in the feature directory.

### 2.1 File Location
- **Global**: `UI/src/shared/i18n/locales/en.json`
- **Feature-specific**: `UI/src/features/feature-name/i18n/en.json`

---

## 3. Implementation Patterns

### 3.1 Client Components
```tsx
import { useTranslation } from '@/shared/i18n';

export function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('feature.title')}</h1>;
}
```

### 3.2 Dynamic Values
Always use interpolation for dynamic content.
- **Key**: `"welcome": "Welcome back, {{name}}!"`
- **Usage**: `t('common.welcome', { name: user.name })`

---

## 4. Maintenance Rule
When adding a new feature, you MUST update the base `en.json` (English) file immediately. Do not leave placeholder text in the UI code.
