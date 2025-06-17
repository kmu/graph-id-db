"""Pytest configuration and fixtures for the graphid-db tests."""

import pytest
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))