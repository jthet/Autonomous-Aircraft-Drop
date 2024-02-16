# test_app.py

import sys
from pathlib import Path

# Add the parent directory to sys.path to import app
sys.path.append(str(Path(__file__).parent.parent))

from app import add_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2

