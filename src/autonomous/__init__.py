"""
FN:__init__.py
Package: src.autonomous
Summary: Layer 1 Autonomous Layer - cognitive epicenter for Torro Agent.

Structure:
- __init__.py
- orchestrator.py
- planner.py
- function_factory.py

Entry Points:
- AgenticOrchestrator (task routing and circuit breaker)
- AgenticPlanner (Airflow DAG generation)
- FunctionFactory (macro generation)

Flow:
- CLI Input -> orchestrator -> planner/function_factory -> execution

Read First:
- orchestrator.py
- planner.py
"""

from .orchestrator import (
    AgenticOrchestrator,
    TaskType,
    TaskStatus,
    TaskResult,
    Task,
    CircuitBreakerError,
)
from .planner import (
    AgenticPlanner,
    DAGConfig,
    TaskConfig,
    PlanResult,
)
from .function_factory import (
    FunctionFactory,
    MacroConfig,
    MacroResult,
)

__all__ = [
    "AgenticOrchestrator",
    "TaskType",
    "TaskStatus",
    "TaskResult",
    "Task",
    "CircuitBreakerError",
    "AgenticPlanner",
    "DAGConfig",
    "TaskConfig",
    "PlanResult",
    "FunctionFactory",
    "MacroConfig",
    "MacroResult",
]
