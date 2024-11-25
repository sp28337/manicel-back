from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from settings import Settings


settings = Settings()

engine = create_async_engine(
    url=settings.get_db_url,
    future=True,
    echo=True,
    pool_pre_ping=True,
)

LocalAsyncSession = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_async_db_session() -> AsyncSession:
    return LocalAsyncSession
