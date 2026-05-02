"""
FN:mode.py
Coordinator mode logic for Torro agent framework.

Functions:
- FN:is_coordinator_mode: Check if coordinator mode is enabled (lines 45-52)
- FN:get_coordinator_user_context: Get coordinator user context (lines 54-68)
- FN:spawn_worker_agent: Spawn a worker agent (lines 70-85)
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AgentHandle:
    """Handle for a spawned worker agent.
    
    Attributes:
        agent_id: Unique agent identifier
        status: Current agent status
        tools: List of tools available to the agent
        context: Agent context data
    """
    agent_id: str
    status: str = "running"
    tools: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_alive(self) -> bool:
        """Check if agent is still running."""
        return self.status == "running"
    
    def terminate(self) -> None:
        """Terminate the agent."""
        self.status = "terminated"


def is_coordinator_mode() -> bool:
    """FN:is_coordinator_mode Check if coordinator mode is enabled.
    
    Coordinator mode enables dynamic agent spawning for complex tasks.
    
    Returns:
        True if coordinator mode is enabled
    """
    return os.getenv("TORRO_COORDINATOR_MODE", "false").lower() == "true"


def get_coordinator_user_context(
    mcp_clients: Optional[List] = None,
    scratchpad_dir: Optional[str] = None
) -> Dict[str, str]:
    """FN:get_coordinator_user_context Get coordinator user context.
    
    Args:
        mcp_clients: List of MCP client connections
        scratchpad_dir: Directory for scratchpad files
        
    Returns:
        Context dict for coordinator agent
    """
    context = {
        "mode": "coordinator",
        "scratchpad_dir": scratchpad_dir or "/tmp/torro_scratchpad",
    }
    
    if mcp_clients:
        context["mcp_clients"] = [str(client) for client in mcp_clients]
    
    return context


def spawn_worker_agent(
    agent_name: str,
    tools: List[str],
    context: Dict[str, Any]
) -> AgentHandle:
    """FN:spawn_worker_agent Spawn a worker agent.
    
    Args:
        agent_name: Name for the new agent
        tools: List of tool names available to the agent
        context: Agent context data
        
    Returns:
        AgentHandle for the spawned agent
    """
    import uuid
    
    agent_id = str(uuid.uuid4())
    logger.info("FN:spawn_worker_agent Spawning agent: %s (%s)", agent_name, agent_id)
    
    handle = AgentHandle(
        agent_id=agent_id,
        status="running",
        tools=tools,
        context=context
    )
    
    return handle
