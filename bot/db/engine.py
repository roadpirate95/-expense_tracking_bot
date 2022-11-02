from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import Union

from bot import config


class Database:
    """Класс подключения к бд"""
    def __init__(self, url: Union[URL, str]):
        async_engine: AsyncEngine = create_async_engine(url, echo=True, encoding='utf-8', pool_pre_ping=True)
        async_session: sessionmaker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
        self.session: AsyncSession = async_session()


database = Database(config.URL_db)
