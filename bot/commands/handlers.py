from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
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


async def all_categories_command(message: Message):
    # res = await db.Category.category_list()
    await message.reply(f'{await db.Category.category_list()}')


async def create_command(message: Message, state: FSMContext):
    await message.reply('Введите категорию и псевдонимы')
    await state.set_state(db.BuildCategory.build_category)


async def handler_create_category(message: Message, state: FSMContext):
    await db.CustomCategory.create_category(message.text)
    await message.reply('Категория добавлена')
    await state.clear()


async def handler_text(message: Message):
    result: bool = await db.Expense.create_communication_between_tables(message.from_user.id, message.html_text)
    if result:
        await message.reply('Расход добавлен')
    await message.reply('Такой категории нет')
