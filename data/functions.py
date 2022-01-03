from aiogram import types
from .db_core import DbCore

def eng_day_to_rus(week_day: str, short=False) -> str:
    "Translates week days to russian"
    if not short:
        week = {
            "everyday": "ежедневное",
            "monday": "понедельник",
            "tuesday": "вторник",
            "wednesday": "среда",
            "thursday": "четверг",
            "friday": "пятница",
            "saturday": "суббота",
            "sunday": "воскресенье",
        }
    else:
        week = {
            "everyday": "Еж",
            "monday": "Пн",
            "tuesday": "Вт",
            "wednesday": "Ср",
            "thursday": "Чт",
            "friday": "Пт",
            "saturday": "Сб",
            "sunday": "Вс",
        }  
    return week[week_day]

def user_input(message: types.Message, command: str) -> str:
    """
    This function returns users output after command
    Example: "/ban 23432422"
        Returns: "23432422"
    :param message: types.Message object gotten from handler
    :param command: This is a commands which will be deleted with a space from message.text
    """
    text = message.text.replace(command + " ", "").strip()
    if command in text or command == "":
        return ""
    return text



