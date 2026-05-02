# Plan Archive Skill

This skill provides a slash command `/plan-archive` to archive old plan files from `agentic/plan/` to `agentic/plan/archive/`, keeping only today's files in the main directory.

## Overview

The Plan Archive skill automates the process of organizing plan files by:
1. Scanning the `agentic/plan/` directory for all `.md` files
2. Identifying files not generated today (based on `YYYYMMDD` date prefix)
3. Moving old files to `agentic/plan/archive/`
4. Preserving special files like `PLAN_INDEX.md` and `README*.md`

## Slash Command

### `/plan-archive`

Archives old plan files, keeping only today's files in the main directory.

**Usage:**
```
/plan-archive [--dry-run] [--force] [--plan-dir PATH]
```

**Options:**
- `--dry-run` - Show what would be archived without moving files
- `--force` - Force archive without confirmation prompt
- `--plan-dir` - Custom plan directory path (default: `agentic/plan`)

**Example:**
```
/plan-archive --dry-run
/plan-archive --force
```

## Architecture

The skill uses the existing agentic function at `agentic/functions/plan/archive_plans.py`:

```
agentic/functions/plan/
├── __init__.py              # Package entry point
├── archive_plans.py         # Main orchestrator (CLI)
└── tasks/
    ├── __init__.py
    ├── plan_scan_task.py    # Scan logic
    └── plan_archive_task.py # Archive logic
```

## Integration

### As a Slash Command

The skill is automatically available when the `.roo/skills/plan-archive` directory is present.

### As a Python Function

```python
from agentic.functions.plan.archive_plans import PlanArchiveOrchestrator

# Create orchestrator
orchestrator = PlanArchiveOrchestrator()

# Run archive
orchestrator.run(["--force"])
```

### With Custom Plan Directory

```python
orchestrator = PlanArchiveOrchestrator(plan_dir="/path/to/plans")
orchestrator.run(["--force"])
```

## Behavior

### Files Archived

- All `.md` files matching `YYYYMMDD_HHMMSS_*.md` pattern
- Files with date prefix older than today
- Non-special files (excludes `PLAN_INDEX.md`, `README*.md`)

### Files Preserved

- Files with today's date prefix (`YYYYMMDD`)
- `PLAN_INDEX.md` - Directory index file
- `README*.md` - Documentation files
- Non-`.md` files (`.log`, `.py`, `.svg`, etc.)

### Archive Directory

- Location: `agentic/plan/archive/`
- Auto-created if doesn't exist
- Preserves original filenames

## Output Format

### Dry Run Output

```
============================================================
[DRY RUN] Plan Archive Summary
============================================================
Today's files to KEEP: 59
  ✓ 20260424_000000_api_test_coverage.md
  ✓ 20260424_142200_plan_naming_compliance_remediation.md
  ...

Old files to ARCHIVE: 98
  → 20260214_000000_plan_jwt_v2_refactor.md
  → 20260215_000000_sqlmodel_migration_plan.md
  ...
============================================================
```

### Archive Results Output

```
============================================================
Archive Results
============================================================
Total processed: 98
Success: 98
  ✓ 20260214_000000_plan_jwt_v2_refactor.md
  ✓ 20260215_000000_sqlmodel_migration_plan.md
  ...
============================================================
```

## Configuration

### Logging

The skill uses Python's logging module with the `agentic.plan` logger namespace.

**Log Levels:**
- `DEBUG` - Detailed operation details
- `INFO` - Operation progress and results
- `WARNING` - Non-critical issues
- `ERROR` - Operation failures

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLAN_ARCHIVE_DIR` | `agentic/plan/archive` | Archive directory path |
| `PLAN_DIR` | `agentic/plan` | Source plan directory |

## Troubleshooting

### Permission Denied

Ensure the user has write permissions for both source and archive directories:
```bash
chmod -R u+w agentic/plan/
```

### Archive Directory Not Created

Check that the parent directory exists and is writable:
```bash
ls -la agentic/plan/
```

### Files Not Archived

Verify files match the expected pattern:
- Must be `.md` files
- Must have `YYYYMMDD_HHMMSS_*.md` naming
- Date prefix must be older than today

## Best Practices

1. **Run Regularly**: Archive old plans weekly or after major milestones
2. **Review Before Force**: Run `--dry-run` first to preview changes
3. **Check Archive**: Verify archived files in `agentic/plan/archive/`
4. **Update Index**: Update `PLAN_INDEX.md` after archiving

## Related Skills

- [`agentic/functions/plan/`](agentic/functions/plan/) - Plan management functions
- [`agentic/plan/`](agentic/plan/) - Plan file directory
- [`agentic/functions/git/`](agentic/functions/git/) - Git operations

## License

Part of the Torro Agentic Coding Standards ecosystem.
