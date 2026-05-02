# Design System & Token Management

## Purpose

This reference document details the architecture and implementation of multi-theme design systems using Figma variables, design tokens, and Storybook integration.

## Design Token Architecture

### Token Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Color | Brand colors, semantic colors | `primary`, `error`, `success` |
| Typography | Font families, sizes, weights | `font-brand`, `h1-size` |
| Spacing | Margins, paddings, gaps | `spacing-sm`, `spacing-lg` |
| Border | Radius, width, style | `radius-button`, `border-thin` |
| Shadow | Elevation levels | `shadow-sm`, `shadow-lg` |
| Animation | Durations, easings | `duration-fast`, `ease-out` |

### Token Structure

```json
{
  "color": {
    "primary": {
      "value": "#8fa0f5",
      "type": "color",
      "description": "Primary brand color"
    },
    "secondary": {
      "value": "#5c6bb5",
      "type": "color",
      "description": "Secondary brand color"
    }
  },
  "typography": {
    "fontFamily": {
      "brand": {
        "value": "Comfortaa",
        "type": "fontFamily"
      },
      "content": {
        "value": "Roboto",
        "type": "fontFamily"
      }
    }
  },
  "spacing": {
    "unit": {
      "value": "4px",
      "type": "dimension"
    }
  }
}
```

## Figma Variable Management

### Creating Variable Collections

```javascript
// Create color collection
figma_create_variable_collection({
  name: "Colors",
  modes: ["Light", "Dark", "Brand"]
});

// Create spacing collection
figma_create_variable_collection({
  name: "Spacing",
  modes: ["Light", "Dark", "Brand"]
});
```

### Setting Up Design Tokens

```javascript
figma_setup_design_tokens({
  tokens: {
    primary: {
      Light: "#8fa0f5",
      Dark: "#6b7dd4",
      Brand: "#8fa0f5"
    },
    secondary: {
      Light: "#5c6bb5",
      Dark: "#4a59a0",
      Brand: "#5c6bb5"
    },
    background: {
      Light: "#ffffff",
      Dark: "#1a1a2e",
      Brand: "#ffffff"
    }
  }
});
```

### Mode Configuration

```javascript
// Configure mode-specific values
figma_create_variable_collection({
  name: "Shadows",
  modes: ["Light", "Dark"]
});

// Set shadow values per mode
{
  "shadow-sm": {
    "Light": "0 1px 2px rgba(0,0,0,0.1)",
    "Dark": "0 1px 2px rgba(0,0,0,0.3)"
  },
  "shadow-md": {
    "Light": "0 4px 6px rgba(0,0,0,0.1)",
    "Dark": "0 4px 6px rgba(0,0,0,0.3)"
  }
}
```

## Multi-Theme Architecture

### Theme Structure

```
themes/
├── tokens/
│   ├── colors.json
│   ├── typography.json
│   └── spacing.json
├── modes/
│   ├── light.json
│   ├── dark.json
│   └── brand.json
└── index.ts
```

### Theme Provider

```tsx
import { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext('light');

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

### CSS Variable Mapping

```css
/* tokens.css */
[data-theme="light"] {
  --color-primary: #8fa0f5;
  --color-secondary: #5c6bb5;
  --color-background: #ffffff;
  --color-text: #001e1d;
}

[data-theme="dark"] {
  --color-primary: #6b7dd4;
  --color-secondary: #4a59a0;
  --color-background: #1a1a2e;
  --color-text: #f5f5f5;
}

[data-theme="brand"] {
  --color-primary: #8fa0f5;
  --color-secondary: #5c6bb5;
  --color-background: #f8f9fa;
  --color-text: #001e1d;
}
```

## Storybook Integration

### Storybook MCP Server

**Purpose**: Access organization's existing UI components and ensure reuse of approved building blocks.

**Installation**:

```bash
npm install --save-dev @storybook/react
```

### Component Discovery

```javascript
// Connect to Storybook MCP
const storybook = await connect_storybook_mcp({
  url: 'https://storybook.torro.com'
});

// List available components
const components = await storybook.list_components();
// Returns: ['Button', 'Card', 'Modal', 'DataTable', ...]

// Get component documentation
const buttonDocs = await storybook.get_component_docs('Button');
```

### Component Catalog

```tsx
// stories/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../components/Button';

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered'
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline']
    }
  }
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button'
  }
};
```

## Token Synchronization

### Figma to Code Sync

```javascript
// sync-tokens.js
import { figma_api } from '@figma/mcp';

async function syncTokens() {
  // Extract tokens from Figma
  const tokens = await figma_api.get_variable_defs({
    fileKey: process.env.FIGMA_FILE_KEY
  });

  // Generate CSS variables
  const css = generate_css_variables(tokens);

  // Write to file
  fs.writeFileSync('src/styles/tokens.css', css);

  // Generate TypeScript types
  const types = generate_typescript_types(tokens);
  fs.writeFileSync('src/types/tokens.ts', types);
}

syncTokens();
```

### Token Validation

```javascript
// validate-tokens.js
import { validate_tokens } from '@design-tokens/validator';

const errors = validate_tokens({
  tokens: designTokens,
  rules: {
    colorContrast: true,
    namingConvention: 'kebab-case',
    requiredCategories: ['color', 'typography', 'spacing']
  }
});

if (errors.length > 0) {
  console.error('Token validation failed:', errors);
  process.exit(1);
}
```

## Component Documentation

### README Template

```markdown
# Component: Button

## Purpose

Primary interactive element for user actions.

## Variants

| Variant | Use Case | Example |
|---------|----------|---------|
| Primary | Main actions | Submit, Save |
| Secondary | Secondary actions | Cancel, Back |
| Outline | Tertiary actions | Learn More |

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'outline'` | `'primary'` | Button style |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disabled state |

## Usage

```tsx
import { Button } from '@torro/ui';

<Button variant="primary" onClick={handleSubmit}>
  Submit
</Button>
```

## Accessibility

- Keyboard accessible (Enter/Space)
- Focus indicator visible
- ARIA labels for icon buttons
```

## Related Files

- [`01-figma-mcp.md`](01-figma-mcp.md) - Figma MCP server integration
