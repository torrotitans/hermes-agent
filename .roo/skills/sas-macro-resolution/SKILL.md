---
name: sas-macro-resolution
description: Resolve SAS macros, %LET variables, and dynamic code generation before modernization including nested macros and symbol table scoping
---

# SAS Macro Resolution

## When to Use

Use this skill when:
- Resolving SAS macro calls (%name)
- Handling %LET variables and &var references
- Processing nested macros (&&var syntax)
- Understanding dynamic code generation
- Converting macros to Python functions or Jinja templates

## When NOT to Use

Do NOT use this skill for:
- DATA step logic conversion (use sas-foundation-semantics)
- SQL conversion tasks (use sas-sql-modernization)
- Lineage extraction (use sas-lineage-extraction)

## Overview

SAS macros are resolved at compile-time through text replacement, not at runtime. The macro processor uses symbol tables (Global and Local) to resolve variable references.

## Workflow

### 1. SCAN Phase

Locate macro elements:
- Macro calls: %MACRO_NAME
- Variable references: &VAR
- Macro definitions: %MACRO ... %MEND
- Special syntax: &&VAR (double ampersand)

### 2. EXPAND Phase

Simulate the SAS Word Scanner:
- Resolve &&VAR to &VAR (two-pass scanning)
- Process nested macro calls
- Handle quoted strings (%STR())
- Track macro execution order

### 3. SCOPE Phase

Determine symbol table priority:
- Local symbol table (current macro)
- Global symbol table (fallback)
- Handle variable shadowing correctly

### 4. ANNOTATE Phase

Document the resolved intent:
- Show final resolved code
- Note dynamic behavior
- Flag complex indirection patterns

## Key Patterns

### Double Ampersand Resolution

```sas
/* SAS: Two-pass resolution */
%LET var1 = value;
%LET varname = var1;
&&&varname  /* Resolves to: value */
```

```python
# Python: Dictionary lookup
variables = {'var1': 'value', 'varname': 'var1'}
value = variables[variables['varname']]
```

### Macro to Function Conversion

```sas
/* SAS Macro */
%MACRO calculate(total, rate);
  %let result = %eval(&total * &rate);
  &result
%MEND;
```

```python
# Python function
def calculate(total: float, rate: float) -> float:
    """FN:calculate Calculate total with rate."""
    return total * rate
```

### Macro Loop to Python Loop

```sas
/* SAS: Macro loop generating code */
%DO i = 1 %TO 3;
  sum_&i = col_&i * 2;
%END;
```

```python
# Python: Dynamic attribute assignment
for i in range(1, 4):
    setattr(result, f'sum_{i}', getattr(row, f'col_{i}') * 2)
```

### CALL SYMPUT Conversion

```sas
/* SAS: Push data value to macro variable */
CALL SYMPUT('total_count', count);
```

```python
# Python: Fetch and store
result = conn.execute(query)
total_count = result.fetchone()[0]
```

## Symbol Table Rules

1. **Local First**: Check local symbol table before global
2. **Nested Macros**: Each macro has its own local table
3. **%GLOBAL**: Explicitly declare global variables
4. **%LOCAL**: Explicitly declare local variables

## Macro Resolution Order

1. Scan for macro triggers (%)
2. Resolve && to & (first pass)
3. Resolve &VAR to value (second pass)
4. Execute macro code
5. Return resolved text

## Verification Checklist

- [ ] All & references resolved to literals or variables
- [ ] &&VAR correctly handled with two-pass resolution
- [ ] Macro scoping (Global vs Local) correctly applied
- [ ] Nested macros properly expanded
- [ ] Dynamic logic mapped to Python/SQL (not string concatenation)
- [ ] No unresolved macro references remain

## Related Skills

- [`sas-foundation-semantics`](.roo/skills/sas-foundation-semantics/SKILL.md) - For DATA step semantics
- [`sas-sql-modernization`](.roo/skills/sas-sql-modernization/SKILL.md) - For SQL conversion
- [`sas-python-modernization`](.roo/skills/sas-python-modernization/SKILL.md) - For Python conversion
