from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import Settings

settings = Settings()

engine = create_engine(
    echo=True,
    url=settings.get_db_url,
)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db_session():
    with Session() as session:
        return session
