# Figma MCP Server Integration

## Purpose

This reference document details the Figma Model Context Protocol (MCP) server integration for extracting design context, managing design tokens, and ensuring design-code parity.

## MCP Servers

### 1. Official Figma MCP Server

**Repository**: https://github.com/figma/mcp-server-guide

**Primary Tools**:

| Tool | Purpose | Example |
|------|---------|---------|
| `get_design_context` | Extract design tokens, typography, spacing from Figma file | `figma:get_design_context({ fileKey: "abc123", nodeId: "456" })` |
| `get_variable_defs` | Retrieve design variables (colors, spacing, typography) | `figma:get_variable_defs({ fileKey: "abc123" })` |
| `create_design_system_rules` | Generate design system rules for agent enforcement | `figma:create_design_system_rules({ tokens: {...} })` |

**Usage Pattern**:

```yaml
# Step 1: Connect to Figma
figma:get_design_context:
  fileKey: "your-file-key"
  nodeId: "node-id"

# Step 2: Extract tokens
figma:get_variable_defs:
  fileKey: "your-file-key"

# Step 3: Apply to codebase
# Agent generates components using extracted tokens
```

### 2. Figma Console MCP (Southleft)

**Repository**: https://github.com/southleft/figma-console-mcp

**Primary Tools**:

| Tool | Purpose | Example |
|------|---------|---------|
| `figma_check_design_parity` | Compare Figma spec vs coded implementation | `figma:check_design_parity({ figmaSpec, codeSpec })` |
| `figma_create_variable_collection` | Create variable collections for themes | `figma:create_variable_collection({ name: "Colors", mode: "Dark" })` |
| `figma_setup_design_tokens` | Set up design tokens for multi-theme | `figma:setup_design_tokens({ tokens: {...} })` |

**Parity Check Workflow**:

1. Extract Figma component spec
2. Extract coded implementation spec
3. Generate scored diff report
4. Apply actionable fixes

## Design Token Extraction

### Color Tokens

```json
{
  "colors": {
    "primary": "#8fa0f5",
    "secondary": "#5c6bb5",
    "text": "#001e1d",
    "muted": "#9fa7ae",
    "glass": {
      "background": "rgba(255, 255, 255, 0.7)",
      "border": "rgba(0, 0, 0, 0.05)"
    }
  }
}
```

### Typography Tokens

```json
{
  "typography": {
    "fontFamily": {
      "brand": "Comfortaa",
      "content": "Roboto"
    },
    "scale": {
      "h1": { "size": "32px", "weight": "700" },
      "h2": { "size": "24px", "weight": "600" },
      "body": { "size": "16px", "weight": "400" }
    }
  }
}
```

### Spacing Tokens

```json
{
  "spacing": {
    "unit": "4px",
    "values": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px"
    }
  }
}
```

### Border Radius Tokens

```json
{
  "borderRadius": {
    "button": "14px",
    "panel": "20px",
    "modal": "24px"
  }
}
```

## Multi-Theme Architecture

### Theme Structure

```
themes/
├── light.json
├── dark.json
└── brand.json
```

### Token Collection Creation

```javascript
// Create color collection for all themes
figma_create_variable_collection({
  name: "Colors",
  modes: ["Light", "Dark", "Brand"]
});

// Set up design tokens
figma_setup_design_tokens({
  tokens: {
    primary: {
      Light: "#8fa0f5",
      Dark: "#6b7dd4",
      Brand: "#8fa0f5"
    }
  }
});
```

## Related Files

- [`02-audit-tools.md`](02-audit-tools.md) - UI/UX audit and parity checking
- [`06-design-system.md`](06-design-system.md) - Design token management
