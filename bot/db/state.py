from aiogram.fsm.state import StatesGroup, State


class BuildCategory(StatesGroup):
    set_name = State()
    question = State()
    set_alias = State()
