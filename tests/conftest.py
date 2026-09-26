from collections.abc import Generator
from pathlib import Path

import pytest
from asynctor.compat import chdir


@pytest.fixture
def tmp_workdir(tmp_path: Path) -> Generator[Path]:
    with chdir(tmp_path):
        yield tmp_path
