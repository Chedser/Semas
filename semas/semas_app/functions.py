SALT = "Python++"

import random
import sqlite3
from .settings import *
from .logs import *

def get_hash(password):
    import hashlib
    key = password + SALT
    hashed = hashlib.md5(key.encode())
    return hashed.hexdigest()


def gen_pass(nick, email):
    if not nick or not email: return
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ""

    length = random.randrange(10,12)

    for i in range(length):
        password += random.choice(chars)

    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        user_exists = cur.execute(
            f"SELECT COUNT(*) FROM user WHERE NOT is_blocked AND nick=? AND login=?", (nick, email)).fetchall()[0][0]

        if not user_exists: return 1

        hash = get_hash(password)

        cur.execute(f"UPDATE user SET password=? WHERE nick=? AND login=?", (hash,nick, email))
        con.commit()

        result = password

    except sqlite3.Error as error:
        con.rollback()
        print(f"DataBase error {error.__str__()}")
        Log.write_log(error.__str__(), gen_pass.__name__)
        result = 2
    finally:
        con.close()

    return result
