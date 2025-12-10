from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.settings import Settings


settings = Settings()

engine = create_async_engine(
    url=settings.get_db_url,
    future=True,
    # echo=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
