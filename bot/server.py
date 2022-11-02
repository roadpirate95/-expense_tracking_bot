from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import logging

import config
from commands import register_user_commands, commands_for_bot
import db


async def main():
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.TOKEN)
    register_user_commands(dp)
    await db.create_categories()
    await bot.set_my_commands(commands=commands_for_bot())
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stop')
