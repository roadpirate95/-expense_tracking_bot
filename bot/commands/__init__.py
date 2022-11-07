__all__ = ['register_user_commands', 'commands_for_bot']


from aiogram import Router, F
from aiogram.filters.command import Command


from bot.commands.handlers import start, help_command, today_command, month_command, year_command, handler_text, \
    all_categories_command, create_command, get_name_category, answer_is_no, answer_is_yes, handler_aliases, expense
from bot.commands.bot_commands import commands_for_bot
from bot.commands.keyboards import inline_markup
from bot import db


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(today_command, Command(commands=['today']))
    router.message.register(month_command, Command(commands=['month']))
    router.message.register(year_command, Command(commands=['year']))
    router.message.register(all_categories_command, Command(commands=['all']))
    router.message.register(create_command, Command(commands=['create']))

    router.message.register(
        get_name_category,
        F.text.regexp(r'^[а-яА-Я][^\t\v\r\n\f-!..]*$'),
        db.BuildCategory.set_name
    )

    router.callback_query.register(
        answer_is_yes,
        db.BuildCategory.question,
        F.data == 'Да'
    )

    router.callback_query.register(
        answer_is_no,
        db.BuildCategory.question,
        F.data == 'Нет'
    )

    router.message.register(
        handler_aliases,
        db.BuildCategory.set_alias
    )

    router.message.register(expense, Command(commands=['expense']))
    router.message.register(
        handler_text,
        F.text.regexp(r'^[а-яА-Я][^\t\v\r\n\f-!..]*\s\d*$'),
        db.BuildExpense.set_expense
    )
