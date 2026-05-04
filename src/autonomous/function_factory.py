"""
FN:function_factory.py
Agentic Function Factory for Layer 1 Autonomous Layer in Torro Agent.

Generates optimized Python macros for frequently used commands to reduce token consumption.

Classes:
- MacroConfig: Configuration for generated macro
- FunctionFactory: Main factory class

Functions:
- FN:analyze_frequency: Analyze command frequency (lines 75-95)
- FN:generate_macro: Generate Python macro function (lines 97-130)
"""

import logging
import re
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class MacroConfig:
    """Configuration for generated macro."""
    name: str
    description: str
    command: str
    parameters: List[str] = field(default_factory=list)
    return_type: str = "str"
    docstring_style: str = "google"
    include_logging: bool = True
    include_error_handling: bool = True


@dataclass
class MacroResult:
    """Result of macro generation."""
    macro_id: str
    config: MacroConfig
    code: str
    token_savings: int
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class FunctionFactory:
    """
    Agentic Function Factory for Layer 1 Autonomous Layer.
    Generates optimized Python macros for frequently used commands.
    
    Responsibilities:
    - Analyze command frequency from execution history
    - Generate optimized Python wrapper functions
    - Track token savings from macro usage
    - Maintain macro library
    """
    
    # Token savings threshold for macro generation
    MIN_FREQUENCY_THRESHOLD = 3
    ESTIMATED_TOKEN_PER_LINE = 10
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the function factory.
        
        Args:
            output_dir: Directory to store generated macros
        """
        self._output_dir = output_dir or "agentic/macros"
        self._command_history: List[str] = []
        self._macro_library: Dict[str, MacroResult] = {}
        self._token_savings: Dict[str, int] = {}
        
        logger.info("FN:__init__ FunctionFactory initialized with output dir: %s", self._output_dir)
    
    def record_command(self, command: str):
        """
        FN:record_command Record a command for frequency analysis.
        
        Args:
            command: Command string to record
        """
        self._command_history.append(command)
        logger.debug("FN:record_command Command recorded: %s", command)
    
    def analyze_frequency(
        self,
        commands: Optional[List[str]] = None
    ) -> Dict[str, int]:
        """
        FN:analyze_frequency Analyze command frequency.
        
        Args:
            commands: Optional list of commands to analyze
            
        Returns:
            Dictionary mapping commands to frequency counts
        """
        history = commands or self._command_history
        return dict(Counter(history))
    
    def get_frequent_commands(
        self,
        threshold: Optional[int] = None
    ) -> List[Tuple[str, int]]:
        """
        FN:get_frequent_commands Get commands exceeding frequency threshold.
        
        Args:
            threshold: Minimum frequency threshold (default: MIN_FREQUENCY_THRESHOLD)
            
        Returns:
            List of (command, frequency) tuples
        """
        threshold = threshold or self.MIN_FREQUENCY_THRESHOLD
        frequency = self.analyze_frequency()
        return [
            (cmd, count) for cmd, count in frequency.items()
            if count >= threshold
        ]
    
    def generate_macro(
        self,
        command: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> MacroResult:
        """
        FN:generate_macro Generate Python macro function for a command.
        
        Args:
            command: Command string to wrap
            name: Optional macro function name
            description: Optional description
            
        Returns:
            MacroResult with generated code
        """
        # Generate macro name from command
        if not name:
            name = self._sanitize_command_name(command)
        
        # Generate description if not provided
        if not description:
            description = f"Execute command: {command}"
        
        # Extract parameters from command
        parameters = self._extract_parameters(command)
        
        # Create macro config
        config = MacroConfig(
            name=name,
            description=description,
            command=command,
            parameters=parameters
        )
        
        # Generate code
        code = self._generate_code(config)
        
        # Estimate token savings
        original_tokens = len(command.split()) * self.ESTIMATED_TOKEN_PER_LINE
        macro_tokens = len(code.split("\n")) * self.ESTIMATED_TOKEN_PER_LINE
        token_savings = (original_tokens - macro_tokens) * self._command_history.count(command)
        
        # Create result
        result = MacroResult(
            macro_id=name,
            config=config,
            code=code,
            token_savings=max(0, token_savings)
        )
        
        # Store in library
        self._macro_library[name] = result
        self._token_savings[name] = token_savings
        
        logger.info("FN:generate_macro Macro generated: %s (saves %d tokens)", name, token_savings)
        
        return result
    
    def _sanitize_command_name(self, command: str) -> str:
        """
        FN:_sanitize_command_name Sanitize command to valid Python function name.
        
        Args:
            command: Command string
            
        Returns:
            Sanitized function name
        """
        # Replace spaces and special chars with underscores
        name = re.sub(r"[^a-zA-Z0-9_]", "_", command)
        
        # Remove consecutive underscores
        name = re.sub(r"_+", "_", name)
        
        # Prefix with 'macro_' if starts with number
        if name[0].isdigit():
            name = f"macro_{name}"
        
        # Truncate if too long
        if len(name) > 50:
            name = name[:50]
        
        return name
    
    def _extract_parameters(self, command: str) -> List[str]:
        """
        FN:_extract_parameters Extract parameters from command.
        
        Args:
            command: Command string
            
        Returns:
            List of parameter names
        """
        parameters = []
        
        # Extract quoted strings as parameters
        quoted = re.findall(r'"([^"]+)"|\'([^\']+)', command)
        for match in quoted:
            param = match[0] or match[1]
            parameters.append(f"arg_{len(parameters)}")
        
        # Extract flags
        flags = re.findall(r"--([a-zA-Z0-9_-]+)", command)
        parameters.extend(flags)
        
        return parameters
    
    def _generate_code(self, config: MacroConfig) -> str:
        """
        FN:_generate_code Generate Python code for macro.
        
        Args:
            config: Macro configuration
            
        Returns:
            Python code string
        """
        # Build function signature
        params = ", ".join(config.parameters) if config.parameters else ""
        signature = f"def {config.name}({params}):"
        
        # Build docstring
        docstring = f'"""{config.description}"""'
        
        # Build function body
        lines = [
            signature,
            f'    """',
            f'    {config.description}',
            f'    """',
        ]
        
        # Add logging if requested
        if config.include_logging:
            lines.append('    import logging')
            lines.append('    logger = logging.getLogger(__name__)')
            lines.append(f'    logger.info("FN:{config.name} Executing: {config.command}")')
        
        # Add command execution
        lines.append(f'    command = "{config.command}"')
        lines.append('    # TODO: Implement actual execution logic')
        lines.append('    result = f"Executed: {command}"')
        lines.append('    return result')
        
        return "\n".join(lines)
    
    def get_macro(self, name: str) -> Optional[MacroResult]:
        """
        FN:get_macro Get macro from library.
        
        Args:
            name: Macro name
            
        Returns:
            MacroResult or None if not found
        """
        return self._macro_library.get(name)
    
    def list_macros(self) -> List[str]:
        """
        FN:list_macros List all generated macros.
        
        Returns:
            List of macro names
        """
        return list(self._macro_library.keys())
    
    def get_token_savings(self, macro_name: Optional[str] = None) -> int:
        """
        FN:get_token_savings Get total token savings from macros.
        
        Args:
            macro_name: Optional specific macro name
            
        Returns:
            Total token savings
        """
        if macro_name:
            return self._token_savings.get(macro_name, 0)
        return sum(self._token_savings.values())
    
    def export_macro(self, name: str) -> str:
        """
        FN:export_macro Export macro to file.
        
        Args:
            name: Macro name to export
            
        Returns:
            Path to exported file
        """
        from pathlib import Path
        
        if name not in self._macro_library:
            raise ValueError(f"Macro not found: {name}")
        
        # Ensure output directory exists
        output_dir = Path(self._output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write macro to file
        output_path = output_dir / f"{name}.py"
        macro = self._macro_library[name]
        output_path.write_text(macro.code)
        
        logger.info("FN:export_macro Macro exported to: %s", output_path)
        
        return str(output_path)
    
    def clear_history(self):
        """
        FN:clear_history Clear command history and reset analysis.
        """
        self._command_history = []
        logger.info("FN:clear_history Command history cleared")


def generate_macro(
    factory: FunctionFactory,
    command: str,
    name: Optional[str] = None
) -> MacroResult:
    """
    FN:generate_macro Standalone function for macro generation.
    
    Args:
        factory: Factory instance
        command: Command to wrap
        name: Optional macro name
        
    Returns:
        MacroResult
    """
    return factory.generate_macro(command, name)
