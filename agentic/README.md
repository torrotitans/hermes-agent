# Torro Agent Framework - Layer 0 & Layer 1 Implementation Guide

## Overview

This guide covers the implementation and usage of Torro Agent's Layer 0 (Presentation/CLI) and Layer 1 (Autonomous Layer) components.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 0: Presentation Layer (CLI)                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ TUI Renderer│  │ Mode Selector│  │ Clarification Manager│   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │Stream Handler│ │Permission Mgr│  │   Session Database  │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Autonomous Layer (The Brain)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Orchestrator  │  │     Planner     │  │ Function Factory│ │
│  │  (Circuit       │  │  (Airflow DAG   │  │  (Macro         │ │
│  │   Breaker)      │  │   Generation)   │  │  Generation)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

1. Python 3.9 or higher
2. pip package manager
3. (Optional) Ollama or LM Studio for local AI models

### Installation

```bash
# Navigate to project root
cd /Users/q4r00t/Github/hermes-agent

# Install dependencies
pip install -r requirements.txt

# Install prompt_toolkit for TUI
pip install prompt_toolkit
```

### Configuration

Edit `config.ini` to configure your AI models:

```ini
[CLI_MODELS]
# Default interactive model
default = local_qwen25_7b

# Model definitions (provider|model_name|base_url)
local_qwen25_7b = ollama|qwen2.5:7b|http://localhost:11434
cloud_qwen35_397b = openai|Intel/Qwen3.5-397B-A17B-int4-AutoRound|http://192.168.3.139:8000/v1
```

## Running the CLI

### Start Interactive Mode

```bash
# From project root
python3 src/cli.py interactive

# Or with specific model (local Ollama)
python3 src/cli.py interactive --model local_qwen35_397b

# Or with network model (OpenAI-compatible API)
python3 src/cli.py interactive --model cloud_qwen35_397b

# Alternative using module syntax
python3 -m src.cli interactive --model local_qwen35_397b
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `mode` | Select operation mode (Plan, Gap Analysis, RCA, Execute) |
| `model` | Switch AI model |
| `list` | List available models |
| `exit` / `quit` | Exit the CLI |

## Test Case: Hello World Program

Here's a complete test case demonstrating the CLI talking to Layer 1 to generate a Python hello world program.

### Step 1: Start the CLI

```bash
cd /Users/q4r00t/Github/hermes-agent
python3 src/cli.py interactive --model local_qwen35_397b
```

**Note:** The model names in `config.ini` use prefixes to indicate the source:
- `local_*` - Ollama/LM Studio models (localhost:11434)
- `cloud_*` - OpenAI-compatible API models (network addresses like 192.168.3.139:8000)

### Step 2: Select Mode

When prompted, select mode `4` (Execute) or type `mode` and select Execute.

### Step 3: Enter Request

Type the following request:

```
Write a hello world program in Python
```

### Expected Output

```
=== Torro Interactive CLI ===
Model: cloud_qwen35_397b
Type 'exit' to quit, 'help' for commands

> Write a hello world program in Python

Assistant: Here's a simple Hello World program in Python:

```python
#!/usr/bin/env python3
"""
FN:hello_world.py
Hello World program demonstrating Torro coding standards.
"""

def greet(name: str = "World") -> str:
    """FN:greet Generate greeting message.
    
    Args:
        name: Name to greet (default: "World")
    
    Returns:
        Greeting string
    """
    return f"Hello, {name}!"


def main():
    """FN:main Main entry point."""
    message = greet()
    print(message)


if __name__ == "__main__":
    main()
```

You can run this program by saving it as `hello_world.py` and executing:
```bash
python3 hello_world.py
```

Output:
```
Hello, World!
```
```

### Step 4: Verify Circuit Breaker

The orchestrator tracks command frequency. If you repeat the same request 3 times, the circuit breaker will trigger:

```
> Write a hello world program in Python

Circuit Breaker: Circuit breaker triggered: 'Write a hello world program in Python' repeated 3 times in 300s window
Please rephrase your request or try a different approach.
```

This prevents infinite recursion and token waste.

## Unit Testing

### Run All Tests

```bash
# Run all autonomous layer tests
python3 -m pytest tests/unit/autonomous/ -v

# Run with coverage
python3 -m pytest tests/unit/autonomous/ -v --cov=src/autonomous
```

### Test Individual Components

```bash
# Test orchestrator
python3 -m pytest tests/unit/autonomous/test_orchestrator.py -v

# Test planner
python3 -m pytest tests/unit/autonomous/test_planner.py -v

# Test function factory
python3 -m pytest tests/unit/autonomous/test_function_factory.py -v
```

### Sample Test Output

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/q4r00t/Github/hermes-agent
configfile: pyproject.toml
plugins: anyio-4.12.1, time-machine-2.19.0, asyncio-1.20.0, base-url-2.1.0, md-report-0.7.0, playwright-0.7.1
asyncio: mode=strict, debug=False, asyncio_default_fixture_loop_scope=function
collecting ... collected 56 items

tests/unit/autonomous/test_orchestrator.py::TestAgenticOrchestrator::test_orchestrator_creation PASSED [  1%]
tests/unit/autonomous/test_orchestrator.py::TestAgenticOrchestrator::test_route_task_simple PASSED [  3%]
...
tests/unit/autonomous/test_function_factory.py::TestFunctionFactory::test_generate_macro_basic PASSED [ 98%]
tests/unit/autonomous/test_planner.py::TestPlanResult::test_plan_result_creation PASSED [100%]

============================== 56 passed in 0.28s ==============================
```

## Programmatic Testing

### Test Orchestrator Directly

```python
from src.autonomous import AgenticOrchestrator, TaskType

# Create orchestrator
orchestrator = AgenticOrchestrator()

# Route a task
task_id = orchestrator.route_task(
    task_type=TaskType.EXECUTION,
    description="Write hello world program",
    payload={"language": "python"}
)

print(f"Task routed: {task_id}")

# Execute the task
result = orchestrator.execute_task(task_id)
print(f"Task result: {result.status}")
```

### Test Planner Directly

```python
from src.autonomous import AgenticPlanner, TaskConfig

# Create planner
planner = AgenticPlanner(dags_dir="airflow/dags")

# Define tasks
tasks = [
    TaskConfig(
        task_id="generate_code",
        task_type="simple",
        description="Generate Python hello world"
    ),
    TaskConfig(
        task_id="run_tests",
        task_type="simple",
        description="Run unit tests",
        dependencies=["generate_code"]
    ),
]

# Generate DAG
result = planner.generate_dag(
    dag_id="hello_world_pipeline",
    description="Hello World Generation Pipeline",
    tasks=tasks
)

print(f"DAG generated: {result.plan_id}")
print(f"Estimated tokens: {result.estimated_tokens}")
print(f"Estimated duration: {result.estimated_duration} minutes")

# Export DAG
output_path = planner.export_dag(result)
print(f"DAG exported to: {output_path}")
```

### Test Function Factory Directly

```python
from src.autonomous import FunctionFactory

# Create factory
factory = FunctionFactory(output_dir="agentic/macros")

# Record commands
for _ in range(5):
    factory.record_command("git status")

# Generate macro
result = factory.generate_macro(
    command="git status",
    name="git_status"
)

print(f"Macro generated: {result.macro_id}")
print(f"Token savings: {result.token_savings}")
print(f"Generated code:\n{result.code}")

# Export macro
output_path = factory.export_macro("git_status")
print(f"Macro exported to: {output_path}")
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'autonomous'`:

```bash
# Ensure you're in the project root
cd /Users/q4r00t/Github/hermes-agent

# Run with PYTHONPATH
PYTHONPATH=/Users/q4r00t/Github/hermes-agent python3 -m src.cli interactive
```

### Circuit Breaker Issues

If circuit breaker triggers unexpectedly:

```python
from src.autonomous import AgenticOrchestrator

orchestrator = AgenticOrchestrator()

# Reset recursion counter
orchestrator.reset_recursion_counter()

# Or reset specific command
orchestrator.reset_recursion_counter("specific command")
```

### Model Connection Issues

If you see connection errors:

```bash
# Check if Ollama is running
ollama list

# Check if model exists
ollama pull qwen2.5:7b

# Test API endpoint
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b","prompt":"Hello"}'
```

## Next Steps

1. **Explore Layer 2**: Implement reporting layer for Jira integration
2. **Add More Modes**: Extend mode selector with additional operation modes
3. **Custom Macros**: Create custom macros for frequently used commands
4. **DAG Execution**: Integrate with actual Airflow deployment

## Reference Documents

- [AGENT.md](standard/AGENT.md) - Agentic coding principles
- [Enterprise Architecture](plan/20260501_181500_torro_agent_enterprise_architecture.md) - 7-layer architecture
- [Layer 0 Plan](plan/20260502_070000_layer0_cli_plan.md) - CLI implementation plan
- [Layer 1 Plan](plan/20260502_082000_layer1_autonomous_plan.md) - Autonomous layer plan
