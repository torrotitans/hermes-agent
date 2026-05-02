"""
FN:errors.py
Error classifier for Torro agent framework SRE.

Classes:
- ErrorClassifier: Classifies errors and suggests fixes
- ErrorCategory: Error category enumeration

Functions:
- FN:classify: Classify error message (lines 48-62)
- FN:get_suggested_fix: Get suggested fix for error category (lines 64-78)
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    """Error category enumeration."""
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    INTERNAL = "internal"
    UNKNOWN = "unknown"


@dataclass
class ErrorClassification:
    """Error classification result.
    
    Attributes:
        category: Error category
        confidence: Confidence score (0.0-1.0)
        suggested_fix: Suggested fix description
    """
    category: ErrorCategory
    confidence: float = 1.0
    suggested_fix: Optional[str] = None


# Error patterns for classification
ERROR_PATTERNS: Dict[ErrorCategory, List[str]] = {
    ErrorCategory.NETWORK: [
        r"connection refused",
        r"connection timed out",
        r"network unreachable",
        r"dns resolution failed",
    ],
    ErrorCategory.AUTHENTICATION: [
        r"unauthorized",
        r"authentication failed",
        r"invalid credentials",
        r"access denied",
    ],
    ErrorCategory.VALIDATION: [
        r"validation error",
        r"invalid input",
        r"required field",
        r"constraint violation",
    ],
    ErrorCategory.TIMEOUT: [
        r"timeout",
        r"timed out",
        r"deadline exceeded",
    ],
    ErrorCategory.RATE_LIMIT: [
        r"rate limit",
        r"too many requests",
        r"throttled",
    ],
    ErrorCategory.INTERNAL: [
        r"internal error",
        r"unexpected error",
        r"server error",
    ],
}

# Suggested fixes for each category
SUGGESTED_FIXES: Dict[ErrorCategory, str] = {
    ErrorCategory.NETWORK: "Check network connectivity and service endpoints",
    ErrorCategory.AUTHENTICATION: "Verify credentials and authentication tokens",
    ErrorCategory.VALIDATION: "Review input data against schema requirements",
    ErrorCategory.TIMEOUT: "Increase timeout settings or optimize query",
    ErrorCategory.RATE_LIMIT: "Implement exponential backoff or request rate limit increase",
    ErrorCategory.INTERNAL: "Contact support with error details and logs",
    ErrorCategory.UNKNOWN: "Review error logs and context for diagnosis",
}


class ErrorClassifier:
    """Classifies errors and suggests fixes.
    
    The ErrorClassifier uses pattern matching to categorize errors
    and provide actionable fix suggestions.
    
    Example:
        ```python
        classifier = ErrorClassifier()
        
        # Classify an error
        classification = classifier.classify("Connection refused to database")
        print(f"Category: {classification.category}")
        print(f"Fix: {classification.suggested_fix}")
        ```
    """
    
    def __init__(self):
        """Initialize the error classifier."""
        self._compiled_patterns: Dict[ErrorCategory, List[re.Pattern]] = {}
        self._compile_patterns()
        logger.info("FN:ErrorClassifier.__init__ Classifier initialized")
    
    def _compile_patterns(self) -> None:
        """FN:_compile_patterns Compile regex patterns for efficiency."""
        for category, patterns in ERROR_PATTERNS.items():
            self._compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def classify(self, error_message: str) -> ErrorClassification:
        """FN:classify Classify an error message.
        
        Args:
            error_message: Error message to classify
            
        Returns:
            ErrorClassification with category and suggested fix
        """
        logger.debug("FN:ErrorClassifier.classify Classifying: %s", error_message)
        
        # Check each category's patterns
        for category, patterns in self._compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(error_message):
                    logger.info("FN:ErrorClassifier.classify Classified as: %s", category.value)
                    return ErrorClassification(
                        category=category,
                        confidence=1.0,
                        suggested_fix=SUGGESTED_FIXES[category]
                    )
        
        # Default to unknown
        logger.warning("FN:ErrorClassifier.classify Unknown error category")
        return ErrorClassification(
            category=ErrorCategory.UNKNOWN,
            confidence=1.0,
            suggested_fix=SUGGESTED_FIXES[ErrorCategory.UNKNOWN]
        )
    
    def should_retry(self, error: Exception) -> bool:
        """FN:should_retry Determine if error is retryable.
        
        Args:
            error: Exception to evaluate
            
        Returns:
            True if the error should be retried
        """
        classification = self.classify(str(error))
        
        # Retryable errors
        retryable_categories = {
            ErrorCategory.NETWORK,
            ErrorCategory.TIMEOUT,
            ErrorCategory.RATE_LIMIT,
        }
        
        return classification.category in retryable_categories
    
    def get_suggested_fix(self, category: ErrorCategory) -> str:
        """FN:get_suggested_fix Get suggested fix for error category.
        
        Args:
            category: Error category
            
        Returns:
            Suggested fix description
        """
        return SUGGESTED_FIXES.get(category, SUGGESTED_FIXES[ErrorCategory.UNKNOWN])
