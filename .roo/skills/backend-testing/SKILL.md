---
name: backend-testing
description: Define testing, validation, and reliability standards for the Torro backend ecosystem including TDD, test data management, and real-world validation
---

# Backend Testing & Validation Skill

This skill defines the core testing, validation, and reliability standards for the Torro backend ecosystem.

## When to use
- When creating new unit tests for API endpoints or database operations
- When setting up test data for integration tests
- When running the test suite
- When validating UI functionality with browser testing
- When implementing test-driven development workflows

## When NOT to use
- For architecture/layering guidance (use `backend-architecture` skill instead)
- For coding standards/naming (use `backend-coding-standards` skill instead)
- For security/dependency management (use `backend-operations` skill instead)

## Inputs required
- Module or component to test
- Test type (unit, integration, e2e)
- Service dependencies (if testing against real services)

## Workflow

### 1. Test-Driven Reliability (TDD)
Ensure robust and reliable code through comprehensive testing practices.

- **Virtual Environment Enforcement:** All local development and testing MUST be performed within a dedicated Python virtual environment named **`.DEV`** or **`UAT`**. The test runner (`tests/main.py`) automatically detects and switches to `.DEV`.
- **Mandatory Unit Testing:** Every new feature, logic branch, or API endpoint MUST be accompanied by an automated unit test.
- **Global API Coverage:** Every service directory in `/engine/api` MUST be covered by at least one unit test.
- **Real-First Strategy:** Tests MUST prioritize executing against **REAL** running services (PostgreSQL, Redis, Airflow, LDAP, etc.).
- **No Skipped Tests:** Every test MUST strictly result in a **PASS** or **FAIL**. Skip decorators (e.g., `@unittest.skip`) are prohibited.

### 2. Test Data Management
Maintain clean, isolated, and standardized test data.

- **Dedicated Test Data:** Hardcoded data dictionaries or large payloads in test files are strictly prohibited.
- **Storage:** All test datasets MUST be stored in `/assets/test_data/` and organized by component.
- **Format:** Use standard formats (JSON, CSV) and load dynamically via helper methods.
- **Business Cases:** High-level business validation scenarios must be documented in `/assets/test_data/ui_business_case/`.

### 3. Test Infrastructure & Reporting
Ensure consistent test execution and clear reporting.

- **Entry Point:** `tests/main.py` is the CLI entry point for running tests. When an agent is asked to "run tests", they MUST invoke `python3 tests/main.py` or `bash platform/scripts/run-tests.sh`, NOT pytest directly.
- **Isolated Reporting:** Test logs must be stored in `/logs/tests/reports/log/`.
- **Structured Output:** The final test report MUST follow a structured table format, explicitly listing every service/test with its status and service mode (Real vs Mock).
- **Test Logging:** All test runs MUST output to `logs/tests/test_run_YYYYMMDD_HHMMSS.log` for audit trails.

**Test Report Structure:**
1. **Test Summary:** Overall status (e.g., `✅ ALL PASSED` or `⚠️ 28/33 PASSED`)
2. **Services Tested:** List infrastructure dependencies with Real/Mock status
3. **Database & Connectivity Verification:** Dedicated sections for service connectivity
4. **Business User Journey & UI Functionality:** Table mapping UI pages to backend services
5. **Individual Test Results Table:** Each test with #, Name, Module, Status, Service Mode
6. **Diagnostics & Logs:** Links to detailed engineering logs

### 4. Real-World Validation
Validate functionality in realistic environments.

- **Mandatory Browser Verification:** For all UI-related tasks, Agents MUST verify functionality by running the application in a real browser using the `browser_subagent` tool.
- **Browser Verification Checklist:**
  - Successful page load (HTTP 200)
  - Absence of critical console errors
  - Basic interactivity (e.g., Login flow)
  - Screenshots or recordings preserved as artifacts

### 5. Test Infrastructure Architecture
- **Entry Point:** `tests/main.py` is the CLI entry point for running tests. It handles logging, environment setup, and delegates to pytest or `run-tests.sh`.
- **Canonical Test Structure:**
  - `tests/unit/domain`: Pure domain/database/util unit verification.
  - `tests/unit/application`: Application/API-layer unit verification.
  - `tests/integration`: Real infra boundary and cross-component verification.
  - `tests/contract`: External API/schema compatibility verification.
  - `tests/e2e`: Full workflow/UI verification.
  - `tests/fixtures`: Shared infrastructure mocks, factories, and test data helpers.
- **Shared Infrastructure:** Reusable base classes and global test mocks belong under `tests/fixtures/infra` (e.g., `BaseApiTest`, global mock wiring).
- **Separation of Concerns:** Entry (`tests/main.py`) vs reusable fixtures/helpers (`tests/fixtures/**`) must remain distinct.

## Examples

**Correct Test Data Loading:**
```python
import json
from pathlib import Path

def _load_test_data(filename: str) -> dict:
    """FN:_load_test_data Load test data from assets."""
    test_data_path = Path("/assets/test_data/auth") / filename
    with open(test_data_path, "r") as f:
        return json.load(f)

def test_login_success():
    """FN:test_login_success Test successful login flow."""
    test_data = _load_test_data("valid_credentials.json")
    # Test implementation
```

**Correct Test Runner Invocation:**
```bash
# Run full test suite
python3 tests/main.py

# Run with PR check (creates temporary UAT environment)
python3 tests/main.py --pr-check

# Run specific test category
bash platform/scripts/run-tests.sh unit
```

**Correct Test Report Format:**
```markdown
# Test Execution Report

## Summary
✅ ALL PASSED (33/33)

## Services Tested
| Service | Status | Mode |
|---------|--------|------|
| PostgreSQL 17 | ✅ PASS | Real |
| Redis | ✅ PASS | Real |
| LDAP | ✅ PASS | Real |
| Airflow | ⚠️ SKIP | Mock |

## Individual Results
| # | Test Name | Module | Status | Service Mode |
|---|-----------|--------|--------|--------------|
| 1 | test_create_user | auth | ✅ PASS | Real (PostgreSQL) |
| 2 | test_login_flow | auth | ✅ PASS | Real (LDAP) |
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Test uses hardcoded data | Move data to `/assets/test_data/` and load dynamically |
| Test uses `pytest` directly | Use `python3 tests/main.py` or `bash platform/scripts/run-tests.sh` |
| Test skipped with `@skip` | Remove skip decorator; test must PASS or FAIL |
| No test coverage for API | Create unit test in `tests/unit/domain/` or `tests/unit/application/` |
| UI test without browser verification | Use `browser_subagent` to verify in real browser |
| Test environment not isolated | Ensure `.DEV` or `UAT` virtual environment is used |
