"""
FN:permission_mgr.py
Permission manager for tool access control in Torro CLI.

Classes:
- PermissionLevel: Enum for permission levels
- PermissionManager: Manages tool permissions and approval requests

Functions:
- FN:check_permission: Check if operation is allowed (lines 50-70)
- FN:request_permission: Request user approval for operation (lines 72-100)
"""

from enum import Enum
from typing import Optional, Dict, List, Any
from dataclasses import dataclass


class PermissionLevel(str, Enum):
    """Enum for permission levels."""
    BYPASS = "bypass"  # No permission needed
    AUTO = "auto"  # Auto-approve safe operations
    ASK = "ask"  # Always ask user
    DENY = "deny"  # Always deny


# Default permission rules for common operations
DEFAULT_PERMISSION_RULES = {
    "read_file": PermissionLevel.AUTO,
    "write_file": PermissionLevel.ASK,
    "delete_file": PermissionLevel.ASK,
    "execute_command": PermissionLevel.ASK,
    "access_network": PermissionLevel.ASK,
    "access_database": PermissionLevel.DENY,
}


@dataclass
class PermissionRequest:
    """Structured permission request."""
    operation: str
    description: str
    risk_level: str  # "low", "medium", "high"
    details: Optional[Dict[str, Any]] = None
    auto_approve: bool = False


class PermissionManager:
    """
    Manages tool permissions and access control for Torro CLI.
    Provides granular control over dangerous operations.
    """

    def __init__(
        self,
        default_level: PermissionLevel = PermissionLevel.ASK
    ):
        """
        Initialize the permission manager.

        Args:
            default_level: Default permission level for unknown operations
        """
        self.default_level = default_level
        self._rules = DEFAULT_PERMISSION_RULES.copy()
        self._granted: Dict[str, bool] = {}
        self._denied: Dict[str, bool] = {}

    def set_permission_level(
        self,
        operation: str,
        level: PermissionLevel
    ):
        """
        FN:set_permission_level Set permission level for an operation.

        Args:
            operation: Operation name
            level: Permission level
        """
        self._rules[operation] = level

    def get_permission_level(self, operation: str) -> PermissionLevel:
        """
        FN:get_permission_level Get permission level for an operation.

        Args:
            operation: Operation name

        Returns:
            Permission level
        """
        return self._rules.get(operation, self.default_level)

    def check_permission(self, operation: str) -> bool:
        """
        FN:check_permission Check if operation is allowed without prompting.

        Args:
            operation: Operation name

        Returns:
            True if allowed, False if needs approval
        """
        level = self.get_permission_level(operation)

        if level == PermissionLevel.BYPASS:
            return True
        elif level == PermissionLevel.AUTO:
            return True
        elif level == PermissionLevel.DENY:
            return False
        else:
            return False

    def request_permission(
        self,
        request: PermissionRequest
    ) -> bool:
        """
        FN:request_permission Request user approval for an operation.

        Args:
            request: Permission request details

        Returns:
            True if granted, False if denied
        """
        # Check if already decided
        if request.operation in self._granted:
            return True
        if request.operation in self._denied:
            return False

        # Auto-approve if configured
        if request.auto_approve:
            self._granted[request.operation] = True
            return True

        # Check permission level
        level = self.get_permission_level(request.operation)
        if level == PermissionLevel.DENY:
            self._denied[request.operation] = True
            return False
        elif level == PermissionLevel.BYPASS:
            self._granted[request.operation] = True
            return True

        # For ASK level, we would prompt user here
        # For now, default to deny
        self._denied[request.operation] = True
        return False

    def grant_permission(self, operation: str):
        """
        FN:grant_permission Grant permission for an operation.

        Args:
            operation: Operation name
        """
        self._granted[operation] = True
        if operation in self._denied:
            del self._denied[operation]

    def deny_permission(self, operation: str):
        """
        FN:deny_permission Deny permission for an operation.

        Args:
            operation: Operation name
        """
        self._denied[operation] = True
        if operation in self._granted:
            del self._granted[operation]

    def reset_permissions(self):
        """
        FN:reset_permissions Reset all granted/denied permissions.
        """
        self._granted = {}
        self._denied = {}

    def get_pending_operations(self) -> List[str]:
        """
        FN:get_pending_operations Get list of operations awaiting decision.

        Returns:
            List of operation names
        """
        # Operations that have rules but no decision yet
        pending = []
        for op in self._rules.keys():
            if op not in self._granted and op not in self._denied:
                pending.append(op)
        return pending


def check_permission(operation: str, manager: Optional[PermissionManager] = None) -> bool:
    """
    FN:check_permission Standalone function to check permission.

    Args:
        operation: Operation name
        manager: Optional permission manager

    Returns:
        True if allowed
    """
    if manager is None:
        manager = PermissionManager()
    return manager.check_permission(operation)


def request_permission(
    operation: str,
    description: str,
    risk_level: str = "medium",
    manager: Optional[PermissionManager] = None
) -> bool:
    """
    FN:request_permission Standalone function to request permission.

    Args:
        operation: Operation name
        description: Operation description
        risk_level: Risk level
        manager: Optional permission manager

    Returns:
        True if granted
    """
    if manager is None:
        manager = PermissionManager()

    request = PermissionRequest(
        operation=operation,
        description=description,
        risk_level=risk_level
    )
    return manager.request_permission(request)
