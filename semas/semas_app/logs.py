import sqlite3
from .settings import *
import time

class Log:

    @staticmethod
    def write_log(message, function):
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"INSERT INTO log(message, function, u_time) VALUES(?,?,?)", (message, function, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}. Function Logs.write_log()")
        finally:
            con.close()