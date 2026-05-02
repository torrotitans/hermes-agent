---
name: airflow
description: Create, maintain, and debug Apache Airflow DAGs and tasks using the TaskFlow API, operators, triggers, and scheduling patterns from Apache Airflow v2.x
license: Apache-2.0
compatibility:
  - python-3.9+
  - apache-airflow-2.3+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://github.com/apache/airflow
---

# Apache Airflow Skill

## When to Use This Skill

Use this skill when you need to:
- Create new Airflow DAGs with the TaskFlow API (`@dag`, `@task`, `@task_group` decorators)
- Write custom operators or sensors for Airflow
- Configure DAG scheduling, dependencies, and execution parameters
- Implement XCom messaging between tasks
- Set up task dependencies using bitshift operators (`>>`, `<<`) or `chain()`
- Use Airflow triggers for async task execution
- Configure Airflow connections, variables, and pools
- Debug DAG parsing errors or task failures
- Implement asset-based DAG triggering (Airflow 2.7+)

## When NOT to Use This Skill

Do NOT use this skill when:
- Working with Airflow 1.x (deprecated, uses different API)
- Creating simple cron jobs without Airflow orchestration needs
- Building non-orchestration Python applications
- Configuring Airflow infrastructure (use infrastructure skills instead)

## Inputs Required

Before starting, ensure you have:
1. Airflow version (default: v2.10+ with Task SDK)
2. DAG purpose and data flow requirements
3. Scheduler type (CeleryExecutor, KubernetesExecutor, etc.)
4. Connection/variable dependencies

## Workflow

### Step 1: Create a Basic DAG with TaskFlow API

Use the modern TaskFlow API with decorators (Airflow 2.7+):

```python
from __future__ import annotations

import logging
from datetime import datetime

from airflow.sdk import dag, task

log = logging.getLogger(__name__)


@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "production"],
    params={"environment": "prod"},
)
def my_etl_dag():
    """ETL pipeline DAG using TaskFlow API."""

    @task()
    def extract():
        """Extract data from source."""
        data = {"records": [1, 2, 3]}
        return data

    @task(multiple_outputs=True)
    def transform(extracted_data: dict):
        """Transform extracted data."""
        transformed = {
            "count": len(extracted_data["records"]),
            "sum": sum(extracted_data["records"]),
        }
        return transformed

    @task()
    def load(transformed_data: dict):
        """Load transformed data."""
        print(f"Loading {transformed_data['count']} records")

    # Task dependencies using function calls (XCom auto-passing)
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)


my_etl_dag = my_etl_dag()
```

### Step 2: Use BashOperator for Shell Commands

```python
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, chain

with DAG(
    dag_id="bash_example",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    # Create tasks
    task1 = BashOperator(
        task_id="echo_hello",
        bash_command="echo 'Hello from Airflow!'",
    )

    task2 = BashOperator(
        task_id="echo_world",
        bash_command="echo 'World!'",
    )

    # Define dependencies
    chain(task1, task2)

    # Alternative: bitshift operators
    # task1 >> task2
```

### Step 3: Create TaskGroups for Organization

```python
from airflow.sdk import DAG, task, task_group

@task
def task_start():
    return "start"

@task
def task_end():
    print("end")

@task_group
def processing_group(data: int):
    """Group related tasks together."""

    @task
    def process(data: int):
        return data * 2

    @task
    def validate(result: int):
        assert result > 0

    validate(process(data))

with DAG(
    dag_id="task_group_example",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    start = task_start()
    end = task_end()

    for i in range(3):
        group = processing_group(i)
        start >> group >> end
```

### Step 4: Use virtualenv Tasks for Isolated Dependencies

```python
@task.virtualenv(
    task_id="virtualenv_task",
    requirements=["pandas", "numpy"],
    system_site_packages=False,
    serializer="dill",
)
def isolated_task():
    import pandas as pd
    import numpy as np
    # Code runs in isolated virtualenv
    return pd.DataFrame({"data": [1, 2, 3]})
```

### Step 5: Configure Advanced DAG Parameters

```python
@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=3,
    max_active_tasks=5,
    default_args={
        "owner": "data-engineering",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": send_alert,
    },
    tags=["production", "critical"],
    doc_md=__doc__,
)
```

### Step 6: Implement Asset-Based Triggering (Airflow 2.7+)

```python
from airflow.sdk import Asset, dag, task

@dag(
    schedule=[Asset(name="processed_data")],
    start_date=datetime(2024, 1, 1),
    catchup=False,
)
def asset_triggered_dag():
    @task(provides_xcom=False)
    def consume_asset():
        print("Asset triggered!")

    consume_asset()
```

## Files Reference

| File | Purpose |
|------|---------|
| `airflow-core/src/airflow/sdk/definitions/dag.py` | DAG class definition |
| `airflow-core/src/airflow/example_dags/` | Example DAGs |
| `task-sdk/src/airflow/sdk/` | Task SDK (modern API) |
| `providers/standard/` | Standard operators |

## Troubleshooting

### Issue: DAG Parsing Error

**Symptom**: `AirflowException: Failed to parse DAG file`

**Solution**:
- Check Python syntax in DAG file
- Ensure all imports are available in Airflow environment
- Verify `schedule` parameter is valid cron or `None`
- Check for circular imports

### Issue: Task Not Found in UI

**Symptom**: Task appears in file but not in Airflow UI

**Solution**:
- Verify DAG file is in `dags/` directory
- Check DAG file name (must be valid Python module)
- Restart scheduler: `airflow scheduler`
- Check scheduler logs: `tail -f /var/log/airflow/scheduler/scheduler.log`

### Issue: XCom Serialization Error

**Symptom**: `TypeError: Object of type X is not JSON serializable`

**Solution**:
- Use `serializer="dill"` for complex objects
- Return only JSON-serializable types (dict, list, str, int, float, bool)
- Use `@task(provides_xcom=False)` if XCom not needed

## Examples

### Example 1: Simple ETL Pipeline

```python
@dag(schedule="@daily", start_date=datetime(2024, 1, 1), catchup=False)
def simple_etl():
    @task()
    def extract():
        return {"data": [1, 2, 3]}

    @task()
    def transform(data: dict):
        return {"result": sum(data["data"])}

    @task()
    def load(result: dict):
        print(f"Loaded: {result}")

    extract() >> transform() >> load()

simple_etl = simple_etl()
```

### Example 2: Parallel Task Execution

```python
with DAG("parallel_example", schedule=None, start_date=datetime(2024, 1, 1)) as dag:
    tasks = [BashOperator(task_id=f"task_{i}", bash_command=f"echo {i}") for i in range(5)]
    # All tasks run in parallel
    chain(*tasks)
```

## Related Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [TaskFlow API Guide](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflows.html)
- [Example DAGs Repository](https://github.com/apache/airflow/tree/main/airflow-core/src/airflow/example_dags)
