__all__ = ['register_user_commands', 'commands_for_bot']

from aiogram import Router
from aiogram.filters.command import Command
from bot.commands.handlers import start, help_command, today_command, month_command, year_command, handler_text
from bot.commands.bot_commands import commands_for_bot


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(today_command, Command(commands=['today']))
    router.message.register(month_command, Command(commands=['month']))
    router.message.register(year_command, Command(commands=['year']))
    router.message.register(handler_text)


