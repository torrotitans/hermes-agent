---
name: sas-lineage-extraction
description: Extract source-to-target data flows and data dictionaries from SAS estates for OpenMetadata or AGE Graph ingestion
---

# SAS Lineage Extraction

## When to Use

Use this skill when:
- Mapping source-to-target data flows in SAS code
- Extracting data dictionaries from SAS datasets
- Building lineage edges for graph databases
- Preparing metadata for OpenMetadata sync
- Creating column-level documentation

## When NOT to Use

Do NOT use this skill for:
- DATA step semantics (use sas-foundation-semantics)
- Macro resolution (use sas-macro-resolution)
- Code modernization (use sas-sql-modernization or sas-python-modernization)

## Overview

Lineage extraction identifies how data flows through SAS programs: which tables are read, which are written, and what transformations occur between them.

## Workflow

### 1. TRACE Phase

Identify all data movement:
- Input datasets: SET, MERGE, FROM clauses
- Output targets: DATA statements, CREATE TABLE
- Intermediate tables: Temporary datasets
- Include files: %INCLUDE statements

### 2. MAP Phase

Build the edge list:
- Source → Transformation → Target
- Track column-level lineage where possible
- Document transformation type (filter, join, aggregate)

### 3. CATALOG Phase

Extract column metadata:
- Column name
- Label (business description)
- Data type (CHAR, NUM, DATE)
- Length/precision
- Format/Informat

### 4. SYNC Phase

Format for ingestion:
- JSON for OpenMetadata API
- CSV for bulk import
- Cypher queries for AGE Graph

## Key Patterns

### Table-Level Edge Extraction

```sas
/* SAS Input */
DATA stg_customer;
  SET pdwa.customer;
RUN;
```

**Extracted Edge:**
```
pdwa.customer → [Ingest] → stg_customer
```

### Column Dictionary Format

```csv
table_name,column_name,label,type,length
pdwa.customer,CUST_ID,Customer ID,NUM,8
pdwa.customer,CUST_NAME,Customer Name,CHAR,100
```

### Multiple Source Tables

```sas
/* SAS: Multiple inputs */
DATA combined;
  SET table_a table_b;
RUN;
```

**Extracted Edges:**
```
table_a → [Append] → combined
table_b → [Append] → combined
```

### MERGE with BY

```sas
/* SAS: Keyed merge */
MERGE orders customers;
BY customer_id;
```

**Extracted Edges:**
```
orders → [Merge BY customer_id] → orders_with_customers
customers → [Merge BY customer_id] → orders_with_customers
```

## Output Formats

### JSON Schema (OpenMetadata)

```json
{
  "source": "pdwa.customer",
  "target": "stg_customer",
  "transformation": "ingest",
  "columns": [
    {"name": "CUST_ID", "type": "NUM", "label": "Customer ID"}
  ]
}
```

### CSV Format

```csv
source,target,transformation,columns
pdwa.customer,stg_customer,ingest,"CUST_ID,CUST_NAME"
```

### Cypher Query (AGE Graph)

```cypher
CREATE (src:Table {name: 'pdwa.customer'})
CREATE (tgt:Table {name: 'stg_customer'})
CREATE (src)-[:WRITES {script: 'stg_customer.sas'}]->(tgt)
```

## Verification Checklist

- [ ] Every target table has at least one source edge
- [ ] All input datasets (SET/MERGE) captured
- [ ] Column dictionary matches SAS catalog exactly
- [ ] JSON/CSV output follows sas2m canonical schema
- [ ] No intermediate tables missed
- [ ] Include files traced recursively

## Related Skills

- [`sas-foundation-semantics`](.roo/skills/sas-foundation-semantics/SKILL.md) - For understanding DATA step behavior
- [`apache-age-dbt-openmetadata`](.roo/skills/apache-age-dbt-openmetadata/SKILL.md) - For graph sync patterns
