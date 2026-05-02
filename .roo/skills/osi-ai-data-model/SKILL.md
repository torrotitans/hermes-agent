---
name: osi-ai-data-model
description: Work with OSI (Open Semantic Interchange) AI data models including creating, validating, and converting semantic models between OSI format and vendor-specific formats (Snowflake, dbt, Salesforce, Databricks). USE FOR: semantic model, OSI model, AI data model, semantic layer, data analytics model, BI semantic model, metric definitions, dataset relationships, AI context annotations, vendor conversion, Snowflake semantic model, dbt semantic model, Salesforce semantic layer, Databricks semantic layer.
---

# OSI AI Data Model Skill

## When to Use

Use this skill when you need to:
- Create or edit OSI-compliant semantic models
- Validate OSI model structure against the specification
- Convert between OSI format and vendor-specific formats
- Define datasets, relationships, metrics, and fields for AI-driven analytics
- Add AI context annotations for LLM-powered data exploration

## When NOT to Use

- For raw SQL query writing (use sqlmodel skill instead)
- For database schema design without semantic layer requirements
- For ETL/ELT pipeline configuration

## Core Concepts

### OSI Semantic Model Structure

The OSI specification defines a standard format for semantic models:

1. **Semantic Model** - Top-level container with name, description, AI context
2. **Datasets** - Logical tables (fact/dimension) with fields and constraints
3. **Relationships** - Foreign key connections between datasets
4. **Metrics** - Aggregate expressions with multi-dialect support
5. **Custom Extensions** - Vendor-specific metadata

### Supported Vendors

| Vendor | Description |
|--------|-------------|
| `SNOWFLAKE` | Snowflake semantic model |
| `DBT` | dbt semantic models YAML |
| `SALESFORCE` | Salesforce/Tableau semantic layer |
| `DATABRICKS` | Databricks semantic layer |

## Workflow

### 1. Create OSI Semantic Model

Create a new OSI-compliant semantic model:

1. Define the top-level `semantic_model` with name and description
2. Add `ai_context` for AI agent instructions
3. Define `datasets` with fields, primary keys, and unique keys
4. Define `relationships` between datasets
5. Define `metrics` with multi-dialect expressions
6. Add `custom_extensions` for vendor-specific metadata

### 2. Validate OSI Model

Validate the model structure:

1. Check required fields (name, datasets)
2. Validate field expressions have dialect definitions
3. Verify relationship column counts match
4. Ensure metric expressions reference valid datasets

### 3. Convert to Vendor Format

Export OSI model to vendor-specific format:

1. Select target vendor (Snowflake, dbt, etc.)
2. Map OSI constructs to vendor equivalents
3. Apply vendor-specific dialect for expressions
4. Extract relevant custom extensions

### 4. Import from Vendor Format

Import vendor model to OSI format:

1. Parse vendor-specific format
2. Map to OSI core constructs
3. Preserve vendor metadata in custom_extensions
4. Validate against OSI schema

## Files

- [references/osi-spec.md](references/osi-spec.md) - Core specification details
- [references/osi-converters.md](references/osi-converters.md) - Converter architecture
- [assets/osi-example.yaml](assets/osi-example.yaml) - Example semantic model

## Examples

### Basic Semantic Model

```yaml
semantic_model:
  - name: sales_analytics
    description: Sales and customer analytics model
    ai_context:
      instructions: "Use this model for sales analysis"
    datasets:
      - name: orders
        source: sales.public.orders
        primary_key: [order_id]
        fields:
          - name: order_id
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: order_id
          - name: amount
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: amount
    metrics:
      - name: total_revenue
        expression:
          dialects:
            - dialect: ANSI_SQL
              expression: SUM(orders.amount)
```

### Multi-Dialect Metric

```yaml
metrics:
  - name: customer_lifetime_value
    expression:
      dialects:
        - dialect: ANSI_SQL
          expression: SUM(orders.amount) / COUNT(DISTINCT customers.id)
        - dialect: SNOWFLAKE
          expression: SUM(orders.amount) / COUNT(DISTINCT customers.id)
    description: Customer lifetime value
```

## Troubleshooting

### Missing Dialect

If a metric/field lacks the target vendor dialect:
1. Fall back to ANSI_SQL
2. Log a warning about the missing dialect

### Relationship Column Mismatch

If relationship `from_columns` and `to_columns` counts differ:
1. This is a validation error
2. Ensure both arrays have the same length

### Invalid Source Reference

If dataset `source` cannot be parsed:
1. Expected format: `database.schema.table`
2. Check for missing components or typos
