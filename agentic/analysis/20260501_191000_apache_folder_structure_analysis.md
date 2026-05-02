# Apache Open Source Folder Structure Analysis

## Current Proposed Structure vs Apache Standards

### Current Proposed Structure (Python-centric)

```
torro-agent/
├── engine/
│   ├── __init__.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── test_*.py
│   ├── context/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── test_*.py
│   └── memory/
│       ├── __init__.py
│       ├── manager.py
│       └── test_*.py
├── tests/
└── docs/
```

### Top-Tier Apache Open Source Structure

Based on analysis of Apache projects (Airflow, Spark, Kafka) and the legacy projects in this workspace:

```
torro-agent/
├── .github/                    # GitHub workflows, issue templates
├── .asf.yaml                   # Apache Foundation config (REQUIRED for Apache)
├── LICENSE                     # Apache 2.0 License
├── NOTICE                      # Apache NOTICE file (REQUIRED for Apache)
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Code of conduct
├── SECURITY.md                 # Security policy
├── CHANGELOG.md                # Version history
├── pyproject.toml              # Python build configuration
├── setup.cfg                   # Package configuration
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Development dependencies
├── docker-compose.yml          # Local development environment
├── Dockerfile                  # Container build instructions
│
├── src/                        # Source code (NOT engine/)
│   └── torro/                  # Package name matches project
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── config.py           # Configuration management
│       │
│       ├── tools/              # Tool definitions
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   └── builtin/        # Built-in tools subdirectory
│       │       ├── bash.py
│       │       └── file_ops.py
│       │
│       ├── context/            # Context management
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── compressor.py
│       │   └── engines/        # Engine implementations
│       │       ├── builtin.py
│       │       └── lcm.py
│       │
│       └── memory/             # Memory management
│           ├── __init__.py
│           ├── manager.py
│           ├── provider.py
│           └── providers/      # Provider implementations
│               ├── builtin.py
│               └── vector.py
│
├── tests/                      # Tests at ROOT level (NOT inside src/)
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── unit/                   # Unit tests
│   │   ├── tools/
│   │   │   ├── test_base.py
│   │   │   └── test_registry.py
│   │   ├── context/
│   │   │   └── test_base.py
│   │   └── memory/
│   │       ├── test_manager.py
│   │       └── test_provider.py
│   ├── integration/            # Integration tests
│   │   └── test_api.py
│   └── e2e/                    # End-to-end tests
│       └── test_workflow.py
│
├── docs/                       # Documentation
│   ├── conf.py                 # Sphinx configuration
│   ├── index.rst
│   ├── getting-started.md
│   ├── architecture.md
│   ├── api/                    # API documentation
│   │   ├── tools.rst
│   │   ├── context.rst
│   │   └── memory.rst
│   └── tutorials/              # Step-by-step guides
│       └── quickstart.md
│
├── examples/                   # Usage examples (REQUIRED for Apache)
│   ├── basic_usage.py
│   ├── advanced_config.py
│   └── custom_provider.py
│
├── scripts/                    # Utility scripts
│   ├── lint.sh
│   ├── test.sh
│   └── release.py
│
├── benchmarks/                 # Performance benchmarks
│   └── test_performance.py
│
└── dist/                       # Distribution artifacts (gitignored)
```

## Key Differences

### 1. Source Directory Naming

| Aspect | Current Proposal | Apache Standard |
|--------|-----------------|-----------------|
| Root directory | `engine/` | `src/torro/` |
| Package name | Implicit | Matches project name |
| Rationale | Descriptive | Import clarity (`import torro.tools`) |

**Recommendation**: Use `src/torro/` pattern for clear package identity.

### 2. Test Location

| Aspect | Current Proposal | Apache Standard |
|--------|-----------------|-----------------|
| Test location | Inside `engine/` | Root-level `tests/` |
| Test file naming | `test_*.py` | `test_*.py` (same) |
| Rationale | Co-location | Separation of concerns |

**Recommendation**: Move tests to root-level `tests/` directory.

### 3. Implementation Subdirectories

| Aspect | Current Proposal | Apache Standard |
|--------|-----------------|-----------------|
| Subdirectories | Flat structure | `builtin/`, `engines/`, `providers/` |
| Extensibility | Limited | Clear extension points |
| Rationale | Simplicity | Plugin architecture support |

**Recommendation**: Add subdirectories for built-in vs custom implementations.

### 4. Required Apache Files

| File | Current | Apache Required |
|------|---------|-----------------|
| LICENSE | ✓ | ✓ (Apache 2.0) |
| NOTICE | ✗ | ✓ (REQUIRED) |
| .asf.yaml | ✗ | ✓ (REQUIRED) |
| README.md | ✓ | ✓ |
| CONTRIBUTING.md | ✗ | ✓ |
| CODE_OF_CONDUCT.md | ✗ | ✓ |
| SECURITY.md | ✗ | ✓ |
| CHANGELOG.md | ✗ | ✓ |
| examples/ | ✗ | ✓ |

**Recommendation**: Add all missing Apache-required files.

## Apache Project References

### Apache Airflow Structure
```
airflow/
├── airflow/              # Main package
│   ├── operators/
│   ├── hooks/
│   ├── sensors/
│   └── providers/
├── tests/
├── docs/
├── scripts/
└── examples/
```

### Apache Spark Structure
```
spark/
├── core/
├── sql/
├── mllib/
├── streaming/
├── examples/
├── python/               # PyML package
└── R/                    # R package
```

### Apache Kafka Structure
```
kafka/
├── core/
├── clients/
├── streams/
├── tools/
├── examples/
└── docs/
```

## Recommended Updates to Plan

### Updated Package Structure

```
torro-agent/
├── src/torro/
│   ├── __init__.py
│   ├── version.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── builtin/
│   │       ├── bash.py
│   │       └── file_ops.py
│   │
│   ├── context/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── compressor.py
│   │   └── engines/
│   │       ├── builtin.py
│   │       └── lcm.py
│   │
│   └── memory/
│       ├── __init__.py
│       ├── manager.py
│       ├── provider.py
│       └── providers/
│           ├── builtin.py
│           └── vector.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── tools/
│   │   ├── context/
│   │   └── memory/
│   ├── integration/
│   └── e2e/
│
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── api/
│   └── tutorials/
│
├── examples/
│   ├── basic_usage.py
│   ├── advanced_config.py
│   └── custom_provider.py
│
└── scripts/
    ├── lint.sh
    └── test.sh
```

### Updated Import Pattern

```python
# Before (current proposal)
from engine.tools.base import Tool
from engine.tools.registry import ToolRegistry
from engine.context.base import ContextEngine
from engine.memory.manager import MemoryManager

# After (Apache standard)
from torro.tools.base import Tool
from torro.tools.registry import ToolRegistry
from torro.context.base import ContextEngine
from torro.memory.manager import MemoryManager
```

## Apache Compliance Checklist

- [ ] Add `NOTICE` file at root
- [ ] Add `.asf.yaml` configuration
- [ ] Add `CONTRIBUTING.md`
- [ ] Add `CODE_OF_CONDUCT.md`
- [ ] Add `SECURITY.md`
- [ ] Add `CHANGELOG.md`
- [ ] Create `examples/` directory with usage examples
- [ ] Move `tests/` to root level
- [ ] Rename `engine/` to `src/torro/`
- [ ] Add `scripts/` directory for utility scripts
- [ ] Add `docs/conf.py` for Sphinx documentation
- [ ] Add `benchmarks/` for performance testing

## Conclusion

The current proposed structure follows **Python package conventions** but does not fully align with **top-tier Apache open source standards**. Key improvements needed:

1. **Source directory**: Change `engine/` to `src/torro/`
2. **Test location**: Move from inside package to root-level `tests/`
3. **Subdirectories**: Add `builtin/`, `engines/`, `providers/` for extensibility
4. **Apache files**: Add NOTICE, .asf.yaml, CONTRIBUTING.md, etc.
5. **Examples**: Add `examples/` directory with usage examples

These changes ensure the project is immediately recognizable as Apache-compliant and follows patterns developers expect from top-tier open source projects.
