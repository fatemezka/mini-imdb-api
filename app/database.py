import aioredis
import os
from app.models import User, Movie, Cast, Writer, Genre, Review  # TODO
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

load_dotenv()

# POSTGRESQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False)


class Base(DeclarativeBase):
    pass


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


# REDIS
REDIS_URL = os.getenv("REDIS_URL")


async def create_redis_pool():
    redis_pool = await aioredis.from_url(url=REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_pool
