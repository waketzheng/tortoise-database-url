import subprocess  # nosec
import sys
from pathlib import Path

from database_url import __version__

if sys.version_info >= (3, 11):
    from contextlib import chdir

else:
    import contextlib
    import os

    class chdir(contextlib.AbstractContextManager):  # Copied from source code of Python3.13
        """Non thread-safe context manager to change the current working directory."""

        def __init__(self, path) -> None:
            self.path = path
            self._old_cwd: list[str] = []

        def __enter__(self) -> None:
            self._old_cwd.append(os.getcwd())
            os.chdir(self.path)

        def __exit__(self, *excinfo) -> None:
            os.chdir(self._old_cwd.pop())


def test_version():
    r = subprocess.run(["pdm", "list", "--fields=name,version", "--csv"], capture_output=True)
    out = r.stdout.decode().strip()
    try:
        me = [j for i in out.splitlines() if (j := i.split(","))[0] == "tortoise-database-url"][0]
    except IndexError:
        # TODO: remove this when deps of python3.14 can be install by pdm in ci
        assert __version__ in Path("database_url/__init__.py").read_text()
    else:
        assert me[-1] == __version__
