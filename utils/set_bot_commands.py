from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "меню"),
        types.BotCommand("start", "старт"),
        types.BotCommand("help", "справка"),
        types.BotCommand("show", "показать установленные ID групп"),
        types.BotCommand("reset", "сбросить ID'и"),
        types.BotCommand("status", "показать сообщения"),
    ])
