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

    pass


class AdminModelPrice:

    @classmethod
    async def create_price(cls, **kwargs):
        create_price_object = cls(**kwargs)
        db.database.session.add(create_price_object)
        await db.database.session.commit()




