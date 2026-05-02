"""
FN:test_config.py
Unit tests for Torro configuration.

Tests:
- TestTorroConfig: Test TorroConfig dataclass
- TestConfig: Test Config class
- TestLoadConfig: Test load_config function
"""

import pytest
import tempfile
import os

from config import (
    Config,
    TorroConfig,
    OpenAIConfig,
    MemoryConfig,
    ContextConfig,
    AutoDreamConfig,
    CheckpointConfig,
    load_config,
    get_config,
)


class TestTorroConfig:
    """Test TorroConfig dataclass."""
    
    def test_torro_config_defaults(self):
        """Test TorroConfig default values."""
        config = TorroConfig()
        assert config.app_name == "Torro Agent Framework"
        assert config.environment == "DEV"
        assert config.log_level == "INFO"
        assert config.coordinator_mode is True
    
    def test_torro_config_custom_values(self):
        """Test TorroConfig with custom values."""
        config = TorroConfig(
            app_name="Custom App",
            environment="PROD",
            log_level="DEBUG"
        )
        assert config.app_name == "Custom App"
        assert config.environment == "PROD"
        assert config.log_level == "DEBUG"


class TestOpenAIConfig:
    """Test OpenAIConfig dataclass."""
    
    def test_openai_config_defaults(self):
        """Test OpenAIConfig default values."""
        config = OpenAIConfig()
        assert config.provider == "OpenAI Compatible"
        assert config.base_url == ""
        assert config.api_key == ""
        assert config.model == ""
        assert config.max_tokens == 8192
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.timeout == 120
    
    def test_openai_config_custom_values(self):
        """Test OpenAIConfig with custom values."""
        config = OpenAIConfig(
            provider="Azure",
            base_url="http://localhost:8000/v1",
            api_key="test-key",
            model="test-model",
            max_tokens=4096,
            temperature=0.5,
            top_p=0.8,
            timeout=60
        )
        assert config.provider == "Azure"
        assert config.base_url == "http://localhost:8000/v1"
        assert config.api_key == "test-key"
        assert config.model == "test-model"
        assert config.max_tokens == 4096
        assert config.temperature == 0.5
        assert config.top_p == 0.8
        assert config.timeout == 60


class TestConfig:
    """Test Config class."""
    
    def test_config_singleton(self):
        """Test Config is a singleton."""
        config1 = Config()
        config2 = Config()
        assert config1 is config2
    
    def test_config_load_nonexistent_file(self):
        """Test loading nonexistent config file."""
        config = Config()
        result = config.load("nonexistent.ini")
        assert isinstance(result, TorroConfig)
        assert result.environment == "DEV"
    
    def test_config_load_from_file(self, tmp_path):
        """Test loading config from file."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("""
[GENERAL]
app_name = Test App
environment = UAT

[OPENAI_API]
provider = Azure
base_url = http://test:8000/v1
api_key = test-key
model = test-model
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        assert result.app_name == "Test App"
        assert result.environment == "UAT"
        assert result.openai.provider == "Azure"
        assert result.openai.base_url == "http://test:8000/v1"
        assert result.openai.api_key == "test-key"
        assert result.openai.model == "test-model"
    
    def test_config_load_all_sections(self, tmp_path):
        """Test loading all config sections."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("""
[GENERAL]
app_name = Test App
environment = PROD
log_level = DEBUG
coordinator_mode = false

[OPENAI_API]
base_url = http://test:8000/v1
model = test-model
max_tokens = 4096
temperature = 0.5
top_p = 0.8
timeout = 60

[MEMORY]
provider = vector
top_k = 10
retention_days = 60

[CONTEXT]
engine = lcm
max_tokens = 8192
compression_ratio = 0.5

[AUTODREAM]
time_gate_hours = 48
session_gate_count = 10

[CHECKPOINTS]
storage = memory
storage_dir = /tmp/test
max_age_hours = 12
max_checkpoints = 50
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        assert result.app_name == "Test App"
        assert result.environment == "PROD"
        assert result.log_level == "DEBUG"
        assert result.coordinator_mode is False
        assert result.openai.max_tokens == 4096
        assert result.openai.temperature == 0.5
        assert result.memory.provider == "vector"
        assert result.memory.top_k == 10
        assert result.context.engine == "lcm"
        assert result.autodream.time_gate_hours == 48
        assert result.checkpoints.storage == "memory"


class TestLoadConfig:
    """Test load_config function."""
    
    def test_load_config_default(self):
        """Test load_config with default path."""
        # Reset global state
        import config as config_module
        config_module._config_instance = None
        
        # Load with nonexistent default path
        result = load_config()
        assert isinstance(result, TorroConfig)
    
    def test_load_config_custom_path(self, tmp_path):
        """Test load_config with custom path."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("""
[GENERAL]
app_name = Custom Config

[OPENAI_API]
base_url = http://custom:8000/v1
""")
        
        # Reset global state
        import config as config_module
        config_module._config_instance = None
        
        result = load_config(str(config_file))
        assert result.app_name == "Custom Config"
        assert result.openai.base_url == "http://custom:8000/v1"


class TestGetConfig:
    """Test get_config function."""
    
    def test_get_config(self):
        """Test get_config function."""
        # Reset global state
        import config as config_module
        config_module._config_instance = None
        
        config = get_config()
        assert isinstance(config, TorroConfig)
        assert config.environment == "DEV"
