#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import middlewares

import aioschedule, asyncio
from aiogram import Dispatcher, executor
from data.schedule_functions import *
from handlers import dp

async def on_startup(dp: Dispatcher):
	from utils.notify_admins import on_startup_notify
	from utils.set_bot_commands import set_default_commands
	
	middlewares.setup(dp)
	await set_default_commands(dp)
	await on_startup_notify(dp)
	asyncio.create_task(scheduler())
	

async def scheduler():
	aioschedule.every().day.at("15:18").do( send_everyday )
	aioschedule.every().monday.at("12:00").do( send_on_monday )
	aioschedule.every().tuesday.at("12:00").do( send_on_tuesday )
	aioschedule.every().wednesday.at("12:00").do( send_on_wednesday )
	aioschedule.every().thursday.at("12:00").do( send_on_thursday )
	aioschedule.every().friday.at("12:00").do( send_on_friday )
	aioschedule.every().saturday.at("12:00").do( send_on_saturday )
	aioschedule.every().friday.at("12:00").do( send_on_sunday )

	while 1:
		await aioschedule.run_pending()
		await asyncio.sleep(1)

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


