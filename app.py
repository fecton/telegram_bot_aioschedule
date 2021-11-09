#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import middlewares

from aiogram import Dispatcher, executor
from handlers import dp

async def on_startup(dp: Dispatcher):
	from utils.notify_admins import on_startup_notify
	from utils.set_bot_commands import set_default_commands
	
	middlewares.setup(dp)
	await set_default_commands(dp)
	await on_startup_notify(dp)
	
if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


