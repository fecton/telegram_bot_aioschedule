from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import TOKEN, DB_NAME
from os import path

from data.functions import DbCore


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

if path.exists(DB_NAME):
    print("[+] The database had already existed!")
else:
    db = DbCore()
    db.create_text_table()
    print("[+] Created database and the text table was created!")
