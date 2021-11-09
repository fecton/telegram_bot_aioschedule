from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data import SUPER_USERS

class Is_Admin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in SUPER_USERS
