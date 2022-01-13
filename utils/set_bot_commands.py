from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "меню"),
        types.BotCommand("start", "старт"),
        types.BotCommand("help", "справка"),
        types.BotCommand("show", "показать группы"),
        types.BotCommand("reset", "сбросить группы"),
        types.BotCommand("status", "показать сообщения"),
    ])
