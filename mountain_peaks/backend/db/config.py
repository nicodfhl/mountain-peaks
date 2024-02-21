from os import environ, getenv

_db_user_f = environ.get("POSTGRES_USER_FILE")
_db_pawd_f = environ.get("POSTGRES_PASSWORD_FILE")
if _db_user_f and _db_pawd_f:
    with open(_db_user_f, "r") as f:
        _db_user = f.read()
    with open(_db_pawd_f, "r") as f:
        _db_pass = f.read()


def hard_get_base_uri():
    return "postgresql://fake_username:fake_password@db:5432/mp_db"


def get_base_uri():
    DEBUG = environ.get("DEBUG")
    DB_USER = getenv("POSTGRES_USER", "fake_username")  # _db_user
    DB_PASS = getenv("POSTGRES_PASSWORD", "fake_password")  # _db_pawd_f
    DB_SERVER = getenv("POSTGRES_SERVER", "postgres-db")
    DB_PORT = getenv("DATABASE_PORT", "5432")
    DB_NAME = getenv("POSTGRES_DB", "mp_db")
    return f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


def get_base_uri_psycopg():
    user = getenv("POSTGRES_USER", "postgres")
    password = getenv("POSTGRES_PASSWORD", "")
    server = getenv("POSTGRES_SERVER", "db")
    db = getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}/{db}"
