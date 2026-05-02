# Torro Agentic Mistakes: Backend & Logic

<mistake_registry domain="Backend">
  <description>Registry of architectural and implementation mistakes in the backend and core logic layers.</description>

  <incident id="M17" severity="critical">
    <issue>Incomplete Raw SQL Purge</issue>
    <root_cause>Searched for execute() but missed text() imports for raw SQL.</root_cause>
    <prevention>MANDATORY: Use regex \btext\s*\( to audit DB directory for 100% SQLModel compliance.</prevention>
  </incident>

  <incident id="M20" severity="medium">
    <issue>CLI Panel Alignment Asymmetry</issue>
    <root_cause>Sub-panels in terminal layout had mismatched heights/padding.</root_cause>
    <prevention>All terminal panels in a shared row MUST use expand=True and Align wrappers.</prevention>
  </incident>

  <incident id="M31" severity="high">
    <issue>Function Signature Mismatch (Cascading Failures)</issue>
    <root_cause>Refactored function signature without updating all callers, leading to runtime crashes.</root_cause>
    <prevention>
      ALWAYS read function definition before fixing callers. Search for ALL usages before committing changes.
    </prevention>
  </incident>
</mistake_registry>
