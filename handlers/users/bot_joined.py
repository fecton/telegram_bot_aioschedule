from loader import dp, bot
from aiogram import types
from data.config import SUPER_USERS
from filters import IsThisBot


@dp.message_handler(IsThisBot(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def send_chat_id_to_admin(message: types.Message):
    await bot.send_message(
        chat_id=SUPER_USERS[0],
        text="GROUP NAME: <b>%s</b>\nGROUP ID: <code>%s</code>" % (message.chat.title, message.chat.id),
        parse_mode=types.ParseMode.HTML
    )
