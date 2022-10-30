__all__ = ['register_user_commands', 'commands_for_bot']

import re

from aiogram import Router, F
from aiogram.filters.command import Command
from bot.commands.handlers import start, help_command, today_command, month_command, year_command, handler_text, \
    all_categories_command, create_command, handler_create_category
from bot.commands.bot_commands import commands_for_bot
from bot import db


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(today_command, Command(commands=['today']))
    router.message.register(month_command, Command(commands=['month']))
    router.message.register(year_command, Command(commands=['year']))
    router.message.register(all_categories_command, Command(commands=['all']))
    router.message.register(create_command, Command(commands=['create']))
    router.message.register(handler_text, F.text.regexp(r'^[а-яА-Я][^\t\v\r\n\f-!..]*\s\d*$'))
    router.message.register(
        handler_create_category,
        db.BuildCategory.build_category,
        F.text.regexp(r'^[а-яА-Я][^\t\v\r\n\f]*\s[^\t\v\r\n\f]*$')
    )





