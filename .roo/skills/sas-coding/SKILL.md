---
name: sas-coding
description: SAS coding specialist for legacy code analysis, standardization, and modernization to Python/SQL with PDV simulation, macro resolution, and validation
---

# SAS Coding Specialist

## When to Use

Use this skill when working with SAS code for:
- Understanding legacy SAS DATA step and PROC SQL behavior
- Simulating Program Data Vector (PDV) execution semantics
- Resolving macro variables and dynamic code generation
- Converting SAS to Trino SQL or Python/Pandas
- Extracting data lineage and column dictionaries
- Validating migration correctness

## When NOT to Use

Do NOT use this skill for:
- General Python or SQL development (use backend-coding-standards)
- Non-SAS data pipeline work
- Direct database operations without SAS context

## Overview

SAS2M (SAS to Modernisation) requires understanding three layers:
1. **SAS Semantics**: PDV lifecycle, macro resolution, merge behavior
2. **Standardization**: Extract contracts, lineage, quality rules
3. **Modernization**: Convert to Trino SQL or Python with validation

## Workflow

### Phase 1: Foundation Semantics

1. **IDENTIFY**: Locate DATA step boundaries, SET/MERGE/BY statements
2. **SIMULATE**: Map Program Data Vector (PDV) and RETAIN variables
3. **RESOLVE**: Handle FIRST./LAST. logic and sequential merge behavior
4. **DOCUMENT**: Annotate stateful nature and ordering dependencies

### Phase 2: Macro Resolution

1. **SCAN**: Locate macro calls (%name) and variable references (&var)
2. **EXPAND**: Simulate SAS Word Scanner for nested macros (&&var)
3. **SCOPE**: Determine Global vs Local symbol table priority
4. **ANNOTATE**: Document resolved intent before translation

### Phase 3: Lineage Extraction

1. **TRACE**: Identify input datasets (SET, MERGE) and output targets
2. **MAP**: Build edge list (Source → Transformation → Target)
3. **CATALOG**: Extract column metadata (Name, Label, Type, Length)
4. **SYNC**: Format for OpenMetadata or AGE Graph ingestion

### Phase 4: SQL Modernization

1. **EXTRACT**: Identify sources, joins, filters, derived columns
2. **REPLACE**: Swap implicit SAS SQL with ANSI CTEs
3. **REMERGE**: Convert implicit remerging to window functions
4. **CAST**: Apply explicit type casting for dates/numerics
5. **VERIFY**: Check row count and aggregate parity

### Phase 5: Python Modernization

1. **VECTORIZE**: Map DATA step iterations to Pandas vectorized ops
2. **IDENTITY**: Add Agentic Head (Identity + ELI5) to every file
3. **OPTIMIZE**: Prohibit iterrows(); use apply/map/boolean indexing
4. **TYPE**: Use Python 3.9+ type hints
5. **VERIFY**: Run pytest with 90%+ coverage

## Key Reference Files

- [`SAS.md`](assets/sas-lineage-main/agentic/SAS.md) - SAS runtime semantics
- [`AGENT.md`](assets/sas-lineage-main/agentic/AGENT.md) - Migration standards
- [`SKILLS.md`](assets/sas-lineage-main/agentic/SKILLS.md) - Skill framework

## SAS Semantic Rules

### DATA Step Lifecycle
- Implicit loop: Read Obs → Execute Logic → Output → Return to Top
- Variables reset to Missing unless RETAIN'd
- MERGE + BY is sequential (1-to-1), NOT Cartesian

### Macro Resolution
- &&VAR resolves to &VAR (two-pass scanner)
- Macros are text replacement, not runtime logic

### Date Conversion
- SAS Epoch: 1960-01-01
- Unix Epoch: 1970-01-01
- **Subtract 3,653 days** when converting

### SQL Patterns
| SAS Construct | Trino SQL Solution |
| :--- | :--- |
| Implicit Remerging | `AVG(Y) OVER (PARTITION BY X)` |
| CALCULATED alias | CTE (WITH clause) |
| WHERE joins | ANSI `JOIN ... ON` |
| RETAIN cumulative | `SUM() OVER (ORDER BY ...)` |
| MERGE 1-to-1 | `FULL OUTER JOIN` with COALESCE |

## Verification Checklist

- [ ] PDV lifecycle correctly simulated
- [ ] FIRST./LAST. logic mapped to SQL Windowing or Python state
- [ ] Date offsets applied (3,653 days)
- [ ] All & references resolved
- [ ] Macro scoping handled
- [ ] Every target has source edge
- [ ] No SELECT * in SQL
- [ ] Joins use ANSI syntax
- [ ] Row counts match SAS → Modernized
- [ ] No for loops for row transformations
- [ ] Unit tests pass
