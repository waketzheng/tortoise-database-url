import subprocess  # nosec
from pathlib import Path

from tortoise_database_url import __version__


def capture_output(command: list[str]) -> str:
    r = subprocess.run(command, capture_output=True, check=False)
    return r.stdout.decode().strip()


def test_version():
    out = capture_output(["pdm", "list", "--fields=name,version", "--csv"])
    try:
        me = next(j for i in out.splitlines() if (j := i.split(","))[0] == "tortoise-database-url")
    except IndexError:
        # TODO: remove this when deps of python3.14 can be install by pdm in ci
        assert __version__ in Path("src/tortoise_database_url/__init__.py").read_text()
    else:
        assert me[-1] == __version__
