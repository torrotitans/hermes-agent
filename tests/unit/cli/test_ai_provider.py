"""
FN:test_ai_provider.py
Unit tests for AI provider components.

Functions:
- FN:test_model_config: Test ModelConfig dataclass (lines 20-40)
- FN:test_model_registry: Test ModelRegistry (lines 43-80)
- FN:test_ollama_provider: Test OllamaProvider (lines 83-120)
- FN:test_openai_provider: Test OpenAIProvider (lines 123-150)
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import json

sys.path.insert(0, 'src')
from cli.ai_provider import (
    ModelConfig,
    ModelRegistry,
    OllamaProvider,
    OpenAIProvider,
    create_provider,
    SwarmConfig
)


class TestModelConfig(unittest.TestCase):
    """Test cases for ModelConfig dataclass."""
    
    def test_model_config_creation(self):
        """FN:test_model_config Test ModelConfig creation."""
        config = ModelConfig(
            name="test_model",
            provider_type="ollama",
            model_name="qwen2.5:7b",
            base_url="http://localhost:11434"
        )
        
        self.assertEqual(config.name, "test_model")
        self.assertEqual(config.provider_type, "ollama")
        self.assertEqual(config.model_name, "qwen2.5:7b")
        self.assertEqual(config.base_url, "http://localhost:11434")
        self.assertEqual(config.context_window, 32768)
        self.assertTrue(config.supports_streaming)
        self.assertFalse(config.supports_images)
        self.assertFalse(config.supports_reasoning)
        self.assertIsNone(config.api_key)
    
    def test_model_config_with_all_fields(self):
        """FN:test_model_config_with_all_fields Test ModelConfig with all fields."""
        config = ModelConfig(
            name="advanced_model",
            provider_type="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com/v1",
            context_window=128000,
            supports_streaming=True,
            supports_images=True,
            supports_reasoning=True,
            api_key="sk-xxx"
        )
        
        self.assertEqual(config.context_window, 128000)
        self.assertTrue(config.supports_images)
        self.assertTrue(config.supports_reasoning)
        self.assertEqual(config.api_key, "sk-xxx")


class TestModelRegistry(unittest.TestCase):
    """Test cases for ModelRegistry class."""
    
    def test_model_registry_empty(self):
        """FN:test_model_registry_empty Test registry with no config."""
        registry = ModelRegistry()
        
        # Registry loads from config.ini, so we check that models exist
        self.assertIsInstance(registry.default_model, str)
        self.assertIsInstance(registry.swarm_model, str)
    
    def test_model_registry_get_model(self):
        """FN:test_model_registry_get_model Test getting model by name."""
        registry = ModelRegistry()
        
        # Add a test model
        registry._models["test_model"] = ModelConfig(
            name="test_model",
            provider_type="ollama",
            model_name="test:7b",
            base_url="http://localhost:11434"
        )
        
        model = registry.get_model("test_model")
        self.assertEqual(model.name, "test_model")
        self.assertEqual(model.provider_type, "ollama")
    
    def test_model_registry_get_model_not_found(self):
        """FN:test_model_registry_get_model_not_found Test getting non-existent model."""
        registry = ModelRegistry()
        
        model = registry.get_model("nonexistent")
        self.assertIsNone(model)
    
    def test_model_registry_list_models(self):
        """FN:test_model_registry_list_models Test listing all models."""
        registry = ModelRegistry()
        
        initial_count = len(registry.list_models())
        
        registry._models["model1"] = ModelConfig(
            name="model1",
            provider_type="ollama",
            model_name="model1:7b",
            base_url="http://localhost:11434"
        )
        registry._models["model2"] = ModelConfig(
            name="model2",
            provider_type="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com/v1"
        )
        
        models = registry.list_models()
        self.assertEqual(len(models), initial_count + 2)
    
    def test_model_registry_get_models_by_provider(self):
        """FN:test_model_registry_get_models_by_provider Test filtering by provider."""
        registry = ModelRegistry()
        
        initial_count = len(registry.get_models_by_provider("ollama"))
        
        registry._models["ollama_model"] = ModelConfig(
            name="ollama_model",
            provider_type="ollama",
            model_name="llama:7b",
            base_url="http://localhost:11434"
        )
        registry._models["openai_model"] = ModelConfig(
            name="openai_model",
            provider_type="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com/v1"
        )
        
        ollama_models = registry.get_models_by_provider("ollama")
        self.assertEqual(len(ollama_models), initial_count + 1)
        self.assertEqual(ollama_models[-1].name, "ollama_model")


class TestSwarmConfig(unittest.TestCase):
    """Test cases for SwarmConfig class."""
    
    def test_swarm_config_defaults(self):
        """FN:test_swarm_config_defaults Test default swarm config."""
        config = SwarmConfig()
        
        self.assertTrue(config.enabled)
        self.assertEqual(config.min_models, 2)
        self.assertEqual(config.max_models, 4)
        self.assertEqual(config.strategy, "debate")
    
    def test_swarm_config_custom(self):
        """FN:test_swarm_config_custom Test custom swarm config."""
        config = SwarmConfig(
            enabled=False,
            min_models=1,
            max_models=3,
            strategy="voting"
        )
        
        self.assertFalse(config.enabled)
        self.assertEqual(config.min_models, 1)
        self.assertEqual(config.max_models, 3)
        self.assertEqual(config.strategy, "voting")


class TestOllamaProvider(unittest.TestCase):
    """Test cases for OllamaProvider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = ModelConfig(
            name="test_model",
            provider_type="ollama",
            model_name="qwen2.5:7b",
            base_url="http://localhost:11434"
        )
        self.provider = OllamaProvider(self.config)
    
    def test_ollama_provider_init(self):
        """FN:test_ollama_provider_init Test OllamaProvider initialization."""
        self.assertEqual(self.provider.config, self.config)
        self.assertEqual(self.provider.endpoint, "http://localhost:11434/api/generate")
    
    @patch('cli.ai_provider.requests.Session')
    def test_ollama_generate(self, mock_session_class):
        """FN:test_ollama_generate Test Ollama generate method."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Hello, World!"}
        mock_session.post.return_value = mock_response
        
        provider = OllamaProvider(self.config)
        result = provider.generate("Test prompt")
        
        self.assertEqual(result, "Hello, World!")
    
    @patch('cli.ai_provider.requests.Session')
    def test_ollama_generate_with_system(self, mock_session_class):
        """FN:test_ollama_generate_with_system Test generate with system prompt."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Response"}
        mock_session.post.return_value = mock_response
        
        provider = OllamaProvider(self.config)
        result = provider.generate("Test prompt", "System prompt")
        
        # Verify system was included in payload
        call_args = mock_session.post.call_args
        payload = call_args[1]['json']
        self.assertEqual(payload["system"], "System prompt")


class TestOpenAIProvider(unittest.TestCase):
    """Test cases for OpenAIProvider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = ModelConfig(
            name="gpt-4",
            provider_type="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com"
        )
        self.provider = OpenAIProvider(self.config)
    
    def test_openai_provider_init(self):
        """FN:test_openai_provider_init Test OpenAIProvider initialization."""
        self.assertEqual(self.provider.config, self.config)
        self.assertEqual(self.provider.endpoint, "https://api.openai.com/v1/chat/completions")
    
    @patch('cli.ai_provider.requests.Session')
    def test_openai_generate(self, mock_session_class):
        """FN:test_openai_generate Test OpenAI generate method."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello, World!"}}]
        }
        mock_session.post.return_value = mock_response
        
        provider = OpenAIProvider(self.config)
        result = provider.generate("Test prompt")
        
        self.assertEqual(result, "Hello, World!")


class TestCreateProvider(unittest.TestCase):
    """Test cases for create_provider factory function."""
    
    @patch('cli.ai_provider.ModelRegistry')
    def test_create_ollama_provider(self, mock_registry_class):
        """FN:test_create_ollama_provider Test creating Ollama provider."""
        mock_registry = MagicMock()
        mock_registry.get_model.return_value = ModelConfig(
            name="test_model",
            provider_type="ollama",
            model_name="qwen2.5:7b",
            base_url="http://localhost:11434"
        )
        mock_registry_class.return_value = mock_registry
        
        provider = create_provider("test_model")
        
        self.assertIsInstance(provider, OllamaProvider)
    
    @patch('cli.ai_provider.ModelRegistry')
    def test_create_openai_provider(self, mock_registry_class):
        """FN:test_create_openai_provider Test creating OpenAI provider."""
        mock_registry = MagicMock()
        mock_registry.get_model.return_value = ModelConfig(
            name="gpt-4",
            provider_type="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com/v1"
        )
        mock_registry_class.return_value = mock_registry
        
        provider = create_provider("gpt-4")
        
        self.assertIsInstance(provider, OpenAIProvider)
    
    @patch('cli.ai_provider.ModelRegistry')
    def test_create_provider_unknown_type(self, mock_registry_class):
        """FN:test_create_provider_unknown_type Test creating provider with unknown type."""
        mock_registry = MagicMock()
        mock_registry.get_model.return_value = ModelConfig(
            name="unknown",
            provider_type="unknown_provider",
            model_name="unknown",
            base_url="http://unknown"
        )
        mock_registry_class.return_value = mock_registry
        
        with self.assertRaises(ValueError) as context:
            create_provider("unknown")
        
        self.assertIn("Unknown provider type", str(context.exception))


if __name__ == '__main__':
    unittest.main()
