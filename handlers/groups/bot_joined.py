from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot
from aiogram import types
from data.config import SUPER_USERS
from filters import IsThisBot
from keyboard.inline import add_group_id
from keyboard.inline.cb_data import add_group_id_data
from data.functions import DbCore
import re
from sqlite3 import IntegrityError


@dp.message_handler(IsThisBot(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def send_chat_id_to_admin(message: types.Message):
    for user in SUPER_USERS:
        await bot.send_message(
            chat_id=user,
            text="🔅 Название группы: <b>%s</b>\n🔸 ID группы: <code>%s</code>" % (message.chat.title, message.chat.id),
            parse_mode=types.ParseMode.HTML,
            reply_markup=add_group_id
        )


@dp.callback_query_handler(add_group_id_data.filter(group_id="add_group_id"))
async def add_or_skip_group_id(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        group_name = call.message.text[re.search(r"🔅 Название группы: ", call.message.text).end():call.message.text.find("\n")]
        group_id = -int(re.search(r"\d+", call.message.text).group())
        DbCore().insert_groups(group_name, group_id)
        await call.answer("✅ Группа успешно добавлена!")
    except IntegrityError:
        await call.answer("🚫 Произошла ошибка")

    await call.message.edit_reply_markup()
