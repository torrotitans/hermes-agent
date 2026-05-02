# OSI Core Specification Reference

## Overview

The OSI (Open Semantic Interchange) specification defines a vendor-neutral, standardized format for semantic models used in AI-driven analytics and BI platforms.

**Version:** 0.1.1

**License:** Apache 2.0 (code), CC BY (specification)

## Goals

1. **Standardization** - Uniform language for semantic model definitions
2. **Extensibility** - Domain-specific extensions while maintaining compatibility
3. **Interoperability** - Exchange and reuse across AI/BI applications

## Core Constructs

### 1. Semantic Model (Top-Level Container)

The root element containing all semantic definitions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier |
| `description` | string | No | Human-readable description |
| `ai_context` | string/object | No | AI agent instructions |
| `datasets` | array | Yes | Logical datasets |
| `relationships` | array | No | Dataset connections |
| `metrics` | array | No | Aggregate measures |
| `custom_extensions` | array | No | Vendor metadata |

### 2. Datasets

Logical tables representing business entities (fact/dimension tables).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Dataset identifier |
| `source` | string | Yes | Physical table reference (e.g., `db.schema.table`) |
| `primary_key` | array | No | Primary key columns |
| `unique_keys` | array of arrays | No | Alternative unique keys |
| `description` | string | No | Human-readable description |
| `ai_context` | object | No | Synonyms, examples for AI |
| `fields` | array | No | Column definitions |
| `custom_extensions` | array | No | Vendor metadata |

#### Primary Key Examples

```yaml
# Simple primary key
primary_key: [customer_id]

# Composite primary key
primary_key: [order_id, line_number]
```

#### Unique Keys Examples

```yaml
unique_keys:
  - [email]                    # Simple unique key
  - [first_name, last_name]    # Composite unique key
```

### 3. Fields

Column-level definitions within datasets.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Field identifier |
| `expression` | object | Yes | SQL expression definition |
| `expression.dialects` | array | Yes | Multi-dialect expressions |
| `description` | string | No | Field description |
| `dimension` | object | No | Dimension properties |
| `dimension.is_time` | boolean | No | Time dimension flag |

#### Expression Format

```yaml
expression:
  dialects:
    - dialect: ANSI_SQL
      expression: order_date
    - dialect: SNOWFLAKE
      expression: ORDER_DATE
```

### 4. Relationships

Foreign key connections between datasets.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Relationship identifier |
| `from` | string | Yes | Source dataset (many side) |
| `to` | string | Yes | Target dataset (one side) |
| `from_columns` | array | Yes | Source columns |
| `to_columns` | array | Yes | Target columns |
| `ai_context` | string | No | Relationship description |

#### Example

```yaml
relationships:
  - name: orders_to_customers
    from: orders
    to: customers
    from_columns: [customer_id]
    to_columns: [id]
```

### 5. Metrics

Aggregate expressions computed over datasets.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Metric identifier |
| `expression` | object | Yes | Aggregate expression |
| `expression.dialects` | array | Yes | Multi-dialect aggregates |
| `description` | string | No | Metric description |
| `ai_context` | object | No | Synonyms for AI |

#### Metric Examples

```yaml
metrics:
  - name: total_revenue
    expression:
      dialects:
        - dialect: ANSI_SQL
          expression: SUM(orders.amount)
    description: Total revenue

  - name: customer_count
    expression:
      dialects:
        - dialect: ANSI_SQL
          expression: COUNT(DISTINCT customers.id)
    description: Total customers
```

### 6. Custom Extensions

Vendor-specific metadata preservation.

```yaml
custom_extensions:
  - vendor_name: SNOWFLAKE
    data: '{"warehouse": "ANALYTICS_WH"}'
  - vendor_name: DBT
    data: '{"project_name": "analytics", "materialized": "table"}'
```

## Supported Dialects

| Dialect | Description |
|---------|-------------|
| `ANSI_SQL` | Standard SQL |
| `SNOWFLAKE` | Snowflake SQL |
| `MDX` | Multi-Dimensional Expressions |
| `TABLEAU` | Tableau calculations |
| `DATABRICKS` | Databricks SQL |

## Supported Vendors

| Vendor | Description |
|--------|-------------|
| `COMMON` | Common extensions |
| `SNOWFLAKE` | Snowflake attributes |
| `SALESFORCE` | Salesforce/Tableau |
| `DBT` | dbt attributes |
| `DATABRICKS` | Databricks attributes |

## AI Context Structure

The `ai_context` field can be:

### Simple String

```yaml
ai_context: "orders, purchases, sales"
```

### Structured Object

```yaml
ai_context:
  instructions: "Use for sales analysis"
  synonyms:
    - "orders"
    - "purchases"
  examples:
    - "Show total sales last month"
```

### Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `instructions` | string | AI usage instructions |
| `synonyms` | array | Alternative names |
| `examples` | array | Sample questions |

## Complete Example

```yaml
semantic_model:
  - name: ecommerce_analytics
    description: E-commerce sales analytics
    ai_context:
      instructions: "Use for sales and customer analysis"

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
          - name: customer_id
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: customer_id
          - name: order_date
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: order_date
            dimension:
              is_time: true
          - name: amount
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: amount

      - name: customers
        source: sales.public.customers
        primary_key: [id]
        fields:
          - name: id
            expression:
              dialects:
                - dialect: ANSI_SQL
                  expression: id

    relationships:
      - name: orders_to_customers
        from: orders
        to: customers
        from_columns: [customer_id]
        to_columns: [id]

    metrics:
      - name: total_revenue
        expression:
          dialects:
            - dialect: ANSI_SQL
              expression: SUM(orders.amount)
        description: Total revenue
        ai_context:
          synonyms:
            - "total sales"
            - "revenue"

    custom_extensions:
      - vendor_name: SNOWFLAKE
        data: '{"warehouse": "ANALYTICS_WH"}'
```

## Validation Rules

1. **Required Fields**: `name` and `datasets` are mandatory
2. **Dialect Requirement**: Every expression must have at least one dialect
3. **Relationship Columns**: `from_columns` and `to_columns` must have same length
4. **Source Format**: Dataset source should be `database.schema.table` format
5. **Primary Key**: Must be an array (even for single column)

## Version History

- **0.1.1** (2025-12-11): Initial release
  - Core semantic model structure
  - Multi-dialect support
  - Vendor extensibility
  - AI context annotations
