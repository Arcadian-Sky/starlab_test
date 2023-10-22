import os
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значения DATABASE_URL из переменных окружения
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL environment variable is not set")

# Создание асинхронного engine
engine = create_async_engine(DATABASE_URL, echo=True)


async def createdbConnection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Error initializing database: {str(e)}")



async def getDbSession() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    # session = async_session()
    # try:
    #     yield session
    # finally:
    #     await session.close()
    return async_session()
