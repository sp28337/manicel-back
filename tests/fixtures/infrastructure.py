import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.settings import Settings
from app.infrastructure.orm_base import Base


@pytest_asyncio.fixture
def settings():
    return Settings()


engine = create_async_engine(
    url="postgresql+asyncpg://postgres:password@localhost:5432/postgres-test",
    future=True,
    echo=True,
    pool_pre_ping=True,
)

AsyncSessionTest = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    async with AsyncSessionTest() as session:
        yield session
