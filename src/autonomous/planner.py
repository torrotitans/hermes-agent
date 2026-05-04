"""
FN:planner.py
Agentic Planner for Layer 1 Autonomous Layer in Torro Agent.

Generates Airflow DAGs for complex task orchestration with token budgets.

Classes:
- DAGConfig: Configuration for generated DAG
- TaskConfig: Configuration for individual task
- AgenticPlanner: Main planner class

Functions:
- FN:generate_dag: Generate Airflow DAG definition (lines 95-130)
- FN:validate_dag: Validate DAG configuration (lines 132-155)
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DAGConfig:
    """Configuration for generated Airflow DAG."""
    dag_id: str
    description: str
    schedule_interval: str = "@once"
    start_date: str = ""
    catchup: bool = False
    max_active_runs: int = 1
    tags: List[str] = field(default_factory=list)
    default_args: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now().isoformat()


@dataclass
class TaskConfig:
    """Configuration for individual task in DAG."""
    task_id: str
    task_type: str
    description: str
    operator: str = "PythonOperator"
    dependencies: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 600  # 10 minutes
    retries: int = 2
    retry_delay: int = 300  # 5 minutes


@dataclass
class PlanResult:
    """Result of planning operation."""
    plan_id: str
    dag_config: DAGConfig
    tasks: List[TaskConfig]
    estimated_tokens: int
    estimated_duration: float
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class AgenticPlanner:
    """
    Agentic Planner for Layer 1 Autonomous Layer.
    Generates Airflow DAGs for complex task orchestration.
    
    Responsibilities:
    - Generate Airflow DAG definitions from task specifications
    - Manage token budgets for each task
    - Validate DAG configurations
    - Track planning history
    """
    
    # Token budget configuration
    DEFAULT_TOKEN_BUDGET = 1_000_000  # 1M tokens per phase
    MAX_TASK_DURATION = 600  # 10 minutes per task
    
    def __init__(self, dags_dir: Optional[str] = None):
        """
        Initialize the agentic planner.
        
        Args:
            dags_dir: Directory to store generated DAG files
        """
        self._dags_dir = dags_dir or "airflow/dags"
        self._plan_history: List[PlanResult] = []
        self._token_budgets: Dict[str, int] = {}
        
        # Ensure DAGs directory exists
        Path(self._dags_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("FN:__init__ AgenticPlanner initialized with DAGs dir: %s", self._dags_dir)
    
    def generate_dag(
        self,
        dag_id: str,
        description: str,
        tasks: List[TaskConfig],
        schedule_interval: str = "@once",
        token_budget: Optional[int] = None
    ) -> PlanResult:
        """
        FN:generate_dag Generate Airflow DAG definition.
        
        Args:
            dag_id: Unique DAG identifier
            description: DAG description
            tasks: List of task configurations
            schedule_interval: Cron expression or @once/@daily/etc
            token_budget: Optional token budget override
            
        Returns:
            PlanResult with generated DAG configuration
        """
        # Create DAG config
        dag_config = DAGConfig(
            dag_id=dag_id,
            description=description,
            schedule_interval=schedule_interval,
            tags=["torro", "autonomous", "layer1"]
        )
        
        # Calculate estimated tokens
        estimated_tokens = sum(
            self._estimate_task_tokens(task) for task in tasks
        )
        
        # Check token budget
        budget = token_budget or self.DEFAULT_TOKEN_BUDGET
        if estimated_tokens > budget:
            logger.warning(
                "FN:generate_dag Estimated tokens (%d) exceed budget (%d)",
                estimated_tokens, budget
            )
        
        # Calculate estimated duration
        estimated_duration = sum(task.timeout for task in tasks) / 60.0  # minutes
        
        # Create plan result
        plan_result = PlanResult(
            plan_id=dag_id,
            dag_config=dag_config,
            tasks=tasks,
            estimated_tokens=estimated_tokens,
            estimated_duration=estimated_duration
        )
        
        # Store in history
        self._plan_history.append(plan_result)
        
        logger.info(
            "FN:generate_dag DAG generated: %s (%d tasks, %d tokens)",
            dag_id, len(tasks), estimated_tokens
        )
        
        return plan_result
    
    def _estimate_task_tokens(self, task: TaskConfig) -> int:
        """
        FN:_estimate_task_tokens Estimate token consumption for a task.
        
        Args:
            task: Task configuration
            
        Returns:
            Estimated token count
        """
        # Base estimation: 1000 tokens per minute of task duration
        base_tokens = (task.timeout // 60) * 1000
        
        # Add overhead for complexity
        complexity_multiplier = 1.0
        if task.task_type == "complex":
            complexity_multiplier = 1.5
        elif task.task_type == "research":
            complexity_multiplier = 2.0
        
        return int(base_tokens * complexity_multiplier)
    
    def validate_dag(self, plan_result: PlanResult) -> List[str]:
        """
        FN:validate_dag Validate DAG configuration.
        
        Args:
            plan_result: Plan result to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check task count
        if len(plan_result.tasks) == 0:
            errors.append("DAG must have at least one task")
        
        # Check for circular dependencies
        task_ids = {task.task_id for task in plan_result.tasks}
        for task in plan_result.tasks:
            for dep in task.dependencies:
                if dep not in task_ids:
                    errors.append(f"Task {task.task_id} depends on non-existent task: {dep}")
        
        # Check for self-dependencies
        for task in plan_result.tasks:
            if task.task_id in task.dependencies:
                errors.append(f"Task {task.task_id} depends on itself")
        
        # Check token budget
        if plan_result.estimated_tokens > self.DEFAULT_TOKEN_BUDGET:
            errors.append(
                f"Estimated tokens ({plan_result.estimated_tokens}) exceed budget"
            )
        
        # Check task timeouts
        for task in plan_result.tasks:
            if task.timeout > self.MAX_TASK_DURATION:
                errors.append(
                    f"Task {task.task_id} timeout ({task.timeout}s) exceeds maximum"
                )
        
        if errors:
            logger.warning("FN:validate_dag Validation errors: %s", errors)
        
        return errors
    
    def export_dag(self, plan_result: PlanResult) -> str:
        """
        FN:export_dag Export DAG as Python file for Airflow.
        
        Args:
            plan_result: Plan result to export
            
        Returns:
            Path to exported DAG file
        """
        dag_id = plan_result.dag_config.dag_id
        output_path = Path(self._dags_dir) / f"{dag_id}.py"
        
        # Generate DAG code
        dag_code = self._generate_dag_code(plan_result)
        
        # Write to file
        output_path.write_text(dag_code)
        logger.info("FN:export_dag DAG exported to: %s", output_path)
        
        return str(output_path)
    
    def _generate_dag_code(self, plan_result: PlanResult) -> str:
        """
        FN:_generate_dag_code Generate Python code for Airflow DAG.
        
        Args:
            plan_result: Plan result to generate code for
            
        Returns:
            Python code string
        """
        config = plan_result.dag_config
        tasks = plan_result.tasks
        
        # Generate imports
        code_lines = [
            '"""',
            f"Auto-generated Airflow DAG: {config.dag_id}",
            f"Description: {config.description}",
            f"Generated: {plan_result.created_at}",
            f"Estimated tokens: {plan_result.estimated_tokens}",
            '"""',
            '',
            'from airflow import DAG',
            'from airflow.operators.python import PythonOperator',
            'from datetime import datetime, timedelta',
            '',
            f'# DAG Configuration',
            f'DAG_ID = "{config.dag_id}"',
            f'DESCRIPTION = "{config.description}"',
            f'SCHEDULE_INTERVAL = "{config.schedule_interval}"',
            f'MAX_ACTIVE_RUNS = {config.max_active_runs}',
            '',
            '# Default arguments',
            'default_args = {',
            '    "owner": "torro",',
            '    "depends_on_past": False,',
            '    "start_date": datetime(2026, 1, 1),',
            '    "email_on_failure": False,',
            '    "email_on_retry": False,',
            '    "retries": 1,',
            '    "retry_delay": timedelta(minutes=5),',
            '}',
            '',
            '# Create DAG',
            'dag = DAG(',
            '    DAG_ID,',
            '    schedule_interval=SCHEDULE_INTERVAL,',
            '    default_args=default_args,',
            '    catchup=False,',
            '    max_active_runs=MAX_ACTIVE_RUNS,',
            '    tags=["torro", "autonomous", "layer1"],',
            ')',
            '',
        ]
        
        # Generate task definitions
        for task in tasks:
            code_lines.extend([
                f'# Task: {task.task_id}',
                f'def {task.task_id}_func(**kwargs):',
                f'    """Execute task: {task.description}"""',
                f'    print("Executing {task.task_id}")',
                f'    # TODO: Implement task logic',
                f'    return {{"status": "completed"}}',
                '',
                f'{task.task_id} = PythonOperator(',
                f'    task_id="{task.task_id}",',
                f'    python_callable={task.task_id}_func,',
                f'    dag=dag,',
                f'    execution_timeout=timedelta(seconds={task.timeout}),',
                f'    retries={task.retries},',
                f'    retry_delay=timedelta(seconds={task.retry_delay}),',
                ')',
                '',
            ])
        
        # Generate dependencies
        for task in tasks:
            for dep in task.dependencies:
                code_lines.append(f'{dep} >> {task.task_id}')
        
        return "\n".join(code_lines)
    
    def get_plan_history(self, limit: int = 10) -> List[PlanResult]:
        """
        FN:get_plan_history Get recent planning history.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of PlanResult objects
        """
        return self._plan_history[-limit:]
    
    def set_token_budget(self, dag_id: str, budget: int):
        """
        FN:set_token_budget Set token budget for a DAG.
        
        Args:
            dag_id: DAG identifier
            budget: Token budget
        """
        self._token_budgets[dag_id] = budget
        logger.info("FN:set_token_budget Token budget set for %s: %d", dag_id, budget)
    
    def get_token_budget(self, dag_id: str) -> int:
        """
        FN:get_token_budget Get token budget for a DAG.
        
        Args:
            dag_id: DAG identifier
            
        Returns:
            Token budget
        """
        return self._token_budgets.get(dag_id, self.DEFAULT_TOKEN_BUDGET)


def generate_dag(
    planner: AgenticPlanner,
    dag_id: str,
    description: str,
    tasks: List[TaskConfig]
) -> PlanResult:
    """
    FN:generate_dag Standalone function for DAG generation.
    
    Args:
        planner: Planner instance
        dag_id: DAG identifier
        description: DAG description
        tasks: List of task configurations
        
    Returns:
        PlanResult
    """
    return planner.generate_dag(dag_id, description, tasks)
