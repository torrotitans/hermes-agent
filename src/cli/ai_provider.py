"""
FN:ai_provider.py
AI provider interface for Ollama, LM Studio, and OpenAI-compatible APIs.

Reads model configurations from config.ini [CLI_MODELS] section.

Classes:
- ModelConfig: Parsed model configuration from config.ini
- ModelRegistry: Registry of available models from config.ini
- SwarmConfig: Swarm/multi-model discussion configuration
- AIProvider: Base class for AI model providers
- OllamaProvider: Ollama-specific implementation
- OpenAIProvider: OpenAI-compatible API implementation

Functions:
- FN:get_model_config: Get model config by name from config.ini (lines 100-115)
- FN:list_models: List all available models (lines 117-130)
- FN:create_provider: Factory function to create provider instance (lines 132-150)
- FN:stream_response: Stream AI response token by token (lines 152-165)
"""

import configparser
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Optional, Generator, Dict, Any, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import requests

logger = logging.getLogger(__name__)


# Default configuration paths
DEFAULT_CONFIG_PATHS = [
    "config.ini",
    os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"),
    os.path.expanduser("~/.torro/config.ini"),
]


@dataclass
class ModelConfig:
    """Parsed model configuration from config.ini."""
    name: str
    provider_type: str  # "ollama", "openai", "lmstudio"
    model_name: str
    base_url: str
    context_window: int = 32768
    supports_streaming: bool = True
    supports_images: bool = False
    supports_reasoning: bool = False
    api_key: Optional[str] = None


@dataclass
class SwarmConfig:
    """Swarm/multi-model discussion configuration."""
    enabled: bool = True
    min_models: int = 2
    max_models: int = 4
    strategy: str = "debate"  # debate, consensus, voting


class ModelRegistry:
    """
    Registry of available models parsed from config.ini [CLI_MODELS] section.
    Provides lookup, listing, and model selection utilities.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the model registry from config.ini.

        Args:
            config_path: Optional path to config.ini
        """
        self._config = configparser.ConfigParser()
        self._models: Dict[str, ModelConfig] = {}
        self._swarm_config = SwarmConfig()
        self._default_model: Optional[str] = None
        self._swarm_model: Optional[str] = None

        # Find and read config
        config_file = self._find_config(config_path)
        if config_file and os.path.exists(config_file):
            self._config.read(config_file)
            self._parse_models()
            self._parse_swarm_config()

    def _find_config(self, config_path: Optional[str]) -> Optional[str]:
        """Find the config.ini file."""
        if config_path:
            return config_path
        for path in DEFAULT_CONFIG_PATHS:
            if os.path.exists(path):
                return path
        return None

    def _parse_models(self):
        """Parse model definitions from config.ini."""
        if not self._config.has_section("CLI_MODELS"):
            return

        # Parse default model
        self._default_model = self._config.get("CLI_MODELS", "default", fallback=None)
        self._base_model = self._config.get("CLI_MODELS", "base", fallback=None)
        self._swarm_model = self._config.get("CLI_MODELS", "swarm", fallback=None)

        # Parse model definitions (format: provider|model_name|base_url)
        for key, value in self._config.items("CLI_MODELS"):
            if key.startswith("meta_") or key.startswith("swarm_"):
                continue
            if "|" in value:
                parts = value.split("|")
                if len(parts) >= 3:
                    provider_type = parts[0]
                    model_name = parts[1]
                    base_url = parts[2] if len(parts) > 2 else ""
                    self._models[key] = ModelConfig(
                        name=key,
                        provider_type=provider_type,
                        model_name=model_name,
                        base_url=base_url
                    )

        # Parse model metadata (format: context_window|supports_streaming|supports_images|supports_reasoning)
        for key, value in self._config.items("CLI_MODELS"):
            if key.startswith("meta_"):
                model_key = key.replace("meta_", "")
                if model_key in self._models:
                    meta = value.split("|")
                    if len(meta) >= 4:
                        self._models[model_key].context_window = int(meta[0])
                        self._models[model_key].supports_streaming = meta[1].lower() == "true"
                        self._models[model_key].supports_images = meta[2].lower() == "true"
                        self._models[model_key].supports_reasoning = meta[3].lower() == "true"

    def _parse_swarm_config(self):
        """Parse swarm configuration from config.ini."""
        if not self._config.has_section("CLI_MODELS"):
            return

        self._swarm_config = SwarmConfig(
            enabled=self._config.getboolean("CLI_MODELS", "swarm_enabled", fallback=True),
            min_models=self._config.getint("CLI_MODELS", "swarm_min_models", fallback=2),
            max_models=self._config.getint("CLI_MODELS", "swarm_max_models", fallback=4),
            strategy=self._config.get("CLI_MODELS", "swarm_strategy", fallback="debate")
        )

    @property
    def default_model(self) -> Optional[str]:
        """Get the default model name."""
        return self._default_model

    @property
    def base_model(self) -> Optional[str]:
        """Get the base model name."""
        return self._base_model

    @property
    def swarm_model(self) -> Optional[str]:
        """Get the swarm model name."""
        return self._swarm_model

    @property
    def swarm_config(self) -> SwarmConfig:
        """Get swarm configuration."""
        return self._swarm_config

    def get_model(self, name: str) -> Optional[ModelConfig]:
        """
        FN:get_model Get model config by name.

        Args:
            name: Model name (e.g., "local/qwen2.5:7b")

        Returns:
            ModelConfig or None if not found
        """
        return self._models.get(name)

    def list_models(self) -> List[ModelConfig]:
        """
        FN:list_models List all available models.

        Returns:
            List of ModelConfig objects
        """
        return list(self._models.values())

    def get_models_by_provider(self, provider_type: str) -> List[ModelConfig]:
        """
        FN:get_models_by_provider Get models filtered by provider type.

        Args:
            provider_type: Provider type (ollama, openai, etc.)

        Returns:
            List of matching ModelConfig objects
        """
        return [m for m in self._models.values() if m.provider_type == provider_type]

    def get_recommended_model(self, task_type: str) -> Optional[ModelConfig]:
        """
        FN:get_recommended_model Get recommended model for task type.

        Args:
            task_type: Task type ("simple", "complex", "creative", "analysis")

        Returns:
            Recommended ModelConfig or None
        """
        recommendations = {
            "simple": self._default_model,
            "complex": self._swarm_model,
            "creative": self._default_model,
            "analysis": self._swarm_model,
        }
        name = recommendations.get(task_type, self._default_model)
        return self.get_model(name) if name else None


def get_model_config(
    model_name: str,
    config_path: Optional[str] = None
) -> Optional[ModelConfig]:
    """
    FN:get_model_config Get model config by name from config.ini.

    Args:
        model_name: Model name
        config_path: Optional config path

    Returns:
        ModelConfig or None
    """
    registry = ModelRegistry(config_path)
    return registry.get_model(model_name)


def list_models(
    config_path: Optional[str] = None
) -> List[ModelConfig]:
    """
    FN:list_models Standalone function to list all models.

    Args:
        config_path: Optional config path

    Returns:
        List of ModelConfig objects
    """
    registry = ModelRegistry(config_path)
    return registry.list_models()


class AIProvider(ABC):
    """
    Abstract base class for AI model providers.
    """

    def __init__(self, config: ModelConfig):
        """
        Initialize the AI provider.

        Args:
            config: Model configuration
        """
        self.config = config
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json"
        })
        if config.api_key:
            self._session.headers.update({
                "Authorization": f"Bearer {config.api_key}"
            })

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate a complete response."""
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Stream a response token by token."""
        pass


class OllamaProvider(AIProvider):
    """Ollama-specific AI provider."""

    def __init__(self, config: ModelConfig):
        """Initialize Ollama provider."""
        super().__init__(config)
        self.endpoint = f"{config.base_url}/api/generate"

    def health_check(self) -> Tuple[bool, str]:
        """
        FN:health_check Check if Ollama API is available and model exists.

        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            response = self._session.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if the specific model is loaded
            models = data.get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            if self.config.model_name not in model_names:
                return (
                    False,
                    f"Ollama is running but model '{self.config.model_name}' is not loaded. "
                    f"Available models: {', '.join(model_names) if model_names else 'none'}"
                )
            
            return (True, f"Ollama API is available with model '{self.config.model_name}'")
        except requests.exceptions.ConnectionError:
            return (False, "Cannot connect to Ollama. Is it running?")
        except requests.exceptions.Timeout:
            return (False, "Ollama API timed out")
        except requests.exceptions.HTTPError as e:
            return (False, f"Ollama API error: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            return (False, f"Failed to parse Ollama response: {e}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """FN:generate Generate complete response from Ollama."""
        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt

        response = self._session.post(
            self.endpoint,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """FN:stream Stream response from Ollama."""
        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": True,
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = self._session.post(
                self.endpoint,
                json=payload,
                stream=True,
                timeout=120
            )
            # Debug: log response status and content-type
            logger.debug("Ollama POST status=%d content-type=%s", response.status_code, response.headers.get("content-type", "unknown"))
            response.raise_for_status()

            for line_num, raw_line in enumerate(response.iter_lines()):
                if raw_line:
                    # Decode bytes to string with error handling
                    line = raw_line.decode("utf-8", errors="replace")
                    logger.debug("Ollama line %d: %s", line_num, line[:200])
                    try:
                        data = json.loads(line)
                        yield data.get("response", "")
                    except json.JSONDecodeError as parse_err:
                        logger.error("JSON parse error on line %d: %s | raw bytes: %s | decoded: %s",
                                     line_num, parse_err, raw_line[:200], line[:200])
                        # Yield diagnostic info instead of crashing
                        error_msg = (f"\n[Error] Non-JSON response from Ollama (line {line_num})\n")
                        error_msg += f"Raw bytes: {raw_line[:200]}\n"
                        error_msg += f"JSON error: {parse_err}\n"
                        error_msg += f"Endpoint: {self.endpoint}\n"
                        yield error_msg
        except requests.exceptions.RequestException as e:
            # Yield error message as part of stream
            error_msg = f"\n\n[Error] API request failed: {str(e)}\n"
            error_msg += "Please check if Ollama is running and the model is available.\n"
            yield error_msg


class OpenAIProvider(AIProvider):
    """OpenAI-compatible API provider."""

    def __init__(self, config: ModelConfig):
        """Initialize OpenAI provider."""
        super().__init__(config)
        # Avoid double /v1 if base_url already contains it
        base = config.base_url
        if base.endswith("/v1"):
            self.endpoint = f"{base}/chat/completions"
        elif "/v1/" in base:
            self.endpoint = f"{base}chat/completions"
        else:
            self.endpoint = f"{base}/v1/chat/completions"

    def health_check(self) -> Tuple[bool, str]:
        """
        FN:health_check Check if OpenAI API is available.

        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            response = self._session.get(
                f"{self.config.base_url}/models",
                timeout=5,
                headers={"Authorization": f"Bearer {self.config.api_key}"} if self.config.api_key else {}
            )
            response.raise_for_status()
            return (True, "OpenAI API is available")
        except requests.exceptions.ConnectionError:
            return (False, "Cannot connect to API. Check your endpoint.")
        except requests.exceptions.Timeout:
            return (False, "API timed out")
        except requests.exceptions.HTTPError as e:
            return (False, f"API error: {e}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """FN:generate Generate complete response from OpenAI-compatible API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": False
        }

        response = self._session.post(
            self.endpoint,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """FN:stream Stream response from OpenAI-compatible API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": True
        }

        try:
            response = self._session.post(
                self.endpoint,
                json=payload,
                stream=True,
                timeout=120
            )
            # Debug: log response status and content-type
            logger.debug("OpenAI POST status=%d content-type=%s", response.status_code, response.headers.get("content-type", "unknown"))
            response.raise_for_status()

            for line_num, raw_line in enumerate(response.iter_lines()):
                if raw_line:
                    line = raw_line.decode("utf-8", errors="replace")
                    logger.debug("OpenAI line %d: %s", line_num, line[:200])
                    if line.startswith("data: "):
                        json_data = line[6:].strip()
                        # Skip heartbeat/keepalive messages
                        if json_data == "[DONE]":
                            continue
                        try:
                            data = json.loads(json_data)
                            delta = data["choices"][0]["delta"]
                            if "content" in delta:
                                yield delta["content"]
                        except (json.JSONDecodeError, KeyError, IndexError) as parse_err:
                            # Log the raw response for debugging
                            logger.error("OpenAI JSON parse error: %s | json_data: %s", parse_err, json_data[:200])
                            error_msg = f"\n[Warning] API returned unexpected format: {json_data[:100]}\n"
                            error_msg += f"Parse error: {parse_err}\n"
                            yield error_msg
        except requests.exceptions.RequestException as e:
            # Yield error message as part of stream
            error_msg = f"\n\n[Error] API request failed: {str(e)}\n"
            error_msg += "Please check your API endpoint and ensure it supports streaming.\n"
            yield error_msg


def create_provider(
    model_name: str,
    config_path: Optional[str] = None
) -> AIProvider:
    """
    FN:create_provider Factory function to create provider from config.ini model name.

    Args:
        model_name: Model name from config.ini (e.g., "local/qwen2.5:7b")
        config_path: Optional config path

    Returns:
        AIProvider instance
    """
    registry = ModelRegistry(config_path)
    model_config = registry.get_model(model_name)

    if not model_config:
        # Fallback: try to parse as provider:model:url format
        parts = model_name.split(":")
        if len(parts) >= 3:
            model_config = ModelConfig(
                name="custom",
                provider_type=parts[0],
                model_name=parts[1],
                base_url=parts[2]
            )
        else:
            raise ValueError(f"Unknown model: {model_name}")

    providers = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "lmstudio": OpenAIProvider,
    }

    provider_class = providers.get(model_config.provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider type: {model_config.provider_type}")

    return provider_class(model_config)


def stream_response(
    provider: AIProvider,
    prompt: str,
    system_prompt: Optional[str] = None
) -> Generator[str, None, None]:
    """
    FN:stream_response Standalone function for streaming response.

    Args:
        provider: AI provider instance
        prompt: User prompt
        system_prompt: Optional system prompt

    Yields:
        Generated tokens
    """
    yield from provider.stream(prompt, system_prompt)
