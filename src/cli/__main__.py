"""
FN:__main__.py
Entry point for running src.cli as a module.

Usage:
    python3 -m src.cli interactive
    python3 -m src.cli status
    python3 -m src.cli --version
"""

import sys
from cli import main

if __name__ == "__main__":
    sys.exit(main())
