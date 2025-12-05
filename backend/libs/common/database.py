from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from libs.common.config import settings


if settings.DATABASE_URL:
    DATABASE_URL = settings.DATABASE_URL
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DATABASE_USER}:"
        f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:"
        f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    )

# Engine
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,
)

# Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
