import json
from .functions import *
from .enums import *
from django.http import JsonResponse
import os
import re
import html
from .logs import *
from .exceptions import *


class Message:
    @staticmethod
    def tolink(txt: str) -> str:
        pattern1 = r'\b((?:https?://)(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        pattern2 = r'\b((?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        result = html.escape(txt)
        if re.findall(pattern1, result):
            result = re.sub(pattern1, r'<a href=\1 target=_blank>\1</a>', result)
        elif re.findall(pattern2, result):
            result = re.sub(pattern2, r'<a href=//\1 target=_blank>\1</a>', result)
        return result

    @staticmethod
    def truncate(txt: str, count: int) -> str:
        if len(txt) <= count: return txt
        return txt[:count] + "..."


class Auth:
    @staticmethod
    def auth(request: object) -> JsonResponse:
        login = request.POST.get('login').strip()
        password = request.POST.get('pass').strip()

        if not len(login) or \
           not len(password) or \
            "admin" in login.lower() or  \
            "админ" in login.lower():
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        response = Response.SUCCESS.value
        user_id = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, login, password FROM user WHERE login=?", (login,)).fetchall()
            if not len(result): raise WrongUserOrPassword

            is_blocked = User.get_info(int(result[0][0]))["is_blocked"]
            if is_blocked: raise UserIsBlocked

            bd_pass = result[0][2]
            if bd_pass != get_hash(password): raise WrongUserOrPassword

            user_id = result[0][0]
            # Создание сессии
            request.session["id"] = user_id
        except sqlite3.Error as error: #Ошибка базы данных
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Auth.auth.__name__)
            response = Response.UNKNOWN_ERROR.value
        except WrongUserOrPassword as error: #Неверный пользователь или пароль
            print(f"{error.__str__()}")
            response = Response.WRONG_USER_OR_PASSWORD.value
        except UserIsBlocked as error: #Пользователь заблокирован
            print(f"{error.__str__()}")
            response = Response.USER_IS_BLOCKED.value
        finally:
            con.close()
        return JsonResponse({'message': response, "id": user_id})


class Reg:
    @staticmethod
    def reg(request: object) -> JsonResponse:
        login = request.POST.get('login').strip()
        nick = request.POST.get('nick').strip()
        sex = request.POST.get('sex')
        password = request.POST.get('pass').strip()
        session = request.session.get("id")

        if session: del session
        if not len(login) or \
            not len(nick) or \
            not len(sex) or \
            "admin" in login.lower() or \
            "админ" in login.lower():
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM user WHERE login=? OR nick=?", (login, nick)).fetchall()

            if len(result):
                response = Response.USER_EXISTS.value
            else:
                hashed_pass = get_hash(password)

                cur.execute("INSERT INTO user (login,password,nick,sex,u_time_of_last_action) \
                 VALUES (?,?,?,?,?)", (login, hashed_pass, nick, sex, int(time.time())))
                con.commit()
                last_id = cur.execute(f"SELECT MAX(id) FROM user WHERE login=?", (login,)).fetchall()[0][0]

                file_path = f"semas_app/static/images/avatars/{last_id}"
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                Log.write_log(f"New user: {nick} {login}", Reg.reg.__name__, LogType.NEW_USER.value)

                cur.execute(f"INSERT INTO notice(entityId, type, u_time) VALUES(?,?,?)", \
                            (last_id, NoticeType.NEW_USER.value, int(time.time())))
                con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Reg.reg.__name__)
            response = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': response})


class MessageWall:
    @staticmethod
    def send_wall_message(request: object) -> JsonResponse:
        message = request.POST.get('message').strip()
        receiver_id = request.POST.get('receiver_id')

        if not len(message) or \
           not receiver_id:
            return JsonResponse({'message': Response.WRONG_USER_OR_PASSWORD.value})

        receiver_id = int(request.POST.get('receiver_id'))

        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            user_info = User.get_info(int(cookie_user_id))
            if user_info:
                is_blocked = user_info["is_blocked"]
                if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        User.update_time_of_last_action(cookie_user_id)

        result = Response.SUCCESS.value

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            cur.execute("INSERT INTO wall_message (senderId, receiverId, text, u_time)\
                  VALUES (?,?,?,?)", (cookie_user_id, receiver_id, message, int(time.time())))
            con.commit()

            lastrowid = cur.lastrowid
            notice_type = NoticeType.SELF_PAGE_MESSAGE.value
            if cookie_user_id != receiver_id:
                notice_type = NoticeType.OTHER_USER_PAGE_MESSAGE.value

            cur.execute("INSERT INTO notice (entityId, type, u_time)\
                              VALUES (?,?,?)", (lastrowid, notice_type, int(time.time())))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), MessageWall.send_wall_message.__name__)
            result = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': result})

    @staticmethod
    def delete_wall_message(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        user_id = request.POST.get("user_id")
        message_id = request.POST.get("message_id")
        sender_id = request.POST.get("sender_id")

        if not user_id or \
                not message_id or \
                not sender_id:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        user_id = int(user_id)
        sender_id = int(sender_id)
        message_id = int(message_id)

        User.update_time_of_last_action(cookie_user_id)

        result = Response.SUCCESS.value

        if cookie_user_id == user_id or cookie_user_id == sender_id:
            try:
                con = sqlite3.connect(DB_NAME)

                cur = con.cursor()
                cur.execute(f"DELETE FROM wall_message WHERE id=?", (message_id,))
                cur.execute(f"DELETE FROM notice WHERE entityId=?", (message_id,))
                con.commit()
            except sqlite3.Error as error:
                con.rollback()
                print(f"DataBase error {error.__str__()}")
                Log.write_log(error.__str__(), MessageWall.delete_wall_message.__name__)
                result = Response.UNKNOWN_ERROR.value
            finally:
                con.close()
            return JsonResponse({'message': result})
        else:
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})

    @staticmethod
    def get_wall_messages(user_id: int) -> list:
        if not user_id: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT wall_message.id AS id, senderId, text, user.nick AS nick, user.avatar AS avatar, date FROM wall_message \
             INNER JOIN user ON wall_message.senderId=user.id "
                                 f"WHERE receiverId=? ORDER BY date DESC", (user_id,)).fetchall()
            return MessageWall._parse_wall_messages(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), MessageWall.get_wall_messages.__name__)
            return None
        finally:
            con.close()

    @staticmethod
    def get_wall_message_by_id(id: int) -> dict:
        if not id: return None

        response = None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, senderId, receiverId, text, date FROM wall_message  WHERE id=?",
                                 (id,)).fetchall()
            if not len(result): return

            response = MessageWall._parse_wall_message(result[0])

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), MessageWall.get_wall_message_by_id.__name__)
        finally:
            con.close()
        return response

    @staticmethod
    def _parse_wall_message(result: list) -> dict:
        if not result:  return None

        id = result[0]
        sender_id = result[1]
        receiver_id = result[2]
        message = result[3]
        date = result[4]
        likes_count = WallMessageLike.get_wall_message_likes_count(id)

        res = dict()
        res["id"] = id
        res["sender_id"] = sender_id
        res["receiver_id"] = receiver_id
        res["message"] = Message.truncate(Message.tolink(message), 256)
        res["likes_count"] = likes_count
        res["date"] = date
        return res

    @staticmethod
    def _parse_wall_messages(wall_messages: list) -> list:
        result = list()

        for wall_message in wall_messages:
            id = wall_message[0]
            sender_id = wall_message[1]
            message = wall_message[2]
            nick = wall_message[3]
            avatar = wall_message[4]
            avatar = User.get_avatar_link(avatar, sender_id)
            date = wall_message[5]

            likes_count = WallMessageLike.get_wall_message_likes_count(id)

            dct = dict()
            dct["id"] = id
            dct["sender_id"] = sender_id
            dct["message"] = Message.tolink(message)
            dct["nick"] = nick
            dct["avatar"] = avatar
            dct["likes_count"] = likes_count
            dct["date"] = date
            result.append(dct)
        return result


class User:
    @staticmethod
    def get_info(user_id: int) -> dict:
        res = None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, sex, is_blocked, u_time_of_last_action, avatar \
                FROM user WHERE id=?", (user_id,)).fetchall()

            if not len(result): raise UserDoesNotExists

            res = User._parse_user_info(result[0])
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.get_info.__name__)
        except UserDoesNotExists as error:
            print(f"{error.__str__()}: {User.get_info.__name__}")
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_user_info(user_info: list) -> dict:
        result = dict()
        user_id = user_info[0]
        nick = user_info[1]
        sex = user_info[2]
        is_blocked = user_info[3]
        time_of_last_action = user_info[4]
        avatar = user_info[5]
        result["id"] = user_id
        result["nick"] = nick
        result["is_blocked"] = is_blocked
        result["time_of_last_action"] = time_of_last_action
        result["is_online"] = User._is_online(time_of_last_action)
        result["avatar"] = User.get_avatar_link(avatar, user_id)
        result["sex"] = sex
        return result

    @staticmethod
    def get_avatar_link(avatar: str, user_id: int) -> str:
        if not avatar:
            link = f"images/default.png"
        else:
            link = f"images/avatars/{user_id}/{avatar}"
        return link

    @staticmethod
    def _is_online(time_of_last_action: int) -> bool:
        return int(time.time() - time_of_last_action) < 300

    @staticmethod
    def get_blocked_users(cookie_user_id: int):
        if not cookie_user_id: return None
        cookie_user_id = int(cookie_user_id)
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT user.id AS id, user.nick AS nick, avatar FROM black_list "
                                 f"INNER JOIN user ON user.id = black_list.user2 "
                                 f"WHERE user1=?", (cookie_user_id,)).fetchall()

            return User._parse_blocked_users(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.get_blocked_users.__name__)
        finally:
            con.close()

    @staticmethod
    def user_is_in_black_list(user_id: int, cookie_user_id: int) -> int:
        if not user_id or not cookie_user_id: return
        res = -1
        if user_id == cookie_user_id: return res

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) FROM black_list WHERE (user1=? AND "
                                 f"user2=?) OR (user1=? AND user2=?)",
                                 (user_id, cookie_user_id, cookie_user_id, user_id)).fetchall()[0][0]

            res = result

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.user_is_in_black_list.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_blocked_users(users: list) -> list:
        result = list()
        for user in users:
            id = user[0]
            nick = user[1]
            avatar = user[2]
            avatar = User.get_avatar_link(avatar, id)

            tmp = dict()
            tmp["id"] = id
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_blocked"] = 1
            result.append(tmp)
        return result

    @staticmethod
    def find_user_for_block(request: object) -> list:
        user_id = request.POST.get("user_id")
        cookie_user_id = request.session.get("id")
        if not user_id or not cookie_user_id: return JsonResponse({"message": 1})
        user_id = int(user_id)
        cookie_user_id = int(cookie_user_id)

        if cookie_user_id == user_id:
            return JsonResponse({"message": 2})

        res = 1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, avatar FROM user WHERE id=?", (user_id,)).fetchall()

            if not len(result): raise UserDoesNotExists

            result = result[0]

            lst = list()
            id = result[0]
            nick = result[1]
            avatar = result[2]
            avatar = User.get_avatar_link(avatar, id)
            is_in_black_list = User.user_is_in_black_list(id, cookie_user_id)
            tmp = dict()
            tmp["id"] = id
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_in_black_list"] = is_in_black_list
            lst.append(tmp)

            User.update_time_of_last_action(cookie_user_id)

            res = json.dumps(lst)

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.find_user_for_block.__name__)
        except UserDoesNotExists as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({"message": res})

    @staticmethod
    def block_user(request: object) -> int:
        user_id = request.POST.get("user_id")
        cookie_user_id = request.session.get("id")
        if not user_id or not cookie_user_id: return JsonResponse({"message": 1})
        user_id = int(user_id)
        cookie_user_id = int(cookie_user_id)

        if cookie_user_id == user_id:
            return JsonResponse({"message": 2})

        User.update_time_of_last_action(cookie_user_id)

        is_blocked = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) FROM black_list WHERE user1=? "
                                 f"AND user2=?", (cookie_user_id, user_id)).fetchall()[0][0]

            if not result:
                cur.execute(f"INSERT INTO black_list(user1, user2, u_time) VALUES "
                            f"(?,?,?)",
                            (cookie_user_id, user_id, int(time.time())))
                is_blocked = 1
            else:
                cur.execute(f"DELETE FROM black_list WHERE user1=? AND user2=?",
                            (cookie_user_id, user_id))

            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.block_user.__name__)
            is_blocked = 2
        finally:
            con.close()
        return JsonResponse({'message': is_blocked})

    @staticmethod
    def update_time_of_last_action(cookie_user_id: int) -> None:
        if not cookie_user_id: return

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"UPDATE user SET  u_time_of_last_action=? WHERE id=?", (int(time.time()), cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.update_time_of_last_action.__name__)
        finally:
            con.close()

    @staticmethod
    def get_all_users() -> list:
        res = None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(
                f"SELECT id, nick, avatar FROM user WHERE NOT is_blocked ORDER BY date_of_reg DESC").fetchall()

            res = User._parse_all_users(result)

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.get_all_users.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_all_users(users: list) -> list:
        result = list()
        for user in users:
            id = user[0]
            nick = user[1]
            avatar = user[2]
            avatar = User.get_avatar_link(avatar, id)

            tmp = dict()
            tmp["id"] = id
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            result.append(tmp)
        return result

    @staticmethod
    def find_user_by_nick(request: object) -> JsonResponse:
        if not request.POST.get("nick"): return JsonResponse({"message": -1})

        nick = request.POST.get("nick")
        response = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(
                f"SELECT id, nick, avatar FROM user WHERE nick LIKE '{nick}%' AND NOT is_blocked ORDER BY length(nick)").fetchall()

            if not len(result):
                result = cur.execute(
                    f"SELECT id, nick, avatar FROM user WHERE nick LIKE '%{nick}%' AND NOT is_blocked ORDER BY length(nick)").fetchall()

            result = User.__parse_all_users(result)

            response = json.dumps(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.find_user_by_nick.__name__)
        finally:
            con.close()
        return JsonResponse({"message": response})

    @staticmethod
    def change_pass(request: object) -> JsonResponse:
        if not request.session.get("id") or not request.POST.get("pass"):
            return JsonResponse({"message": Response.WRONG_INPUT.value})

        cookie_user_id = int(request.session.get("id"))
        pass_ = request.POST.get("pass").strip()

        if not len(pass_): return JsonResponse({"message": Response.WRONG_INPUT.value})

        hashed_pass = get_hash(pass_)
        result = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"UPDATE user SET password=? WHERE id=?", (hashed_pass, cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), User.change_pass.__name__)
            result = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({"message": result})


class File:
    # расширения файлов, которые разрешено загружать
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 3 * 10 ** 6

    def _allowed_file(content_type: str) -> bool:
        return content_type.split('/')[1] in File.ALLOWED_EXTENSIONS

    def _get_extension(content_type: str) -> str:
        return content_type.split('/')[1]

    def _rename_file(content_type: str) -> str:
        return f"{int(time.time())}.{File._get_extension(content_type)}"

    def _upload_file(file: str, url: str) -> None:
        with open(url, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    def change_avatar(request: object) -> JsonResponse:
        avatar = request.FILES.get("avatar")
        if request.session.get("id") and \
                request.POST.get("MAX_FILE_SIZE") and \
                avatar:
            max_file_size_client = int(request.POST.get("MAX_FILE_SIZE"))
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        if max_file_size_client > File.MAX_FILE_SIZE or \
                not avatar or \
                not File._allowed_file(avatar.content_type):
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        new_file_name = File._rename_file(avatar.content_type)

        url = f'./semas_app/static/images/avatars/{cookie_user_id}/{new_file_name}'

        File._upload_file(avatar, url)
        User.update_time_of_last_action(cookie_user_id)

        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"UPDATE user SET avatar=? WHERE id=?", (new_file_name, cookie_user_id))
            con.commit()

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), File.change_avatar.__name__)
            response = Response.WRONG_INPUT.value
        finally:
            con.close()
        return JsonResponse({'message': response})


class Friend:
    @staticmethod
    def get_friend_requests_count(cookie_user_id: int) -> int:
        if not cookie_user_id: return 0
        res = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) FROM friend_request WHERE friend2=?",
                                 (int(cookie_user_id),)).fetchall()[0][0]
            con.commit()
            res = result
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friend_requests_count.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def get_friends_count(cookie_user_id: int) -> int:
        if cookie_user_id is None: return 0
        res = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) \
                                                FROM friend WHERE friend1=? OR friend2=?",
                                 (cookie_user_id, cookie_user_id)).fetchall()[0][0]
            con.commit()
            res = result
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friends_count.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def get_friend_requests(cookie_user_id: int) -> list:
        if not cookie_user_id: return

        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, user.nick AS nick, user.avatar AS avatar \
                                     FROM friend_request INNER JOIN user ON user.id=friend1 \
                                      WHERE friend2=?", (cookie_user_id,)).fetchall()
            if not len(result): raise NoFriendRequests
            res = Friend._parse_friend_requests(result, cookie_user_id)
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friend_requests.__name__)
        except NoFriendRequests as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return res

    @staticmethod
    def get_friend_request_status(cookie_user_id: int, user_id: int) -> int:
        if not cookie_user_id: return FriendStatus.UNAUTHED.value
        if cookie_user_id == user_id: return FriendStatus.SAME_PAGE.value  # Сидим на своей странице

        friend_status = FriendStatus.NOT_FRIEND.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result_friends = cur.execute(f"SELECT friend1, friend2 FROM friend WHERE (friend1={int(cookie_user_id)} \
                 AND friend2={user_id}) OR (friend1={int(user_id)} AND friend2={cookie_user_id})").fetchall()
            result_request = cur.execute(
                f"SELECT friend1, friend2 FROM friend_request WHERE (friend1={int(cookie_user_id)} \
                             AND friend2={user_id}) OR (friend1={int(user_id)} AND friend2={cookie_user_id})").fetchall()
            if not len(result_friends) and \
                not len(result_request):
                friend_status = FriendStatus.NOT_FRIEND.value  # В друзьях нет в заявках тоже
            if not len(result_friends) and len(result_request):  # В друзьях нет в заявках есть
                if result_request[0][0] == cookie_user_id:
                    friend_status = FriendStatus.CANCEL_REQUEST.value  # Заявку отправил куки юзер. Отменить заявку
                else:
                    friend_status = FriendStatus.DECLINE_REQUEST.value  # Заявку оправил тот, у которого сидим. Отклонить
            if len(result_friends) and not len(result_request):
                friend_status = FriendStatus.IS_FRIEND.value  # Друзья

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friend_request_status.__name__)
            friend_status = FriendStatus.UNKNOWN_ERROR.value
        finally:
            con.close()
        return friend_status

    @staticmethod
    def send_friend_request(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = int(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        User.update_time_of_last_action(cookie_user_id)
        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result_friends = cur.execute(f"SELECT friend1, friend2 FROM friend WHERE (friend1={(cookie_user_id)} \
                     AND friend2={user_id}) OR (friend1={(user_id)} AND friend2={cookie_user_id})").fetchall()
            result_request = cur.execute(
                f"SELECT friend1, friend2 FROM friend_request WHERE (friend1={cookie_user_id} \
                                 AND friend2={user_id}) OR (friend1={user_id} AND friend2={cookie_user_id})").fetchall()
            if len(result_friends) == 0 and len(result_request) == 0:  # В друзьях нет в заявках тоже
                cur.execute("INSERT INTO friend_request (friend1, friend2, u_time) \
                        VALUES (?,?,?)", (cookie_user_id, user_id, (int)(time.time())))
                con.commit()
            else:
                response = Response.WRONG_INPUT.value
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.send_friend_request.__name__)
            response = Response.WRONG_INPUT.value
        finally:
            con.close()
        return JsonResponse({'message': response})

    @staticmethod
    def cancel_friend_request(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = int(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        User.update_time_of_last_action(cookie_user_id)

        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend_request WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.cancel_friend_request.__name__)
            response = Response.WRONG_INPUT.value
        finally:
            con.close()
        return JsonResponse({'message': response})

    @staticmethod
    def accept_friend_request(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        user_id = int(user_id)
        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        User.update_time_of_last_action(cookie_user_id)
        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend_request WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()
            cur.execute("INSERT INTO friend (friend1, friend2, u_time) \
                               VALUES (?,?,?)", (cookie_user_id, user_id, (int)(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.accept_friend_request.__name__)
            response = Response.WRONG_INPUT.value
        finally:
            con.close()
        return JsonResponse({'message': response})

    @staticmethod
    def delete_friend(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        user_id = int(user_id)
        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        User.update_time_of_last_action(cookie_user_id)

        response = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                 OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.delete_friend.__name__)
            response = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': response})

    @staticmethod
    def get_friends(cookie_user_id: int) -> list:
        if not cookie_user_id: return None

        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, friend2 FROM friend \
                 WHERE friend1=? OR friend2=?",
                                 (cookie_user_id, cookie_user_id)).fetchall()
            if not len(result): raise NoFriends

            for user in result:
                current_user = list()
                if user[0] != cookie_user_id:
                    current_user.append(user[0])
                elif user[1] != cookie_user_id:
                    current_user.append(user[1])
                result2 = cur.execute(f"SELECT nick, avatar FROM user \
                                 WHERE id=?", (current_user[0],)).fetchall()
                tmp = dict()
                tmp["id"] = current_user[0]
                tmp["nick"] = result2[0][0]
                avatar = User.get_avatar_link(result2[0][1], current_user[0])
                tmp["avatar"] = avatar
                res.append(tmp)

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friends.__name__)
        except NoFriends as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return res

    @staticmethod
    def get_friends_user_page(cookie_user_id: int, limit: int) -> list:
        if not cookie_user_id: return None

        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, friend2 FROM friend \
                        WHERE friend1={int(cookie_user_id)} OR friend2={int(cookie_user_id)} LIMIT {limit}").fetchall()
            if not len(result): raise NoFriends

            for user in result:
                current_user = list()
                if user[0] != cookie_user_id:
                    current_user.append(user[0])
                elif user[1] != cookie_user_id:
                    current_user.append(user[1])
                result2 = cur.execute(f"SELECT nick, avatar FROM user \
                                        WHERE id=?", (current_user[0],)).fetchall()
                tmp = dict()
                tmp["id"] = current_user[0]
                tmp["nick"] = result2[0][0]
                avatar = User.get_avatar_link(result2[0][1], current_user[0])
                tmp["avatar"] = avatar
                res.append(tmp)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Friend.get_friends_user_page.__name__)
        except NoFriends as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_friend_requests(friend_requests: list, cookie_user_id: int) -> list:
        result = list()
        for friend_request in friend_requests:
            friend1 = friend_request[0]
            nick = friend_request[1]
            avatar = friend_request[2]
            avatar = User.get_avatar_link(avatar, friend1)
            is_in_black_list = User.user_is_in_black_list(friend1, cookie_user_id)

            tmp = dict()
            tmp["id"] = friend1
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_in_black_list"] = is_in_black_list
            result.append(tmp)
        return result


class Forum:
    @staticmethod
    def create_forum(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        if request.POST.get('message') and request.POST.get('topic').strip():
            message = request.POST.get('message').strip()
            topic = request.POST.get('topic').strip()
            topic_modified = re.sub("[\s|\W]", "", topic)

            if not len(topic_modified):
                return JsonResponse({'message': ForumCreateResponse.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': ForumCreateResponse.WRONG_INPUT.value})

        if not len(message) or not len(topic):
            return JsonResponse({'message': ForumCreateResponse.WRONG_INPUT.value})
        User.update_time_of_last_action(cookie_user_id)

        res = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            forum_count = cur.execute(f"SELECT COUNT(*) FROM forum WHERE name_lower=?",
                                      (topic_modified,)).fetchall()[0][0]
            if forum_count: raise ForumExists

            cur.execute("INSERT INTO forum (creatorId, name, name_lower, text, u_time)\
                          VALUES (?,?,?,?,?)", (cookie_user_id, topic, topic_modified, message, int(time.time())))
            con.commit()

            lastrowid = cur.lastrowid
            notice_type = NoticeType.CREATE_FORUM.value
            cur.execute("INSERT INTO notice (entityId, type, u_time) VALUES (?,?,?)",
                        (lastrowid, notice_type, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.create_forum.__name__)
            res = ForumCreateResponse.UNKNOWN_ERROR.value
        except ForumExists as error:
            res = ForumCreateResponse.FORUM_EXISTS.value
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def get_forums() -> list:
        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute("SELECT forum.id AS id, creatorId, name, text, date, user.avatar AS avatar, user.nick AS nick \
             FROM forum INNER JOIN user ON forum.creatorId=user.id ORDER BY date DESC").fetchall()

            res = Forum._parse_forums(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.get_forums.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_forums(forums: list) -> list:
        result = list()
        for forum in forums:
            id = forum[0]
            creatorId = forum[1]
            forum_name = forum[2]
            message = forum[3]
            date = forum[4]
            avatar = forum[5]
            avatar = User.get_avatar_link(avatar, creatorId)
            nick = forum[6]
            likes_count = ForumMainMessageLike.get_forum_main_message_likes_count(id)

            tmp = dict()
            tmp["id"] = id
            tmp["creator_id"] = creatorId
            tmp["name"] = forum_name
            tmp["message"] = Message.truncate(message, 256)
            tmp["date"] = date
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["likes_count"] = likes_count
            result.append(tmp)
        return result

    @staticmethod
    def _parse_forum_info(forum: list) -> dict:
        id = forum[0]
        creatorId = forum[1]
        forum_name = forum[2]
        message = forum[3]
        date = forum[4]
        avatar = forum[5]
        avatar = User.get_avatar_link(avatar, creatorId)
        nick = forum[6]

        likes_count = ForumMainMessageLike.get_forum_main_message_likes_count(id)

        res = dict()
        res["id"] = id
        res["creator_id"] = creatorId
        res["name"] = forum_name
        res["message"] = Message.tolink(message)
        res["date"] = date
        res["nick"] = nick
        res["avatar"] = avatar
        res["likes_count"] = likes_count
        return res

    @staticmethod
    def _parse_messages(messages):
        result = list()
        for message in messages:
            id = message[0]
            senderId = message[1]
            txt = message[2]
            date = message[3]
            avatar = message[4]
            nick = message[5]
            avatar = User.get_avatar_link(avatar, senderId)

            likes_count = ForumMessageLike.get_forum_message_likes_count(id)

            tmp = dict()
            tmp["id"] = id
            tmp["sender_id"] = senderId
            tmp["message"] = Message.tolink(txt)
            tmp["date"] = date
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["likes_count"] = likes_count
            result.append(tmp)
        return result

    @staticmethod
    def get_messages(id: int) -> list:
        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT forum_message.id AS id, senderId, text, date, user.avatar AS avatar, user.nick AS nick \
                 FROM forum_message INNER JOIN user ON forum_message.senderId=user.id WHERE forumId=?",
                                 (id,)).fetchall()

            if not len(result): raise NoMessages

            res = Forum._parse_messages(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.get_messages.__name__)
        except NoMessages as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return res

    @staticmethod
    def send_message(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        message = request.POST.get('message').strip()
        forum_id = request.POST.get('id')
        User.update_time_of_last_action(cookie_user_id)
        if not message or not forum_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        forum_info = Forum.get_forum_info(forum_id)
        if not forum_info: return JsonResponse({'message': Response.WRONG_INPUT.value})

        res = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute("INSERT INTO forum_message (senderId, forumId, text, u_time)\
                                     VALUES (?,?,?,?)",
                        (cookie_user_id, forum_id, message, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.send_message.__name__)
            res = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def get_forum_info(id: int) -> dict:
        res = dict()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT forum.id AS id,  creatorId, name, text, forum.date AS date, user.avatar AS avatar, user.nick AS nick  \
                    FROM forum INNER JOIN user ON forum.creatorId=user.id WHERE forum.id=?", (id,)).fetchall()
            if not len(result): return NoForumInfo
            result = result[0]
            res = Forum._parse_forum_info(result)
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.get_forum_info.__name__)
        except NoForumInfo as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return res

    @staticmethod
    def delete_message(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        message_id = request.POST.get("message_id")
        sender_id = request.POST.get("sender_id")

        if not message_id or not sender_id:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        sender_id = int(sender_id)
        message_id = int(message_id)

        if sender_id != cookie_user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        User.update_time_of_last_action(cookie_user_id)
        res = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM forum_message WHERE id=?", (message_id,))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Forum.delete_message.__name__)
            res = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': res})


class Dialog:
    @staticmethod
    def _create_dialog(sender_id: int, receiver_id: int, message: str) -> bool:
        is_blocked_sender_id = User.get_info(sender_id)["is_blocked"]
        is_blocked_receiver_id = User.get_info(receiver_id)["is_blocked"]
        if is_blocked_sender_id or is_blocked_receiver_id: return False
        user_is_in_black_list = User.user_is_in_black_list(is_blocked_sender_id, is_blocked_receiver_id)
        if user_is_in_black_list: return False
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute("INSERT INTO dialog (senderId, receiverId, last_message, u_time)\
                                     VALUES (?,?,?,?)",
                        (sender_id, receiver_id, message, int(time.time())))
            con.commit()

            lastrowid = cur.lastrowid
            cur.execute("INSERT INTO dialog_message (userId, dialogId, text, u_time)\
                                                 VALUES (?,?,?,?)",
                        (sender_id, lastrowid, message, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog._create_dialog.__name__)
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def get_dialog_id(cookie_user_id: int, receiver_id: int):
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM dialog "
                                 f"WHERE senderId={cookie_user_id} AND receiverId={receiver_id} "
                                 f"OR senderId={receiver_id} AND receiverId={cookie_user_id}").fetchall()
            dialog_id = 0
            if len(result): dialog_id = result[0][0]

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialog_id.__name__)
        finally:
            con.close()
        return dialog_id

    @staticmethod
    def get_active_dialogs_count(cookie_user_id: int) -> int:
        if not cookie_user_id: return 0
        dialogs_count = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            dialogs_count = cur.execute(f"SELECT COUNT(*)  FROM dialog"
                                        f" WHERE receiverId=? AND is_readen=0", (cookie_user_id,)).fetchall()[0][0]
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_active_dialogs_count.__name__)
        finally:
            con.close()
        return dialogs_count

    @staticmethod
    def get_dialogs_count(cookie_user_id: int) -> int:
        if not cookie_user_id: return 0
        dialogs_count = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            dialogs_count = cur.execute(f"SELECT COUNT(*)  FROM dialog"
                                        f" WHERE senderId=? OR  receiverId=?",
                                        (cookie_user_id, cookie_user_id)).fetchall()[0][0]
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialogs_count.__name__)
        finally:
            con.close()
        return dialogs_count

    @staticmethod
    def _send_outer_in_existing_dialog(dialog_id: int, sender_id: int, receiver_id: int, message: str) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET senderId=?, receiverId=?, last_message=?, is_readen=0, u_time=? WHERE id=?",
                (sender_id, receiver_id, message, int(time.time()), dialog_id))
            con.commit()
            cur.execute("INSERT INTO dialog_message (userId, dialogId, text, u_time)\
                                                         VALUES (?,?,?,?)",
                        (sender_id, dialog_id, message, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.__send_outer_in_existing_dialog.__name__)
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def get_dialog_info(dialog_id: int) -> dict:
        result = dict()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            dialog = cur.execute(
                f"SELECT id, senderId, receiverId, is_readen, date FROM dialog WHERE id=?",
                (dialog_id,)).fetchall()
            if not dialog: raise NoDialogInfo
            result["id"] = dialog[0][0]
            result["sender_id"] = dialog[0][1]
            result["receiver_id"] = dialog[0][2]
            result["is_readen"] = dialog[0][3]
            result["date"] = dialog[0][4]
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialog_info.__name__)
        except NoDialogInfo as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return result

    @staticmethod
    def get_dialog_opponent_info(cookie_user_id: int, dialog_id: int):
        result = dict()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            dialog = cur.execute(
                f"SELECT senderId, receiverId FROM dialog WHERE id=?", (dialog_id,)).fetchall()[0]

            if not len(dialog): raise NoDialogOpponentInfo

            sender_id = dialog[0]
            receiver_id = dialog[1]
            opponent_id = receiver_id

            if sender_id != cookie_user_id: opponent_id = sender_id

            result = User.get_info(opponent_id)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialog_opponent_info.__name__)
        except NoDialogOpponentInfo as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return result

    @staticmethod
    def update_status(cookie_user_id: int, dialog_id: int) -> bool:
        dialog_info = Dialog.get_dialog_info(dialog_id)
        receiver_id = dialog_info["receiver_id"]

        result = True
        if len(dialog_info) and receiver_id:
            receiver_id = int(receiver_id)
        if receiver_id != cookie_user_id: return False
        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET is_readen=1, u_time=? WHERE id=?",
                (int(time.time()), dialog_id))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.update_status.__name__)
            result = False
        finally:
            con.close()
        return result

    # ДОДЕЛАТЬ
    @staticmethod
    def get_dialogs(cookie_user_id: int) -> list:
        result = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE receiverId=? AND is_readen=0 " \
                  "ORDER by u_time DESC"

            dialogs_not_readen = cur.execute(sql, (cookie_user_id,)).fetchall()

            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE receiverId=? AND is_readen=1 " \
                  "ORDER by u_time DESC"

            dialogs_readen = cur.execute(sql, (cookie_user_id,)).fetchall()

            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE senderId=? " \
                  "ORDER by u_time DESC"

            dialogs_sender = cur.execute(sql, (cookie_user_id,)).fetchall()

            # sql = f"SELECT id, senderId, receiverId, last_message, is_readen," \
            # f"date, u_time FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=0 " \
            # f"UNION " \
            # f"SELECT id, senderId, receiverId, last_message, is_readen, " \
            # f"date, u_time FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=1 " \
            # f"UNION " \
            # f"SELECT id, senderId, receiverId, last_message, is_readen, " \
            # f"date, u_time FROM dialog WHERE senderId={cookie_user_id} " \
            # f"ORDER BY date DESC"

            dialogs = dialogs_not_readen + dialogs_readen + dialogs_sender

            # sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
            # f"date FROM dialog WHERE senderId=? OR receiverId=? " \
            # "ORDER by date DESC,is_readen ASC"

            if not len(dialogs): raise NoDialogs

            result = Dialog._parse_dialogs(dialogs, cookie_user_id)
            User.update_time_of_last_action(cookie_user_id)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialogs.__name__)
        except NoDialogs as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return result

    @staticmethod
    def _parse_dialogs(dialogs: list, cookie_user_id: int) -> list:
        result = list()
        for dialog in dialogs:
            id = dialog[0]
            sender_id = dialog[1]
            receiver_id = dialog[2]

            is_cookie_user = False
            if sender_id == cookie_user_id:
                sender_id = receiver_id
                is_cookie_user = True
            last_message = Message.truncate(dialog[3], 100)
            is_readen = dialog[4]
            date = dialog[5]
            user_info = User.get_info(sender_id)
            avatar = user_info["avatar"]
            nick = user_info["nick"]

            tmp = dict()
            tmp["id"] = id
            tmp["sender_id"] = sender_id
            tmp["receiver_id"] = receiver_id
            tmp["is_readen"] = 1

            if receiver_id == cookie_user_id and is_readen == 0:
                tmp["is_readen"] = 0

            tmp["last_message"] = last_message
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_cookie_user"] = is_cookie_user
            tmp["date"] = date
            result.append(tmp)
        return result

    @staticmethod
    def _send_inner_in_existing_dialog(dialog_id: int, sender_id: int, receiver_id: int, message: str, is_readen: int) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET senderId=?, receiverId=?, last_message=?, is_readen=?, u_time=? WHERE id=?",
                (sender_id, receiver_id, message, is_readen, int(time.time()), dialog_id))
            con.commit()
            cur.execute("INSERT INTO dialog_message (userId, dialogId, text, u_time)\
                                                            VALUES (?,?,?,?)",
                        (sender_id, dialog_id, message, int(time.time())))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.__send_inner_in_existing_dialog.__name__)
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def send_inner(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        dialog_id = request.POST.get('dialog_id')
        message = request.POST.get('message').strip()

        if not dialog_id or not message:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        dialog_id = int(dialog_id)
        dialog_info = Dialog.get_dialog_info(dialog_id)

        sender_id = dialog_info["sender_id"]
        receiver_id = dialog_info["receiver_id"]
        user_is_in_black_list = User.user_is_in_black_list(sender_id, receiver_id)

        if user_is_in_black_list != 0: return JsonResponse({'message': Response.WRONG_INPUT.value})

        if receiver_id == cookie_user_id:
            sender_id, receiver_id = receiver_id, sender_id

        result = Dialog._send_inner_in_existing_dialog(dialog_id, sender_id, receiver_id, message, 0)
        User.update_time_of_last_action(cookie_user_id)

        if result:
            return JsonResponse({'message': Response.SUCCESS.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

    @staticmethod
    def send_outer(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(int(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        receiver_id = request.POST.get('receiver_id')
        message = request.POST.get('message').strip()

        if not receiver_id or \
            not message or \
                cookie_user_id == receiver_id:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        receiver_id = int(receiver_id)

        user_is_in_black_list = User.user_is_in_black_list(cookie_user_id, receiver_id)

        if user_is_in_black_list != 0: return JsonResponse({'message': Response.WRONG_INPUT.value})
        User.update_time_of_last_action(cookie_user_id)

        res = Response.UNKNOWN_ERROR.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            dialog_id = cur.execute(f"SELECT id FROM dialog "
                                    f"WHERE senderId={cookie_user_id} AND receiverId={receiver_id} "
                                    f"OR senderId={receiver_id} AND receiverId={cookie_user_id}").fetchall()

            if not len(dialog_id):
                # Создать диалог
                dialog_created = Dialog._create_dialog(cookie_user_id, receiver_id, message)
                if dialog_created:
                    return JsonResponse({'message': Response.SUCCESS.value})
                else:
                    return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
            else:
                # Написать сообщение в существующий диалог
                dialog_id = dialog_id[0][0]
                result = Dialog._send_outer_in_existing_dialog(dialog_id, cookie_user_id, receiver_id, message)

                if result: res = Response.SUCCESS.value
        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.send_outer.__name__)
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def get_dialog_messages(dialog_id: int) -> list:
        result = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            sql = f"SELECT dialog_message.id AS id, userId, text, date, user.nick AS nick, user.avatar AS avatar " \
                  f"FROM dialog_message " \
                  f"INNER JOIN user ON user.id=userId " \
                  f"WHERE dialogId=? " \
                  f"ORDER by date"

            messages = cur.execute(sql, (dialog_id,)).fetchall()

            if not len(messages): raise NoDialogMessages

            result = Dialog._parse_dialog_messages(messages)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Dialog.get_dialog_messages.__name__)
        except NoDialogMessages as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return result

    @staticmethod
    def _parse_dialog_messages(messages: list) -> list:
        result = list()
        for message in messages:
            id = message[0]
            user_id = message[1]
            msg = message[2]
            date = message[3]
            nick = message[4]
            avatar = message[5]
            avatar = User.get_avatar_link(avatar, user_id)

            tmp = dict()
            tmp["id"] = id
            tmp["user_id"] = user_id
            tmp["message"] = Message.tolink(msg)
            tmp["date"] = date
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            result.append(tmp)
        return result


class UserPageLike:
    @staticmethod
    def get_page_likes_count(user_id: int) -> int:
        if not user_id: return  0
        result = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = \
                cur.execute(f"SELECT COUNT(*) FROM user_page_like WHERE userId=?", (user_id,)).fetchall()[0][0]

            result = likes_count
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), UserPageLike.get_page_likes_count.__name__)
        finally:
            con.close()
        return result

    @staticmethod
    def set_page_like(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        user_id = request.POST.get('user_id')

        if not user_id: return JsonResponse({'message': -1})

        user_id = int(user_id)

        User.update_time_of_last_action(cookie_user_id)
        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count_from_user = cur.execute(f"SELECT COUNT(*) FROM user_page_like WHERE userId=? AND likerId=?",
                                                (user_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = UserPageLike.get_page_likes_count(user_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if UserPageLike._update_page_like(user_id, cookie_user_id, insert):
                res = likes_count_total

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), UserPageLike.set_page_like.__name__)
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def _update_page_like(user_id: int, cookie_user_id: int, insert: bool) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO user_page_like(userId,likerId,u_time) VALUES (?,?,?)",
                            (user_id, cookie_user_id, int(time.time())))
            else:
                cur.execute(f"DELETE FROM  user_page_like WHERE userId=? AND likerId=?",
                            (user_id, cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), UserPageLike.__update_page_like.__name__)
            result = False
        finally:
            con.close()
        return result


class WallMessageLike:
    @staticmethod
    def get_wall_message_likes_count(message_id: int) -> int:
        if not message_id: return 0

        result = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = \
                cur.execute(f"SELECT COUNT(*) FROM wall_message_like WHERE messageId=?", (message_id,)).fetchall()[0][0]

            result = likes_count
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.get_wall_message_likes_count.__name__)
        finally:
            con.close()
        return result

    @staticmethod
    def set_wall_message_like(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        message_id = request.POST.get('message_id')

        if not message_id: return JsonResponse({'message': -1})

        message_id = int(message_id)

        User.update_time_of_last_action(cookie_user_id)
        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            message_exists = cur.execute(f"SELECT COUNT(*) FROM wall_message WHERE id=?",
                                         (message_id,)).fetchall()[0][0]

            if not message_exists:  raise MessageDoesNotExists

            likes_count_from_user = \
                cur.execute(f"SELECT COUNT(*) FROM wall_message_like WHERE messageId=? AND likerId=?",
                            (message_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = WallMessageLike.get_wall_message_likes_count(message_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if WallMessageLike._update_wall_message_like(message_id, cookie_user_id, insert):
                res = likes_count_total

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.set_wall_message_like.__name__)
        except MessageDoesNotExists as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def _update_wall_message_like(message_id: int, cookie_user_id: int, insert: bool) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO wall_message_like(messageId,likerId,u_time) VALUES (?,?,?)",
                            (message_id, cookie_user_id, int(time.time())))
            else:
                cur.execute(f"DELETE FROM  wall_message_like WHERE messageId=? AND likerId=?",
                            (message_id, cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.__update_wall_message_like.__name__)
            result = False
        finally:
            con.close()
        return result


class ForumMessageLike:
    @staticmethod
    def get_forum_message_likes_count(message_id: int) -> int:
        if not message_id: return 0

        result = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM forum_message_like WHERE messageId=?",
                            (message_id,)).fetchall()[0][0]

            result = likes_count
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike.get_forum_message_likes_count.__name__)
        finally:
            con.close()
        return result

    @staticmethod
    def set_forum_message_like(request: object) -> JsonResponse:
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        message_id = request.POST.get('message_id')

        if not message_id: return JsonResponse({'message': -1})

        message_id = int(message_id)

        User.update_time_of_last_action(cookie_user_id)

        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            message_exists = cur.execute(f"SELECT COUNT(*) FROM forum_message WHERE id=?",
                                         (message_id,)).fetchall()[0][0]

            if not message_exists: raise MessageDoesNotExists

            likes_count_from_user = \
                cur.execute(f"SELECT COUNT(*) FROM forum_message_like WHERE messageId=? AND likerId=?",
                            (message_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = ForumMessageLike.get_forum_message_likes_count(message_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if ForumMessageLike._update_forum_message_like(message_id, cookie_user_id, insert):
                res = likes_count_total

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike.set_forum_message_like.__name__)
        except MessageDoesNotExists as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def _update_forum_message_like(message_id: int, cookie_user_id: int, insert: bool) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO forum_message_like(messageId,likerId,u_time) VALUES (?,?,?)",
                            (message_id, cookie_user_id, int(time.time())))
            else:
                cur.execute(f"DELETE FROM  forum_message_like WHERE messageId=? AND likerId=?",
                            (message_id, cookie_user_id))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike._update_forum_message_like.__name__)
            result = False
        finally:
            con.close()
        return result


class ForumMainMessageLike:
    @staticmethod
    def get_forum_main_message_likes_count(forum_id: int) -> int:
        if not forum_id: return 0
        result = 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM forum_main_message_like WHERE forumId=?",
                            (forum_id,)).fetchall()[0][0]

            result = likes_count
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMainMessageLike.get_forum_main_message_likes_count.__name__)
        finally:
            con.close()
        return result

    @staticmethod
    def set_forum_main_message_like(request: object) -> JsonResponse:
        if request.session.get("id") and request.POST.get('forum_id'):
            cookie_user_id = int(request.session.get("id"))
            forum_id = int(request.POST.get('forum_id'))
        else:
            return JsonResponse({'message': -1})

        if not forum_id: return JsonResponse({'message': -1})

        User.update_time_of_last_action(cookie_user_id)
        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            forum_exists = cur.execute(f"SELECT COUNT(*) FROM forum WHERE id=?",
                                       (forum_id,)).fetchall()[0][0]

            if not forum_exists: raise NoForumInfo

            likes_count_from_user = \
                cur.execute(f"SELECT COUNT(*) FROM forum_main_message_like WHERE forumId=? AND likerId=?",
                            (forum_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = ForumMainMessageLike.get_forum_main_message_likes_count(forum_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if ForumMainMessageLike._update_forum_main_message_like(forum_id, cookie_user_id, insert):
                res = likes_count_total
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMainMessageLike.set_forum_main_message_like.__name__)
        except NoForumInfo as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def _update_forum_main_message_like(forum_id: int, cookie_user_id: int, insert: bool) -> bool:
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO forum_main_message_like(forumId,likerId,u_time) VALUES (?,?,?)",
                            (forum_id, cookie_user_id, int(time.time())))
            else:
                cur.execute(f"DELETE FROM  forum_main_message_like WHERE forumId=? AND likerId=?",
                            (forum_id, cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.__update_forum_message_like.__name__)
            result = False
        finally:
            con.close()
        return result


class Notice:
    @staticmethod
    def get_notice(cookie_user_id=None) -> list:
        if cookie_user_id:
            cookie_user_id = int(cookie_user_id)
            User.update_time_of_last_action(cookie_user_id)
        result = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            notice = cur.execute(
                f"SELECT id, entityId, type, date FROM notice ORDER by id DESC").fetchall()

            result = Notice._parse_notice(notice)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Notice.get_notice.__name__)
        finally:
            con.close()
        return result

    @staticmethod
    def _parse_notice(notices: list) -> list:
        result = list()
        for notice in notices:
            id = notice[0]
            entity_id = notice[1]
            type = notice[2]
            date = notice[3]

            tmp = dict()
            tmp["id"] = id
            tmp["type"] = type

            if type == NoticeType.SELF_PAGE_MESSAGE.value or \
                    type == NoticeType.OTHER_USER_PAGE_MESSAGE.value:
                wall_message = MessageWall.get_wall_message_by_id(entity_id)
                sender_id = wall_message["sender_id"]
                sender_info = User.get_info(sender_id)
                sender_nick = sender_info["nick"]
                sender_avatar = sender_info["avatar"]

                receiver_id = wall_message["receiver_id"]
                receiver_info = User.get_info(receiver_id)
                receiver_nick = receiver_info["nick"]
                receiver_avatar = receiver_info["avatar"]

                message = wall_message["message"]

                tmp["sender_id"] = sender_id
                tmp["sender_nick"] = sender_nick
                tmp["sender_avatar"] = sender_avatar

                tmp["receiver_id"] = receiver_id
                tmp["receiver_nick"] = receiver_nick
                tmp["receiver_avatar"] = receiver_avatar

                tmp["message"] = message

            if type == NoticeType.CREATE_FORUM.value:
                forum_info = Forum.get_forum_info(entity_id)
                id = forum_info["id"]
                creatorId = forum_info["creator_id"]
                name = forum_info["name"]
                nick = forum_info["nick"]
                avatar = forum_info["avatar"]
                message = forum_info["message"]

                tmp["id"] = id
                tmp["creator_id"] = creatorId
                tmp["name"] = name
                tmp["message"] = Message.tolink(message)
                tmp["date"] = date
                tmp["nick"] = nick
                tmp["avatar"] = avatar

            if type == NoticeType.NEW_USER.value:
                id = entity_id
                user_info = User.get_info(id)
                nick = user_info["nick"]
                avatar = user_info["avatar"]

                tmp["nick"] = nick
                tmp["avatar"] = avatar

            tmp["date"] = date
            result.append(tmp)
        return result


class Superuser:
    @staticmethod
    def auth(request: object) -> int:
        login = request.POST.get('login').strip()
        password = request.POST.get('pass').strip()

        if not len(login) or not len(password):
            return 0

        res = 0
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            result = cur.execute(f"SELECT id, login, password FROM superuser WHERE login='{login}'").fetchall()
            if not len(result): raise NoSuperuserFound

            bd_pass = result[0][2]

            if bd_pass != get_hash(password): raise NoSuperuserFound
            request.session["su"] = login
            res = 1

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.auth.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def get_users() -> list:
        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, is_blocked, avatar FROM user").fetchall()

            res = Superuser._parse_users(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.get_users.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def get_forums() -> list:
        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, name FROM forum ORDER BY date DESC").fetchall()

            res = Superuser._parse_forums(result)

        except sqlite3.Error as error:
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.get_forums.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_forums(forums: list) -> list:
        result = list()
        for forum in forums:
            id = forum[0]
            topic = forum[1]

            tmp = dict()
            tmp["id"] = id
            tmp["topic"] = topic
            result.append(tmp)
        return result

    @staticmethod
    def _parse_users(users: list):
        result = list()
        for user in users:
            id = user[0]
            nick = user[1]
            is_blocked = user[2]
            avatar = user[3]
            avatar = User.get_avatar_link(avatar, id)

            tmp = dict()
            tmp["id"] = id
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_blocked"] = is_blocked
            result.append(tmp)
        return result

    @staticmethod
    def block_user(request: object) -> JsonResponse:
        user_id = request.POST.get("user_id")
        if not user_id: return -1
        user_id = int(user_id)

        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            result = cur.execute(f"SELECT is_blocked FROM user WHERE id={user_id}").fetchall()
            is_blocked = result[0][0]

            if not is_blocked: is_blocked = 1
            else:   is_blocked = 0

            cur.execute(f"UPDATE user SET is_blocked=? WHERE id=?", \
                        (is_blocked, user_id))
            con.commit()
            res = is_blocked
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.block_user.__name__)
        finally:
            con.close()
        return JsonResponse({'message': res})

    @staticmethod
    def delete_forum(request: object) -> JsonResponse:
        forum_id = request.POST.get("forum_id")

        if not forum_id: return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        forum_id = int(forum_id)

        result = Response.SUCCESS.value
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM forum WHERE id=?", (forum_id,))
            cur.execute(f"DELETE FROM notice WHERE entityId=?", (forum_id,))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.delete_forum.__name__)
            result = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': result})

    @staticmethod
    def find_user(request: object) -> JsonResponse:
        user_id = request.POST.get("user_id")
        if not user_id: return -1
        user_id = int(user_id)

        res = -1
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, is_blocked, avatar FROM user WHERE id={user_id}").fetchall()

            if not len(result): raise UserDoesNotExists

            result = result[0]

            lst = list()
            id = result[0]
            nick = result[1]
            is_blocked = result[2]
            avatar = result[3]
            avatar = User.get_avatar_link(avatar, id)

            tmp = dict()
            tmp["id"] = id
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["is_blocked"] = is_blocked
            lst.append(tmp)

            res = json.dumps(lst)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.find_user.__name__)
        except UserDoesNotExists as error:
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return JsonResponse({"message": res})

    @staticmethod
    def find_forum(request: object) -> JsonResponse:
        forum_id = request.POST.get("forum_id")
        if not forum_id: return -1
        forum_id = int(forum_id)

        res = None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, name FROM forum WHERE id={forum_id}").fetchall()

            if not len(result): raise NoForumInfo

            result = result[0]

            lst = list()
            id = result[0]
            topic = result[1]

            tmp = dict()
            tmp["id"] = id
            tmp["topic"] = topic
            lst.append(tmp)
            res = json.dumps(lst)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.find_forum.__name__)
        except NoForumInfo as error:
            print(f"{error.__str__()}")
        finally:
            con.close()
        return JsonResponse({"message": res})

    @staticmethod
    def get_logs():
        res = list()
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, text, type, date FROM log ORDER BY date DESC").fetchall()

            res = Superuser._parse_logs(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), Superuser.get_logs.__name__)
        finally:
            con.close()
        return res

    @staticmethod
    def _parse_logs(logs: list) -> list:
        result = list()
        for log in logs:
            id = log[0]
            message = log[1]
            type = log[2]
            date = log[3]

            tmp = dict()
            tmp["id"] = id
            tmp["message"] = message
            tmp["type"] = type
            tmp["date"] = date
            result.append(tmp)
        return result
