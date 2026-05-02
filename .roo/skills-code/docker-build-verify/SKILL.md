---
name: docker-build-verify
description: Verify Docker-based builds for frontend and backend components. USE FOR: docker build verification, containerized build testing, pre-commit Docker checks, validate npm install and pip install in isolated containers, run /build-check slash command. DO NOT USE FOR: Docker image deployment, Docker registry operations, Kubernetes orchestration.
---

# Docker Build Verification Skill

## Slash Command

Use `/build-check` to run Docker build verification for frontend and backend components.

## When to Use
- Before committing UI/backend code changes
- Before running the full test suite
- As a pre-commit verification step
- When switching branches to verify builds work in isolated containers
- When troubleshooting build failures that only occur in CI/CD

## When NOT to Use
- For Docker image deployment (use kubernetes-deploy or docker-container skill)
- For Docker registry operations (use docker-registry skill)
- For local development without Docker (use standard npm/pip commands)

## Prerequisites
- Docker CLI installed and accessible in PATH
- Docker daemon running and accessible
- Project root directory with `scripts/docker-build-verify.sh`

## Workflow

### 1. Run Verification Script

```bash
# Verify both frontend and backend (default)
bash scripts/docker-build-verify.sh --all

# Verify only frontend
bash scripts/docker-build-verify.sh --frontend

# Verify only backend
bash scripts/docker-build-verify.sh --backend
```

### 2. Frontend Docker Build

The frontend verification uses `node:22-alpine` in an isolated container:

```bash
docker run --rm \
    -v "$(pwd):/app" \
    node:22-alpine \
    sh -c "cd /app/UI && npm ci --no-audit --no-fund && npm run build"
```

**Expected Output:**
- `npm ci` completes successfully (installs dependencies from package-lock.json)
- `npm run build` completes with zero warnings and exit code 0
- `.next/` directory is created with valid build output

### 3. Backend Docker Build

The backend verification uses `python:3.12-slim` in an isolated container:

```bash
docker run --rm \
    -v "$(pwd):/app" \
    python:3.12-slim \
    sh -c "cd /app && apt-get update -qq && apt-get install -y --no-install-recommends libpq-dev gcc && pip install --no-cache-dir -r requirements.txt"
```

**Expected Output:**
- `apt-get update` and `apt-get install` complete successfully
- `pip install` completes with zero errors
- All dependencies in `requirements.txt` are installable

### 4. Verify Results

| Result | Action |
|--------|--------|
| All checks PASSED | Proceed with commit or test execution |
| Frontend FAILED | Fix UI build issues, re-run verification |
| Backend FAILED | Fix dependency issues, re-run verification |
| Docker not available | Install Docker or skip verification |

## Integration with Test Suite

The Docker build verification is integrated into `tests/conftest.py` as a mandatory pre-test gate. The `_verify_docker_builds_for_tests()` function:

1. Checks Docker availability via `docker info`
2. Runs frontend verification in `node:22-alpine`
3. Runs backend verification in `python:3.12-slim`
4. Fails the test suite if either build fails

## Common Issues and Resolution

### npm ci Fails with ENOENT
- **Cause**: `package-lock.json` is missing or out of sync
- **Fix**: Run `npm install` locally to regenerate lockfile, then commit

### pip install Fails with Build Errors
- **Cause**: Missing system dependencies (libpq-dev, gcc)
- **Fix**: Ensure `apt-get install -y --no-install-recommends libpq-dev gcc` runs before pip install

### Docker Permission Denied
- **Cause**: Docker socket access not granted
- **Fix**: Ensure Docker Desktop is running and socket access is granted in settings

### Container Image Pull Fails
- **Cause**: Network issues or image not available
- **Fix**: Run `docker pull node:22-alpine` and `docker pull python:3.12-slim` manually

## Acceptance Criteria

- [ ] `docker-build-verify.sh --frontend` passes
- [ ] `docker-build-verify.sh --backend` passes (if backend changes included)
- [ ] All changes committed with updated `package-lock.json` and `requirements.txt`
- [ ] Test suite passes after Docker verification

## References

- [`scripts/docker-build-verify.sh`](scripts/docker-build-verify.sh:1) - Main verification script
- [`tests/conftest.py`](tests/conftest.py:405) - Test suite Docker verification hook
- [`agentic/AGENT.md`](agentic/AGENT.md:1150) - TDD and Real-World Validation standards
- [`agentic/UI.md`](agentic/UI.md:1649) - NPM Dependency Management standards
