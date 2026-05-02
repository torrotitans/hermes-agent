---
name: agentic-task-planning
description: Create structured agentic task plans with phase breakdown, progress tracking, and test validation. Saves plans to /agentic/plan/ with UTC timestamp format. USE FOR: multi-step agentic workflows, task decomposition, progress tracking, test-driven development planning, 7B model optimization.
---

# Agentic Task Planning Skill

## When to Use
- Planning complex multi-step agentic workflows
- Breaking down tasks for 7B parameter models
- Tracking progress across phases with checkpoint validation
- Creating auditable task documentation with test coverage

## When NOT to Use
- Simple single-step tasks (use direct implementation)
- Tasks that don't require test validation
- Quick exploratory work without defined phases

## Inputs Required
- Task description or objective
- Expected complexity (token estimate)
- Test coverage requirements

## Workflow

### 1. Create Plan Directory Structure
Ensure the plan will be saved to `/agentic/plan/` with the format: `YYYYMMDD_HHMMSS_<task_name>.md`

### 2. Define Phases (1M Token Budget Each)
Break the task into phases, where each phase:
- Has a clear objective and deliverable
- Can be completed within ~1M tokens
- Includes entry/exit criteria
- Has associated test modules

### 3. Decompose Tasks for 7B Models
Each task must be broken into subtasks that:
- Take ~5 minutes for a 7B model to complete
- Have explicit input/output specifications
- Include validation criteria
- Are atomic and testable

### 4. Add Progress Tracking
Use checkbox format for all tasks and phases:
- `[ ]` for pending items
- `[x]` for completed items

### 5. Include Test Modules
Each phase must have:
- Corresponding test file in `tests/`
- Mock data in `assets/test_data/`
- Clear pass/fail criteria

### 6. Review conftest.py Updates
After task completion, review `tests/conftest.py` for updates needed in:
- API test fixtures
- UI test fixtures
- Backend test fixtures
- Infrastructure connectivity tests

## Output Format

Plans must be saved to `/agentic/plan/` with filename format:
```
YYYYMMDD_HHMMSS_<task_name>.md
```

Example structure:
```markdown
# Task: <Task Name>

## Phase 1: <Phase Name>
- [ ] Subtask 1.1
- [ ] Subtask 1.2
- [ ] Subtask 1.3

### Test Module
- File: `tests/test_<phase_name>.py`
- Mock Data: `assets/test_data/<phase_name>_data.json`

## Phase 2: <Phase Name>
...
```

## Examples

See [`references/EXAMPLE_PLAN.md`](references/EXAMPLE_PLAN.md) for a complete example plan.

## Troubleshooting

### Task Too Complex for 7B Model
- Further decompose subtasks into smaller units
- Add more explicit input/output examples
- Include schema definitions for data structures

### Phase Exceeds Token Budget
- Split the phase into two separate phases
- Move detailed specifications to reference files
- Use progressive disclosure for complex documentation

## Linked Files
- [`references/EXAMPLE_PLAN.md`](references/EXAMPLE_PLAN.md) - Example task plan format
- [`references/TASK_SCHEMA.md`](references/TASK_SCHEMA.md) - Task decomposition schema
- [`scripts/validate_plan.sh`](scripts/validate_plan.sh) - Plan format validation script
