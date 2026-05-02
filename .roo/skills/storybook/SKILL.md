---
name: storybook
description: Build, document, and test UI components with Storybook including stories, addons, visual testing, and component documentation
license: MIT
compatibility:
  - react-18.0+
  - storybook-8.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/storybook
---

# Storybook Skill

## When to Use This Skill

Use this skill when you need to:
- Create component stories for documentation
- Build isolated component development environment
- Implement visual regression testing with Chromatic
- Document component props and usage
- Create interactive component demos
- Test components across different themes and states
- Use Storybook addons (Controls, Actions, Docs)
- Implement component variants and edge cases
- Set up Storybook with Next.js or Vite
- Run Storybook in CI/CD pipelines

## When NOT to Use This Skill

Do NOT use this skill when:
- Writing unit tests (use Vitest/Jest instead)
- Building E2E tests (use Playwright instead)
- Creating simple static pages (use regular React)
- Developing backend APIs (use API documentation tools)

## Inputs Required

Before starting, ensure you have:
1. Framework (React, Vue, Angular, etc.)
2. Component library (MUI, Chakra, Radix, custom)
3. Storybook version (default: 8.x)
4. Testing requirements (visual regression, accessibility)

## Workflow

### Step 1: Basic Story Setup

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'outline'],
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'],
    },
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Primary: Story = {
  args: {
    variant: 'primary',
    size: 'md',
    children: 'Button',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
}

export const WithIcon: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
    icon: '🚀',
  },
}
```

### Step 2: Component with Props Documentation

```typescript
// Card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Card } from './Card'

const meta = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'A flexible card component for displaying content.',
      },
    },
  },
  args: {
    title: 'Card Title',
    children: 'Card content goes here.',
  },
} satisfies Meta<typeof Card>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const WithImage: Story = {
  args: {
    image: 'https://example.com/image.jpg',
    title: 'Card with Image',
    children: 'Content with an image header.',
  },
}

export const WithActions: Story = {
  args: {
    title: 'Interactive Card',
    children: 'This card has action buttons.',
    actions: [
      { label: 'Edit', onClick: () => alert('Edit clicked') },
      { label: 'Delete', onClick: () => alert('Delete clicked'), variant: 'danger' },
    ],
  },
}
```

### Step 3: Storybook Parameters and Layouts

```typescript
// ComplexComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { ComplexComponent } from './ComplexComponent'

const meta = {
  title: 'Components/ComplexComponent',
  component: ComplexComponent,
  parameters: {
    layout: 'centered',
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
      ],
    },
    controls: {
      expanded: true,
      hideNoControlsWarning: true,
    },
  },
} satisfies Meta<typeof ComplexComponent>

export default meta
type Story = StoryObj<typeof meta>

export const LightMode: Story = {
  parameters: {
    backgrounds: { default: 'light' },
  },
}

export const DarkMode: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
  },
}

export const AllVariants = {
  render: (args: any) => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
      <ComplexComponent {...args} variant="default" />
      <ComplexComponent {...args} variant="elevated" />
      <ComplexComponent {...args} variant="outlined" />
    </div>
  ),
}
```

### Step 4: Using Addons (Controls, Actions, Docs)

```typescript
// FormComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { FormComponent } from './FormComponent'
import { fn } from '@storybook/test'

const meta = {
  title: 'Components/FormComponent',
  component: FormComponent,
  tags: ['autodocs'],
  argTypes: {
    onSubmit: { action: 'submitted' },
    onCancel: { action: 'cancelled' },
  },
  args: {
    onSubmit: fn(),
    onCancel: fn(),
  },
} satisfies Meta<typeof FormComponent>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    fields: [
      { name: 'name', label: 'Name', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'email', required: true },
      { name: 'message', label: 'Message', type: 'textarea' },
    ],
  },
}

export const WithValidation: Story = {
  args: {
    fields: [
      { name: 'username', label: 'Username', type: 'text', required: true, minLength: 3 },
      { name: 'password', label: 'Password', type: 'password', required: true, minLength: 8 },
    ],
    onSubmit: fn((data) => console.log('Form submitted:', data)),
  },
}
```

### Step 5: Component States and Edge Cases

```typescript
// Table.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Table } from './Table'

const meta = {
  title: 'Components/Table',
  component: Table,
  tags: ['autodocs'],
} satisfies Meta<typeof Table>

export default meta
type Story = StoryObj<typeof meta>

export const Empty: Story = {
  args: {
    columns: [{ key: 'name', label: 'Name' }],
    data: [],
  },
}

export const Loading: Story = {
  args: {
    columns: [{ key: 'name', label: 'Name' }, { key: 'email', label: 'Email' }],
    data: [],
    loading: true,
  },
}

export const WithPagination: Story = {
  args: {
    columns: [
      { key: 'id', label: 'ID' },
      { key: 'name', label: 'Name' },
      { key: 'email', label: 'Email' },
    ],
    data: Array.from({ length: 50 }, (_, i) => ({
      id: i + 1,
      name: `User ${i + 1}`,
      email: `user${i + 1}@example.com`,
    })),
    pagination: {
      pageSize: 10,
      totalItems: 50,
    },
  },
}

export const LongContent: Story = {
  args: {
    columns: [{ key: 'description', label: 'Description' }],
    data: [
      {
        description: 'This is a very long description that should demonstrate how the table handles content that exceeds the available width. It should wrap or truncate appropriately.',
      },
    ],
  },
}
```

### Step 6: Theme and Design System Stories

```typescript
// ThemeDecorator.ts
import type { Decorator } from '@storybook/react'
import { ThemeProvider } from './ThemeProvider'

export const withTheme: Decorator = (Story, context) => {
  const theme = context.globals.theme || 'light'

  return (
    <ThemeProvider theme={theme}>
      <Story />
    </ThemeProvider>
  )
}

// .storybook/preview.ts
import type { Preview } from '@storybook/react'
import { withTheme } from './ThemeDecorator'

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    globals: {
      theme: 'light',
    },
  },
  decorators: [withTheme],
}

export default preview
```

### Step 7: Interactive Component Demos

```typescript
// InteractiveDemo.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { useState } from 'react'
import { Button } from './Button'
import { Input } from './Input'

const meta = {
  title: 'Demos/ContactForm',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        story: 'An interactive contact form demo with validation.',
      },
    },
  },
} satisfies Meta<typeof ContactForm>

function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  })
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
    setTimeout(() => setSubmitted(false), 3000)
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0 auto' }}>
      <Input
        label="Name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        required
      />
      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
      />
      <textarea
        value={formData.message}
        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
        rows={4}
        style={{ width: '100%', padding: '8px', marginBottom: '16px' }}
      />
      <Button type="submit" variant="primary">
        {submitted ? 'Sent!' : 'Send Message'}
      </Button>
    </form>
  )
}

export default meta
type Story = StoryObj<typeof meta>

export const Interactive: Story = {
  render: () => <ContactForm />,
}
```

### Step 8: Storybook Configuration

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/nextjs'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-storysource',
  ],
  framework: {
    name: '@storybook/nextjs',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  staticDirs: ['../public'],
}

export default config
```

### Step 9: Visual Regression Testing

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react'

const preview: Preview = {
  parameters: {
    chromatic: {
      pauseAnimationAtEnd: true,
      diffThreshold: 0.2,
      modes: {
        visualRegression: {
          thresholds: 0.2,
        },
      },
    },
  },
}

export default preview
```

```bash
# Run Chromatic in CI
npx chromatic --project-token=your-token
```

### Step 10: Accessibility Testing

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react'

const preview: Preview = {
  parameters: {
    a11y: {
      config: {
        rules: [
          { id: 'color-contrast', selector: '*' },
          { id: 'heading-order', selector: 'h1, h2, h3, h4, h5, h6' },
          { id: 'label', selector: 'input, select, textarea' },
        ],
      },
      options: {
        detailed: false,
        stopOnError: false,
      },
    },
  },
}

export default preview
```

## Files Reference

| File | Purpose |
|------|---------|
| `.storybook/main.ts` | Storybook configuration |
| `.storybook/preview.ts` | Preview globals and decorators |
| `src/**/*.stories.tsx` | Component stories |
| `src/**/*.mdx` | Documentation pages |

## Troubleshooting

### Issue: Stories Not Loading

**Symptom**: Storybook shows "No stories found"

**Solution**:
- Check `stories` pattern in `main.ts`
- Verify story files match `*.stories.tsx` naming
- Run `storybook dev --quiet` for debug output

### Issue: Controls Not Working

**Symptom**: Args controls not updating component

**Solution**:
- Ensure component accepts props correctly
- Check `argTypes` configuration
- Verify `args` are passed to component

### Issue: Build Fails in CI

**Symptom**: Storybook build fails in CI/CD

**Solution**:
- Install all dependencies before build
- Set `NODE_ENV=production`
- Check for missing environment variables
- Use `storybook build --quiet` for debugging

## Examples

### Example 1: Button Component Stories

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'outline'] },
    size: { control: 'radio', options: ['sm', 'md', 'lg'] },
    disabled: { control: 'boolean' },
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Primary: Story = { args: { variant: 'primary', children: 'Primary' } }
export const Secondary: Story = { args: { variant: 'secondary', children: 'Secondary' } }
export const Disabled: Story = { args: { variant: 'primary', disabled: true, children: 'Disabled' } }
```

### Example 2: Form Component Stories

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Form } from './Form'

const meta = {
  title: 'Components/Form',
  component: Form,
  tags: ['autodocs'],
} satisfies Meta<typeof Form>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    fields: [
      { name: 'name', label: 'Name', type: 'text', required: true },
      { name: 'email', label: 'Email', type: 'email', required: true },
    ],
  },
}
```

## Related Resources

- [Storybook Documentation](https://storybook.js.org/)
- [Storybook Addons](https://storybook.js.org/addons)
- [Storybook React](https://storybook.js.org/docs/react/get-started)
