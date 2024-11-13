from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("postgresql+psycopg2://postgres:password@0.0.0.0:5432/postgres", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db_session():
    with Session() as session:
        return session
