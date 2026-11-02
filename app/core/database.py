from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

url = get_settings().DATABASE_URL
connect_args = {"ssl": "require"} if get_settings().ENV == "prod" else {}

engine = create_async_engine(
    url=str(get_settings().DATABASE_URL),
    connect_args=connect_args,
    echo=get_settings().ENV != "prod",
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
