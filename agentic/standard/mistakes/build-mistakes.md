# Torro Agentic Mistakes: Build & Infrastructure

<mistake_registry domain="Infrastructure">
  <description>Registry of build, deployment, and infrastructure configuration mistakes.</description>

  <incident id="M18" severity="high">
    <issue>Next.js Standalone Unstyled HTML</issue>
    <root_cause>Next.js standalone mode strips static assets; failed to copy public/static folders.</root_cause>
    <prevention>Append asset copy commands (cp -r public/static) after npm run build in standalone pipelines.</prevention>
  </incident>

  <incident id="M21" severity="high">
    <issue>Next.js Standalone Path Misconfiguration</issue>
    <root_cause>Incorrect paths for server.js and nested static assets in standalone mode.</root_cause>
    <prevention>Verify output structure (ls -la .next/standalone/) before writing build commands.</prevention>
  </incident>

  <incident id="M22" severity="critical">
    <issue>Port Conflict Blindspot (DataHub vs Airflow)</issue>
    <root_cause>Configured multiple services to use port 8080, breaking integration tests.</root_cause>
    <prevention>MANDATORY: Verify unique port allocations across docker-compose.yml and config.ini before startup.</prevention>
  </incident>

  <incident id="M30" severity="high">
    <issue>TypeScript Build Errors in Route Handlers</issue>
    <root_cause>Incorrect proxyToBackend signature and D3.js type issues.</root_cause>
    <prevention>Run npm run typecheck before committing. Use single config object for proxyToBackend.</prevention>
  </incident>

  <incident id="M33" severity="high">
    <issue>Duplicate Module Resolution Conflicts</issue>
    <root_cause>Existence of both .ts and .tsx files for the same component; TS preferred .ts (broken).</root_cause>
    <prevention>Check for duplicate .ts/.tsx files. TS defaults to .ts which may lack JSX support.</prevention>
  </incident>

  <incident id="M35" severity="critical">
    <issue>Middleware Conflicts & FSD Boundary Violations</issue>
    <root_cause>Dual middleware.ts/proxy.ts existence and shared layer depending on entities.</root_cause>
    <prevention>Consolidate middleware into a single file. Shared layer MUST NEVER depend on entities.</prevention>
  </incident>

  <incident id="M36" severity="critical">
    <issue>.gitignore Overly Broad Pattern Ignoring Source Files</issue>
    <root_cause>The pattern 'lib/' in .gitignore matches ANY directory named 'lib' anywhere in the repository. This caused UI/src/shared/lib/security/, UI/src/shared/lib/utils/, UI/src/shared/lib/validation/, UI/src/lib/, and other lib/ directories to be silently ignored by git. Files were never tracked, causing local code to diverge from remote without any git status warnings.</root_cause>
    <prevention>MANDATORY: Use anchored patterns like '/lib/' to match only root-level directories. After modifying .gitignore, run 'git status' and 'git check-ignore -v <path>' to verify files are tracked. Add git sync verification to CI/build pipeline.</prevention>
  </incident>
</mistake_registry>
