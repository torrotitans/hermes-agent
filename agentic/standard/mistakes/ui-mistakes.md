# Torro Agentic Mistakes: UI & Aesthetic

<mistake_registry domain="UI">
  <description>Registry of architectural, design, and implementation mistakes in the UI layer to prevent recurrence.</description>

  <incident id="M1" severity="low">
    <issue>Incorrect Torro Logo Vectors</issue>
    <root_cause>Used a hexagon SVG instead of the mandated 3-color rounded bars.</root_cause>
    <prevention>Refer to P18 in SKILL.md and check torro-icon.tsx first.</prevention>
  </incident>

  <incident id="M2" severity="low">
    <issue>Sidebar Icon Alignment</issue>
    <root_cause>Icons were not perfectly centered in collapsed mode due to asymmetrical padding.</root_cause>
    <prevention>Use justify-center and remove horizontal padding in collapsed sidebars.</prevention>
  </incident>

  <incident id="M3" severity="medium">
    <issue>Sidebar Roundness (Apple Liquid Glass)</issue>
    <root_cause>Used rounded-xl instead of Apple-style rounded-3xl/squircle.</root_cause>
    <prevention>Use rounded-[14px] (0.875rem) for 40px items to achieve the "squircle" effect.</prevention>
  </incident>

  <incident id="M11" severity="high">
    <issue>Border on Active State Shrinks Internal Padding</issue>
    <root_cause>Adding border to active nav items consumes padding, causing misalignment vs inactive items.</root_cause>
    <prevention>NEVER use border on active-only states if inactive has no border. Use ring-1 ring-inset instead.</prevention>
  </incident>

  <incident id="M15" severity="medium">
    <issue>Icon Reuse Confusion</issue>
    <root_cause>Using same icons for different navigation items (Shield for Policies and Tags).</root_cause>
    <prevention>HARD RULE: Every navigation item MUST have a UNIQUE icon representing its label.</prevention>
  </incident>

  <incident id="M23" severity="high">
    <issue>Apple Liquid Glass Styling Violations</issue>
    <root_cause>Used solid colors or inconsistent opacities instead of the mandated glass recipe.</root_cause>
    <prevention>
      MANDATORY: Follow the Glass Recipe: backdrop-blur-xl, bg-white/80, border-black/5, rounded-[20px], shadow-torro-glass.
    </prevention>
  </incident>

  <incident id="M25" severity="medium">
    <issue>D3 Zoom Functionality Broken</issue>
    <root_cause>Zoom behavior re-created on every render; transform state not maintained in ref.</root_cause>
    <prevention>
      MUST use transformRef to maintain state across renders. Initialize zoom only once (empty dependency array).
    </prevention>
  </incident>

  <incident id="M26" severity="high">
    <issue>Missing Feature Exports (Barrel Files)</issue>
    <root_cause>Feature index.ts failed to export public utility functions, causing build errors.</root_cause>
    <prevention>Every feature directory MUST have an index.ts barrel file exporting all public APIs.</prevention>
  </incident>

  <incident id="M29" severity="high">
    <issue>Nested AppShell Duplication</issue>
    <root_cause>Wrapped child page in AppShell when parent SecureLayout already provided it.</root_cause>
    <prevention>Check parent layout structure before adding AppShell. Child pages inherit layout shell.</prevention>
  </incident>

  <incident id="M32" severity="critical">
    <issue>CSS Fragmentation (Secondary CSS Files)</issue>
    <root_cause>Created torro-standards.css instead of consolidating into globals.css.</root_cause>
    <prevention>HARD RULE: globals.css is the single source of truth. NO secondary global CSS files allowed.</prevention>
  </incident>

  <incident id="M34" severity="high">
    <issue>UI Test Drift & Brittle Locators</issue>
    <root_cause>Tests used brittle text locators and were not updated alongside component refactors.</root_cause>
    <prevention>
      Enforce Component-Test Co-evolution. Use getByRole or data-testid instead of getByText.
    </prevention>
  </incident>

  <incident id="M36" severity="high">
    <issue>React Lifecycle Misuse: set-state-in-effect</issue>
    <root_cause>Used useEffect to sync props to state or load localStorage, causing cascading renders.</root_cause>
    <prevention>Use Lazy Initializers (useState(() => ...)) and Render-Phase State Syncing.</prevention>
  </incident>

  <incident id="M37" severity="critical">
    <issue>Type Safety Gap: 'any' Pollution</issue>
    <root_cause>Widespread use of 'any' in feature layers masking structural drift.</root_cause>
    <prevention>Prohibit 'any'. Use Zod schemas and explicit interfaces with API parsers.</prevention>
  </incident>
</mistake_registry>
