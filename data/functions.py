from aiogram import types
from data import DB_NAME
import sqlite3
from typing import Union

def eng_day_to_rus(week_day: str) -> str:
    week = {
        "everyday": "ежендневное",
        "monday": "понедельник",
        "tuesday": "вторник",
        "wednesday": "среда",
        "thursday": "четверг",
        "friday": "пятница",
        "saturday": "суббота",
        "sunday": "воскресенье",
    }
    return week[week_day]


def send_to_db(message, func):
    text = user_input(message.text, "/%s"%func)
    if len(text) != "":
        db = DbCore()
        db.insert_into_text_table(func, text)
        print("[+] %s message was updated!" % func.title())


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

class DbCore:
    def __init__(self) -> None:
        self._path_to_db = DB_NAME

    @property
    def connection(self) -> sqlite3:
        return sqlite3.connect(self._path_to_db)

    def execute(self, sql_query: str = "", parameters: Union[list, tuple] = (),
                fetchone: bool = False, fetchall: bool = False, commit: bool = False) -> list:

        if isinstance(parameters, list):
            parameters = tuple(parameters)

        connection = self.connection

        query_output = connection.cursor().execute(sql_query, parameters)


        if fetchone:
            return query_output.fetchone()
        elif fetchall:
            return query_output.fetchall()

        if commit:
            connection.commit()

        connection.close()

    def create_text_table(self) -> None:
        query = """
            CREATE TABLE `text` (
                day VARCHAR(128) PRIMARY KEY NOT NULL,
                text     TEXT DEFAULT "",
                photo    TEXT DEFAULT ""
        )"""
        self.execute(query, commit=True)

        query2 = """
            INSERT INTO `text` (day, text) VALUES (?,?)
        """

        for func in ["everyday", "monday", "tuesday", "wednesday", "thursday", "friday"]:
            self.execute(query2, parameters=(func, ""), commit=True)


    def update_table_data(self, day: str, text: str) -> None:
        """
        Update day's text
        """
        query = """
            UPDATE `text` SET text="%s" WHERE day="%s"
        """ % (text, day)
        self.execute(query, commit=True)


    def insert_photo(self, photo_id: str, day: str) -> None:
        """
        Update photo id in day
        """

        query = """
            UPDATE `text` SET photo="%s" WHERE day="%s"
        """ % (photo_id, day)
        
        self.execute(query, commit=True)


    def clear_photo(self, day) -> None:
        """
        Clear photo id in database from the day
        """
        query = """
            UPDATE `text` SET photo="" WHERE day="%s"
        """ % day
        self.execute(query, commit=True)

    def get_all_from_text_table(self) -> dict:
        query = """
            SELECT * FROM `text`
        """
        array = self.execute(query, fetchall=True)
        dictionary = {}
        for i in range(len(array)): 
            dictionary[array[i][0]] = array[i][1]
        return dictionary

    def get_day_from_text_table(self, day: str) -> dict:
        query = """
            SELECT * FROM `text` WHERE day="%s"
        """ % day
        info = self.execute(query, fetchone=True)
        return info


            