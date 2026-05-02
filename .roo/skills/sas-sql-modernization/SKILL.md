---
name: sas-sql-modernization
description: Convert SAS PROC SQL and SQL-heavy DATA steps into deterministic ANSI/Trino SQL with CTEs, window functions, and explicit type casting
---

# SAS SQL Modernization

## When to Use

Use this skill when:
- Converting SAS PROC SQL to Trino/ANSI SQL
- Handling implicit remerging in SAS queries
- Translating CALCULATED keyword usage
- Converting SAS joins to ANSI JOIN syntax
- Working with GROUP BY and aggregate functions

## When NOT to Use

Do NOT use this skill for:
- DATA step logic without SQL (use sas-foundation-semantics)
- Python conversion tasks (use sas-python-modernization)
- Macro-only code (use sas-macro-resolution)

## Overview

SAS PROC SQL supports non-ANSI behaviors that must be refactored for Trino. Key differences include implicit remerging, CALCULATED keyword, and non-standard joins.

## Workflow

### 1. EXTRACT Phase

Identify SQL components:
- Source tables (FROM, JOIN)
- Derived columns (SELECT with expressions)
- Filters (WHERE, HAVING)
- Aggregations (GROUP BY)
- Output target (CREATE TABLE)

### 2. REPLACE Phase

Convert SAS-specific patterns:
- CALCULATED keyword → CTEs (WITH clause)
- Implicit joins → ANSI JOIN ... ON
- OUTER UNION CORR → UNION ALL with NULL padding

### 3. REMERGE Phase

Handle implicit remerging:
- Identify aggregate functions in SELECT
- Convert to window functions with OVER()
- Add PARTITION BY for grouped remerging

### 4. CAST Phase

Apply explicit typing:
- CAST for numeric conversions
- Date format standardization
- Handle SAS date epoch (subtract 3,653 days)

### 5. VERIFY Phase

Validate correctness:
- Compare row counts (SAS vs Trino)
- Verify aggregate parity
- Check column data types

## Key Patterns

### Implicit Remerging

```sas
/* SAS: Automatic remerge of aggregate to detail */
PROC SQL;
  CREATE TABLE high_variance AS
  SELECT Region, Sales, Sales - MEAN(Sales) as Diff
  FROM transactions;
QUIT;
```

```sql
-- Trino: Explicit window function
CREATE TABLE high_variance AS
SELECT
  Region,
  Sales,
  Sales - AVG(Sales) OVER () as Diff
FROM transactions;
```

### CALCULATED Keyword

```sas
/* SAS: Reference calculated column in WHERE */
PROC SQL;
  SELECT X * 2 as Y
  FROM T
  WHERE Y > 10;  /* CALCULATED implied */
QUIT;
```

```sql
-- Trino: Use CTE
WITH t1 AS (
  SELECT X * 2 as Y FROM T
)
SELECT * FROM t1 WHERE Y > 10;
```

### Non-Standard Joins

```sas
/* SAS: WHERE clause join */
PROC SQL;
  SELECT *
  FROM A, B
  WHERE A.x = B.x;
QUIT;
```

```sql
-- Trino: ANSI JOIN
SELECT *
FROM A
JOIN B ON A.x = B.x;
```

### RETAIN to Window Function

```sas
/* SAS: Cumulative sum with RETAIN */
DATA cumulative;
  SET sales;
  RETAIN RunningTotal 0;
  RunningTotal + Amount;
RUN;
```

```sql
-- Trino: Window function
SELECT
  *,
  SUM(Amount) OVER (
    ORDER BY TransactionDate
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as RunningTotal
FROM sales;
```

### MERGE to FULL OUTER JOIN

```sas
/* SAS: 1-to-1 merge */
MERGE A B;
BY ID;
```

```sql
-- Trino: FULL OUTER JOIN with COALESCE
SELECT
  COALESCE(A.col, B.col) as col
FROM A
FULL OUTER JOIN B ON A.id = B.id;
```

### WHERE vs IF Conversion

```sas
/* SAS: WHERE filters input, IF filters output */
DATA filtered;
  SET source;
  WHERE amount > 100;  /* Pre-PDV filter */
  IF total > 1000;     /* Post-PDV filter */
RUN;
```

```sql
-- Trino: Both as WHERE/HAVING
SELECT *
FROM source
WHERE amount > 100
HAVING total > 1000;
```

## Date Conversion

SAS uses epoch 1960-01-01, Trino uses 1970-01-01.

```sas
/* SAS: Date as integer from 1960 */
birth_date = '01JAN1990'd;
```

```sql
-- Trino: Subtract 3,653 days
SELECT DATE '1960-01-01' + INTERVAL (sas_date_int - 3653) DAY
```

## Verification Checklist

- [ ] No SELECT * used; columns are explicit
- [ ] All joins use ANSI JOIN ... ON syntax
- [ ] Implicit remerging converted to window functions
- [ ] CALCULATED references moved to CTEs
- [ ] Row counts match between SAS and Trino
- [ ] Aggregate values match (within tolerance)
- [ ] Date conversions apply 3,653-day offset
- [ ] Explicit CAST for type conversions

## Related Skills

- [`sas-foundation-semantics`](.roo/skills/sas-foundation-semantics/SKILL.md) - For DATA step semantics
- [`sas-python-modernization`](.roo/skills/sas-python-modernization/SKILL.md) - For Python conversion
- [`sas-lineage-extraction`](.roo/skills/sas-lineage-extraction/SKILL.md) - For lineage documentation
