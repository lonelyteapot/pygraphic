from pathlib import Path

import pytest
from pytest import FixtureRequest


@pytest.fixture
def script_directory(request: FixtureRequest):
    """Return the directory of the currently running test script"""
    return Path(request.path).parent
