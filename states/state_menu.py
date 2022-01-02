from aiogram.dispatcher.filters.state import State, StatesGroup


class MemMenu(StatesGroup):
    start_state = State()
    set_week_day = State()
    set_action = State()
    set_photo = State()
    set_text = State()

