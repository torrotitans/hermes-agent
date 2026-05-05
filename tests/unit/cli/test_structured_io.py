"""
FN:test_structured_io.py
Unit tests for StructuredIO class.

Functions:
- FN:test_message_creation: Test message creation (lines 20-40)
- FN:test_control_request: Test control request (lines 43-60)
- FN:test_parse_message: Test NDJSON parsing (lines 63-85)
- FN:test_serialize_message: Test message serialization (lines 88-105)
"""

import unittest
import sys
import json
from io import StringIO
from unittest.mock import patch, MagicMock

# Import CLI components
sys.path.insert(0, 'src')
from cli.structured_io import StructuredIO, Message, MessageType, ControlRequest, ControlResponse


class TestMessageTypes(unittest.TestCase):
    """Test cases for MessageType enum."""
    
    def test_message_type_values(self):
        """FN:test_message_type_values Test MessageType enum values."""
        self.assertEqual(MessageType.USER.value, "user")
        self.assertEqual(MessageType.ASSISTANT.value, "assistant")
        self.assertEqual(MessageType.SYSTEM.value, "system")
        self.assertEqual(MessageType.CONTROL_REQUEST.value, "control_request")
        self.assertEqual(MessageType.CONTROL_RESPONSE.value, "control_response")


class TestMessage(unittest.TestCase):
    """Test cases for Message dataclass."""
    
    def test_message_creation(self):
        """FN:test_message_creation Test basic message creation."""
        msg = Message(
            type=MessageType.USER,
            content="Hello, World!"
        )
        
        self.assertEqual(msg.type, MessageType.USER)
        self.assertEqual(msg.content, "Hello, World!")
        self.assertIsNone(msg.session_id)
        self.assertIsNone(msg.timestamp)
        self.assertIsNone(msg.metadata)
    
    def test_message_with_metadata(self):
        """FN:test_message_with_metadata Test message with metadata."""
        msg = Message(
            type=MessageType.SYSTEM,
            content="System notification",
            session_id="session_123",
            metadata={"priority": "high"}
        )
        
        self.assertEqual(msg.session_id, "session_123")
        self.assertEqual(msg.metadata, {"priority": "high"})
    
    def test_message_to_dict(self):
        """FN:test_message_to_dict Test message to dictionary conversion."""
        msg = Message(
            type=MessageType.ASSISTANT,
            content="Response text"
        )
        
        result = msg.to_dict()
        
        self.assertEqual(result["type"], "assistant")
        self.assertEqual(result["content"], "Response text")


class TestControlRequest(unittest.TestCase):
    """Test cases for ControlRequest dataclass."""
    
    def test_control_request_creation(self):
        """FN:test_control_request_creation Test control request creation."""
        req = ControlRequest(
            request_id="req_123",
            operation="file_write",
            description="Write to file",
            risk_level="high"
        )
        
        self.assertEqual(req.request_id, "req_123")
        self.assertEqual(req.operation, "file_write")
        self.assertEqual(req.risk_level, "high")
    
    def test_control_request_to_dict(self):
        """FN:test_control_request_to_dict Test control request to dict."""
        req = ControlRequest(
            request_id="req_456",
            operation="delete",
            description="Delete file"
        )
        
        result = req.to_dict()
        
        self.assertEqual(result["request_id"], "req_456")
        self.assertEqual(result["operation"], "delete")
    
    def test_control_request_to_message(self):
        """FN:test_control_request_to_message Test conversion to Message."""
        req = ControlRequest(
            request_id="req_789",
            operation="execute",
            description="Run command"
        )
        
        msg = req.to_message()
        
        self.assertEqual(msg.type, MessageType.CONTROL_REQUEST)
        self.assertEqual(msg.content, "Run command")
        self.assertEqual(msg.metadata["request_id"], "req_789")


class TestControlResponse(unittest.TestCase):
    """Test cases for ControlResponse dataclass."""
    
    def test_control_response_creation(self):
        """FN:test_control_response_creation Test control response creation."""
        resp = ControlResponse(
            request_id="req_123",
            approved=True,
            reason="User approved"
        )
        
        self.assertEqual(resp.request_id, "req_123")
        self.assertTrue(resp.approved)
        self.assertEqual(resp.reason, "User approved")
    
    def test_control_response_to_message(self):
        """FN:test_control_response_to_message Test conversion to Message."""
        resp = ControlResponse(
            request_id="req_456",
            approved=False,
            reason="User denied"
        )
        
        msg = resp.to_message()
        
        self.assertEqual(msg.type, MessageType.CONTROL_RESPONSE)
        self.assertEqual(msg.content, "denied")


class TestStructuredIO(unittest.TestCase):
    """Test cases for StructuredIO class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sio = StructuredIO()
    
    def test_parse_valid_message(self):
        """FN:test_parse_valid_message Test parsing valid NDJSON message."""
        json_line = '{"type": "user", "content": "Hello"}\n'
        result = self.sio.parse_message(json_line)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.type, MessageType.USER)
        self.assertEqual(result.content, "Hello")
    
    def test_parse_invalid_json(self):
        """FN:test_parse_invalid_json Test parsing invalid JSON."""
        json_line = 'not valid json\n'
        result = self.sio.parse_message(json_line)
        
        self.assertIsNone(result)
    
    def test_parse_missing_fields(self):
        """FN:test_parse_missing_fields Test parsing message with missing fields."""
        json_line = '{"content": "Hello"}\n'
        result = self.sio.parse_message(json_line)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.type, MessageType.USER)
        self.assertEqual(result.content, "Hello")
    
    def test_serialize_message(self):
        """FN:test_serialize_message Test message serialization."""
        msg = Message(
            type=MessageType.ASSISTANT,
            content="Response"
        )
        
        result = self.sio.serialize_message(msg)
        parsed = json.loads(result.strip())
        
        self.assertEqual(parsed["type"], "assistant")
        self.assertEqual(parsed["content"], "Response")
        self.assertTrue(result.endswith("\n"))
    
    def test_read_message(self):
        """FN:test_read_message Test reading message from stdin."""
        with patch('sys.stdin.readline', return_value='{"type": "user", "content": "test"}\n'):
            result = self.sio.read_message()
            
            self.assertIsNotNone(result)
            self.assertEqual(result.type, MessageType.USER)
            self.assertEqual(result.content, "test")
    
    def test_write_message(self):
        """FN:test_write_message Test writing message to stdout."""
        msg = Message(
            type=MessageType.SYSTEM,
            content="Test message"
        )
        
        with patch('sys.stdout.write') as mock_write:
            with patch('sys.stdout.flush') as mock_flush:
                result = self.sio.write_message(msg)
                
                self.assertTrue(result)
                mock_write.assert_called_once()
                mock_flush.assert_called_once()
    
    def test_send_control_request(self):
        """FN:test_send_control_request Test sending control request."""
        req = ControlRequest(
            request_id="test_req",
            operation="test_op",
            description="Test operation"
        )
        
        with patch.object(self.sio, 'write_message') as mock_write:
            result = self.sio.send_control_request(req)
            
            self.assertTrue(result)
            self.assertIn("test_req", self.sio._pending_requests)
    
    def test_receive_control_response(self):
        """FN:test_receive_control_response Test receiving control response."""
        # First send a request
        req = ControlRequest(
            request_id="resp_test",
            operation="test",
            description="Test"
        )
        self.sio.send_control_request(req)
        
        # Then receive response
        resp = ControlResponse(
            request_id="resp_test",
            approved=True
        )
        result = self.sio.receive_control_response(resp)
        
        self.assertTrue(result)
        self.assertNotIn("resp_test", self.sio._pending_requests)
    
    def test_get_pending_requests(self):
        """FN:test_get_pending_requests Test getting pending requests."""
        req = ControlRequest(
            request_id="pending_test",
            operation="test",
            description="Test"
        )
        self.sio.send_control_request(req)
        
        pending = self.sio.get_pending_requests()
        
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].request_id, "pending_test")


if __name__ == '__main__':
    unittest.main()
