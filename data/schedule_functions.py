from .functions import DbCore
from .config import GROUPS
from loader import bot

async def send_day_message(week_day: str) -> None:
    info_about_day = DbCore().get_day_from_text_table(week_day)
    message = info_about_day[1]
    photo_id = info_about_day[2]
    if message.strip(" ") != "":
        for group_id in GROUPS:
            await bot.send_message(
                group_id,
                message
            )
            if photo_id:
                await bot.send_photo(
                    group_id,
                    photo_id
                )
        print("%s's text was sent" % week_day.title())

async def send_everyday():
    await send_day_message("everyday")

async def send_on_monday():
    await send_day_message("monday")

async def send_on_tuesday():
    await send_day_message("tuesday")

async def send_on_wednesday():
    await send_day_message("wednesday")

async def send_on_thursday():
    await send_day_message("thursday")

async def send_on_friday():
    await send_day_message("friday")

async def send_on_saturday():
    await send_day_message("saturday")

async def send_on_sunday():
    await send_day_message("sunday")

