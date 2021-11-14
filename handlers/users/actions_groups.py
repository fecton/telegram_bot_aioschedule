from loader import dp
from filters import IsAdminPrivate
from data.functions import user_input, DbCore, eng_day_to_rus
from aiogram import types
from sqlite3 import IntegrityError


@dp.message_handler(IsAdminPrivate(), commands="set")
async def set_groups(message: types.Message):
    groups = user_input(message, "/set").split(" ")
    if groups != "":
        groups = [i for i in groups if not i.strip(" ").isalpha() and len(i) > 5]
        try:
            DbCore().insert_groups(groups)
        except IntegrityError:
            await message.answer("Одна из групп уже записана!")
        if groups:
            await message.answer("Успешно добавлено!")


@dp.message_handler(IsAdminPrivate(), commands="reset")
async def reset_groups(message: types.Message):
    DbCore().clear_all_groups()
    await message.answer("Все группы очищены!")


@dp.message_handler(IsAdminPrivate(), commands="show")
async def show_groups(message: types.Message):
    all_groups = "\n".join(list(map(lambda x: x[0], DbCore().get_all_groups())))
    if all_groups:
        await message.answer(all_groups)
    else:
        await message.answer("Ещё нету групп!")


@dp.message_handler(IsAdminPrivate(), commands="status")
async def check_messages_for_days(message: types.Message):
    all_messages = DbCore().get_all_from_text_table()

    output_message = ""
    for day in ["everyday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        if not all_messages[day]:
            x = "❌"
        else:
            x = all_messages[day]
        output_message += "🔰"+eng_day_to_rus(day)+": " + x + "\n"

    await message.answer(output_message)
