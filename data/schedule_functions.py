from .functions import DbCore
from loader import bot
from aiogram.utils.exceptions import ChatNotFound


async def send_day_message(week_day: str) -> None:
    info_about_day = DbCore().get_day_from_text_table(week_day)
    GROUPS = DbCore().get_all_groups()

    message = info_about_day[1]
    photo_id = info_about_day[2]

    for group_id in GROUPS:
        if message.strip(" ") != "":
            await bot.send_message(
                group_id[0],
                message
            )
            if photo_id:
                await bot.send_photo(
                    group_id[0],
                    photo_id
                )

            print("%s's text was sent" % week_day.upper())


# async def test_message():
#     GROUPS = DbCore().get_all_groups()
#     for i in GROUPS:
#         try:
#             await bot.send_message(
#                 i[0],
#                 "Тест каждые 5 секунд"
#             )
#         except ChatNotFound:
#             print("Chat %s was not found! Check the GROUPS!" % i[0])


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
