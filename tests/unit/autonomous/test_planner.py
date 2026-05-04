"""
FN:test_planner.py
Unit tests for Torro autonomous layer planner.

Tests:
- TestAgenticPlanner: Test planner functions
- TestDAGConfig: Test DAG configuration
- TestTaskConfig: Test task configuration
"""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.autonomous.planner import (
    AgenticPlanner,
    DAGConfig,
    TaskConfig,
    PlanResult,
)


class TestAgenticPlanner:
    """Test agentic planner functions."""
    
    @pytest.fixture
    def temp_dags_dir(self):
        """Create temporary DAGs directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_planner_creation(self, temp_dags_dir):
        """Test creating a planner instance."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        assert planner is not None
        assert Path(temp_dags_dir).exists()
    
    def test_generate_dag_basic(self, temp_dags_dir):
        """Test generating a basic DAG."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="First task"
            )
        ]
        
        result = planner.generate_dag(
            dag_id="test_dag",
            description="Test DAG",
            tasks=tasks
        )
        
        assert result.plan_id == "test_dag"
        assert len(result.tasks) == 1
        assert result.estimated_tokens > 0
    
    def test_generate_dag_multiple_tasks(self, temp_dags_dir):
        """Test generating DAG with multiple tasks."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="First task"
            ),
            TaskConfig(
                task_id="task2",
                task_type="complex",
                description="Second task"
            ),
            TaskConfig(
                task_id="task3",
                task_type="research",
                description="Third task"
            ),
        ]
        
        result = planner.generate_dag(
            dag_id="multi_task_dag",
            description="Multi-task DAG",
            tasks=tasks
        )
        
        assert result.plan_id == "multi_task_dag"
        assert len(result.tasks) == 3
        assert result.estimated_tokens > 0
    
    def test_generate_dag_with_dependencies(self, temp_dags_dir):
        """Test generating DAG with task dependencies."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="First task"
            ),
            TaskConfig(
                task_id="task2",
                task_type="simple",
                description="Second task",
                dependencies=["task1"]
            ),
        ]
        
        result = planner.generate_dag(
            dag_id="dependent_dag",
            description="Dependent DAG",
            tasks=tasks
        )
        
        assert result.plan_id == "dependent_dag"
        assert result.tasks[1].dependencies == ["task1"]
    
    def test_validate_dag_empty(self, temp_dags_dir):
        """Test validating an empty DAG."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        result = PlanResult(
            plan_id="empty_dag",
            dag_config=DAGConfig(
                dag_id="empty_dag",
                description="Empty DAG"
            ),
            tasks=[],
            estimated_tokens=0,
            estimated_duration=0
        )
        
        errors = planner.validate_dag(result)
        
        assert "DAG must have at least one task" in errors
    
    def test_validate_dag_missing_dependency(self, temp_dags_dir):
        """Test validating DAG with missing dependency."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="First task",
                dependencies=["non_existent"]
            )
        ]
        
        result = PlanResult(
            plan_id="missing_dep_dag",
            dag_config=DAGConfig(
                dag_id="missing_dep_dag",
                description="Missing dependency DAG"
            ),
            tasks=tasks,
            estimated_tokens=1000,
            estimated_duration=10
        )
        
        errors = planner.validate_dag(result)
        
        assert any("non-existent task" in err for err in errors)
    
    def test_validate_dag_self_dependency(self, temp_dags_dir):
        """Test validating DAG with self-dependency."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="Self-dependent task",
                dependencies=["task1"]
            )
        ]
        
        result = PlanResult(
            plan_id="self_dep_dag",
            dag_config=DAGConfig(
                dag_id="self_dep_dag",
                description="Self-dependency DAG"
            ),
            tasks=tasks,
            estimated_tokens=1000,
            estimated_duration=10
        )
        
        errors = planner.validate_dag(result)
        
        assert any("depends on itself" in err for err in errors)
    
    def test_export_dag(self, temp_dags_dir):
        """Test exporting DAG to file."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        tasks = [
            TaskConfig(
                task_id="task1",
                task_type="simple",
                description="Test task"
            )
        ]
        
        result = planner.generate_dag(
            dag_id="export_test",
            description="Export test DAG",
            tasks=tasks
        )
        
        output_path = planner.export_dag(result)
        
        assert Path(output_path).exists()
        assert output_path.endswith("export_test.py")
    
    def test_get_plan_history(self, temp_dags_dir):
        """Test getting plan history."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        # Generate some plans
        for i in range(5):
            tasks = [
                TaskConfig(
                    task_id=f"task{i}",
                    task_type="simple",
                    description=f"Task {i}"
                )
            ]
            planner.generate_dag(
                dag_id=f"dag_{i}",
                description=f"DAG {i}",
                tasks=tasks
            )
        
        history = planner.get_plan_history(limit=3)
        
        assert len(history) == 3
    
    def test_set_token_budget(self, temp_dags_dir):
        """Test setting token budget."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        planner.set_token_budget("test_dag", 500000)
        budget = planner.get_token_budget("test_dag")
        
        assert budget == 500000
    
    def test_get_default_token_budget(self, temp_dags_dir):
        """Test getting default token budget."""
        planner = AgenticPlanner(dags_dir=temp_dags_dir)
        
        budget = planner.get_token_budget("unknown_dag")
        
        assert budget == planner.DEFAULT_TOKEN_BUDGET


class TestDAGConfig:
    """Test DAGConfig dataclass."""
    
    def test_dag_config_creation(self):
        """Test creating a DAG config."""
        config = DAGConfig(
            dag_id="test_dag",
            description="Test DAG"
        )
        
        assert config.dag_id == "test_dag"
        assert config.description == "Test DAG"
        assert config.schedule_interval == "@once"
        assert config.catchup is False
    
    def test_dag_config_with_custom_values(self):
        """Test creating a DAG config with custom values."""
        config = DAGConfig(
            dag_id="custom_dag",
            description="Custom DAG",
            schedule_interval="@daily",
            max_active_runs=2,
            tags=["custom", "test"]
        )
        
        assert config.schedule_interval == "@daily"
        assert config.max_active_runs == 2
        assert config.tags == ["custom", "test"]


class TestTaskConfig:
    """Test TaskConfig dataclass."""
    
    def test_task_config_creation(self):
        """Test creating a task config."""
        config = TaskConfig(
            task_id="task1",
            task_type="simple",
            description="Test task"
        )
        
        assert config.task_id == "task1"
        assert config.task_type == "simple"
        assert config.description == "Test task"
        assert config.operator == "PythonOperator"
        assert config.timeout == 600
    
    def test_task_config_with_dependencies(self):
        """Test creating a task config with dependencies."""
        config = TaskConfig(
            task_id="task2",
            task_type="complex",
            description="Dependent task",
            dependencies=["task1"],
            timeout=1200
        )
        
        assert config.dependencies == ["task1"]
        assert config.timeout == 1200


class TestPlanResult:
    """Test PlanResult dataclass."""
    
    def test_plan_result_creation(self):
        """Test creating a plan result."""
        result = PlanResult(
            plan_id="test_plan",
            dag_config=DAGConfig(
                dag_id="test_dag",
                description="Test DAG"
            ),
            tasks=[],
            estimated_tokens=1000,
            estimated_duration=60.0
        )
        
        assert result.plan_id == "test_plan"
        assert result.estimated_tokens == 1000
        assert result.estimated_duration == 60.0
        assert result.created_at is not None
