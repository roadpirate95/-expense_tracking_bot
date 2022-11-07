from datetime import datetime

from sqlalchemy import Column, Integer, String, VARCHAR, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import select, or_

from bot import db


BaseModel = declarative_base()


class User(BaseModel):

    __tablename__ = 'users'

    user_id = Column(Integer(), unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    date_registration = Column(Date, default=datetime.today())

    @classmethod
    async def create_user(cls, **kwargs) -> None:
        """Создает нового пользователя"""
        res = await db.database.session.get(cls, kwargs['user_id'])
        if not res:
            user = cls(**kwargs)
            db.database.session.add(user)
            await db.database.session.commit()


class Category(BaseModel):

    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name_category = Column(String(100), unique=True, nullable=False)
    aliases = Column(String(150))
    id_user = Column(Integer(), ForeignKey('users.user_id'), nullable=True)

    @classmethod
    async def category_list(cls, user_id):
        """Возвращает все категории созданные пользователем и категории заложенные в бота"""
        return (await db.database.session.execute(
            select(cls.name_category, cls.aliases).
            where(or_(cls.id_user == user_id, cls.id_user == None)))).all()

    @classmethod
    async def create_category(cls, user_id: int, category: str, alias=None):
        """Создание и сохранение в бд пользовательской категории"""
        create_custom_category = cls(name_category=category, aliases=alias, id_user=user_id)
        db.database.session.add(create_custom_category)
        await db.database.session.commit()

    @staticmethod
    def parse_text(text) -> tuple[str, int]:
        """Парсит текст занесения расхода"""
        arr = text.split(' ')
        return arr[0].lower(), int(arr[1])


class Price(BaseModel):

    __tablename__ = 'prices'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    amount = Column(Integer(), nullable=False)
    date = Column(Date, default=datetime.today())
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    category_id = Column(Integer(), ForeignKey('categories.id'))

    @classmethod
    async def create_price(cls, **kwargs) -> None:
        """Создает и сохраняет цену"""
        create_price_object = cls(**kwargs)
        db.database.session.add(create_price_object)
        await db.database.session.commit()
