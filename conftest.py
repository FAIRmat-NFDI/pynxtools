"""Root conftest: ensures local src/ takes precedence over installed packages.

This is needed during development when running tests from a git worktree where
the editable install may point to a different source tree.
"""
import sys
from pathlib import Path

_SRC = str(Path(__file__).parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
