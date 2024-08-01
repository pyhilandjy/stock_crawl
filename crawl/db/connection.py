# import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

postgresql_url = (
    "postgresql+psycopg2://ultimax:The1upm^^@210.222.115.23:65432/ultimax_dev"
)

Base = declarative_base()


class DBConnection:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_db(self):
        db_session = self.SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()


postgresql_connection = DBConnection(postgresql_url)
