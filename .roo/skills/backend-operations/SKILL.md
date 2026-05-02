---
name: backend-operations
description: Define operational, security, dependency management, and resource stewardship standards for the Torro backend ecosystem
---

# Backend Operations & Security Skill

This skill defines the core operational, security, and resource management standards for the Torro backend ecosystem.

## When to use
- When managing dependencies in `requirements.txt`
- When adding new logging statements
- When handling static assets or test data
- When optimizing resource usage (memory, connections)
- When implementing startup banners or environment detection

## When NOT to use
- For architecture/layering guidance (use `backend-architecture` skill instead)
- For coding standards/naming (use `backend-coding-standards` skill instead)
- For testing-specific guidance (use `backend-testing` skill instead)

## Inputs required
- Dependency to add/update (if managing dependencies)
- Asset type and location (if handling assets)
- Resource type (if managing connections/lifecycle)

## Workflow

### 1. Security & Dependency Management
Ensure a secure and reliable dependency supply chain.

- **Dependency Single Source of Truth (MANDATORY):** `requirements.txt` is the **only** authoritative dependency list for Python in this repo. Auxiliary requirements files (e.g., `requirements-dbt.txt`) must be merged and removed.
- **Vulnerability Scanning:** All dependencies must pass Sonar or equivalent security scanning with NO high or critical vulnerabilities.
- **Version Pinning & CVE Verification:** Pin all production dependencies to specific versions in `platform/requirements.txt`. Every package MUST have an inline comment verifying its vulnerability status:
  - Format 1 (Mitigated): `# Mitigates High CVE-YYYY-XXXX (Month Year)`
  - Format 2 (Safe): `# Verified secure, no active CVEs (Month Year)`
- **No Downgrades:** Dependencies MUST NEVER be downgraded to mitigate security vulnerabilities. Upgrade forward or adopt secure alternatives.
- **Dependency Conflicts:** Prioritize security patches over feature updates. Exceptions are permitted only if strictly required by core infrastructure services (e.g., Airflow, PostgreSQL).

**Minimum Secure Versions (as of 2026-01):**
- Flask ≥ 3.0.3
- Werkzeug ≥ 3.1.5
- Jinja2 ≥ 3.1.6
- cryptography ≥ 46.0.3
- requests ≥ 2.32.4
- urllib3 ≥ 2.6.3
- SQLAlchemy ≥ 2.0.46

### 2. Unified Observability & Structured Logging
Maintain comprehensive and traceable system logs.

- **Mandatory Prefix:** Every log statement MUST start with the `FN:functionName` prefix to ensure immediate traceability (e.g., `logger.debug("FN:getAuthInfo Info:...")`).
- **No Print Statements:** The `print()` function is strictly prohibited for system output. Always use `logger.debug` for granular tracing.
- **Traceability:** Every log entry should include relevant metadata: unique request IDs, timestamps, and the specific functional scope.

**Log Levels:**
| Level | Value | Usage |
| :--- | :--- | :--- |
| `DEBUG` | 10 | Granular data for developer troubleshooting |
| `INFO` | 20 | Confirmation of high-level system milestones |
| `WARNING` | 30 | Indications of unexpected behavior that doesn't break the system |
| `ERROR` | 40 | Failure of a specific operation requiring investigation |

### 3. Unified Local Artifact & Log Management
Ensure clean repository state and structured artifact storage.

- **Isolated Artifacts:** All runtime-generated artifacts (application logs, error dumps, test reports, exported CSVs) MUST be directed to the root `/logs` directory.
- **Clean Repository State:** The `.gitignore` MUST strictly exclude the `/logs` directory. Agents MUST verify that their actions do not introduce local path noise.
- **Structured Output:** Logs should be sub-divided into logical categories (e.g., `/logs/app`, `/logs/tests`, `/logs/errors`) to facilitate efficient filtering and analysis.

### 4. Mandatory Asset & Resource Centralization
Centralize and manage static assets securely.

- **Centralization:** All static assets (certificates, templates, config JSONs, and test datasets) MUST live under `/assets`.
- **Test Data:** All test datasets MUST be stored in `/assets/test_data/` and organized by component or domain.
- **Path Safety:** Never hardcode absolute paths. Always resolve via `PROJECT_ROOT` helpers (e.g., `get_resource`).
- **Discoverability:** Each major asset subfolder MUST include a concise `README.md` explaining purpose and contents.
- **RAG Alignment:** If assets support API/DB/UI flows, reference the related service topology in the README to guide agents.

### 5. Resource Stewardship
Optimize algorithmic efficiency and resource lifecycle management.

- **Algorithmic Efficiency:** Prioritize optimal Big O complexity. Avoid redundant iterations and unnecessary deep-copying of large data structures.
- **Memory Management:** Implement lazy loading for heavy assets. Use generators or streaming for processing large datasets to minimize the memory footprint.
- **Connection Lifecycle:** Ensure all external resources (database handles, network sockets, file pointers) are managed via context managers (e.g., `with` statements) to prevent leaks.

### 6. Startup & Identity
Ensure clear system readiness indicators.

- **Banner Requirement:** All entry points (main scripts) MUST log a standard ASCII banner at startup to indicate the system is ready. (Exception: `tests/main.py`).
- **Environment Display:** The banner MUST display the current version and environment (DEV/PROD).
- **Confidence Check:** If the banner doesn't show, the system is considered "DOWN".

## Examples

**Correct Logging Pattern:**
```python
logger.debug("FN:getAuthInfo Info:Fetching authentication token for user_id=%s", user_id)
logger.info("FN:process_request Request processed successfully in %dms", elapsed_ms)
logger.error("FN:save_data Failed to save data: %s", str(error))
```

**Correct Asset Loading Pattern:**
```python
from engine.config import get_resource

# Load asset via PROJECT_ROOT helper
cert_path = get_resource("certs/ca_cert.pem")
with open(cert_path, "r") as f:
    cert_data = f.read()
```

**Correct Connection Management:**
```python
# Use context manager for connection lifecycle
with database.get_connection() as conn:
    result = conn.execute(query)
# Connection automatically closed
```

**Correct Startup Banner:**
```python
def print_banner():
    """FN:print_banner Display system startup banner."""
    banner = """
    ╔════════════════════════════════════════════╗
    ║         TORRO DATA PLATFORM                ║
    ║         Version: 2.0.0  |  ENV: DEV       ║
    ╚════════════════════════════════════════════╝
    """
    logger.info(banner)
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Dependency has CVE | Upgrade to secure version; add CVE comment to `requirements.txt` |
| Print statement found | Replace with `logger.debug()` with `FN:` prefix |
| Hardcoded absolute path | Use `get_resource()` helper with relative path from `/assets` |
| Missing startup banner | Add ASCII banner to entry point; display version and environment |
| Connection not closed | Wrap in `with` statement or use context manager |
| Log missing `FN:` prefix | Add `FN:functionName` prefix to all log statements |
