import re
from enum import Enum
from pathlib import Path
from typing import Optional, Union
from urllib.parse import quote_plus


class DatabaseUrlError(Exception): ...


class InvalidEngine(DatabaseUrlError): ...


class DbDefaultEnum(Enum):
    """Db type -- username, password, port"""

    postgres = "postgres", "postgres", 5432
    mysql = "root", "123456", 3306
    mssql = "sa", "Abcd12345678", 1432
    oracle = "SYSTEM", "123456", 1521


def should_quote(value: str) -> bool:
    return not re.match(r"[-%\w]+$", value)


def generate(
    name: Union[Path, str, None] = "db.sqlite3",
    engine: str = "sqlite",
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: Union[str, int, None] = None,
    **extras,
) -> str:
    if engine == "sqlite" or (engine := engine.split(".")[-1]) in ("sqlite", "sqlite3"):
        if name is None:
            name = ":memory:"
        return f"sqlite://{name}"
    if engine in (
        "postgres",
        "asyncpg",
        "psycopg",
        "postgresql",
    ):
        engine = engine.replace("postgresql", "postgres")
        default_user, default_pw, default_port = DbDefaultEnum.postgres.value
    elif engine in ("mysql", "mariadb"):
        default_user, default_pw, default_port = DbDefaultEnum.mysql.value
    elif engine == "mssql":
        default_user, default_pw, default_port = DbDefaultEnum.mssql.value
    elif engine == "oracle":
        default_user, default_pw, default_port = DbDefaultEnum.oracle.value
    else:
        raise InvalidEngine(engine)
    if port is None:
        port = default_port
    if host is None:
        host = "127.0.0.1"
    if user is None:
        user = default_user
    if password is None:
        password = default_pw
    elif should_quote(password):
        password = quote_plus(password)
    url = f"{engine}://{user}:{password}@{host}:{port}/{name}"
    if extras:
        url += "?" + "&".join(f"{k}={v}" for k, v in extras.items())
    return url


def from_django_item(default: dict) -> str:
    return generate(**{k.lower(): v for k, v in default.items()})
