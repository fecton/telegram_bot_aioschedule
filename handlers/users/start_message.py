from aiogram.types.callback_query import CallbackQuery
from data.config import SUPER_USERS, content
from loader import dp
from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from filters import Is_Admin, Is_Private
from keyboard.inline import menu_inline_keyboard, status_inline_keyboard
from keyboard.inline.cb_data import week_day, action_data
from data.functions import eng_day_to_rus



@dp.message_handler(Is_Private(), CommandStart())
async def start_message(message: types.Message):
    if message.from_user.id in SUPER_USERS: await message.answer(content["start_admin"])
    else:                                   await message.answer(content["start_user"])


@dp.message_handler(Is_Private(), Is_Admin(), commands="days")
async def help_message(message: types.Message):
    await message.answer("Список дней:", reply_markup=menu_inline_keyboard)


@dp.callback_query_handler(week_day.filter())
async def send_action_keyboard(call: CallbackQuery, callback_data: dict):
    week_day = eng_day_to_rus(callback_data["week_day"]).upper()
    await call.answer("Отлично! Вы выбрали %s" % week_day)
    await call.message.edit_text("(%s) Выберите действие: " % week_day)
    await call.message.edit_reply_markup(reply_markup=status_inline_keyboard)


@dp.callback_query_handler(action_data.filter(action_choice="change"))
async def send_action_keyboard(call: CallbackQuery, callback_data: dict):
    week_day = callback_data.get("week_day")
    await call.message.answer(week_day)
    await call.message.edit_text("Список дней:")
    await call.message.edit_reply_markup(reply_markup=menu_inline_keyboard)


@dp.callback_query_handler(action_data.filter(action_choice="go_back"))
async def send_action_keyboard(call: CallbackQuery, callback_data: dict):
    await call.message.edit_text("Список дней:")
    await call.message.edit_reply_markup(reply_markup=menu_inline_keyboard)


@dp.message_handler(Is_Private(), Is_Admin(), commands="status")
async def check_messages_for_days(message: types.Message):
    from data.functions import DbCore
    db = DbCore()
    all_messages = db.get_all_from_text_table()

    eng_to_rus = {
        "everyday": "Ежендневное",
        "monday": "Понедельник",
        "tuesday": "Вторник",
        "wednesday": "Среда",
        "thursday": "Четверг",
        "friday": "Пятница",
        "saturday": "Суббота",
        "sunday": "Воскресенье",
    }

    output_message = "Все сообщения\n\n"
    for day in ["everyday", "monday", "tuesday", "wednesday", "thursday", "friday"]:
        if not all_messages[day]: x = "❌"
        else:                     x = all_messages[day]
        output_message += "🔰"+eng_to_rus[day]+": " + x + "\n"

    await message.answer(output_message)



