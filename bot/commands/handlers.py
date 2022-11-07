from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.commands.keyboards import inline_markup
from bot import db
from bot.commands.bot_commands import bot_commands


async def start(message: Message) -> Message:
    """Обработчик команды /start"""
    await db.User.create_user(user_id=message.from_user.id, username=message.from_user.username)
    return await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def help_command(message: Message, command: CommandObject) -> Message:
    """Обработчки команды /help"""
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
    """Расходы за день"""
    expense = await db.Expense.get_expense_for_today(message.from_user.id)
    await message.reply(f'Расходы за день {expense}') if expense else await message.reply('Расходы за день: 0')


async def month_command(message: Message):
    """Расходы за месяц"""
    expense = await db.Expense.get_expense_for_month(message.from_user.id)
    await message.reply(f'Расходы за месяц {expense}') if expense else await message.reply('Расходы за месяц: 0')


async def year_command(message: Message):
    """Расходы за год"""
    expense = await db.Expense.get_expense_for_year(message.from_user.id)
    await message.reply(f'Расходы за год {expense}') if expense else await message.reply('Расходы за год: 0')


async def all_categories_command(message: Message):
    """Списко категорий пользователя"""
    all_user_categories = await db.Category.category_list(message.from_user.id)
    message_for_user = ''
    for category_num in range(len(all_user_categories)):
        if all_user_categories[category_num] != all_user_categories[-1]:
            if all_user_categories[category_num][1]:
                message_for_user += f'{category_num+1}) Категория: ' \
                                    f'{all_user_categories[category_num][0]},{all_user_categories[category_num][1]}\n'
            else:
                message_for_user += f'{category_num + 1}) Категория: ' \
                                    f'{all_user_categories[category_num][0]}\n'
        else:
            if all_user_categories[category_num][1]:
                message_for_user += f'{category_num + 1}) Категория: ' \
                                    f'{all_user_categories[category_num][0]},{all_user_categories[category_num][1]}'
            else:
                message_for_user += f'{category_num + 1}) Категория: {all_user_categories[category_num][0]}'
    await message.answer(f'{message_for_user}')


async def create_command(message: Message, state: FSMContext):
    """
    Обрабатывает команду /create для создания пользовательской категории,
    устанавливает состояние в db.BuildCategory.set_name
    """

    await state.set_state(db.BuildCategory.set_name)
    await message.reply('Введите категорию')


async def get_name_category(message: Message, state: FSMContext):
    """
    Выполняет проверку по созданным категориям,
    сохраняет имя пользовательской категории, устанавливает состояние в db.BuildCategory.question
    """

    name = message.text
    result: bool = await db.check_for_availability(message.from_user.id, name)
    if result:
        await state.set_data({'name': name, 'user_id': message.from_user.id})
        await message.answer('Добивать альтернативное название?', reply_markup=inline_markup.as_markup())
        await state.set_state(db.BuildCategory.question)
    else:
        await message.reply('Такая категория или псевдоним уже существует!\nПовторите попытку')


async def answer_is_no(call: CallbackQuery, state: FSMContext):
    """Если ответ от пользователя 'нет', сохраняет категорию и очищает состояние"""
    data: dict = await state.get_data()
    await db.Category.create_category(data['user_id'], data['name'].lower())
    await state.clear()
    await call.message.reply('Категория добавлена')


async def answer_is_yes(call: CallbackQuery, state: FSMContext):
    """Если ответ от пользователя 'да', переводит состояние в db.BuildCategory.set_alias"""
    await call.message.reply('Введите псевдонимы')
    await state.set_state(db.BuildCategory.set_alias)


async def handler_aliases(message: Message, state: FSMContext):
    """Выполняет проверку по уже созданным категориям, если все ок, создает новую категорию и очищает состояние"""
    alias = message.text
    result: bool = await db.check_for_availability(message.from_user.id, alias)
    if result:
        category = await state.get_data()
        await db.Category.create_category(
            message.from_user.id, category['name'].lower(),
            alias=message.text.lower().strip()
        )
        await state.clear()
        await message.reply('Категория добавлена')
    else:
        await message.reply('Такая категория или псевдоним уже существует!\nПовторите попытку')


async def expense(message: Message, state: FSMContext):
    await message.reply('Введите расход. Ввод должен быть: "Категория" "цена"')
    await state.set_state(db.BuildExpense.set_expense)


async def handler_text(message: Message, state: FSMContext):
    """Обрабатывает текст внесения расхода и добавляет расход  в базу"""
    result: bool = await db.Expense.adding_an_expense(message.from_user.id, message.html_text)
    await message.reply('Расход добавлен') if result else await message.reply('Такой категории нет')
    await state.clear()
