"""
FN:model_metadata.py
Model metadata management for intelligent model selection and swarm decisions.

Classes:
- ModelCapability: Enum for model capabilities
- ModelTier: Enum for model performance tiers
- ModelMetadata: Complete model metadata with capabilities and constraints

Functions:
- FN:evaluate_task_complexity: Analyze task and recommend model tier (lines 120-145)
- FN:should_use_swarm: Decide if swarm mode is needed (lines 147-175)
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
import re


class ModelCapability(str, Enum):
    """Enum for model capabilities."""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    IMAGE_ANALYSIS = "image_analysis"
    IMAGE_GENERATION = "image_generation"
    REASONING = "reasoning"
    MATH = "math"
    MULTILINGUAL = "multilingual"
    LONG_CONTEXT = "long_context"
    STREAMING = "streaming"
    FUNCTION_CALLING = "function_calling"


class ModelTier(str, Enum):
    """Enum for model performance tiers."""
    FAST = "fast"  # Fast, cheap, for simple tasks
    STANDARD = "standard"  # Balanced performance/cost
    SMART = "smart"  # Most capable, for complex reasoning
    SPECIALIZED = "specialized"  # Specialized for specific tasks


@dataclass
class ModelMetadata:
    """
    Complete metadata for an AI model.
    
    Used by the swarm decision logic to determine when to use
    multi-model discussion vs single model.
    """
    name: str
    provider: str
    tier: ModelTier
    context_window: int
    capabilities: Set[ModelCapability] = field(default_factory=set)
    
    # Performance characteristics
    tokens_per_second: float = 0.0
    latency_ms: float = 0.0
    
    # Cost (per 1K tokens)
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0
    
    # Constraints
    max_output_tokens: int = 4096
    supports_streaming: bool = True
    supports_vision: bool = False
    supports_function_calling: bool = True
    
    # Metadata
    description: Optional[str] = None
    recommended_for: List[str] = field(default_factory=list)
    not_recommended_for: List[str] = field(default_factory=list)
    
    def can_handle_task(self, task_type: str) -> bool:
        """
        FN:can_handle_task Check if model can handle a task type.
        
        Args:
            task_type: Type of task to check
            
        Returns:
            True if model is suitable for the task
        """
        if task_type in self.not_recommended_for:
            return False
        if task_type in self.recommended_for:
            return True
        
        # Map task types to capabilities
        task_to_capability = {
            "coding": ModelCapability.CODE_GENERATION,
            "math": ModelCapability.MATH,
            "reasoning": ModelCapability.REASONING,
            "image_analysis": ModelCapability.IMAGE_ANALYSIS,
            "creative_writing": ModelCapability.TEXT_GENERATION,
            "summarization": ModelCapability.LONG_CONTEXT,
        }
        
        capability = task_to_capability.get(task_type)
        if capability:
            return capability in self.capabilities
        
        return True  # Default to allowing
    
    def get_complexity_score(self) -> float:
        """
        FN:get_complexity_score Calculate model complexity score.
        
        Higher score = more capable model for complex tasks.
        
        Returns:
            Complexity score (0.0-10.0)
        """
        score = 0.0
        
        # Context window contribution (max 3 points)
        if self.context_window >= 100000:
            score += 3.0
        elif self.context_window >= 50000:
            score += 2.0
        elif self.context_window >= 10000:
            score += 1.0
        
        # Capabilities contribution (max 4 points)
        capability_scores = {
            ModelCapability.REASONING: 1.5,
            ModelCapability.CODE_GENERATION: 1.0,
            ModelCapability.MATH: 1.0,
            ModelCapability.IMAGE_ANALYSIS: 0.5,
            ModelCapability.LONG_CONTEXT: 0.5,
        }
        for cap in self.capabilities:
            score += capability_scores.get(cap, 0.25)
        
        # Tier contribution (max 3 points)
        tier_scores = {
            ModelTier.SMART: 3.0,
            ModelTier.STANDARD: 2.0,
            ModelTier.FAST: 1.0,
            ModelTier.SPECIALIZED: 2.5,
        }
        score += tier_scores.get(self.tier, 1.0)
        
        return min(score, 10.0)  # Cap at 10.0


# Task complexity patterns
TASK_COMPLEXITY_PATTERNS = {
    "low": [
        r"\b(simple|basic|easy|quick)\b",
        r"\b(list|show|find|get)\b",
        r"^\s*what\s+is\s+",
        r"^\s*define\s+",
    ],
    "medium": [
        r"\b(explain|compare|analyze)\b",
        r"\b(how\s+to|why\s+does)\b",
        r"\b(create|build|make)\s+\w+\s+for\b",
    ],
    "high": [
        r"\b(optimize|debug|troubleshoot)\b",
        r"\b(architecture|design\s+pattern|system\s+design)\b",
        r"\b(complex|advanced|enterprise)\b",
        r"\b(multi[- ]step|multi[- ]phase)\b",
    ],
}


def evaluate_task_complexity(task_description: str) -> str:
    """
    FN:evaluate_task_complexity Analyze task and recommend complexity level.
    
    Args:
        task_description: User's task description
        
    Returns:
        Complexity level: "low", "medium", or "high"
    """
    task_lower = task_description.lower()
    
    # Count pattern matches for each complexity level
    scores = {"low": 0, "medium": 0, "high": 0}
    
    for level, patterns in TASK_COMPLEXITY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, task_lower):
                scores[level] += 1
    
    # Determine complexity based on highest score
    # High complexity patterns weigh more
    if scores["high"] > 0 or scores["medium"] >= 2:
        return "high"
    elif scores["medium"] > 0:
        return "medium"
    else:
        return "low"


def should_use_swarm(
    task_description: str,
    available_models: List[ModelMetadata],
    base_model: Optional[ModelMetadata] = None,
    swarm_config: Optional[Dict[str, Any]] = None
) -> bool:
    """
    FN:should_use_swarm Decide if swarm mode is needed for a task.
    
    Swarm mode uses multiple models for discussion/debate when:
    1. Task complexity is high
    2. Base model capability is insufficient
    3. Multiple perspectives would be valuable
    
    Args:
        task_description: User's task description
        available_models: List of available model metadata
        base_model: Current base model (optional)
        swarm_config: Swarm configuration (optional)
        
    Returns:
        True if swarm mode should be used
    """
    # Default config
    config = swarm_config or {}
    enabled = config.get("enabled", True)
    min_complexity = config.get("min_complexity", "high")
    complexity_threshold = config.get("complexity_threshold", 0.7)
    
    if not enabled:
        return False
    
    # Evaluate task complexity
    complexity = evaluate_task_complexity(task_description)
    complexity_scores = {"low": 0.3, "medium": 0.6, "high": 1.0}
    task_score = complexity_scores.get(complexity, 0.5)
    
    if task_score < complexity_threshold:
        return False
    
    # Check if base model can handle it
    if base_model:
        base_capability = base_model.get_complexity_score()
        if base_capability >= 7.0:
            # Base model is very capable, may not need swarm
            return False
    
    # Check if we have diverse models available
    if len(available_models) < 2:
        return False
    
    # Check model diversity (different tiers/providers)
    tiers = {m.tier for m in available_models}
    providers = {m.provider for m in available_models}
    
    if len(tiers) >= 2 or len(providers) >= 2:
        # Diverse models available for swarm discussion
        return True
    
    return False


# Predefined model metadata for common models
KNOWN_MODELS: Dict[str, ModelMetadata] = {
    "qwen2.5:7b": ModelMetadata(
        name="qwen2.5:7b",
        provider="ollama",
        tier=ModelTier.FAST,
        context_window=32768,
        capabilities={
            ModelCapability.TEXT_GENERATION,
            ModelCapability.CODE_GENERATION,
            ModelCapability.STREAMING,
        },
        tokens_per_second=50.0,
        recommended_for=["simple_qa", "chat", "drafting"],
    ),
    "qwen3.5:397b": ModelMetadata(
        name="qwen3.5:397b",
        provider="ollama",
        tier=ModelTier.SMART,
        context_window=262144,
        capabilities={
            ModelCapability.TEXT_GENERATION,
            ModelCapability.CODE_GENERATION,
            ModelCapability.REASONING,
            ModelCapability.MATH,
            ModelCapability.LONG_CONTEXT,
            ModelCapability.STREAMING,
        },
        tokens_per_second=10.0,
        recommended_for=["complex_reasoning", "code_review", "analysis"],
    ),
    "Qwen/Qwen3.6-35B-A3B-FP8": ModelMetadata(
        name="Qwen/Qwen3.6-35B-A3B-FP8",
        provider="openai",
        tier=ModelTier.STANDARD,
        context_window=262144,
        capabilities={
            ModelCapability.TEXT_GENERATION,
            ModelCapability.CODE_GENERATION,
            ModelCapability.REASONING,
            ModelCapability.IMAGE_ANALYSIS,
            ModelCapability.STREAMING,
        },
        tokens_per_second=30.0,
        recommended_for=["general_tasks", "multimodal", "coding"],
    ),
}


def get_model_metadata(model_name: str) -> Optional[ModelMetadata]:
    """
    FN:get_model_metadata Get metadata for a known model.
    
    Args:
        model_name: Model name to look up
        
    Returns:
        ModelMetadata or None if unknown
    """
    return KNOWN_MODELS.get(model_name)


def infer_metadata_from_config(model_config: Dict[str, Any]) -> ModelMetadata:
    """
    FN:infer_metadata_from_config Infer metadata from model config.
    
    Args:
        model_config: Model configuration dict
        
    Returns:
        Inferred ModelMetadata
    """
    name = model_config.get("name", "unknown")
    provider = model_config.get("provider", "unknown")
    context_window = model_config.get("context_window", 4096)
    
    # Infer tier from context window
    if context_window >= 200000:
        tier = ModelTier.SMART
    elif context_window >= 50000:
        tier = ModelTier.STANDARD
    else:
        tier = ModelTier.FAST
    
    # Infer capabilities
    capabilities = {ModelCapability.TEXT_GENERATION, ModelCapability.STREAMING}
    
    if "reasoning" in name.lower():
        capabilities.add(ModelCapability.REASONING)
    if "code" in name.lower() or "coder" in name.lower():
        capabilities.add(ModelCapability.CODE_GENERATION)
    if context_window >= 100000:
        capabilities.add(ModelCapability.LONG_CONTEXT)
    
    return ModelMetadata(
        name=name,
        provider=provider,
        tier=tier,
        context_window=context_window,
        capabilities=capabilities,
    )
