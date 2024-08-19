from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
