from sqlalchemy import select

from bot import db


CATEGORIES = (("продукты", "еда"),
              ("кафе", "ресторан,рест,мак,макдональдс,макдак,kfc"),
              ("общ. транспорт", "метро,автобус,metro"),
              ("такси", "яндекс такси,yandex taxi"),
              ("телефон", "труба,связь"),
              ("интернет", "инет,inet"),
              ("заправка", "авто,бензин,малышка"),
              ("прочее", ""))


def _initial_category() -> list[db.Category]:
    """Создает список категорий"""
    arr_category = [db.Category(name_category=category[0], aliases=category[1]) for category in CATEGORIES]
    return arr_category


async def create_categories() -> None:
    """Добавляет основные категории в базу,если их нет"""
    users = (await db.database.session.execute(select(db.Category))).scalars().all()
    if not users:
        db.database.session.add_all(_initial_category())
        await db.database.session.commit()


async def check_for_availability(user_id: int, word: str) -> bool:
    """Проверяет на наличие word в бд"""
    all_user_categories = await db.Category.category_list(user_id)
    for category in all_user_categories:
        if word != category[0]:
            if category[1]:
                list_aliases = category[1].split(',')
                if word.strip() in list_aliases:
                    return False
            else:
                continue
        else:
            return False

    return True
