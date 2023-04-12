import sqlite3
from .settings import *
import time
from .enums import *

class Log:
    @staticmethod
    def write_log(message, function, type = LogType.DB_ERROR.value):
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"INSERT INTO log(text, function, type, u_time) VALUES(?,?,?,?)", (message, function, type, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}. Function Logs.write_log()")
        finally:
            con.close()