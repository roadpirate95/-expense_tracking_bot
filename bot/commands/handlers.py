from aiogram.filters import CommandObject
from aiogram.types import Message

from bot import db
from bot.commands.bot_commands import bot_commands


async def start(message: Message) -> Message:
    await db.User.create_user(user_id=message.from_user.id, username=message.from_user.username)
    return await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def help_command(message: Message, command: CommandObject) -> Message:
    if command.args:
        for comm in bot_commands:
            if comm[0] == command.args:
                return await message.answer(
                    f'{comm[0]} - {comm[1]}\n\n{comm[2]}'
                )
            else:
                return await message.answer('Команда не найдена')

    return await message.reply('Помощь в работе с ботом')


async def today_command(message: Message):
    expense = await db.Expense.get_expense_for_today(message.from_user.id)
    await message.reply(f'Расходы за день {expense}')


async def month_command(message: Message):
    expense = await db.Expense.get_expense_for_month(message.from_user.id)
    await message.reply(f'Расходы за месяц {expense}')


async def year_command(message: Message):
    expense = await db.Expense.get_expense_for_year(message.from_user.id)
    await message.reply(f'Расходы за год {expense}')


async def handler_text(message: Message) -> Message:
    await db.Expense.create_communication_between_tables(message.from_user.id, message.html_text)
    return await message.reply('Расход добавлен')
