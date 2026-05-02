"""
FN:config.py
Configuration management for Torro agent framework.

Classes:
- Config: Configuration loader and accessor

Functions:
- FN:load_config: Load configuration from INI file (lines 48-68)
- FN:get_config: Get configuration instance (lines 70-80)
"""

import configparser
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class OpenAIConfig:
    """OpenAI API configuration.
    
    Attributes:
        provider: API provider name
        base_url: API base URL
        api_key: API key for authentication
        model: Model name to use
        max_tokens: Maximum tokens for completion
        temperature: Sampling temperature
        top_p: Nucleus sampling top-p
        timeout: Request timeout in seconds
    """
    provider: str = "OpenAI Compatible"
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    max_tokens: int = 8192
    temperature: float = 0.7
    top_p: float = 0.9
    timeout: int = 120


@dataclass
class MemoryConfig:
    """Memory configuration.
    
    Attributes:
        provider: Memory provider type
        top_k: Maximum memories to retrieve
        retention_days: Memory retention period
    """
    provider: str = "builtin"
    top_k: int = 5
    retention_days: int = 30


@dataclass
class ContextConfig:
    """Context engine configuration.
    
    Attributes:
        engine: Context engine type
        max_tokens: Maximum tokens before compression
        compression_ratio: Target compression ratio
        preserve_system_prompt: Whether to preserve system prompt
    """
    engine: str = "builtin"
    max_tokens: int = 4096
    compression_ratio: float = 0.8
    preserve_system_prompt: bool = True


@dataclass
class AutoDreamConfig:
    """AutoDream configuration.
    
    Attributes:
        time_gate_hours: Hours between consolidations
        session_gate_count: Sessions before consolidation
    """
    time_gate_hours: int = 24
    session_gate_count: int = 5


@dataclass
class CheckpointConfig:
    """Checkpoint configuration.
    
    Attributes:
        storage: Storage type
        storage_dir: Storage directory
        max_age_hours: Maximum checkpoint age
        max_checkpoints: Maximum number of checkpoints
    """
    storage: str = "file"
    storage_dir: str = "/tmp/torro_checkpoints"
    max_age_hours: int = 24
    max_checkpoints: int = 100


@dataclass
class TorroConfig:
    """Main Torro configuration.
    
    Attributes:
        app_name: Application name
        environment: Environment name
        log_level: Logging level
        coordinator_mode: Enable coordinator mode
        openai: OpenAI API configuration
        memory: Memory configuration
        context: Context configuration
        autodream: AutoDream configuration
        checkpoints: Checkpoint configuration
    """
    app_name: str = "Torro Agent Framework"
    environment: str = "DEV"
    log_level: str = "INFO"
    coordinator_mode: bool = True
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    autodream: AutoDreamConfig = field(default_factory=AutoDreamConfig)
    checkpoints: CheckpointConfig = field(default_factory=CheckpointConfig)


class Config:
    """Configuration loader and accessor.
    
    Example:
        ```python
        config = Config()
        config.load("config.ini")
        
        # Access configuration
        print(config.openai.base_url)
        print(config.openai.model)
        ```
    """
    
    _instance: Optional["Config"] = None
    
    def __new__(cls) -> "Config":
        """Create or return singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._config: Optional[TorroConfig] = None
        self._initialized = True
    
    def load(self, config_path: str) -> TorroConfig:
        """FN:load Load configuration from INI file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            TorroConfig instance
        """
        logger.info("FN:Config.load Loading config from: %s", config_path)
        
        if not os.path.exists(config_path):
            logger.warning("FN:Config.load Config file not found: %s", config_path)
            self._config = TorroConfig()
            return self._config
        
        parser = configparser.ConfigParser()
        parser.read(config_path)
        
        # Parse OpenAI section
        openai = OpenAIConfig(
            provider=parser.get("OPENAI_API", "provider", fallback="OpenAI Compatible"),
            base_url=parser.get("OPENAI_API", "base_url", fallback=""),
            api_key=parser.get("OPENAI_API", "api_key", fallback=""),
            model=parser.get("OPENAI_API", "model", fallback=""),
            max_tokens=parser.getint("OPENAI_API", "max_tokens", fallback=8192),
            temperature=parser.getfloat("OPENAI_API", "temperature", fallback=0.7),
            top_p=parser.getfloat("OPENAI_API", "top_p", fallback=0.9),
            timeout=parser.getint("OPENAI_API", "timeout", fallback=120),
        )
        
        # Parse Memory section
        memory = MemoryConfig(
            provider=parser.get("MEMORY", "provider", fallback="builtin"),
            top_k=parser.getint("MEMORY", "top_k", fallback=5),
            retention_days=parser.getint("MEMORY", "retention_days", fallback=30),
        )
        
        # Parse Context section
        context = ContextConfig(
            engine=parser.get("CONTEXT", "engine", fallback="builtin"),
            max_tokens=parser.getint("CONTEXT", "max_tokens", fallback=4096),
            compression_ratio=parser.getfloat("CONTEXT", "compression_ratio", fallback=0.8),
            preserve_system_prompt=parser.getboolean("CONTEXT", "preserve_system_prompt", fallback=True),
        )
        
        # Parse AutoDream section
        autodream = AutoDreamConfig(
            time_gate_hours=parser.getint("AUTODREAM", "time_gate_hours", fallback=24),
            session_gate_count=parser.getint("AUTODREAM", "session_gate_count", fallback=5),
        )
        
        # Parse Checkpoints section
        checkpoints = CheckpointConfig(
            storage=parser.get("CHECKPOINTS", "storage", fallback="file"),
            storage_dir=parser.get("CHECKPOINTS", "storage_dir", fallback="/tmp/torro_checkpoints"),
            max_age_hours=parser.getint("CHECKPOINTS", "max_age_hours", fallback=24),
            max_checkpoints=parser.getint("CHECKPOINTS", "max_checkpoints", fallback=100),
        )
        
        # Parse General section
        self._config = TorroConfig(
            app_name=parser.get("GENERAL", "app_name", fallback="Torro Agent Framework"),
            environment=parser.get("GENERAL", "environment", fallback="DEV"),
            log_level=parser.get("GENERAL", "log_level", fallback="INFO"),
            coordinator_mode=parser.getboolean("GENERAL", "coordinator_mode", fallback=True),
            openai=openai,
            memory=memory,
            context=context,
            autodream=autodream,
            checkpoints=checkpoints,
        )
        
        logger.info("FN:Config.load Configuration loaded successfully")
        return self._config
    
    @property
    def config(self) -> TorroConfig:
        """FN:config Get configuration.
        
        Returns:
            TorroConfig instance
        """
        if self._config is None:
            self._config = TorroConfig()
        return self._config
    
    @property
    def openai(self) -> OpenAIConfig:
        """FN:openai Get OpenAI configuration.
        
        Returns:
            OpenAIConfig instance
        """
        return self.config.openai
    
    @property
    def memory(self) -> MemoryConfig:
        """FN:memory Get memory configuration.
        
        Returns:
            MemoryConfig instance
        """
        return self.config.memory
    
    @property
    def context(self) -> ContextConfig:
        """FN:context Get context configuration.
        
        Returns:
            ContextConfig instance
        """
        return self.config.context
    
    @property
    def autodream(self) -> AutoDreamConfig:
        """FN:autodream Get AutoDream configuration.
        
        Returns:
            AutoDreamConfig instance
        """
        return self.config.autodream
    
    @property
    def checkpoints(self) -> CheckpointConfig:
        """FN:checkpoints Get checkpoint configuration.
        
        Returns:
            CheckpointConfig instance
        """
        return self.config.checkpoints


# Module-level functions
_config_instance: Optional[Config] = None


def load_config(config_path: Optional[str] = None) -> TorroConfig:
    """FN:load_config Load configuration from INI file.
    
    Args:
        config_path: Path to configuration file.
                    Defaults to config.ini in current directory.
                    
    Returns:
        TorroConfig instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config()
    
    if config_path is None:
        config_path = "config.ini"
    
    return _config_instance.load(config_path)


def get_config() -> TorroConfig:
    """FN:get_config Get configuration instance.
    
    Returns:
        TorroConfig instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config()
    
    return _config_instance.config
