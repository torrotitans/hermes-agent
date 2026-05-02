# Testing & Reliability Standards

## Test-Driven Reliability (TDD)
- **Mandatory Unit Testing**: Every new feature or API endpoint must have an automated test.
- **Real-First Strategy**: Prioritize executing against **REAL** running services (PostgreSQL, Redis, Airflow, etc.).
- **No Skipped Tests**: Every test must result in a **PASS** or **FAIL**.

## Docker Build Verification
All test executions MUST include Docker-based build verification before proceeding.
```bash
bash scripts/docker-build-verify.sh --all
```

## Test Data Management
- **Storage**: Store datasets in `/assets/test_data/`.
- **Prohibition**: No hardcoded large payloads in test files.

## Executive Test Report Format
Reports must be structured for high-level readability:
1. Test Summary (Pass/Fail table).
2. Services Tested (Real vs Mock).
3. Business User Journey (UI to Backend mapping).
4. Mandatory Browser Verification (via `browser_subagent`).
