from sqlalchemy import select

from bot import db

CATEGORIES = (("продукты", "еда"),
              ("кафе", "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
              ("общ. транспорт", "метро, автобус, metro"),
              ("такси", "яндекс такси, yandex taxi"),
              ("телефон", "теле2, связь"),
              ("интернет", "инет, inet"),
              ("заправка", "авто, бензин, малышка"),
              ("прочее", ""))


def _initial_category() -> list[db.Category]:
    arr_category = [db.Category(name_category=category[0], aliases=category[1]) for category in CATEGORIES]
    return arr_category


async def create_categories() -> None:
    users = (await db.database.session.execute(select(db.Category))).scalars().all()
    if not users:
        db.database.session.add_all(_initial_category())
        await db.database.session.commit()
