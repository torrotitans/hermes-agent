# OSI Converters Reference

## Overview

OSI converters translate between the OSI semantic model format and specific vendor implementations. This enables teams to author a semantic model once in OSI format and generate vendor-specific representations automatically.

## Hub-and-Spoke Architecture

OSI converters follow a **hub-and-spoke** model:

```
                ┌─────────────┐
                │  Snowflake  │
                └──────┬──────┘
                       │
┌─────────────┐    ┌───┴───┐    ┌─────────────┐
│     dbt     ├────┤  OSI  ├────┤  Salesforce │
└─────────────┘    └───┬───┘    └─────────────┘
                       │
                ┌──────┴──────┐
                │  Databricks │
                └─────────────┘
```

### Efficiency Comparison

| Approach | Converter Count |
|----------|----------------|
| Point-to-Point | N × (N-1) |
| OSI Hub-and-Spoke | 2 × N |

For 4 vendors:
- Point-to-point: 4 × 3 = 12 converters
- OSI: 2 × 4 = 8 converters

## Converter Responsibilities

### Export (OSI → Vendor)

Read an OSI semantic model and produce vendor-specific representation:

- OSI → Snowflake semantic model definition
- OSI → dbt `semantic_models` YAML
- OSI → Tableau data source / Salesforce semantic layer
- OSI → Databricks semantic layer definition

### Import (Vendor → OSI)

Read vendor-specific semantic model and produce valid OSI model:

- Parse vendor format
- Map to OSI core constructs
- Preserve vendor metadata in `custom_extensions`
- Validate against OSI schema

## Supported Vendors

| Vendor | Description |
|--------|-------------|
| `SNOWFLAKE` | Snowflake semantic model |
| `SALESFORCE` | Salesforce / Tableau semantic layer |
| `DBT` | dbt semantic models |
| `DATABRICKS` | Databricks semantic layer |

## Mapping Core Constructs

### Semantic Model Mapping

| OSI Field | Vendor Equivalent |
|-----------|------------------|
| `name` | Model/project name |
| `description` | Description field |
| `ai_context` | AI annotations (if supported) |
| `datasets` | Tables/entities |
| `relationships` | Joins/associations |
| `metrics` | Measures/calculations |
| `custom_extensions` | Extract matching vendor |

### Dataset Mapping

| OSI Field | Vendor Equivalent |
|-----------|------------------|
| `name` | Table/entity name |
| `source` | Parse `database.schema.table` |
| `primary_key` | Primary key constraint |
| `unique_keys` | Unique constraints |
| `fields` | Columns |
| `ai_context` | Semantic annotations |
| `custom_extensions` | Vendor metadata |

### Field Mapping

| OSI Field | Vendor Equivalent |
|-----------|------------------|
| `name` | Column name |
| `expression.dialects` | Select matching dialect |
| `dimension.is_time` | Time dimension marker |
| `ai_context` | Column description |
| `custom_extensions` | Column metadata |

### Relationship Mapping

| OSI Field | Vendor Equivalent |
|-----------|------------------|
| `name` | Relationship/join name |
| `from` | Source table |
| `to` | Target table |
| `from_columns` | Foreign key columns |
| `to_columns` | Referenced columns |
| `ai_context` | Join description |

### Metric Mapping

| OSI Field | Vendor Equivalent |
|-----------|------------------|
| `name` | Measure name |
| `expression.dialects` | Select matching dialect |
| `description` | Measure description |
| `ai_context` | Business terms |
| `custom_extensions` | Measure metadata |

## Dialect Selection Logic

Converters implement a fallback chain for dialect selection:

```
1. Prefer vendor-specific dialect (e.g., SNOWFLAKE)
2. Fall back to ANSI_SQL
3. Error if neither available
```

### Example

```yaml
expression:
  dialects:
    - dialect: ANSI_SQL
      expression: order_date
    - dialect: SNOWFLAKE
      expression: ORDER_DATE
```

For Snowflake export: Use `SNOWFLAKE` dialect
For other vendors: Use `ANSI_SQL` dialect

## Writing a Converter

### Step-by-Step Guide

1. **Validate Input**
   - Use OSI JSON Schema
   - Run validation script
   - Ensure valid OSI model before conversion

2. **Parse OSI Model**
   - Load YAML file
   - Iterate over `semantic_model` entries
   - Extract name, description, ai_context

3. **Map Datasets**
   - Translate `name`, `source`, `primary_key`
   - Parse `source` into catalog/schema/table
   - Map fields to columns

4. **Map Fields with Dialect Selection**
   - Select dialect matching target vendor
   - Implement fallback to ANSI_SQL
   - Log warnings for missing dialects

5. **Map Relationships**
   - Translate to vendor join syntax
   - Preserve composite key ordering
   - Validate column counts match

6. **Map Metrics**
   - Select appropriate dialect
   - Resolve dataset references
   - Generate vendor measure syntax

7. **Apply Custom Extensions**
   - Extract entries matching target vendor
   - Apply vendor-specific settings
   - Preserve other vendors for round-tripping

8. **Validate Output**
   - Run vendor validation tools
   - Verify generated model is valid

### Handling Edge Cases

| Scenario | Recommended Approach |
|----------|---------------------|
| Missing vendor dialect | Fall back to ANSI_SQL; log warning |
| Composite primary keys | Ensure vendor supports composite keys |
| Cross-dataset metrics | Validate referenced datasets exist |
| Unknown custom extension | Preserve for round-tripping |
| AI context unsupported | Store in custom_extension |

## Round-Trip Fidelity

A well-implemented converter pair preserves information:

```
Vendor A model → [Import] → OSI model → [Export] → Vendor A model
```

### Preservation Rules

1. **Never Discard Silently**
   - Store vendor-specific attributes in `custom_extensions`
   - Preserve all vendor extensions

2. **Preserve Field Ordering**
   - Some vendors are declaration-order sensitive
   - Maintain original order where possible

3. **Preserve All Extensions**
   - Keep extensions for all vendors
   - Allows multi-vendor metadata in single OSI model

## Example Conversion Flow

Given TPC-DS semantic model, Snowflake export:

1. Read `tpcds_retail_model` semantic model
2. Create Snowflake model with same name
3. Map datasets to Snowflake table references
4. Select `ANSI_SQL` dialect for each field
5. Translate relationships to Snowflake joins
6. Translate metrics to Snowflake measures
7. Extract `SALESFORCE` and `DBT` extensions (preserve)
8. Validate generated Snowflake model

## Contributing a New Converter

To add support for a new vendor:

1. Add vendor to `vendors` enum in core spec
2. Define custom extension schema for vendor
3. Implement export converter (OSI → Vendor)
4. Implement import converter (Vendor → OSI)
5. Add tests using TPC-DS example model
6. Document limitations or unsupported constructs

## Validation Script

Use the OSI validation script to verify models:

```bash
python3 validation/validate.py path/to/osi-model.yaml
```

This validates against the JSON Schema and checks:
- Required fields present
- Dialect availability
- Relationship column counts
- Source format validity
