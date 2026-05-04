"""
FN:test_orchestrator.py
Unit tests for Torro autonomous layer orchestrator.

Tests:
- TestAgenticOrchestrator: Test orchestrator functions
- TestCircuitBreaker: Test circuit breaker functionality
"""

import pytest
import time
from unittest.mock import Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.autonomous.orchestrator import (
    AgenticOrchestrator,
    TaskType,
    TaskStatus,
    TaskResult,
    Task,
    CircuitBreakerError,
)


class TestAgenticOrchestrator:
    """Test agentic orchestrator functions."""
    
    def test_orchestrator_creation(self):
        """Test creating an orchestrator instance."""
        orchestrator = AgenticOrchestrator()
        assert orchestrator is not None
        assert orchestrator.pending_tasks == 0
        assert orchestrator.is_running is False
    
    def test_route_task_simple(self):
        """Test routing a simple task."""
        orchestrator = AgenticOrchestrator()
        task_id = orchestrator.route_task(
            task_type=TaskType.SIMPLE,
            description="Test task"
        )
        
        assert task_id is not None
        assert orchestrator.pending_tasks == 1
    
    def test_route_task_with_priority(self):
        """Test routing a task with priority."""
        orchestrator = AgenticOrchestrator()
        task_id = orchestrator.route_task(
            task_type=TaskType.COMPLEX,
            description="High priority task",
            priority=10
        )
        
        assert task_id is not None
        assert orchestrator.pending_tasks == 1
    
    def test_route_task_with_payload(self):
        """Test routing a task with payload."""
        orchestrator = AgenticOrchestrator()
        payload = {"key": "value", "data": [1, 2, 3]}
        task_id = orchestrator.route_task(
            task_type=TaskType.EXECUTION,
            description="Task with payload",
            payload=payload
        )
        
        assert task_id is not None
        assert orchestrator.pending_tasks == 1
    
    def test_get_task_status_queued(self):
        """Test getting status of queued task."""
        orchestrator = AgenticOrchestrator()
        task_id = orchestrator.route_task(
            task_type=TaskType.SIMPLE,
            description="Test task"
        )
        
        status = orchestrator.get_task_status(task_id)
        assert status == TaskStatus.PENDING
    
    def test_get_task_status_not_found(self):
        """Test getting status of non-existent task."""
        orchestrator = AgenticOrchestrator()
        status = orchestrator.get_task_status("non-existent-id")
        assert status is None
    
    def test_execute_task(self):
        """Test executing a task."""
        orchestrator = AgenticOrchestrator()
        task_id = orchestrator.route_task(
            task_type=TaskType.SIMPLE,
            description="Test task"
        )
        
        result = orchestrator.execute_task(task_id)
        
        assert result.task_id == task_id
        assert result.status == TaskStatus.COMPLETED
        assert result.error is None
    
    def test_execute_task_not_found(self):
        """Test executing a non-existent task."""
        orchestrator = AgenticOrchestrator()
        result = orchestrator.execute_task("non-existent-id")
        
        assert result.task_id == "non-existent-id"
        assert result.status == TaskStatus.FAILED
        assert "Task not found" in result.error
    
    def test_get_command_frequency(self):
        """Test getting command frequency."""
        orchestrator = AgenticOrchestrator()
        
        # Route some tasks (circuit breaker limits to 3)
        orchestrator.route_task(TaskType.SIMPLE, "cmd1")
        orchestrator.route_task(TaskType.SIMPLE, "cmd2")
        
        frequency = orchestrator.get_command_frequency()
        
        # Commands are recorded when executed, not when routed
        assert frequency == {}
    
    def test_get_frequent_commands(self):
        """Test getting frequent commands."""
        orchestrator = AgenticOrchestrator()
        
        # Route tasks (circuit breaker limits to 3)
        orchestrator.route_task(TaskType.SIMPLE, "frequent_cmd")
        orchestrator.route_task(TaskType.SIMPLE, "frequent_cmd")
        
        frequent = orchestrator.get_frequent_commands(threshold=2)
        
        # Commands are recorded when executed, not when routed
        assert frequent == []
    
    def test_reset_recursion_counter(self):
        """Test resetting recursion counter."""
        orchestrator = AgenticOrchestrator()
        
        # Trigger recursion counter
        for _ in range(3):
            orchestrator.route_task(TaskType.SIMPLE, "test")
        
        # Reset counter
        orchestrator.reset_recursion_counter("test")
        
        # Should not raise after reset
        orchestrator.route_task(TaskType.SIMPLE, "test")
    
    def test_get_task_history(self):
        """Test getting task history."""
        orchestrator = AgenticOrchestrator()
        
        # Execute some tasks
        for i in range(5):
            task_id = orchestrator.route_task(
                TaskType.SIMPLE,
                f"Task {i}"
            )
            orchestrator.execute_task(task_id)
        
        history = orchestrator.get_task_history(limit=3)
        
        assert len(history) == 3
    
    def test_circuit_breaker_triggers(self):
        """Test that circuit breaker triggers after repeated tasks."""
        orchestrator = AgenticOrchestrator()
        
        # Trigger circuit breaker
        for _ in range(3):
            orchestrator.route_task(
                TaskType.SIMPLE,
                "repeated_task"
            )
        
        # Fourth attempt should raise CircuitBreakerError
        with pytest.raises(CircuitBreakerError):
            orchestrator.route_task(
                TaskType.SIMPLE,
                "repeated_task"
            )
    
    def test_circuit_breaker_resets_after_window(self):
        """Test that circuit breaker resets after time window."""
        orchestrator = AgenticOrchestrator()
        orchestrator.RECUSION_WINDOW_SECONDS = 0.1  # 100ms for testing
        
        # Trigger circuit breaker
        for _ in range(3):
            orchestrator.route_task(
                TaskType.SIMPLE,
                "repeated_task"
            )
        
        # Wait for window to expire
        time.sleep(0.2)
        
        # Should not raise after window expires
        orchestrator.route_task(TaskType.SIMPLE, "repeated_task")


class TestTaskResult:
    """Test TaskResult dataclass."""
    
    def test_task_result_creation(self):
        """Test creating a task result."""
        result = TaskResult(
            task_id="test-123",
            status=TaskStatus.COMPLETED
        )
        
        assert result.task_id == "test-123"
        assert result.status == TaskStatus.COMPLETED
        assert result.result is None
        assert result.error is None
    
    def test_task_result_with_error(self):
        """Test creating a task result with error."""
        result = TaskResult(
            task_id="test-123",
            status=TaskStatus.FAILED,
            error="Something went wrong"
        )
        
        assert result.task_id == "test-123"
        assert result.status == TaskStatus.FAILED
        assert result.error == "Something went wrong"
    
    def test_task_result_with_metadata(self):
        """Test creating a task result with metadata."""
        result = TaskResult(
            task_id="test-123",
            status=TaskStatus.COMPLETED,
            result={"key": "value"},
            metadata={"extra": "data"}
        )
        
        assert result.result == {"key": "value"}
        assert result.metadata == {"extra": "data"}


class TestTask:
    """Test Task dataclass."""
    
    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            task_id="test-123",
            task_type=TaskType.SIMPLE,
            description="Test task",
            payload={}
        )
        
        assert task.task_id == "test-123"
        assert task.task_type == TaskType.SIMPLE
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_error_message(self):
        """Test circuit breaker error message."""
        error = CircuitBreakerError("Test error")
        assert str(error) == "Test error"
    
    def test_circuit_breaker_prevents_recursion(self):
        """Test that circuit breaker prevents infinite recursion."""
        orchestrator = AgenticOrchestrator()
        orchestrator.MAX_RECURSION_COUNT = 2
        
        # First two should succeed
        orchestrator.route_task(TaskType.SIMPLE, "recursive")
        orchestrator.route_task(TaskType.SIMPLE, "recursive")
        
        # Third should fail
        with pytest.raises(CircuitBreakerError):
            orchestrator.route_task(TaskType.SIMPLE, "recursive")
