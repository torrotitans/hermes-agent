---
name: sas-foundation-semantics
description: Parse and explain SAS execution behavior including DATA step semantics, PDV lifecycle, BY group processing, and ordering dependencies
---

# SAS Foundation Semantics

## When to Use

Use this skill when:
- Interpreting SAS DATA step runtime behavior
- Understanding PDV (Program Data Vector) lifecycle
- Analyzing ordering dependencies in SAS code
- Explaining MERGE + BY behavior
- Handling RETAIN variables and stateful logic

## When NOT to Use

Do NOT use this skill for:
- SQL conversion tasks (use sas-sql-modernization)
- Macro resolution (use sas-macro-resolution)
- Lineage extraction (use sas-lineage-extraction)

## Overview

SAS DATA step execution follows a specific lifecycle that differs from SQL. Understanding the PDV is critical for accurate migration.

## Workflow

### 1. IDENTIFY Phase

Locate key DATA step elements:
- DATA step boundaries (DATA statement to RUN)
- Input statements: SET, MERGE, BY
- RETAIN statements
- FIRST./LAST. variable usage

### 2. SIMULATE Phase

Map the Program Data Vector:
- Track variable initialization order
- Identify variables that reset each iteration
- Identify RETAIN'd variables (persist across iterations)
- Map the implicit loop: Read → Execute → Output → Return

### 3. RESOLVE Phase

Handle special SAS behaviors:
- FIRST./LAST. group logic for BY processing
- Sequential MERGE behavior (1-to-1 matching)
- Missing value propagation
- Physical sort order dependencies

### 4. DOCUMENT Phase

Annotate the program:
- Document stateful nature
- Note ordering dependencies
- Flag potential migration risks

## Key Patterns

### The RETAIN Rule

```sas
/* SAS: Variable persists across iterations */
RETAIN Total 0;
Total + Amount;
```

```sql
-- Trino: Use window function
SUM(Amount) OVER (ORDER BY Date ROWS UNBOUNDED PRECEDING)
```

### Sequential MERGE

```sas
/* SAS: 1-to-1 sequential match, NOT Cartesian */
MERGE A B;
BY ID;
```

```sql
-- Trino: FULL OUTER JOIN with COALESCE
SELECT COALESCE(A.col, B.col) as col
FROM A
FULL OUTER JOIN B ON A.id = B.id
```

### Date Conversion

SAS Epoch: 1960-01-01
Unix Epoch: 1970-01-01

**Rule**: Subtract 3,653 days when converting SAS dates to Python/SQL dates.

### FIRST./LAST. Processing

```sas
/* SAS: Group-level processing */
BY Region;
IF FIRST.Region THEN RunningTotal = 0;
```

```python
# Python: Use groupby with cumsum
df['RunningTotal'] = df.groupby('Region')['Amount'].cumsum()
```

## Verification Checklist

- [ ] PDV lifecycle correctly simulated
- [ ] RETAIN variables identified and handled
- [ ] FIRST./LAST. logic mapped correctly
- [ ] MERGE behavior documented as sequential
- [ ] Date offsets applied (3,653 days)
- [ ] Physical order dependencies noted

## Related Skills

- [`sas-macro-resolution`](.roo/skills/sas-macro-resolution/SKILL.md) - For macro variable resolution
- [`sas-sql-modernization`](.roo/skills/sas-sql-modernization/SKILL.md) - For SQL conversion
- [`sas-python-modernization`](.roo/skills/sas-python-modernization/SKILL.md) - For Python conversion
