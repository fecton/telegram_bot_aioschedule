from aiogram.dispatcher.filters import BoundFilter
from loader import dp
from aiogram import types


class IsThisBot(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        bot_id = (await dp.bot.get_me())["id"]
        users_id = message.new_chat_members

        for user_id in users_id:
            if user_id["id"] == bot_id:
                return True
        
        return False
