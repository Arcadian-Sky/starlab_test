import os
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значения DATABASE_URL из переменных окружения
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL environment variable is not set")

# Создание асинхронного engine
engine = create_async_engine(DATABASE_URL, echo=True)


async def create_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Error initializing database: {str(e)}")


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
