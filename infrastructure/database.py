from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import Settings


settings = Settings()

engine = create_engine(
    # echo=True,
    url=settings.get_db_url,
)

LocalSession: Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session() -> LocalSession:
    return LocalSession
