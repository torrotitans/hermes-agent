# Task Decomposition Schema

## Overview

This schema defines the standard format for decomposing tasks into phases and subtasks optimized for 7B parameter models.

## Phase Structure

Each phase must contain:

```yaml
Phase:
  name: string (required, unique identifier)
  description: string (required, 1-2 sentences)
  token_budget: integer (default: 1000000, max recommended: 1M)
  entry_criteria: list[string] (conditions to start)
  exit_criteria: list[string] (conditions to complete)
  status: enum [pending, in_progress, completed, blocked]
  subtasks: list[Subtask]
  test_module: TestModule
```

## Subtask Structure

Each subtask must contain:

```yaml
Subtask:
  id: string (required, format: phase.subtask_number)
  description: string (required, atomic action)
  estimated_time: integer (minutes, default: 5)
  input: list[string] (required files/data)
  output: list[string] (required deliverables)
  validation: string (acceptance criteria)
  status: enum [pending, in_progress, completed, blocked]
  dependencies: list[string] (subtask IDs)
```

## Test Module Structure

Each test module must contain:

```yaml
TestModule:
  file: string (required, path to test file)
  mock_data: string (required, path to test data)
  coverage_target: float (default: 0.8)
  test_types: list[enum] (unit, integration, e2e)
```

## Progress Tracking

### Checkbox Format
- `[ ]` = Not started
- `[x]` = Completed
- `[-]` = In progress
- `[!]` = Blocked

### Status Transitions
```
pending → in_progress → completed
              ↓
           blocked
```

## Naming Conventions

### File Paths
- Use snake_case for Python files
- Use kebab-case for markdown files
- Include descriptive prefixes (test_, schema_, etc.)

### Task IDs
- Format: `<phase>.<subtask>` (e.g., "1.1", "2.3")
- Sequential numbering within phases

## Token Budget Guidelines

| Complexity | Token Count | Subtask Duration |
|------------|-------------|------------------|
| Simple     | 100K-500K   | 2-3 minutes      |
| Medium     | 500K-1M     | 5 minutes        |
| Complex    | 1M-2M       | Split into phases|

## Validation Rules

1. **Atomic Subtasks**: Each subtask must be completable in one session
2. **Clear I/O**: Input and output must be explicitly defined
3. **Testable**: Each subtask must have validation criteria
4. **Ordered Dependencies**: Dependencies must reference earlier subtasks

## Example

```yaml
Phase:
  name: "Data Validation"
  description: "Implement data validation logic"
  token_budget: 1000000
  entry_criteria:
    - "Schema defined"
    - "Test data available"
  exit_criteria:
    - "Validator passes all tests"
    - "Coverage >= 80%"
  status: in_progress
  subtasks:
    - id: "1.1"
      description: "Create validator class"
      estimated_time: 5
      input: ["schema.json"]
      output: ["validator.py"]
      validation: "Class instantiates without errors"
      status: completed
    - id: "1.2"
      description: "Add validate method"
      estimated_time: 5
      input: ["validator.py", "test_data.json"]
      output: ["validator.py"]
      validation: "Method returns boolean"
      status: pending
  test_module:
    file: "tests/test_validator.py"
    mock_data: "assets/test_data/validation_test.json"
    coverage_target: 0.8
    test_types: [unit, integration]
```

## Common Pitfalls

1. **Too Large Subtasks**: If a subtask takes >10 minutes, split it
2. **Unclear Validation**: "Works correctly" is not valid; use measurable criteria
3. **Missing Dependencies**: Always list required inputs and prerequisite subtasks
4. **No Test Coverage**: Every phase must have corresponding tests
