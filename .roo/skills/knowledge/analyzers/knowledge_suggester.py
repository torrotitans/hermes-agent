"""
FN:knowledge_suggester Module
Package: .roo.skills.knowledge.analyzers
Summary: Analyzes code changes and suggests knowledge entries
Structure:
  - KnowledgeSuggestionEngine: Main analysis engine
  - PatternDetector: Detects code patterns worth capturing
  - Suggestion: Data class for knowledge suggestions
Entry Points: KnowledgeSuggestionEngine class
Flow: analyze_change() -> detect_patterns() -> generate_suggestion() -> return suggestion list
Read First: KnowledgeSuggestionEngine class
"""

import re
import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Suggestion:
    """Represents a suggested knowledge entry."""
    FN: "Suggestion"
    
    title: str
    entry_type: str  # pattern, best-practice, lesson-learned, discovery, anti-pattern
    category: str  # frontend, backend, architecture, security, testing, devops
    context: str
    problem: str
    solution: str
    code_reference: str
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.5  # 0.0 to 1.0
    raw_diff: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "entry_type": self.entry_type,
            "category": self.category,
            "context": self.context,
            "problem": self.problem,
            "solution": self.solution,
            "code_reference": self.code_reference,
            "tags": self.tags,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }
    
    def to_markdown(self) -> str:
        """Convert suggestion to knowledge.md entry format."""
        return f"""## {self.title}
- **Type:** {self.entry_type}
- **Category:** {self.category}
- **Date:** {self.created_at.strftime('%Y-%m-%d')}
- **Context:** {self.context}
- **Problem:** {self.problem}
- **Solution:** {self.solution}
- **Code Reference:** {self.code_reference}
- **Tags:** [{', '.join(self.tags)}]
- **Validation:** Pending human verification
"""


@dataclass
class PatternMatch:
    """Represents a detected code pattern."""
    FN: "PatternMatch"
    
    pattern_name: str
    description: str
    file_path: str
    line_number: int
    matched_code: str
    context: str


class PatternDetector:
    """
    Detects patterns in code that might be worth capturing as knowledge.
    """
    FN: "PatternDetector"
    
    # Known patterns to detect
    PATTERNS = {
        "class_pattern": {
            "regex": r'class\s+(\w+)[\s\(]*:',
            "type": "pattern",
            "category": "architecture",
            "description": "Class definition detected"
        },
        "function_pattern": {
            "regex": r'def\s+(\w+)\s*\([^)]*\):',
            "type": "pattern",
            "category": "backend",
            "description": "Function definition detected"
        },
        "try_except_pattern": {
            "regex": r'try:.*except\s+(\w+)',
            "type": "best-practice",
            "category": "backend",
            "description": "Exception handling pattern"
        },
        "test_pattern": {
            "regex": r'def\s(test_|test_)\w+',
            "type": "best-practice",
            "category": "testing",
            "description": "Test function detected"
        },
        "component_pattern": {
            "regex": r'function\s+(\w+)\s*\([^)]*\)\s*\{.*return.*jsx',
            "type": "pattern",
            "category": "frontend",
            "description": "React component detected"
        },
        "api_route_pattern": {
            "regex": r'(GET|POST|PUT|DELETE|PATCH)\s*\(',
            "type": "pattern",
            "category": "backend",
            "description": "HTTP method handler detected"
        },
        "sql_model_pattern": {
            "regex": r'class\s+\w+.*\(.*SQLModel.*\):',
            "type": "pattern",
            "category": "backend",
            "description": "SQLModel definition detected"
        },
        "config_pattern": {
            "regex": r'(\w+)Config|config\.(\w+)',
            "type": "pattern",
            "category": "architecture",
            "description": "Configuration pattern detected"
        },
        "logging_pattern": {
            "regex": r'logger\.(debug|info|warning|error)\(',
            "type": "best-practice",
            "category": "development",
            "description": "Logging statement detected"
        },
        "type_hint_pattern": {
            "regex": r'(\w+):\s*(str|int|float|bool|List|Dict|Optional|Any)',
            "type": "best-practice",
            "category": "development",
            "description": "Type hint detected"
        }
    }
    
    def __init__(self):
        """Initialize the pattern detector."""
        self._compiled_patterns = {}
        for name, info in self.PATTERNS.items():
            try:
                self._compiled_patterns[name] = re.compile(info['regex'], re.MULTILINE | re.DOTALL)
            except re.error as e:
                logger.error("FN:__init__ Invalid regex for pattern %s: %s", name, e)
    
    def detect(self, content: str, file_path: str) -> List[PatternMatch]:
        """
        Detect patterns in the given content.
        
        Args:
            content: File content to analyze
            file_path: Path to the file for context
            
        Returns:
            List of detected patterns
        """
        matches = []
        
        for pattern_name, pattern_info in self.PATTERNS.items():
            compiled = self._compiled_patterns.get(pattern_name)
            if not compiled:
                continue
            
            for match in compiled.finditer(content):
                line_number = content[:match.start()].count('\n') + 1
                
                # Extract surrounding context
                lines = content.split('\n')
                start_idx = max(0, line_number - 3)
                end_idx = min(len(lines), line_number + 3)
                context = '\n'.join(lines[start_idx:end_idx])
                
                matches.append(PatternMatch(
                    pattern_name=pattern_name,
                    description=pattern_info['description'],
                    file_path=file_path,
                    line_number=line_number,
                    matched_code=match.group(0),
                    context=context
                ))
        
        return matches
    
    def analyze_changes(self, file_path: str, old_content: str, new_content: str) -> List[PatternMatch]:
        """
        Analyze changes between old and new content.
        
        Args:
            file_path: Path to the modified file
            old_content: Content before change
            new_content: Content after change
            
        Returns:
            List of new patterns detected in the change
        """
        # Get new patterns in new content
        new_patterns = self.detect(new_content, file_path)
        
        # Get old patterns in old content
        old_patterns = self.detect(old_content, file_path) if old_content else []
        
        # Find new patterns (not in old content)
        new_pattern_signatures = {(p.pattern_name, p.line_number, p.matched_code[:50]) 
                                   for p in new_patterns}
        old_pattern_signatures = {(p.pattern_name, p.line_number, p.matched_code[:50]) 
                                   for p in old_patterns}
        
        added_patterns = []
        for pattern in new_patterns:
            sig = (pattern.pattern_name, pattern.line_number, pattern.matched_code[:50])
            if sig not in old_pattern_signatures:
                added_patterns.append(pattern)
        
        return added_patterns


class KnowledgeSuggestionEngine:
    """
    Engine that analyzes file changes and generates knowledge entry suggestions.
    """
    FN: "KnowledgeSuggestionEngine"
    
    def __init__(self, knowledge_file: str):
        """
        Initialize the suggestion engine.
        
        Args:
            knowledge_file: Path to the knowledge.md file
        """
        self.knowledge_file = Path(knowledge_file)
        self.pattern_detector = PatternDetector()
        
        # Heuristics for categorization
        self.category_rules = {
            "frontend": ["tsx", "jsx", "css", "scss", "html", "tailwind"],
            "backend": ["py", "flask", "fastapi", "sqlmodel"],
            "testing": ["test_", "_test", ".test.", "pytest", "jest"],
            "security": ["auth", "login", "permission", "role", "security", "key", "secret"],
            "architecture": ["config", "pattern", "abstract", "base"],
            "devops": ["docker", "kubernetes", "deploy", "ci", "cd", "github"]
        }
        
        logger.info("FN:__init__ KnowledgeSuggestionEngine initialized")
    
    def _categorize_file(self, file_path: str) -> str:
        """Determine category based on file path and extension."""
        path_lower = file_path.lower()
        
        for category, keywords in self.category_rules.items():
            if any(kw in path_lower for kw in keywords):
                return category
        
        return "development"  # Default category
    
    def _generate_title(self, patterns: List[PatternMatch], file_path: str) -> str:
        """Generate a descriptive title from detected patterns."""
        if not patterns:
            return f"Unknown change in {Path(file_path).name}"
        
        # Use most significant pattern for title
        primary = patterns[0]
        
        # Extract key terms
        if "class" in primary.pattern_name:
            return f"{primary.matched_code.split()[1]} Class Pattern" if len(primary.matched_code.split()) > 1 else "Class Pattern"
        elif "function" in primary.pattern_name:
            parts = primary.matched_code.replace("def ", "").split("(")
            func_name = parts[0] if parts else "function"
            return f"{func_name}() Implementation Pattern"
        elif "test" in primary.pattern_name:
            parts = primary.matched_code.replace("def ", "").split("(")
            test_name = parts[0] if parts else "test"
            return f"Test: {test_name}()"
        else:
            return f"Pattern in {Path(file_path).stem}"
    
    def _extract_problem_solution(self, patterns: List[PatternMatch], file_path: str) -> Tuple[str, str]:
        """Extract problem and solution from pattern analysis."""
        if not patterns:
            return ("Unknown change", "File was modified")
        
        primary = patterns[0]
        
        # Generate problem description based on pattern type
        pattern_type = primary.pattern_name
        
        if "try_except" in pattern_type:
            problem = "Potential error condition requires handling"
            solution = "Exception handling added to gracefully manage error conditions"
        elif "test" in pattern_type:
            problem = "Functionality requires validation through automated testing"
            solution = "Test case implemented to verify correct behavior"
        elif "logging" in pattern_type:
            problem = "System behavior needs to be observable for debugging and monitoring"
            solution = "Structured logging added for traceability"
        elif "type_hint" in pattern_type:
            problem = "Function interface lacks explicit type contracts"
            solution = "Type hints added for clarity and IDE support"
        elif "class" in pattern_type:
            problem = "Complex logic requires encapsulation and reusability"
            solution = "Class-based abstraction implemented for better code organization"
        elif "api_route" in pattern_type:
            problem = "HTTP endpoint requires implementation"
            solution = "API route handler configured with appropriate HTTP method"
        elif "sql_model" in pattern_type:
            problem = "Data persistence requires structured model definition"
            solution = "SQLModel class created for database operations"
        elif "component" in pattern_type:
            problem = "UI functionality requires reusable component"
            solution = "React component created for consistent UI rendering"
        else:
            problem = "Code structure was modified"
            solution = "Implementation updated to address requirements"
        
        return (problem, solution)
    
    def _generate_tags(self, patterns: List[PatternMatch], file_path: str) -> List[str]:
        """Generate relevant tags for the knowledge entry."""
        tags = set()
        
        # Add file extension as tag
        ext = Path(file_path).suffix.lstrip('.')
        if ext:
            tags.add(ext)
        
        # Add category-specific tags
        for pattern in patterns:
            tags.add(pattern.pattern_name.replace("_", "-"))
        
        # Add framework tags based on patterns
        if any("jsx" in p.pattern_name or "react" in p.description.lower() for p in patterns):
            tags.add("react")
        if any("sqlmodel" in p.pattern_name for p in patterns):
            tags.add("sqlmodel")
        if any("flask" in file_path.lower() for _ in patterns):
            tags.add("flask")
        
        return list(tags)
    
    def analyze_change(self, change) -> List[Suggestion]:
        """
        Analyze a file change and generate knowledge suggestions.
        
        Args:
            change: FileChange object from the file watcher
            
        Returns:
            List of suggested knowledge entries
        """
        suggestions = []
        
        # Skip certain file types
        if any(ext in change.path for ext in ['.png', '.jpg', '.gif', '.ico', '.svg']):
            return suggestions
        
        # Read file content
        try:
            with open(change.path, 'r', encoding='utf-8') as f:
                new_content = f.read()
        except Exception as e:
            logger.error("FN:analyze_change Failed to read %s: %s", change.path, e)
            return suggestions
        
        # For deletions, just log
        if change.change_type == "deleted":
            logger.info("FN:analyze_change File deleted: %s", change.path)
            return suggestions
        
        # Detect patterns
        patterns = self.pattern_detector.detect(new_content, change.path)
        
        if not patterns:
            return suggestions
        
        # Categorize
        category = self._categorize_file(change.path)
        
        # Generate title
        title = self._generate_title(patterns, change.path)
        
        # Extract problem/solution
        problem, solution = self._extract_problem_solution(patterns, change.path)
        
        # Generate tags
        tags = self._generate_tags(patterns, change.path)
        
        # Determine entry type based on pattern analysis
        entry_type = "pattern"
        if any("test" in p.pattern_name for p in patterns):
            entry_type = "best-practice"
        elif any("logging" in p.pattern_name for p in patterns):
            entry_type = "best-practice"
        elif any("try_except" in p.pattern_name for p in patterns):
            entry_type = "best-practice"
        
        # Calculate confidence score
        confidence = min(0.9, 0.5 + (len(patterns) * 0.1))
        
        suggestion = Suggestion(
            title=title,
            entry_type=entry_type,
            category=category,
            context=f"Detected changes in {change.path}",
            problem=problem,
            solution=solution,
            code_reference=change.path,
            tags=tags,
            confidence=confidence
        )
        
        suggestions.append(suggestion)
        
        # Log analysis result
        logger.info("FN:analyze_change Generated %d suggestion(s) for %s", len(suggestions), change.path)
        
        return suggestions
    
    def suggest_from_code_review(self, file_path: str, review_notes: str) -> List[Suggestion]:
        """
        Generate suggestions from manual code review notes.
        
        Args:
            file_path: Path to the reviewed file
            review_notes: Human review notes about the code
            
        Returns:
            List of suggested knowledge entries
        """
        suggestions = []
        
        # Parse review notes for patterns
        if "bug" in review_notes.lower() or "issue" in review_notes.lower():
            suggestions.append(Suggestion(
                title=f"Bug Fix: {Path(file_path).stem}",
                entry_type="lesson-learned",
                category=self._categorize_file(file_path),
                context="Manual code review identified an issue",
                problem="Code contained a defect requiring correction",
                solution=review_notes,
                code_reference=file_path,
                tags=["bugfix", "review"],
                confidence=0.9
            ))
        
        if "optim" in review_notes.lower() or "performance" in review_notes.lower():
            suggestions.append(Suggestion(
                title=f"Performance Optimization: {Path(file_path).stem}",
                entry_type="discovery",
                category=self._categorize_file(file_path),
                context="Manual code review identified optimization opportunity",
                problem="Code could be more efficient",
                solution=review_notes,
                code_reference=file_path,
                tags=["performance", "optimization"],
                confidence=0.85
            ))
        
        return suggestions


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test the engine
    engine = KnowledgeSuggestionEngine("data/knowledge.md")
    
    # Simulate a change
    class MockChange:
        path = "tests/example_test.py"
        change_type = "created"
    
    suggestions = engine.analyze_change(MockChange())
    for s in suggestions:
        print(s.to_markdown())
