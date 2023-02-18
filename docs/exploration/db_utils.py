import re
import sqlite3
import time
from typing import Optional

from pandas import DataFrame

from config import DB_PATH


class DbUtils:
    def __init__(self):
        with sqlite3.connect(DB_PATH) as connection:

            cursor = connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS news (Title text, URL text, Author text, Snippet text, Related int);"
            )
            connection.commit()

    def get_data(self, limit: int=0, balanced: bool=False, related: int=0):
        if balanced:
            return self.read_from_db(f"SELECT * FROM (Select * from news where Related=0 LIMIT 524) UNION Select * from news where Related=1;")
        if limit>0:
            return self.read_from_db(f"SELECT * FROM news LIMIT {limit};")
        return self.read_from_db("SELECT * FROM news;")

    def get_data_cond(self, related: int):
        return self.read_from_db(f"SELECT * FROM train_cleaned_v3 WHERE Related = {related};")


    def write_to_db(self, insert_string: str):
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()

            cursor.execute(insert_string)

            connection.commit()
            cursor.close()
            connection.close()

            del cursor
            del connection
        except sqlite3.OperationalError:
            time.sleep(5)  # TODO: retry

    def read_from_db(self, read_string: str) -> list:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(read_string)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        del cursor
        del connection

        return result
