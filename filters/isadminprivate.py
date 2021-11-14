from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data import SUPER_USERS


class IsAdminPrivate(BoundFilter):
    async def check(self, mobj: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(mobj, types.CallbackQuery):
            return (mobj.message.chat.id in SUPER_USERS) and (mobj.message.chat.type == "private")
        return (mobj.from_user.id in SUPER_USERS) and (mobj.chat.type == "private")


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
