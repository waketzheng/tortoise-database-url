from pathlib import Path
from typing import Dict

import pytest

from database_url import DbDefaultEnum, InvalidEngine, from_django_item, generate

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES: Dict[str, dict] = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "xe",
        "USER": "a_user",
        "PASSWORD": "a_password",
        "HOST": "dbprod01ned.mycompany.com",
        "PORT": "1540",
    },
    "MySQL/MariaDB": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test_1",
    },
    "psql": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": None,
    },
    "oracle": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "",
    },
    "sqlite": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "test.db"},
    "complex_password": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "foo",
        "PASSWORD": "Hello@world",
    },
    "quoted_password": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "foo",
        "PASSWORD": "Hello%40world",
    },
}


def test_django_item() -> None:
    assert (
        from_django_item(DATABASES["default"])
        == "oracle://a_user:a_password@dbprod01ned.mycompany.com:1540/xe"
    )
    assert (
        from_django_item(DATABASES["MySQL/MariaDB"])
        == "mysql://root:123456@127.0.0.1:3306/test_1"
    )
    assert (
        from_django_item(DATABASES["psql"])
        == "postgres://postgres:postgres@127.0.0.1:5432/None"
    )
    assert (
        from_django_item(DATABASES["oracle"])
        == "oracle://SYSTEM:123456@127.0.0.1:1521/"
    )
    assert from_django_item(DATABASES["sqlite"]) == f"sqlite://{BASE_DIR/'test.db'}"
    assert (
        from_django_item(DATABASES["complex_password"])
        == from_django_item(DATABASES["quoted_password"])
        == "mysql://root:Hello%40world@127.0.0.1:3306/foo"
    )


def test_generate() -> None:
    assert generate(None) == "sqlite://:memory:"
    assert generate() == "sqlite://db.sqlite3"
    assert generate(BASE_DIR / "db.sqlite3") == f"sqlite://{BASE_DIR/'db.sqlite3'}"
    # postgresql
    default_postgres_port: int = DbDefaultEnum.postgres.value[-1]
    assert (
        generate("my_db", engine="postgres")
        == generate("my_db", engine="postgresql")
        == (f"postgres://postgres:postgres@127.0.0.1:{default_postgres_port}/my_db")
    )
    assert generate("my_db", engine="asyncpg") == (
        f"asyncpg://postgres:postgres@127.0.0.1:{default_postgres_port}/my_db"
    )
    assert generate("my_db", engine="psycopg") == (
        f"psycopg://postgres:postgres@127.0.0.1:{default_postgres_port}/my_db"
    )
    # MySQL & MariaDB
    default_mysql_port: int = DbDefaultEnum.mysql.value[-1]
    assert (
        generate("my_db", engine="mysql")
        == generate("my_db", engine="mariadb")
        == (f"mysql://root:123456@127.0.0.1:{default_mysql_port}/my_db")
    )
    assert (
        generate("test_db", "mssql") == "mssql://sa:Abcd12345678@127.0.0.1:1432/test_db"
    )
    # Other
    assert (
        generate("test_db", "mssql", driver="ODBC Driver 18 for SQL Server")
        == "mssql://sa:Abcd12345678@127.0.0.1:1432/test_db?driver=ODBC Driver 18 for SQL Server"
    )

    with pytest.raises(InvalidEngine):
        generate(engine="mongo")
