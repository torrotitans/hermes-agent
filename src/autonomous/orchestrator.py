"""
FN:orchestrator.py
Agentic Orchestrator for Layer 1 Autonomous Layer in Torro Agent.

Classes:
- TaskType: Enum for task types
- TaskResult: Result of task execution
- AgenticOrchestrator: Main orchestrator class

Functions:
- FN:route_task: Route task to appropriate handler (lines 85-120)
- FN:check_recursion: Check for recursion patterns (lines 122-145)
"""

import logging
import time
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    """Enum for task types handled by orchestrator."""
    SIMPLE = "simple"
    COMPLEX = "complex"
    PLANNING = "planning"
    EXECUTION = "execution"
    RESEARCH = "research"


class TaskStatus(str, Enum):
    """Enum for task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"


@dataclass
class TaskResult:
    """Result of task execution."""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Task definition for orchestration."""
    task_id: str
    task_type: TaskType
    description: str
    payload: Dict[str, Any]
    priority: int = 0
    created_at: float = field(default_factory=time.time)
    status: TaskStatus = TaskStatus.PENDING


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker threshold is exceeded."""
    pass


class AgenticOrchestrator:
    """
    Agentic Orchestrator for Layer 1 Autonomous Layer.
    Manages task routing, circuit breaking, and execution tracking.
    
    Responsibilities:
    - Route tasks to planner or direct execution
    - Implement circuit breaker for recursion prevention
    - Track task execution metrics
    - Manage task queue and priorities
    """
    
    # Circuit breaker configuration
    MAX_RECURSION_COUNT = 3
    RECUSION_WINDOW_SECONDS = 300  # 5 minutes
    
    def __init__(self):
        """Initialize the agentic orchestrator."""
        self._task_queue: List[Task] = []
        self._task_history: Dict[str, TaskResult] = {}
        self._recursion_counter: Dict[str, List[float]] = defaultdict(list)
        self._command_history: Dict[str, int] = defaultdict(int)
        self._is_running = False
        
    def route_task(
        self,
        task_type: TaskType,
        description: str,
        payload: Optional[Dict[str, Any]] = None,
        priority: int = 0
    ) -> str:
        """
        FN:route_task Route task to appropriate handler.
        
        Args:
            task_type: Type of task
            description: Task description
            payload: Task payload data
            priority: Task priority (higher = more urgent)
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        # Check circuit breaker
        self._check_recursion(description)
        
        # Create task
        task = Task(
            task_id=task_id,
            task_type=task_type,
            description=description,
            payload=payload or {},
            priority=priority
        )
        
        # Add to queue
        self._task_queue.append(task)
        logger.info("FN:route_task Task routed: %s (%s)", task_id, task_type.value)
        
        return task_id
    
    def _check_recursion(self, description: str):
        """
        FN:_check_recursion Check for recursion patterns and trigger circuit breaker.
        
        Args:
            description: Task description to check
            
        Raises:
            CircuitBreakerError: If recursion threshold exceeded
        """
        now = time.time()
        
        # Clean old entries
        self._recursion_counter[description] = [
            t for t in self._recursion_counter[description]
            if now - t < self.RECUSION_WINDOW_SECONDS
        ]
        
        # Check threshold
        if len(self._recursion_counter[description]) >= self.MAX_RECURSION_COUNT:
            raise CircuitBreakerError(
                f"Circuit breaker triggered: '{description}' repeated "
                f"{len(self._recursion_counter[description])} times in "
                f"{self.RECUSION_WINDOW_SECONDS}s window"
            )
        
        # Record this attempt
        self._recursion_counter[description].append(now)
        logger.debug("FN:_check_recursion Recursion check passed for: %s", description)
    
    def execute_task(self, task_id: str) -> TaskResult:
        """
        FN:execute_task Execute a queued task.
        
        Args:
            task_id: ID of task to execute
            
        Returns:
            TaskResult with execution outcome
        """
        # Find task
        task = None
        for i, t in enumerate(self._task_queue):
            if t.task_id == task_id:
                task = self._task_queue.pop(i)
                break
        
        if not task:
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error=f"Task not found: {task_id}"
            )
        
        # Execute task
        start_time = time.time()
        task.status = TaskStatus.RUNNING
        self._is_running = True
        
        try:
            # Simulate task execution (to be implemented by planner)
            logger.info("FN:execute_task Executing task: %s", task_id)
            
            # Record command frequency
            self._command_history[task.description] += 1
            
            # Create result
            result = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                result={"message": "Task completed successfully"},
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            result = TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error=str(e),
                execution_time=time.time() - start_time
            )
        
        # Store in history
        self._task_history[task_id] = result
        self._is_running = False
        
        return result
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        FN:get_task_status Get status of a task.
        
        Args:
            task_id: Task ID to check
            
        Returns:
            TaskStatus or None if not found
        """
        # Check queue
        for task in self._task_queue:
            if task.task_id == task_id:
                return task.status
        
        # Check history
        if task_id in self._task_history:
            return self._task_history[task_id].status
        
        return None
    
    def get_command_frequency(self) -> Dict[str, int]:
        """
        FN:get_command_frequency Get frequency count of commands.
        
        Returns:
            Dictionary mapping command descriptions to frequency
        """
        return dict(self._command_history)
    
    def get_frequent_commands(self, threshold: int = 3) -> List[str]:
        """
        FN:get_frequent_commands Get list of frequently used commands.
        
        Args:
            threshold: Minimum frequency to be considered frequent
            
        Returns:
            List of command descriptions
        """
        return [
            cmd for cmd, count in self._command_history.items()
            if count >= threshold
        ]
    
    def reset_recursion_counter(self, description: Optional[str] = None):
        """
        FN:reset_recursion_counter Reset recursion counter.
        
        Args:
            description: Specific description to reset, or None for all
        """
        if description:
            self._recursion_counter[description] = []
        else:
            self._recursion_counter.clear()
    
    def get_task_history(self, limit: int = 10) -> List[TaskResult]:
        """
        FN:get_task_history Get recent task history.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of TaskResult objects
        """
        return list(self._task_history.values())[-limit:]
    
    @property
    def is_running(self) -> bool:
        """Check if orchestrator is currently executing a task."""
        return self._is_running
    
    @property
    def pending_tasks(self) -> int:
        """Get count of pending tasks."""
        return len(self._task_queue)


def route_task(
    orchestrator: AgenticOrchestrator,
    task_type: TaskType,
    description: str,
    payload: Optional[Dict[str, Any]] = None
) -> str:
    """
    FN:route_task Standalone function for task routing.
    
    Args:
        orchestrator: Orchestrator instance
        task_type: Task type
        description: Task description
        payload: Task payload
        
    Returns:
        Task ID
    """
    return orchestrator.route_task(task_type, description, payload)
