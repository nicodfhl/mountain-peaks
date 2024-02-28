from os import getenv
from pydantic import PostgresDsn


def get_base_uri():
    _db_user_f = getenv("POSTGRES_USER_FILE")
    _db_pawd_f = getenv("POSTGRES_PASSWORD_FILE")
    if not (_db_user_f and _db_pawd_f):
        raise IOError("Secret files should exist")
    with open(_db_user_f, "r") as f:
        _db_user = f.read()
    with open(_db_pawd_f, "r") as f:
        _db_pass = f.read()
    _debug = getenv("DEBUG")
    _db_server = getenv("POSTGRES_SERVER")
    _db_port = int(getenv("DATABASE_PORT"))
    _db_name = getenv("POSTGRES_DB")
    return str(PostgresDsn.build(
        scheme="postgresql",
        username=_db_user,
        password=_db_pass,
        host=_db_server,
        port=_db_port,
        path=_db_name,
    ))
