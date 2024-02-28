from os import getenv


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
    _db_port = getenv("DATABASE_PORT", "5432")
    _db_name = getenv("POSTGRES_DB", "mp_db")
    # return f"postgresql+psycopg://{user}:{password}@{server}/{db}"
    return f"postgresql://{_db_user}:{_db_pass}@{_db_server}:{_db_port}/{_db_name}"
