# tests/test_app.py
"""Tests for the arithmetic operations in app module."""

import sys
from pathlib import Path

# Add the parent directory to sys.path to import app
# pylint: disable=wrong-import-position
sys.path.append(str(Path(__file__).parent.parent))

from app import add_numbers

def test_add_numbers():
    """Test that add_numbers correctly adds two numbers."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2
