"""
FN:structured_io.py
Structured I/O layer for NDJSON communication in Torro CLI.

Classes:
- MessageType: Enum for message types
- Message: Base message class
- ControlRequest: Control request message
- ControlResponse: Control response message
- StructuredIO: Handles NDJSON parsing and serialization

Functions:
- FN:parse_message: Parse NDJSON message from stdin (lines 65-82)
- FN:serialize_message: Serialize message to NDJSON format (lines 84-100)
"""

import json
import sys
from enum import Enum
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, asdict


class MessageType(str, Enum):
    """Enum defining valid message types for NDJSON communication."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    CONTROL_REQUEST = "control_request"
    CONTROL_RESPONSE = "control_response"


@dataclass
class Message:
    """Structured message for NDJSON communication."""
    type: MessageType
    content: str
    session_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class ControlRequest:
    """
    Control request for tool permissions.
    Used to request user approval for dangerous operations.
    """
    request_id: str
    operation: str
    description: str
    risk_level: str = "medium"
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_message(self) -> Message:
        """Convert control request to Message object."""
        return Message(
            type=MessageType.CONTROL_REQUEST,
            content=self.description,
            metadata={
                "request_id": self.request_id,
                "operation": self.operation,
                "risk_level": self.risk_level,
                "details": self.details
            }
        )


@dataclass
class ControlResponse:
    """
    Control response for tool permissions.
    Used to communicate user approval or denial.
    """
    request_id: str
    approved: bool
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_message(self) -> Message:
        """Convert control response to Message object."""
        return Message(
            type=MessageType.CONTROL_RESPONSE,
            content="approved" if self.approved else "denied",
            metadata={
                "request_id": self.request_id,
                "approved": self.approved,
                "reason": self.reason
            }
        )


class StructuredIO:
    """
    Handles NDJSON (newline-delimited JSON) parsing and serialization
    for stdin/stdout communication in Torro CLI.
    """

    def __init__(self):
        """Initialize the structured I/O handler."""
        self.buffer = ""
        self._pending_requests: Dict[str, ControlRequest] = {}

    def parse_message(self, line: str) -> Optional[Message]:
        """
        FN:parse_message Parse a single NDJSON line into a Message object.

        Args:
            line: Raw JSON line from stdin

        Returns:
            Message object or None if parsing fails
        """
        try:
            data = json.loads(line.strip())
            return Message(
                type=MessageType(data.get("type", "user")),
                content=data.get("content", ""),
                session_id=data.get("session_id"),
                timestamp=data.get("timestamp"),
                metadata=data.get("metadata")
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing message: {e}", file=sys.stderr)
            return None

    def serialize_message(self, message: Message) -> str:
        """
        FN:serialize_message Convert a Message object to NDJSON format.

        Args:
            message: Message object to serialize

        Returns:
            JSON string with newline terminator
        """
        return json.dumps(message.to_dict()) + "\n"

    def read_message(self) -> Optional[Message]:
        """
        FN:read_message Read and parse a message from stdin.

        Returns:
            Message object or None if read fails
        """
        try:
            line = sys.stdin.readline()
            if not line:
                return None
            return self.parse_message(line)
        except IOError as e:
            print(f"Error reading from stdin: {e}", file=sys.stderr)
            return None

    def write_message(self, message: Message) -> bool:
        """
        FN:write_message Write a message to stdout in NDJSON format.

        Args:
            message: Message object to write

        Returns:
            True if successful, False otherwise
        """
        try:
            sys.stdout.write(self.serialize_message(message))
            sys.stdout.flush()
            return True
        except IOError as e:
            print(f"Error writing to stdout: {e}", file=sys.stderr)
            return False

    def send_control_request(self, request: ControlRequest) -> bool:
        """
        FN:send_control_request Send a control request for user approval.

        Args:
            request: Control request to send

        Returns:
            True if sent successfully
        """
        # Store pending request
        self._pending_requests[request.request_id] = request

        # Send as message
        return self.write_message(request.to_message())

    def receive_control_response(
        self,
        response: ControlResponse
    ) -> bool:
        """
        FN:receive_control_response Receive a control response.

        Args:
            response: Control response to process

        Returns:
            True if processed successfully
        """
        # Validate request ID exists
        if response.request_id not in self._pending_requests:
            print(
                f"Unknown request ID: {response.request_id}",
                file=sys.stderr
            )
            return False

        # Remove from pending
        del self._pending_requests[response.request_id]

        return True

    def get_pending_requests(self) -> List[ControlRequest]:
        """
        FN:get_pending_requests Get list of pending control requests.

        Returns:
            List of pending requests
        """
        return list(self._pending_requests.values())
