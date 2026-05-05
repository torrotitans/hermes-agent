# Torro Agent Framework Makefile
# Apache-style build and run targets
#
# Usage:
#   make help          Show available commands
#   make run           Run the Hello World example
#   make test          Run all unit tests
#   make lint          Run linting checks
#   make clean         Clean build artifacts

.PHONY: help run run-quickstart test lint clean setup cli status

# Default target
help:
	@echo "=== Torro Agent Framework ==="
	@echo ""
	@echo "Available commands:"
	@echo "  make run           Run Hello World example"
	@echo "  make run-quickstart Run quickstart example"
	@echo "  make cli           Run interactive CLI mode"
	@echo "  make test          Run all unit tests"
	@echo "  make lint          Run linting checks"
	@echo "  make clean         Clean build artifacts"
	@echo "  make setup         Set up development environment"
	@echo "  make status        Check Torro status"
	@echo ""
	@echo "Configuration:"
	@echo "  Edit config.ini to configure OpenAI API settings"
	@echo ""

# Run Hello World example
run:
	@echo "=== Running Torro Agent Hello World ==="
	PYTHONPATH=$(PWD)/src python3 examples/agent_helloworld.py

# Run quickstart example
run-quickstart:
	@echo "=== Running Torro Quickstart ==="
	PYTHONPATH=$(PWD)/src python3 examples/quickstart.py

# Run all unit tests
test:
	@echo "=== Running Torro Unit Tests ==="
	PYTHONPATH=$(PWD)/src python3 -m pytest tests/unit/ -v --tb=short

# Run linting checks
lint:
	@echo "=== Running Lint Checks ==="
	python3 -m flake8 src/torro/ examples/ tests/unit/ --max-line-length=100 --ignore=E501,W503 || true

# Clean build artifacts
clean:
	@echo "=== Cleaning Build Artifacts ==="
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/torro/__pycache__
	rm -rf src/torro/*/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/unit/__pycache__
	rm -rf tests/unit/*/__pycache__
	rm -rf .pytest_cache
	rm -rf output/
	rm -rf /tmp/torro_checkpoints
	@echo "Clean complete."

# Set up development environment
setup:
	@echo "=== Setting Up Development Environment ==="
	python3 -m pip install -r requirements.txt
	@echo "Setup complete."

# Check Torro status
status:
	@echo "=== Torro Status ==="
	PYTHONPATH=$(PWD)/src python3 -m src.cli status

# Run interactive CLI
cli:
	@echo "=== Torro Interactive CLI ==="
	PYTHONPATH=$(PWD)/src python3 -m src.cli interactive

# Run with verbose output
run-verbose:
	@echo "=== Running Torro Agent (Verbose) ==="
	PYTHONPATH=$(PWD)/src python3 examples/agent_helloworld.py

# Check Python version
python-version:
	@echo "=== Python Version ==="
	python3 --version

# Show configuration
show-config:
	@echo "=== Torro Configuration ==="
	PYTHONPATH=$(PWD)/src python3 -c "from torro.config import get_config; c = get_config(); print(f'App: {c.app_name}'); print(f'Environment: {c.environment}'); print(f'Model: {c.openai.model}'); print(f'API URL: {c.openai.base_url}')"
