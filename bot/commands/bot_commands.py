from aiogram.types import BotCommand

bot_commands = (
    ('start', 'Стартуем!!', 'Начало работы с ботом'),
    ('help', 'Помощь', 'Нажимай если нужна помощь'),
    ('today', 'Расходы за сегодня'),
    ('month', 'Расходы за месяц'),
    ('year', 'Расходы за год'),
    ('all', 'Все категории'),
    ('create', 'Создать категорию расходов'),
    ('expense', 'Добавить расходы'),
)


def commands_for_bot() -> list[BotCommand]:
    commands_bot = []
    for comm in bot_commands:
        commands_bot.append(BotCommand(command=comm[0], description=comm[1]))
    return commands_bot
