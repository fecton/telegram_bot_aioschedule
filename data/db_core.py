import sqlite3
from typing import Union
from data import DB_NAME

class DbCore:
    """
    Interface for working with database
    """
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

        query = """
            INSERT INTO `text` (day, text) VALUES (?,?)
        """

        for func in ["everyday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            self.execute(query, parameters=(func, ""), commit=True)

        query = """
            CREATE TABLE `groups` (
                id         VARCHAR(128)  PRIMARY KEY NOT NULL,
                group_name VARCHAR(128)  NOT NULL
            )
        """
        self.execute(query, commit=True)


    def update_table_data(self, day: str, text: str) -> None:
        """
        Update day's text
        """
        query = """
            UPDATE `text` SET text="%s" WHERE day="%s"
        """ % (text, day)
        self.execute(query, commit=True)


    def insert_groups(self, group_name, group_id) -> None:
        query = """
            INSERT INTO `groups` (id, group_name) VALUES (?, ?)
        """
        self.execute(query, (group_name, group_id), commit=True)


    def get_all_groups(self) -> list:
        query = """
            SELECT * FROM `groups`
        """
        return self.execute(query, fetchall=True)

    def clear_all_groups(self) -> None:
        query = """
            DELETE FROM `groups`
        """
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

    def get_day_from_text_table(self, day: str) -> list:
        query = """
            SELECT * FROM `text` WHERE day="%s"
        """ % day
        info = self.execute(query, fetchone=True)
        return info
