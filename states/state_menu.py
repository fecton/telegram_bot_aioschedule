from aiogram.dispatcher.filters.state import State, StatesGroup

class Mem_Menu(StatesGroup):
    got_week_day = State()
    got_action = State()



