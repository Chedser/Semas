import sqlite3
from settings import *
import time

class Recaptcha:
    @staticmethod
    def add(csrftoken):
        if not csrftoken: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT * FROM recaptcha "
                                 f"WHERE csrftoken=?", (csrftoken,)).fetchall()

            if not len(result):
                cur.execute(f"INSERT INTO recaptcha(csrftoken,u_time) VALUES(?,?)",
                            (csrftoken, int(time.time())))

            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    @staticmethod
    def update(csrftoken):
        if not csrftoken: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT csrftoken FROM recaptcha "
                                 f"WHERE csrftoken=?", (csrftoken,)).fetchall()

            if not len(result):
                cur.execute(f"UPDATE recaptcha SET is_used=1, u_time=? WHERE csrftoken=?",
                            (int(time.time())), csrftoken)

            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    @staticmethod
    def is_used(csrftoken):
        if not csrftoken: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            is_used = cur.execute(f"SELECT is_used FROM recaptcha "
                                 f"WHERE csrftoken=?", (csrftoken,)).fetchall()

            result = None

            if len(result):
                result = is_used[0]

            con.commit()

            return result

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()




