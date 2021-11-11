from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from data.config import SUPER_USERS, content
from loader import dp
from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from filters import Is_Admin_Private, Is_Private
from keyboard.inline import menu_inline_keyboard, status_inline_keyboard, cancel_keyboard
from keyboard.inline.cb_data import week_day, action_data
from data.functions import DbCore, eng_day_to_rus
from states import Mem_Menu


# starting message for user or admin /start
@dp.message_handler(Is_Private(), CommandStart())
async def start_message(message: types.Message):
    if message.from_user.id in SUPER_USERS: await message.answer(content["start_admin"])
    else:                                   await message.answer(content["start_user"])


# send inline menu to user /days
@dp.message_handler(commands="days")
async def help_message(message: types.Message):
    await message.answer("Список дней:", reply_markup=menu_inline_keyboard)
    await Mem_Menu.start_state.set()

# get week data from user's choice and save it
@dp.callback_query_handler(Is_Admin_Private(), week_day.filter(), state=Mem_Menu.start_state)
async def send_action_keyboard(call: CallbackQuery, callback_data: dict, state: FSMContext):
    week_day = eng_day_to_rus(callback_data["week_day"]).upper()
    await state.update_data(week_day=callback_data["week_day"])
    await Mem_Menu.next()

    await call.answer("Отлично! Вы выбрали %s" % week_day)
    await call.message.edit_text("(%s) Выберите действие: " % week_day)
    await call.message.edit_reply_markup(reply_markup=status_inline_keyboard)


# click on button 'change the text' and send cancel_keyboard and start reading text
@dp.callback_query_handler(action_data.filter(action_choice="change"), state=Mem_Menu.set_week_day)
async def send_action_keyboard(call: CallbackQuery, callback_data: dict, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    await state.update_data(week_day=week_day)
    
    # await state.update_data(week_day=week_day, action="change")
    
    await call.message.edit_reply_markup()
    await call.message.edit_text("(%s) Введите ваш текст:" % eng_day_to_rus(week_day).upper())
    await call.message.edit_reply_markup(reply_markup=cancel_keyboard)

    await Mem_Menu.next()

@dp.callback_query_handler(action_data.filter(action_choice="attach_photo"), state=Mem_Menu.set_week_day)
async def attaching_photos(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer("🌄 Отлично, теперь отправьте фото")
    await call.message.edit_text("Для отмены:")
    await call.message.edit_reply_markup(reply_markup=cancel_keyboard)

    await Mem_Menu.next()

@dp.callback_query_handler(action_data.filter(action_choice="status_day"), state=Mem_Menu.set_week_day)
async def send_status_day(call: CallbackQuery, callback_data: dict, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    rus_week_day = eng_day_to_rus(week_day).upper()
    info = DbCore().get_day_from_text_table(week_day)

    if info[1]: day_text = info[1]
    else:       day_text = "❌"

    photo_id = info[2]

    if photo_id in ["❌", "", "None", None]:
        output_message = "День недели: %s\nТекст: %s\nФото: ❌"% (rus_week_day, day_text)
    else:
        output_message = "День недели: %s\nТекст: %s\nФото:"% (rus_week_day, day_text)
        await call.message.answer_photo(photo_id)  
    
    await call.message.edit_reply_markup()
    await call.message.edit_text(output_message)
    
    await state.reset_state(with_data=True)

@dp.message_handler(content_types="photo", state=Mem_Menu.set_action)
async def get_photos_and_set_to_message(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    day = (await state.get_data("week_day"))["week_day"]
    DbCore().insert_photo(photo_id, day)
    await message.answer("Хорошо, фото будут прикреплено ко дню %s" % eng_day_to_rus((await state.get_data("week_day"))["week_day"]) )
    await state.reset_state(with_data=True)


# if user clicks on cancel then that returns to action keyboard
@dp.callback_query_handler(action_data.filter(action_choice="cancel"), state=Mem_Menu.set_action)
async def cancel_action(call: CallbackQuery, callback_data: dict, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    await call.message.edit_text("(%s) Выберите действие: " % eng_day_to_rus(week_day).upper())
    await call.message.edit_reply_markup(reply_markup=status_inline_keyboard)
    await state.reset_state(with_data=False)
    await Mem_Menu.set_week_day.set()

# else user write his text and bot writes changes to the database
@dp.message_handler(content_types="text", state=Mem_Menu.set_action)
async def get_text_to_change(message: types.Message, state: FSMContext):
    week_day = (await state.get_data("week_day"))["week_day"]
    DbCore().update_table_data(week_day, message.text)
    await message.answer("👍")
    await state.update_data(week_day=week_day, text=message.text)
    await Mem_Menu.next()
    await state.reset_state(with_data=True)


@dp.callback_query_handler(action_data.filter(action_choice="go_back"), state=Mem_Menu.set_week_day)
async def send_action_keyboard(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_text("Список дней:")
    await call.message.edit_reply_markup(reply_markup=menu_inline_keyboard)
    await state.reset_state(with_data=True)
    await Mem_Menu.start_state.set()


@dp.message_handler(Is_Admin_Private(), commands="status")
async def check_messages_for_days(message: types.Message):
    all_messages = DbCore().get_all_from_text_table()

    output_message = ""
    for day in ["everyday", "monday", "tuesday", "wednesday", "thursday", "friday"]:
        if not all_messages[day]: x = "❌"
        else:                     x = all_messages[day]
        output_message += "🔰"+eng_day_to_rus(day)+": " + x + "\n"

    await message.answer(output_message)



