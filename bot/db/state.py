from aiogram.fsm.state import StatesGroup, State


class BuildCategory(StatesGroup):
    """Состояния для создания категории расхода"""
    set_name = State()
    question = State()
    set_alias = State()


class BuildExpense(StatesGroup):
    """Состояние для внесения расхода"""
    set_expense = State()
