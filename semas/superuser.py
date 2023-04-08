import datetime
import getpass
import sqlite3

MIN_LEN_PASS = 5


def get_hash(password):
    import hashlib
    salt = "Python++"
    key = password + salt
    hashed = hashlib.md5(key.encode())
    return hashed.hexdigest()

def get_new_user():
    lst = list()
    while True:
        print("Input login")
        login = input()

        if len(login) < 2:
            print("Login is too short")
            continue

        password = getpass.getpass("Input password\n")

        if len(password) < MIN_LEN_PASS:
            print(f"Password must have at least {MIN_LEN_PASS} symbols")
            continue

        password_repeat = getpass.getpass("Repeat password\n")

        if len(password) != len(password_repeat):
            print("Passwords must be equals\n")
            print("Try again Y\\N?")
            user_answer = input()
            if user_answer != "Y" or user_answer != "y":
                exit()
        lst.append(login)
        lst.append(get_hash(password))
        break
    return lst

try:

    con = sqlite3.connect('db.sqlite3')

    result = cur.execute("SELECT COUNT(*) FROM superuser").fetchall()

    if result.pop(0)[0] == 0:
        print("Create new user\n")
        new_user = get_new_user()
        cur.execute("INSERT INTO superuser (login,password) VALUES (?,?)", (new_user[0], new_user[1]))
        con.commit()
        print("Superuser was created")

    else:
            print("Change password\n")
            print("Type login")
            login = input()
            result = cur.execute(f"SELECT login, password FROM superuser WHERE login='{login}'").fetchall()
            if len(result) == 0:
                print("User not found")
                con.close()
                exit()

            typed_pass = getpass.getpass("Input password\n")
            bd_pass = result.pop(0)[1]

            if bd_pass != get_hash(typed_pass):
                print("Wrong password")
                con.close()
                exit()

            new_pass = getpass.getpass("Input new password\n")

            if len(new_pass) == 0:
                print("Wrong input")
                con.close()
                exit()

            repeat_pass = getpass.getpass("Repeat new password\n")

            if new_pass != repeat_pass:
                print("Passwords must be equals")
                exit()

            cur.execute(f"UPDATE superuser SET password=?, date_of_change=? WHERE login='{login}'", (get_hash(new_pass), \
             datetime.datetime.now().strftime("%d-%m-%Y %H:%M")))
            con.commit()

except sqlite3.Error as error:
    con.rollback()
    print(f"DataBase error")
finally:
    con.close()
