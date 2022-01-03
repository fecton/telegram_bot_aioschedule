from filters import IsAdminPrivate
from aiogram import types
from keyboard.inline import menu_inline_keyboard, cancel_keyboard, status_inline_keyboard
from aiogram.dispatcher import FSMContext
from states import MemMenu
from keyboard.inline.cb_data import *
from loader import dp
from data.functions import eng_day_to_rus, DbCore

# send inline menu to user /days
@dp.message_handler(IsAdminPrivate(), commands="menu")
async def help_message(message: types.Message):
    await message.answer("Список дней:", reply_markup=menu_inline_keyboard)
    await MemMenu.start_state.set()


# get week data from user's choice and save it
@dp.callback_query_handler(IsAdminPrivate(), week_day.filter(), state=MemMenu.start_state)
async def send_action_keyboard(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    week_day = eng_day_to_rus(callback_data["week_day"]).upper()
    await state.update_data(week_day=callback_data["week_day"])
    await MemMenu.next()

    await call.answer("Отлично! Вы выбрали %s" % week_day)
    await call.message.edit_text("(%s) Выберите действие: " % week_day)
    await call.message.edit_reply_markup(reply_markup=status_inline_keyboard)


# click on button 'change the text' and send cancel_keyboard and start reading text
@dp.callback_query_handler(IsAdminPrivate(), action_data.filter(action_choice="change"), state=MemMenu.set_week_day)
async def send_action_keyboard(call: types.CallbackQuery, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    await state.update_data(week_day=week_day)

    # await state.update_data(week_day=week_day, action="change")

    await call.message.edit_reply_markup()
    await call.message.edit_text("(%s) Введите ваш текст:" % eng_day_to_rus(week_day).upper())
    await call.message.edit_reply_markup(reply_markup=cancel_keyboard)

    await MemMenu.next()


@dp.callback_query_handler(IsAdminPrivate(), action_data.filter(action_choice="attach_photo"),
                           state=MemMenu.set_week_day)
async def attaching_photos(call: types.CallbackQuery, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    await call.answer("🌄 Отлично, теперь отправьте фото")
    await call.message.edit_text("(%s) Для отмены:" % eng_day_to_rus(week_day).upper())
    await call.message.edit_reply_markup(reply_markup=cancel_keyboard)

    await MemMenu.set_photo.set()


@dp.callback_query_handler(IsAdminPrivate(), action_data.filter(action_choice="status_day"),
                           state=MemMenu.set_week_day)
async def send_status_day(call: types.CallbackQuery, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    rus_week_day = eng_day_to_rus(week_day).upper()
    info = DbCore().get_day_from_text_table(week_day)

    if info[1]:
        day_text = info[1]
    else:
        day_text = "❌"

    photo_id = info[2]

    if photo_id in ["❌", "", "None", None]:
        output_message = "День недели: %s\nТекст: %s\nФото: ❌" % (rus_week_day, day_text)
    else:
        output_message = "День недели: %s\nТекст: %s\nФото:" % (rus_week_day, day_text)
        await call.message.answer_photo(photo_id)

    await call.message.edit_reply_markup()
    await call.message.edit_text(output_message)

    await state.reset_state(with_data=True)


@dp.message_handler(IsAdminPrivate(), content_types="photo", state=MemMenu.set_photo)
async def get_photos_and_set_to_message(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    day = (await state.get_data("week_day"))["week_day"]
    DbCore().insert_photo(photo_id, day)
    await message.answer("👍")
    await state.reset_state(with_data=True)


# if user clicks on cancel then that returns to action keyboard
@dp.callback_query_handler(IsAdminPrivate(), action_data.filter(action_choice="cancel"),
                           state=[MemMenu.set_action, MemMenu.set_photo])
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    await call.message.edit_text("(%s) Выберите действие: " % eng_day_to_rus(week_day).upper())
    await call.message.edit_reply_markup(reply_markup=status_inline_keyboard)
    await state.reset_state(with_data=False)
    await MemMenu.set_week_day.set()


# else user write his text and bot writes changes to the database
@dp.message_handler(IsAdminPrivate(), content_types="text", state=MemMenu.set_action)
async def get_text_to_change(message: types.Message, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    DbCore().update_table_data(week_day, message.text)
    await message.answer("👍")
    await state.update_data(week_day=week_day, text=message.text)
    await MemMenu.next()
    await state.reset_state(with_data=True)

# returns to day menu
@dp.callback_query_handler(IsAdminPrivate(), action_data.filter(action_choice="go_back"), state=MemMenu.set_week_day)
async def send_action_keyboard(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Список дней:")
    await call.message.edit_reply_markup(reply_markup=menu_inline_keyboard)
    await state.reset_state(with_data=True)
    await MemMenu.start_state.set()
