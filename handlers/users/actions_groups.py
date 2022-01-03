from loader import dp
from filters import IsAdminPrivate
from data.functions import user_input, DbCore, eng_day_to_rus
from aiogram import types
from sqlite3 import IntegrityError


@dp.message_handler(IsAdminPrivate(), commands="reset")
async def reset_groups(message: types.Message):
    DbCore().clear_all_groups()
    await message.answer("Все группы очищены!")


@dp.message_handler(IsAdminPrivate(), commands="show")
async def show_groups(message: types.Message):
    all_groups = DbCore().get_all_groups()

    if all_groups:
        all_groups = "\n".join(list(map(lambda x: "%s : %s" % x, all_groups))).title()
        await message.answer("Список групп:\n" + all_groups)
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
        
        output_message += "🔰 %s:%s%s\n" % (
            eng_day_to_rus(day, short=True),
            " "*3,
            x
        )
    await message.answer(output_message)
