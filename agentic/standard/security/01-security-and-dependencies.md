# Security & Dependency Management

## Dependency Single Source of Truth
- **Authoritative List**: `requirements.txt` is the only authoritative list.
- **Vulnerability Scanning**: Must pass security scanning with NO high/critical vulnerabilities.
- **Version Pinning**: Pin all production dependencies.

## CVE Verification Format
Every package MUST have an inline comment:
- `# Mitigates High CVE-YYYY-XXXX (Month Year)`
- `# Verified secure, no active CVEs (Month Year)`

## Zero Downgrade Policy
Dependencies MUST NEVER be downgraded to mitigate vulnerabilities; resolve by **upgrading** forward.

## Python Version Requirement
**Python 3.12 or higher** is MANDATORY for all development and testing environments.
