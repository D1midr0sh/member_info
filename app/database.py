from sqlmodel import create_engine, SQLModel, Session

from .users import models


sqlite_file_name = 'membership.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'  # TODO: move to .env

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)

def create_session():
    with Session(engine) as session:
        return session
