from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import SUPER_USERS, content
from loader import dp
from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from filters import IsAdminPrivate, IsPrivate


# starting message for user or admin /start
@dp.message_handler(IsPrivate(), CommandStart())
async def start_message(message: types.Message):
    if message.from_user.id in SUPER_USERS:
        await message.answer(content["start_admin"])
    else:
        await message.answer(content["start_user"])


@dp.message_handler(IsAdminPrivate(), CommandHelp())
async def send_help_message(message: types.Message):
    await message.answer(content["help"])
