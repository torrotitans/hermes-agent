"""
FN:test_errors.py
Unit tests for Torro error classifier.

Tests:
- TestErrorCategory: Test ErrorCategory enum
- TestErrorClassification: Test ErrorClassification dataclass
- TestErrorClassifier: Test ErrorClassifier class
"""

import pytest
from unittest.mock import patch

from sre.errors import (
    ErrorCategory,
    ErrorClassification,
    ErrorClassifier,
    ERROR_PATTERNS,
    SUGGESTED_FIXES,
)


class TestErrorCategory:
    """Test ErrorCategory enum."""
    
    def test_error_category_values(self):
        """Test ErrorCategory enum values."""
        assert ErrorCategory.NETWORK.value == "network"
        assert ErrorCategory.AUTHENTICATION.value == "authentication"
        assert ErrorCategory.VALIDATION.value == "validation"
        assert ErrorCategory.TIMEOUT.value == "timeout"
        assert ErrorCategory.RATE_LIMIT.value == "rate_limit"
        assert ErrorCategory.INTERNAL.value == "internal"
        assert ErrorCategory.UNKNOWN.value == "unknown"


class TestErrorClassification:
    """Test ErrorClassification dataclass."""
    
    def test_error_classification_defaults(self):
        """Test ErrorClassification default values."""
        classification = ErrorClassification(category=ErrorCategory.UNKNOWN)
        assert classification.category == ErrorCategory.UNKNOWN
        assert classification.confidence == 1.0
        assert classification.suggested_fix is None
    
    def test_error_classification_custom(self):
        """Test ErrorClassification with custom values."""
        classification = ErrorClassification(
            category=ErrorCategory.NETWORK,
            confidence=0.9,
            suggested_fix="Check network"
        )
        assert classification.category == ErrorCategory.NETWORK
        assert classification.confidence == 0.9
        assert classification.suggested_fix == "Check network"


class TestErrorClassifier:
    """Test ErrorClassifier class."""
    
    def test_error_classifier_init(self):
        """Test ErrorClassifier initialization."""
        classifier = ErrorClassifier()
        assert classifier._compiled_patterns is not None
    
    def test_classify_network_error(self):
        """Test classifying network error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Connection refused to database")
        
        assert result.category == ErrorCategory.NETWORK
        assert result.confidence == 1.0
        assert "network" in result.suggested_fix.lower()
    
    def test_classify_authentication_error(self):
        """Test classifying authentication error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Authentication failed: invalid token")
        
        assert result.category == ErrorCategory.AUTHENTICATION
        assert result.confidence == 1.0
    
    def test_classify_validation_error(self):
        """Test classifying validation error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Validation error: missing required field")
        
        assert result.category == ErrorCategory.VALIDATION
        assert result.confidence == 1.0
    
    def test_classify_timeout_error(self):
        """Test classifying timeout error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Request timed out after 30 seconds")
        
        assert result.category == ErrorCategory.TIMEOUT
        assert result.confidence == 1.0
    
    def test_classify_rate_limit_error(self):
        """Test classifying rate limit error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Rate limit exceeded: too many requests")
        
        assert result.category == ErrorCategory.RATE_LIMIT
        assert result.confidence == 1.0
    
    def test_classify_internal_error(self):
        """Test classifying internal error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Internal server error occurred")
        
        assert result.category == ErrorCategory.INTERNAL
        assert result.confidence == 1.0
    
    def test_classify_unknown_error(self):
        """Test classifying unknown error."""
        classifier = ErrorClassifier()
        result = classifier.classify("Some random error message")
        
        assert result.category == ErrorCategory.UNKNOWN
        assert result.confidence == 1.0
    
    def test_should_retry_network_error(self):
        """Test should_retry for network error."""
        classifier = ErrorClassifier()
        error = Exception("Connection refused")
        
        assert classifier.should_retry(error) is True
    
    def test_should_retry_timeout_error(self):
        """Test should_retry for timeout error."""
        classifier = ErrorClassifier()
        error = Exception("Request timed out")
        
        assert classifier.should_retry(error) is True
    
    def test_should_retry_rate_limit_error(self):
        """Test should_retry for rate limit error."""
        classifier = ErrorClassifier()
        error = Exception("Rate limit exceeded")
        
        assert classifier.should_retry(error) is True
    
    def test_should_retry_validation_error(self):
        """Test should_retry for validation error."""
        classifier = ErrorClassifier()
        error = Exception("Validation failed")
        
        assert classifier.should_retry(error) is False
    
    def test_get_suggested_fix(self):
        """Test getting suggested fix."""
        classifier = ErrorClassifier()
        
        fix = classifier.get_suggested_fix(ErrorCategory.NETWORK)
        assert "network" in fix.lower()
        
        fix = classifier.get_suggested_fix(ErrorCategory.AUTHENTICATION)
        assert "credential" in fix.lower() or "authentication" in fix.lower()
    
    def test_get_suggested_fix_unknown(self):
        """Test getting suggested fix for unknown category."""
        classifier = ErrorClassifier()
        fix = classifier.get_suggested_fix(ErrorCategory.UNKNOWN)
        assert fix is not None
