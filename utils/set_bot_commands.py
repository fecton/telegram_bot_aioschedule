from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "меню"),
        types.BotCommand("start", "старт"),
        types.BotCommand("help", "справка"),
        types.BotCommand("show", "показать установленные ID групп"),
        types.BotCommand("reset", "сбросить ID'и"),
        types.BotCommand("set", "установить ID'и"),
        types.BotCommand("status", "показать сообщения"),
    ])
