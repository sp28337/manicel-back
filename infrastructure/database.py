from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import Settings

settings = Settings()

engine = create_engine(
    echo=True,
    url=settings.get_db_url,
)
LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)




def get_db_session():
    with LocalSession() as session:
        return session
