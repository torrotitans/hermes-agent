"""
FN:clarification.py
Logic clarification manager for Torro CLI to detect and resolve ambiguity.

Classes:
- ClarificationManager: Handles ambiguity detection and clarification questions

Functions:
- FN:detect_ambiguity: Detect ambiguous terms in input (lines 45-65)
- FN:ask_clarification: Generate clarification questions (lines 67-100)
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


# Ambiguity patterns to detect
AMBIGUITY_PATTERNS = {
    "vague_quantity": [
        r"\b(some|many|few|several|a lot|lots|plenty)\b",
        r"\b(more|less|fewer)\s+\w+\b",
    ],
    "vague_time": [
        r"\b(soon|later|ASAP|quickly|slowly|eventually)\b",
        r"\b(in a|within)\s+\d+\s+\w+\b",
    ],
    "vague_reference": [
        r"\b(this|that|these|those|it|thing|stuff)\b",
        r"\b(something|anything|everything|nothing)\b",
    ],
    "incomplete_requirement": [
        r"\b(etc|and so on|and more|and other)\b",
        r"\b(maybe|perhaps|possibly|probably)\b",
    ],
}


@dataclass
class ClarificationRequest:
    """Structured clarification request."""
    field: str
    question: str
    suggestions: List[str]
    required: bool = True


class ClarificationManager:
    """
    Manages logic clarification for Torro CLI.
    Detects ambiguous requirements and generates clarification questions.
    """

    def __init__(self):
        """Initialize the clarification manager."""
        self._pending_requests: List[ClarificationRequest] = []
        self._clarified_values: Dict[str, Any] = {}

    def detect_ambiguity(self, text: str) -> List[str]:
        """
        FN:detect_ambiguity Detect ambiguous terms in input text.

        Args:
            text: Input text to analyze

        Returns:
            List of detected ambiguity types
        """
        detected = []
        text_lower = text.lower()

        for category, patterns in AMBIGUITY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected.append(category)
                    break  # One match per category is enough

        return detected

    def generate_clarification_questions(
        self,
        ambiguity_types: List[str]
    ) -> List[ClarificationRequest]:
        """
        FN:generate_clarification_questions Generate questions for detected ambiguities.

        Args:
            ambiguity_types: List of ambiguity types detected

        Returns:
            List of ClarificationRequest objects
        """
        questions = []

        question_templates = {
            "vague_quantity": ClarificationRequest(
                field="quantity",
                question="What specific quantity or number do you need?",
                suggestions=["1", "5", "10", "All"],
                required=True
            ),
            "vague_time": ClarificationRequest(
                field="timeframe",
                question="What is the specific deadline or timeframe?",
                suggestions=["1 hour", "1 day", "1 week", "End of sprint"],
                required=True
            ),
            "vague_reference": ClarificationRequest(
                field="reference",
                question="What specifically are you referring to?",
                suggestions=["The user module", "The API layer", "The database schema"],
                required=True
            ),
            "incomplete_requirement": ClarificationRequest(
                field="requirements",
                question="Can you specify the complete requirements?",
                suggestions=["List all requirements", "Provide examples", "Define acceptance criteria"],
                required=True
            ),
        }

        for ambiguity in ambiguity_types:
            if ambiguity in question_templates:
                questions.append(question_templates[ambiguity])

        return questions

    def ask_clarification(
        self,
        input_text: str
    ) -> List[ClarificationRequest]:
        """
        FN:ask_clarification Main method to detect ambiguity and generate questions.

        Args:
            input_text: User input to clarify

        Returns:
            List of ClarificationRequest objects
        """
        # Detect ambiguity
        ambiguities = self.detect_ambiguity(input_text)

        # Generate questions
        questions = self.generate_clarification_questions(ambiguities)

        # Store pending requests
        self._pending_requests.extend(questions)

        return questions

    def add_clarified_value(self, field: str, value: Any):
        """
        FN:add_clarified_value Store a clarified value.

        Args:
            field: Field name
            value: Clarified value
        """
        self._clarified_values[field] = value

    def get_clarified_values(self) -> Dict[str, Any]:
        """
        FN:get_clarified_values Get all clarified values.

        Returns:
            Dictionary of clarified values
        """
        return self._clarified_values.copy()

    def clear_pending(self):
        """
        FN:clear_pending Clear all pending clarification requests.
        """
        self._pending_requests = []

    @property
    def has_pending(self) -> bool:
        """
        FN:has_pending Check if there are pending clarification requests.

        Returns:
            True if there are pending requests
        """
        return len(self._pending_requests) > 0


def detect_ambiguity(text: str) -> List[str]:
    """
    FN:detect_ambiguity Standalone function to detect ambiguity.

    Args:
        text: Input text

    Returns:
        List of ambiguity types
    """
    manager = ClarificationManager()
    return manager.detect_ambiguity(text)


def ask_clarification(text: str) -> List[ClarificationRequest]:
    """
    FN:ask_clarification Standalone function for clarification.

    Args:
        text: Input text

    Returns:
        List of ClarificationRequest objects
    """
    manager = ClarificationManager()
    return manager.ask_clarification(text)
