from pathlib import Path

import pytest


@pytest.fixture
def golden_dir():
    """Return the directory of the currently running test script"""
    return Path("golden_files")
