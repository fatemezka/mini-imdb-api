import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

load_dotenv()

# SQLALCHEMY POSTGRESQL
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
        from app.models import User, Listing
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def drop_all_tables():
    async with engine.begin() as conn:
        from app.models import User, Listing
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
