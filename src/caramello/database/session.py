from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

from caramello.core.config import settings

sqlite_url = settings.database_url

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
