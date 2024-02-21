from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# from backend.app.main import app, db
# with app.app_context():
#     db.create_all()


from .config import get_base_uri

# create the db engine instance
_ENGINE = create_engine(get_base_uri())


def get_session(engine=_ENGINE):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # provides the database session and called in each endpoint
    database = get_session()()
    try:
        yield database
    finally:
        # close the db after each request
        database.close()


class Base(DeclarativeBase):
    @classmethod
    def create_all_tables(cls, engine=None):
        # make sure the original database is used properly
        if (
            engine is None
            and getenv("AUTHORIZE_PROD_DB_TABLES_CREATION", "NO") == "YES"
        ):
            engine = _ENGINE
        cls.metadata.create_all(bind=engine)
