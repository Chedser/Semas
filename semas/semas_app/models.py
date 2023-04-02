import sqlite3
import json
import time
from .functions import *
from .enums import *
from django.http import JsonResponse
from settings import *
import os

class Message:
    def tolink(txt):
        import re
        import html
        pattern1 = r'\b((?:https?://)(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        pattern2 = r'\b((?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        result = html.escape(txt)
        if re.findall(pattern1, result):
            result = re.sub(pattern1, r'<a href=\1 target=_blank>\1</a>', result)
        elif re.findall(pattern2, result):
            result = re.sub(pattern2, r'<a href=//\1 target=_blank>\1</a>', result)
        return result

    def truncate(txt, count):
        if len(txt) <= count:
            return txt
        else:
            return txt[:count] + "..."


class Auth:
    @staticmethod
    def auth(request):
        login = request.POST.get('login').strip()
        password = request.POST.get('pass').strip()

        if len(login) == 0 or len(password) == 0:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        user_id = 0

        if "admin" in login.lower() or \
                "админ" in login.lower():
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            result = cur.execute(f"SELECT id, login, password FROM user WHERE login='{login}'").fetchall()
            if len(result) == 0:
                con.close()
                return JsonResponse({'message': Response.WRONG_USER_OR_PASSWORD.value})

            is_blocked = User.get_info((int)(result[0][0]))["is_blocked"]

            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})

            bd_pass = result[0][2]

            if bd_pass != get_hash(password):
                con.close()
                return JsonResponse({'message': Response.WRONG_USER_OR_PASSWORD.value})
            user_id = result[0][0]

            request.session["id"] = user_id

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': Response.SUCCESS.value, 'id': user_id})


class Reg:
    def reg(request):
        login = request.POST.get('login').strip()
        nick = request.POST.get('nick').strip()
        sex = request.POST.get('sex')
        password = request.POST.get('pass').strip()

        if len(login) == 0 or \
                len(nick) == 0 or \
                len(sex) == 0 or \
                ("admin" in login.lower()) or \
                ("админ" in login.lower()):
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        response = Response.SUCCESS.value

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM user WHERE login='{login}' OR nick='{nick}'").fetchall()
            if len(result) != 0:
                response = Response.USER_EXISTS.value
            else:
                hash = get_hash(password)

                cur.execute("INSERT INTO user (login,password,nick,sex,time_of_change_info," \
                            " time_of_last_action) \
                 VALUES (?,?,?,?,?,?)", (login, hash, nick, sex, (int)(time.time()), (int)(time.time())))
                con.commit()
                last_id = cur.execute(f"SELECT MAX(id) FROM user WHERE login='{login}'").fetchall()

                os.mkdir(f"semas_app/static/images/avatars/{last_id[0][0]}")

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            response = Response.UNKNOWN_ERROR.value
        finally:
            con.close()
        return JsonResponse({'message': response})


class MessageWall:

    def send_wall_message(request):
        message = request.POST.get('message').strip()
        receiver_id = request.POST.get('receiver_id')

        if len(message) == 0 or \
                not receiver_id:
            return JsonResponse({'message': Response.WRONG_USER_OR_PASSWORD.value})

        receiver_id = int(request.POST.get('receiver_id'))

        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            cur.execute("INSERT INTO wall_message (senderId, receiverId, message, timestamp)\
                  VALUES (?,?,?,?)", (cookie_user_id, receiver_id, message, (int)(time.time())))
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    def delete_wall_message(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
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

        user_id = (int)(user_id)
        sender_id = (int)(sender_id)
        message_id = (int)(message_id)

        User.update_time_of_last_action(cookie_user_id)

        if cookie_user_id == user_id or cookie_user_id == sender_id:
            try:
                con = sqlite3.connect(DB_NAME)

                cur = con.cursor()

                cur.execute(f"DELETE FROM wall_message WHERE id=?", (message_id,))
                con.commit()
                return JsonResponse({'message': Response.SUCCESS.value})
            except sqlite3.Error as error:
                con.rollback()
                print(f"DataBase error {error.__str__()}")
                return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
            finally:
                con.close()
        else:
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})

    def get_wall_messages(user_id):
        if not user_id: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT wall_message.id AS id, senderId, message, user.nick AS nick, user.avatar AS avatar, date FROM wall_message \
             INNER JOIN user ON wall_message.senderId=user.id WHERE receiverId={user_id} ORDER BY date DESC").fetchall()
            return MessageWall.__parse_wall_messages(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return None
        finally:
            con.close()

    def __parse_wall_messages(wall_messages):
        result = list()

        for wall_message in wall_messages:
            id = wall_message[0]
            sender_id = wall_message[1]
            message = wall_message[2]
            nick = wall_message[3]
            avatar = wall_message[4]
            avatar = User.get_avatar_link(avatar, sender_id)
            date = wall_message[5]
            tmp = dict()
            tmp["id"] = id
            tmp["sender_id"] = sender_id
            tmp["message"] = Message.tolink(message)
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            tmp["date"] = date
            result.append(tmp)
        return result


class User:
    def get_info(user_id):
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, sex, is_blocked, time_of_last_action, avatar \
                FROM user WHERE id={user_id}").fetchall()
            if len(result) == 0:
                return None
            return User.__parse_user_info(result[0])

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return None
        finally:
            con.close()
        return None

    def __parse_user_info(user_info):
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
        result["is_online"] = User.__is_online(time_of_last_action)
        result["avatar"] = User.get_avatar_link(avatar, user_id)
        return result

    def get_avatar_link(avatar, user_id):
        if not avatar:
            link = f"images/default.png"
        else:
            link = f"images/avatars/{user_id}/{avatar}"
        return link

    def __is_online(time_of_last_action):
        return (((int)(time.time()) - time_of_last_action) < 300)

    @staticmethod
    def get_blocked_users(cookie_user_id):
        if not cookie_user_id: return None
        cookie_user_id = int(cookie_user_id)
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT user.id AS id, user.nick AS nick, avatar FROM black_list "
                                 f"INNER JOIN user ON user.id = black_list.user2 "
                                 f"WHERE user1={cookie_user_id}").fetchall()

            return User.__parse_blocked_users(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    @staticmethod
    def user_is_in_black_list(user_id, cookie_user_id):
        if not user_id or not cookie_user_id: return
        if user_id == cookie_user_id: return -1

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) FROM black_list WHERE (user1={user_id} AND "
                                 f"user2={cookie_user_id}) OR "
                                 f"(user1={cookie_user_id} AND user2={user_id})").fetchall()[0][0]

            return result

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    @staticmethod
    def __parse_blocked_users(users):
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
    def find_user_for_block(request):
        user_id = request.POST.get("user_id")
        cookie_user_id = request.session.get("id")
        if not user_id or not cookie_user_id: return JsonResponse({"message": 1})
        user_id = int(user_id)
        cookie_user_id = int(cookie_user_id)

        if cookie_user_id == user_id:
            return JsonResponse({"message": 2})

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, is_blocked, avatar FROM user WHERE id={user_id}").fetchall()

            if len(result) == 0: return JsonResponse({"message": 1})

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

            return JsonResponse({"message": json.dumps(lst)})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({"message": 1})
        finally:
            con.close()

    @staticmethod
    def block_user(request):
        user_id = request.POST.get("user_id")
        cookie_user_id = request.session.get("id")
        if not user_id or not cookie_user_id: return JsonResponse({"message": 1})
        user_id = int(user_id)
        cookie_user_id = int(cookie_user_id)

        if cookie_user_id == user_id:
            return JsonResponse({"message": 2})

        try:

            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            result = cur.execute(f"SELECT COUNT(*) FROM black_list WHERE user1={cookie_user_id} "
                                 f"AND user2={user_id}").fetchall()[0][0]

            is_blocked = 0

            if not result:
                cur.execute(f"INSERT INTO black_list(user1, user2, timestamp) VALUES "
                            f"(?,?,?)", \
                            (cookie_user_id, user_id, int(time.time())))
                is_blocked = 1
            else:
                cur.execute(f"DELETE FROM black_list WHERE user1=? AND user2=?", \
                            (cookie_user_id, user_id))

            con.commit()
            return JsonResponse({'message': is_blocked})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': 2})

    def update_time_of_last_action(cookie_user_id):
        if not cookie_user_id: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"UPDATE user SET  time_of_last_action=? WHERE id=?", ((int)(time.time()), cookie_user_id))
            con.commit()
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()


class File:
    # расширения файлов, которые разрешено загружать
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __allowed_file(content_type):
        return content_type.split('/')[1] in File.ALLOWED_EXTENSIONS

    def __get_extension(content_type):
        return content_type.split('/')[1]

    def __rename_file(content_type):
        return f"{int(time.time())}.{File.__get_extension(content_type)}"

    def __upload_file(file, url):
        with open(url, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    def change_avatar(request):
        MAX_FILE_SIZE = 3 * 10 ** 6

        avatar = request.FILES.get("avatar")
        if request.session.get("id") and \
                request.POST.get("MAX_FILE_SIZE") and \
                avatar:
            max_file_size_client = (int)(request.POST.get("MAX_FILE_SIZE"))
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        if max_file_size_client > MAX_FILE_SIZE or \
                not avatar or \
                not File.__allowed_file(avatar.content_type):
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        new_file_name = File.__rename_file(avatar.content_type)

        url = f'./semas_app/static/images/avatars/{cookie_user_id}/{new_file_name}'

        File.__upload_file(avatar, url)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"UPDATE user SET avatar='{new_file_name}' WHERE id={cookie_user_id}")
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        finally:
            con.close()

class Friend:
    def get_friend_requests_count(cookie_user_id):
        if cookie_user_id is None: return 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) \
                                            FROM friend_request WHERE friend2={(int)(cookie_user_id)}").fetchall()[0][0]
            con.commit()
            return result
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def get_friends_count(cookie_user):
        if cookie_user is None: return 0
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT COUNT(*) \
                                                FROM friend WHERE friend1={(int)(cookie_user)} OR friend2={cookie_user}").fetchall()[
                0][0]
            con.commit()
            return result
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def get_friend_requests(cookie_user):
        if cookie_user is None: return 0

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, user.nick AS nick, user.avatar AS avatar \
                                     FROM friend_request INNER JOIN user ON user.id=friend1 \
                                      WHERE friend2={(int)(cookie_user)}").fetchall()
            if len(result) == 0: return result
            return Friend.__parse_friend_requests(result, cookie_user)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def get_friend_request_status(cookie_user_id: int, user_id):
        if not cookie_user_id: return FriendStatus.UNAUTHED.value
        if cookie_user_id == user_id: return FriendStatus.SAME_PAGE.value  # Сидим на своей странице
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result_friends = cur.execute(f"SELECT friend1, friend2 FROM friend WHERE (friend1={(int)(cookie_user_id)} \
                 AND friend2={user_id}) OR (friend1={(int)(user_id)} AND friend2={cookie_user_id})").fetchall()
            result_request = cur.execute(
                f"SELECT friend1, friend2 FROM friend_request WHERE (friend1={(int)(cookie_user_id)} \
                             AND friend2={user_id}) OR (friend1={(int)(user_id)} AND friend2={cookie_user_id})").fetchall()
            if len(result_friends) == 0 and len(
                    result_request) == 0: return FriendStatus.NOT_FRIEND.value  # В друзьях нет в заявках тоже
            if len(result_friends) == 0 and len(result_request) == 1:  # В друзьях нет в заявках есть
                if result_request[0][0] == cookie_user_id:
                    return FriendStatus.CANCEL_REQUEST.value  # Заявку отправил куки юзер. Отменить заявку
                else:
                    return FriendStatus.DECLINE_REQUEST.value  # Заявку оправил тот, у которого сидим. Отклонить
            if len(result_friends) == 1 and len(result_request) == 0: return FriendStatus.IS_FRIEND.value  # Друзья

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return FriendStatus.UNKNOWN_ERROR.value
        finally:
            con.close()

    def send_friend_request(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = (int)(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result_friends = cur.execute(f"SELECT friend1, friend2 FROM friend WHERE (friend1={(cookie_user_id)} \
                     AND friend2={user_id}) OR (friend1={(user_id)} AND friend2={cookie_user_id})").fetchall()
            result_request = cur.execute(
                f"SELECT friend1, friend2 FROM friend_request WHERE (friend1={cookie_user_id} \
                                 AND friend2={user_id}) OR (friend1={user_id} AND friend2={cookie_user_id})").fetchall()
            if len(result_friends) == 0 and len(result_request) == 0:  # В друзьях нет в заявках тоже
                cur.execute("INSERT INTO friend_request (friend1, friend2, timestamp) \
                        VALUES (?,?,?)", (cookie_user_id, user_id, (int)(time.time())))
                con.commit()
                return JsonResponse({'message': Response.SUCCESS.value})
            else:
                return JsonResponse({'message': Response.WRONG_INPUT.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        finally:
            con.close()
        return JsonResponse({'message': Response.WRONG_INPUT.value})

    def cancel_friend_request(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = (int)(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend_request WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        finally:
            con.close()

    def accept_friend_request(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = (int)(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend_request WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()
            cur.execute("INSERT INTO friend (friend1, friend2, timestamp) \
                               VALUES (?,?,?)", (cookie_user_id, user_id, (int)(time.time())))
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        finally:
            con.close()

    def delete_friend(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = request.POST.get('user_id')
        if not user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})
        user_id = (int)(user_id)

        if cookie_user_id == user_id:  # Самому себе нельзя отправлять запрос
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute(f"DELETE FROM friend WHERE (friend1={cookie_user_id} AND friend2={user_id}) \
                 OR (friend1={user_id} AND friend2={cookie_user_id})")
            con.commit()

            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def get_friends(cookie_user):
        if not cookie_user: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, friend2 FROM friend \
                 WHERE friend1={(int)(cookie_user)} OR friend2={(int)(cookie_user)}").fetchall()
            if len(result) == 0: return {}

            total = list()
            for user in result:
                current_user = list()
                if user[0] != cookie_user:
                    current_user.append(user[0])
                elif user[1] != cookie_user:
                    current_user.append(user[1])
                result2 = cur.execute(f"SELECT nick, avatar FROM user \
                                 WHERE id={current_user[0]}").fetchall()
                tmp = dict()
                tmp["id"] = current_user[0]
                tmp["nick"] = result2[0][0]
                avatar = User.get_avatar_link(result2[0][1], current_user[0])
                tmp["avatar"] = avatar
                total.append(tmp)

            return total
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def get_friends_user_page(cookie_user, limit):
        if not cookie_user: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT friend1, friend2 FROM friend \
                        WHERE friend1={(int)(cookie_user)} OR friend2={(int)(cookie_user)} LIMIT {limit}").fetchall()
            if len(result) == 0: return {}

            total = list()
            for user in result:
                current_user = list()
                if user[0] != cookie_user:
                    current_user.append(user[0])
                elif user[1] != cookie_user:
                    current_user.append(user[1])
                result2 = cur.execute(f"SELECT nick, avatar FROM user \
                                        WHERE id={current_user[0]}").fetchall()
                tmp = dict()
                tmp["id"] = current_user[0]
                tmp["nick"] = result2[0][0]
                avatar = User.get_avatar_link(result2[0][1], current_user[0])
                tmp["avatar"] = avatar
                total.append(tmp)

            return total
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    def __parse_friend_requests(friend_requests, cookie_user_id):
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
    def create_forum(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        message = request.POST.get('message').strip()
        topic = request.POST.get('topic').strip()

        if len(message) == 0 or len(topic) == 0:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            forum_count = cur.execute(f"SELECT COUNT(*) FROM forum WHERE name_lower='{topic.lower()}'").fetchall()[0][0]
            if forum_count > 0: return JsonResponse({'message': Response.UNKNOWN_ERROR.value})

            cur.execute("INSERT INTO forum (creatorId, name, name_lower, message, timestamp)\
                          VALUES (?,?,?,?,?)", (cookie_user_id, topic, topic.lower(), message, (int)(time.time())))
            con.commit()

            """lastrowid = cur.lastrowid

            cur.execute("INSERT INTO forum_message (forumId, senderId, message, timestamp)\
                                     VALUES (?,?,?,?)", (lastrowid, cookie_user_id, message, (int)(time.time())))
            con.commit() """

            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    @staticmethod
    def get_forums():
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            result = cur.execute("SELECT forum.id AS id, creatorId, name, message, date, user.avatar AS avatar, user.nick AS nick \
             FROM forum INNER JOIN user ON forum.creatorId=user.id ORDER BY date DESC").fetchall()

            return Forum.__parse_forums(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    def __parse_forums(forums):
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
            tmp = dict()
            tmp["id"] = id
            tmp["creator_id"] = creatorId
            tmp["name"] = forum_name
            tmp["message"] = Message.truncate(message, 256)
            tmp["date"] = date
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            result.append(tmp)
        return result

    def __parse_forum_info(forum):
        id = forum[0]
        creatorId = forum[1]
        forum_name = forum[2]
        message = forum[3]
        date = forum[4]
        avatar = forum[5]
        avatar = User.get_avatar_link(avatar, creatorId)
        nick = forum[6]
        res = dict()
        res["id"] = id
        res["creator_id"] = creatorId
        res["name"] = forum_name
        res["message"] = Message.tolink(message)
        res["date"] = date
        res["nick"] = nick
        res["avatar"] = avatar
        return res

    def __parse_messages(messages):
        result = list()
        for message in messages:
            id = message[0]
            senderId = message[1]
            txt = message[2]
            date = message[3]
            avatar = message[4]
            nick = message[5]
            avatar = User.get_avatar_link(avatar, senderId)
            tmp = dict()

            tmp["id"] = id
            tmp["sender_id"] = senderId
            tmp["message"] = Message.tolink(txt)
            tmp["date"] = date
            tmp["nick"] = nick
            tmp["avatar"] = avatar
            result.append(tmp)
        return result

    def get_messages(id):
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            result = cur.execute(f"SELECT forum_message.id AS id, senderId, message, date, user.avatar AS avatar, user.nick AS nick \
                 FROM forum_message INNER JOIN user ON forum_message.senderId=user.id WHERE forumId={id}").fetchall()

            if not len(result): return None

            return Forum.__parse_messages(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    def send_message(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        message = request.POST.get('message').strip()
        forum_id = request.POST.get('id')

        if not message or not forum_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            cur.execute("INSERT INTO forum_message (senderId, forumId, message, timestamp)\
                                     VALUES (?,?,?,?)",
                        (cookie_user_id, forum_id, message, (int)(time.time())))
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    def get_forum_info(id):
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            result = cur.execute(f"SELECT forum.id AS id,  creatorId, name, message, date, user.avatar AS avatar, user.nick AS nick \
                    FROM forum INNER JOIN user ON forum.creatorId=user.id WHERE forum.id={id}").fetchall()
            if not len(result): return None
            result = result[0]
            return Forum.__parse_forum_info(result)
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    def delete_message(request):
        if request.session.get("id"):
            cookie_user_id = (int)(request.session.get("id"))
            is_blocked = User.get_info(cookie_user_id)["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.WRONG_INPUT.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        message_id = request.POST.get("message_id")
        sender_id = request.POST.get("sender_id")

        if not message_id or not sender_id:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        sender_id = (int)(sender_id)
        message_id = (int)(message_id)

        if sender_id != cookie_user_id: return JsonResponse({'message': Response.WRONG_INPUT.value})

        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            cur.execute(f"DELETE FROM forum_message WHERE id=?", (message_id,))
            con.commit()
            return JsonResponse({'message': Response.SUCCESS.value})
        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()


class Dialog:
    @staticmethod
    def __create_dialog(sender_id, receiver_id, message):
        is_blocked_sender_id = User.get_info(sender_id)["is_blocked"]
        is_blocked_receiver_id = User.get_info(receiver_id)["is_blocked"]
        if is_blocked_sender_id or is_blocked_receiver_id : return False
        user_is_in_black_list = User.user_is_in_black_list(is_blocked_sender_id, is_blocked_receiver_id)
        if user_is_in_black_list: return False
        result = True
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            cur.execute("INSERT INTO dialog (senderId, receiverId, last_message, timestamp)\
                                     VALUES (?,?,?,?)",
                        (sender_id, receiver_id, message, (int)(time.time())))
            con.commit()

            lastrowid = cur.lastrowid

            cur.execute("INSERT INTO dialog_message (userId, dialogId, message, timestamp)\
                                                 VALUES (?,?,?,?)",
                        (sender_id, lastrowid, message, (int)(time.time())))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def get_active_dialogs_count(cookie_user_id):
        if not cookie_user_id: return None
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            dialogs_count = cur.execute(f"SELECT COUNT(*)  FROM dialog"
                                        f" WHERE receiverId={cookie_user_id} AND is_readen=0").fetchall()[0][0]
            return dialogs_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return None

    @staticmethod
    def get_dialogs_count(cookie_user_id):
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            dialogs_count = cur.execute(f"SELECT COUNT(*)  FROM dialog"
                                        f" WHERE senderId={cookie_user_id} OR  receiverId={cookie_user_id}").fetchall()[
                0][0]
            return dialogs_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return None

    @staticmethod
    def __send_outer_in_existing_dialog(dialog_id, sender_id, receiver_id, message):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET senderId=?, receiverId=?, last_message=?, is_readen=0, timestamp=? WHERE id=?",
                (sender_id, receiver_id, message, (int)(time.time()), dialog_id))
            con.commit()
            cur.execute("INSERT INTO dialog_message (userId, dialogId, message, timestamp)\
                                                         VALUES (?,?,?,?)",
                        (sender_id, dialog_id, message, (int)(time.time())))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def get_dialog_info(dialog_id):
        result = dict()
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            dialog = cur.execute(
                f"SELECT id, senderId, receiverId, is_readen, date FROM dialog WHERE id={dialog_id}").fetchall()
            if not dialog:
                return None
            else:
                result["id"] = dialog[0][0]
                result["sender_id"] = dialog[0][1]
                result["receiver_id"] = dialog[0][2]
                result["is_readen"] = dialog[0][3]
                result["date"] = dialog[0][4]
                return result

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def get_dialog_opponent_info(cookie_user_id, dialog_id):
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            dialog = cur.execute(
                f"SELECT senderId, receiverId FROM dialog WHERE id={dialog_id}").fetchall()[
                0]

            if not len(dialog):
                return None
            else:
                sender_id = dialog[0]
                receiver_id = dialog[1]
                opponent_id = receiver_id

                if sender_id != cookie_user_id:
                    opponent_id = sender_id

                user_info = User.get_info(opponent_id)

                return user_info

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def update_status(cookie_user_id, dialog_id):
        dialog_info = Dialog.get_dialog_info(dialog_id)
        receiver_id = dialog_info["receiver_id"]

        if receiver_id != cookie_user_id: return

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET is_readen=1, timestamp=? WHERE id=?",
                ((int)(time.time()), dialog_id))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    # ДОДЕЛАТЬ
    @staticmethod
    def get_dialogs(cookie_user_id):

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=0 " \
                  "ORDER by timestamp DESC"

            dialogs_not_readen = cur.execute(sql).fetchall()

            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=1 " \
                  "ORDER by timestamp DESC"

            dialogs_readen = cur.execute(sql).fetchall()

            sql = f"SELECT id, senderId, receiverId, last_message, is_readen, " \
                  f"date FROM dialog WHERE senderId={cookie_user_id} " \
                  "ORDER by timestamp DESC"

            dialogs_sender = cur.execute(sql).fetchall()

             # sql = f"SELECT id, senderId, receiverId, last_message, is_readen," \
            #f"date, timestamp FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=0 " \
            #f"UNION " \
            #f"SELECT id, senderId, receiverId, last_message, is_readen, " \
            #f"date, timestamp FROM dialog WHERE receiverId={cookie_user_id} AND is_readen=1 " \
            #f"UNION " \
            #f"SELECT id, senderId, receiverId, last_message, is_readen, " \
            #f"date, timestamp FROM dialog WHERE senderId={cookie_user_id} " \
            #f"ORDER BY timestamp DESC"

            dialogs = dialogs_not_readen + dialogs_readen + dialogs_sender

            if not len(dialogs):
                return None

            result = Dialog.__parse_dialogs(dialogs, cookie_user_id)
            print(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = None
        finally:
            con.close()
        return result

    def __parse_dialogs(dialogs, cookie_user_id):
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
    def __send_inner_in_existing_dialog(dialog_id, sender_id, receiver_id, message, is_readen):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            cur.execute(
                f"UPDATE dialog SET senderId=?, receiverId=?, last_message=?, is_readen=?, timestamp=? WHERE id=?",
                (sender_id, receiver_id, message, is_readen, (int)(time.time()), dialog_id))
            con.commit()
            cur.execute("INSERT INTO dialog_message (userId, dialogId, message, timestamp)\
                                                            VALUES (?,?,?,?)",
                        (sender_id, dialog_id, message, (int)(time.time())))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = False
        finally:
            con.close()
        return result

    @staticmethod
    def send_inner(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
            if is_blocked: return JsonResponse({'message': Response.USER_IS_BLOCKED.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        dialog_id = request.POST.get('dialog_id')
        message = request.POST.get('message').strip()

        if not dialog_id or \
                not message:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

        dialog_id = int(dialog_id)

        dialog_info = Dialog.get_dialog_info(dialog_id)

        sender_id = dialog_info["sender_id"]
        receiver_id = dialog_info["receiver_id"]
        user_is_in_black_list = User.user_is_in_black_list(sender_id, receiver_id)

        if user_is_in_black_list != 0: return JsonResponse({'message': Response.WRONG_INPUT.value})

        if receiver_id == cookie_user_id:
            sender_id, receiver_id = receiver_id, sender_id

        result = Dialog.__send_inner_in_existing_dialog(dialog_id, sender_id, receiver_id, message, 0)

        if result:
            return JsonResponse({'message': Response.SUCCESS.value})
        else:
            return JsonResponse({'message': Response.WRONG_INPUT.value})

    @staticmethod
    def send_outer(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
            is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
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

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            dialog_id = cur.execute(f"SELECT id FROM dialog "
                                    f"WHERE senderId={cookie_user_id} AND receiverId={receiver_id} "
                                    f"OR senderId={receiver_id} AND receiverId={cookie_user_id}").fetchall()

            if not len(dialog_id):
                # Создать диалог
                dialog_created = Dialog.__create_dialog(cookie_user_id, receiver_id, message)
                if dialog_created:
                    return JsonResponse({'message': Response.SUCCESS.value})
                else:
                    return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
            else:
                # Написать сообщение в существующий диалог
                dialog_id = dialog_id[0][0]
                Dialog.__send_outer_in_existing_dialog(dialog_id, cookie_user_id, receiver_id, message)
                dialog_info = Dialog.get_dialog_info(dialog_id)
                is_readen = dialog_info["is_readen"]

                return JsonResponse({'message': Response.UNKNOWN_ERROR.value})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': Response.UNKNOWN_ERROR.value})
        finally:
            con.close()

    @staticmethod
    def get_dialog_messages(dialog_id):
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            sql = f"SELECT dialog_message.id AS id, userId, message, date, user.nick AS nick, user.avatar AS avatar " \
                  f"FROM dialog_message " \
                  f"INNER JOIN user ON user.id=userId " \
                  f"WHERE dialogId={dialog_id} " \
                  f"ORDER by date"

            messages = cur.execute(sql).fetchall()

            if not len(messages):
                return None

            result = Dialog.__parse_dialog_messages(messages)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = None
        finally:
            con.close()
        return result

    def __parse_dialog_messages(messages):
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
    def get_page_likes_count(user_id):
        if not user_id: return None
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            likes_count = cur.execute(f"SELECT COUNT(*) FROM user_page_like WHERE userId=?", (user_id,)).fetchall()[0][
                0]

            result = likes_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def set_page_like(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        user_id = request.POST.get('user_id')

        if not user_id: return JsonResponse({'message': -1})

        user_id = (int)(user_id)

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

            if UserPageLike.__update_page_like(user_id, cookie_user_id, insert):
                return JsonResponse({'message': likes_count_total})
            else:
                return JsonResponse({'message': -1})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({'message': -1})
        finally:
            con.close()

    @staticmethod
    def __update_page_like(user_id, cookie_user_id, insert):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO user_page_like(userId,likerId,timestamp) VALUES (?,?,?)",
                            (user_id, cookie_user_id, (int)(time.time())))
            else:
                cur.execute(f"DELETE FROM  user_page_like WHERE userId=? AND likerId=?",
                            (user_id, cookie_user_id))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            result = False
        finally:
            con.close()
        return result

class Superuser:

    @staticmethod
    def auth(request):
        login = request.POST.get('login').strip()
        password = request.POST.get('pass').strip()

        if len(login) == 0 or len(password) == 0:
            return 0

        try:
            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()
            result = cur.execute(f"SELECT id, login, password FROM superuser WHERE login='{login}'").fetchall()
            if len(result) == 0:
                con.close()
                return 0

            bd_pass = result[0][2]

            if bd_pass != get_hash(password):
                con.close()
                return 0

            return 1

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return 0
        finally:
            con.close()

    @staticmethod
    def get_users():
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, is_blocked, avatar FROM user").fetchall()

            return Superuser.__parse_users(result)

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()

    @staticmethod
    def __parse_users(users):
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
    def block_user(request):
        user_id = request.POST.get("user_id")
        if not user_id: return -1
        user_id = int(user_id)

        try:

            con = sqlite3.connect(DB_NAME)

            cur = con.cursor()

            result = cur.execute(f"SELECT is_blocked FROM user WHERE id={user_id}").fetchall()
            is_blocked = result[0][0]

            if is_blocked == 0:
                is_blocked = 1
            else:
                is_blocked = 0

            cur.execute(f"UPDATE user SET is_blocked=? WHERE id=?", \
                        (is_blocked, user_id))
            con.commit()
            return JsonResponse({'message': is_blocked})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
        finally:
            con.close()
        return JsonResponse({'message': 2})

    @staticmethod
    def find_user(request):
        user_id = request.POST.get("user_id")
        if not user_id: return -1
        user_id = int(user_id)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute(f"SELECT id, nick, is_blocked, avatar FROM user WHERE id={user_id}").fetchall()

            if len(result) == 0: return JsonResponse({"message": -1})

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

            return JsonResponse({"message": json.dumps(lst)})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            return JsonResponse({"message": -1})
        finally:
            con.close()
