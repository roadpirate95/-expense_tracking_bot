from typing import Union

from sqlalchemy import select

from bot import db


class AdminModelUser:

    @classmethod
    async def create_user(cls, **kwargs) -> None:
        res = await db.database.session.get(cls, kwargs['user_id'])
        if not res:
            user = cls(**kwargs)
            db.database.session.add(user)
            await db.database.session.commit()


class AdminModelCategory:

    @classmethod
    async def category_list(cls):
        return (await db.database.session.execute(select(cls))).all()

    @classmethod
    async def create_category(cls):
        pass


class AdminModelCustomCategory:

    @classmethod
    async def create_category(cls, text: str):
        category, aliases = cls.parse_text(text)
        create_custom_category = cls(name_category=category, aliases=aliases)
        db.database.session.add(create_custom_category)
        await db.database.session.commit()

    @staticmethod
    def parse_text(text) -> tuple[str, str]:
        arr = text.split(' ')
        return arr[0].lower(), arr[1].lower()


class AdminModelPrice:

    @classmethod
    async def create_price(cls, **kwargs) -> None:
        create_price_object = cls(**kwargs)
        db.database.session.add(create_price_object)
        await db.database.session.commit()
