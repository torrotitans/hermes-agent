"""
FN:test_mode.py
Unit tests for Torro coordinator mode.

Tests:
- TestCoordinatorMode: Test coordinator mode functions
- TestAgentHandle: Test agent handle class
"""

import pytest
from unittest.mock import Mock, patch

from coordinator.mode import (
    is_coordinator_mode,
    get_coordinator_user_context,
    spawn_worker_agent,
    AgentHandle,
)


class TestCoordinatorMode:
    """Test coordinator mode functions."""
    
    def test_is_coordinator_mode_false(self, monkeypatch):
        """Test is_coordinator_mode returns False by default."""
        monkeypatch.delenv("TORRO_COORDINATOR_MODE", raising=False)
        assert is_coordinator_mode() is False
    
    def test_is_coordinator_mode_true(self, monkeypatch):
        """Test is_coordinator_mode returns True when enabled."""
        monkeypatch.setenv("TORRO_COORDINATOR_MODE", "true")
        assert is_coordinator_mode() is True
    
    def test_is_coordinator_mode_case_insensitive(self, monkeypatch):
        """Test is_coordinator_mode is case insensitive."""
        monkeypatch.setenv("TORRO_COORDINATOR_MODE", "TRUE")
        assert is_coordinator_mode() is True
        
        monkeypatch.setenv("TORRO_COORDINATOR_MODE", "True")
        assert is_coordinator_mode() is True


class TestGetCoordinatorUserContext:
    """Test get_coordinator_user_context function."""
    
    def test_get_coordinator_user_context_defaults(self):
        """Test get_coordinator_user_context with default values."""
        context = get_coordinator_user_context()
        assert context["mode"] == "coordinator"
        assert context["scratchpad_dir"] == "/tmp/torro_scratchpad"
    
    def test_get_coordinator_user_context_custom_scratchpad(self):
        """Test get_coordinator_user_context with custom scratchpad."""
        context = get_coordinator_user_context(
            scratchpad_dir="/custom/scratchpad"
        )
        assert context["scratchpad_dir"] == "/custom/scratchpad"
    
    def test_get_coordinator_user_context_with_mcp_clients(self):
        """Test get_coordinator_user_context with MCP clients."""
        mock_clients = [Mock(), Mock()]
        context = get_coordinator_user_context(mcp_clients=mock_clients)
        assert "mcp_clients" in context
        assert len(context["mcp_clients"]) == 2


class TestSpawnWorkerAgent:
    """Test spawn_worker_agent function."""
    
    def test_spawn_worker_agent_basic(self):
        """Test spawning a basic worker agent."""
        handle = spawn_worker_agent(
            agent_name="test_agent",
            tools=["read", "write"],
            context={"key": "value"}
        )
        
        assert handle.agent_id is not None
        assert handle.status == "running"
        assert handle.tools == ["read", "write"]
        assert handle.context == {"key": "value"}
    
    def test_spawn_worker_agent_generates_unique_id(self):
        """Test that each spawned agent gets a unique ID."""
        handle1 = spawn_worker_agent("agent1", [], {})
        handle2 = spawn_worker_agent("agent2", [], {})
        
        assert handle1.agent_id != handle2.agent_id


class TestAgentHandle:
    """Test AgentHandle class."""
    
    def test_agent_handle_creation(self):
        """Test creating an agent handle."""
        handle = AgentHandle(agent_id="test-123")
        assert handle.agent_id == "test-123"
        assert handle.status == "running"
        assert handle.tools == []
        assert handle.context == {}
    
    def test_agent_handle_with_tools(self):
        """Test creating an agent handle with tools."""
        handle = AgentHandle(
            agent_id="test-123",
            tools=["tool1", "tool2"],
            context={"key": "value"}
        )
        assert handle.tools == ["tool1", "tool2"]
        assert handle.context == {"key": "value"}
    
    def test_agent_handle_is_alive(self):
        """Test agent handle is_alive method."""
        handle = AgentHandle(agent_id="test-123")
        assert handle.is_alive() is True
        
        handle.status = "completed"
        assert handle.is_alive() is False
    
    def test_agent_handle_terminate(self):
        """Test agent handle terminate method."""
        handle = AgentHandle(agent_id="test-123")
        assert handle.status == "running"
        
        handle.terminate()
        assert handle.status == "terminated"
        assert handle.is_alive() is False
