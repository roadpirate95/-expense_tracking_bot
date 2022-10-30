import datetime

from sqlalchemy import select, or_, func
from sqlalchemy.sql import Select

from bot import db


class Expense:

    @classmethod
    async def get_expense_for_today(cls, user_id: int):
        date = datetime.datetime.today().date()
        sum_for_today = await cls._select(user_id, date)
        return sum_for_today

    @classmethod
    async def get_expense_for_month(cls, user_id: int):
        today = datetime.datetime.today()
        date = datetime.datetime.today().date() - datetime.timedelta(days=today.day)
        sum_for_month = await cls._select(user_id, date, today)
        return sum_for_month

    @classmethod
    async def get_expense_for_year(cls, user_id: int):
        today = datetime.datetime.today()
        date = datetime.datetime(today.year, 1, 1)
        sum_for_month = await cls._select(user_id, date, today)
        return sum_for_month

    @staticmethod
    async def create_communication_between_tables(user_id: int, text: str):
        category, price = db.CustomCategory.parse_text(text)
        user_obj: db.User = await db.database.session.get(db.User, user_id)

        query_category: Select = (
            select(db.Category).
            where(or_(db.Category.name_category == category, db.Category.aliases.like(f'%{category}%')))
        )
        category_obj: db.Category = (await db.database.session.execute(query_category)).scalars().first()

        if category_obj:
            await db.Price.create_price(amount=price, user_id=user_obj.user_id, category_id=category_obj.id)
            return True

        query_category_custom: Select = (
            select(db.CustomCategory).
            where(or_(db.CustomCategory.name_category == category, db.CustomCategory.aliases.like(f'%{category}%')))
        )
        custom_category_obj: db.CustomCategory = (await db.database.session.execute(query_category_custom)).scalars().first()
        print(custom_category_obj.id)
        await db.Price.create_price(amount=int(price), user_id=user_obj.user_id, custom_category_id=custom_category_obj.id)

        if custom_category_obj:
            return True

        return False

    # @staticmethod
    # def _parse_text(text: str) -> tuple[str, int]:
    #     list_word = text.split(' ')
    #     if len(list_word) == 2:
    #         if isinstance(list_word[0], str) and isinstance(int(list_word[1]), int):
    #             return list_word[0].lower(), int(list_word[1])

    @staticmethod
    async def _select(user_id, date, today=None) -> Select:
        if today:
            query: Select = (select(func.sum(db.Price.amount))).\
                     where(db.User.user_id == user_id, db.Price.date.between(date, today))
            sum_price = (await db.database.session.execute(query)).first()[0]
        else:
            query: Select = (select(func.sum(db.Price.amount))).where(db.User.user_id == user_id, db.Price.date == date)
            sum_price = (await db.database.session.execute(query)).first()[0]

        return sum_price
