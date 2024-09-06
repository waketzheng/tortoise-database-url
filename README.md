# database-url
![Python Versions](https://img.shields.io/pypi/pyversions/tortoise-database-url)
[![LatestVersionInPypi](https://img.shields.io/pypi/v/tortoise-database-url.svg?style=flat)](https://pypi.org/project/tortoise-database-url/)
[![GithubActionResult](https://github.com/waketzheng/database-url/workflows/ci/badge.svg)](https://github.com/waketzheng/database-url/actions?query=workflow:ci)
[![Coverage Status](https://coveralls.io/repos/github/waketzheng/database-url/badge.svg?branch=main)](https://coveralls.io/github/waketzheng/database-url?branch=main)
![Mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Some async functions that using anyio, and toolkit for excel read.

## Installation

```bash
pip install tortoise-database-url
```

## Usage

- generate

```py
import database_url

db_url = database_url.generate('my_db', engine='mysql', user='root', password='Me@example.com')
print(db_url)
# mysql://root@Me%40example.com/127.0.0.1:3306/my_db
```

- from_django_item
```py
import pathlib
import database_url

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": pathlib.Path("/tmp") / "db.sqlite3"
    },
}

db_url = database_url.from_django_item(DATABASES["default"])
print(db_url)
# sqlte:///tmp/db.sqlite3
```
See more at: https://github.com/waketzheng/database-url/blob/main/tests/test_main.py
