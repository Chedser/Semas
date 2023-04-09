from django.http import JsonResponse
from .logs import *

class UserPageLike:
    @staticmethod
    def get_page_likes_count(user_id):
        if not user_id: return None
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM user_page_like WHERE userId=?", (user_id,)).fetchall()[0][0]

            result = likes_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), UserPageLike.get_page_likes_count.__name__)
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

        User.update_time_of_last_action(cookie_user_id)

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
            Log.write_log(error.__str__(), UserPageLike.set_page_like.__name__)
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
                cur.execute(f"INSERT INTO user_page_like(userId,likerId,u_time) VALUES (?,?,?)",
                            (user_id, cookie_user_id, (int)(time.time())))
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
    def get_wall_message_likes_count(message_id):
        if not message_id: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM wall_message_like WHERE messageId=?", (message_id,)).fetchall()[0][0]

            result = likes_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.get_wall_message_likes_count.__name__)
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def set_wall_message_like(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        message_id = request.POST.get('message_id')

        if not message_id: return JsonResponse({'message': -1})

        message_id = (int)(message_id)

        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            message_exists = cur.execute(f"SELECT COUNT(*) FROM wall_message WHERE id=?",
                        (message_id,)).fetchall()[0][0]

            if not message_exists: return JsonResponse({'message': -1})

            likes_count_from_user = cur.execute(f"SELECT COUNT(*) FROM wall_message_like WHERE messageId=? AND likerId=?",
                                                (message_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = WallMessageLike.get_wall_message_likes_count(message_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if WallMessageLike.__update_wall_message_like(message_id, cookie_user_id, insert):
                return JsonResponse({'message': likes_count_total})
            else:
                return JsonResponse({'message': -1})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), WallMessageLike.set_wall_message_like.__name__)
            return JsonResponse({'message': -1})
        finally:
            con.close()

    @staticmethod
    def __update_wall_message_like(message_id, cookie_user_id, insert):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO wall_message_like(messageId,likerId,u_time) VALUES (?,?,?)",
                            (message_id, cookie_user_id, (int)(time.time())))
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
    def get_forum_message_likes_count(message_id):
        if not message_id: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM forum_message_like WHERE messageId=?", (message_id,)).fetchall()[0][0]

            result = likes_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike.get_forum_message_likes_count.__name__)
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def set_forum_message_like(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        message_id = request.POST.get('message_id')

        if not message_id: return JsonResponse({'message': -1})

        message_id = (int)(message_id)

        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            message_exists = cur.execute(f"SELECT COUNT(*) FROM forum_message WHERE id=?",
                        (message_id,)).fetchall()[0][0]

            if not message_exists: return JsonResponse({'message': -1})

            likes_count_from_user = cur.execute(f"SELECT COUNT(*) FROM forum_message_like WHERE messageId=? AND likerId=?",
                                                (message_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = ForumMessageLike.get_forum_message_likes_count(message_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if ForumMessageLike.__update_forum_message_like(message_id, cookie_user_id, insert):
                return JsonResponse({'message': likes_count_total})
            else:
                return JsonResponse({'message': -1})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike.set_forum_message_like.__name__)
            return JsonResponse({'message': -1})
        finally:
            con.close()

    @staticmethod
    def __update_forum_message_like(message_id, cookie_user_id, insert):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO forum_message_like(messageId,likerId,u_time) VALUES (?,?,?)",
                            (message_id, cookie_user_id, (int)(time.time())))
            else:
                cur.execute(f"DELETE FROM  forum_message_like WHERE messageId=? AND likerId=?",
                            (message_id, cookie_user_id))
            con.commit()

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMessageLike.__update_forum_message_like.__name__)
            result = False
        finally:
            con.close()
        return result

class ForumMainMessageLike:
    @staticmethod
    def get_forum_main_message_likes_count(forum_id):
        if not forum_id: return None

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            likes_count = cur.execute(f"SELECT COUNT(*) FROM forum_main_message_like WHERE forumId=?", (forum_id,)).fetchall()[0][0]

            result = likes_count

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMainMessageLike.get_forum_main_message_likes_count.__name__)
            result = None
        finally:
            con.close()
        return result

    @staticmethod
    def set_forum_main_message_like(request):
        if request.session.get("id"):
            cookie_user_id = int(request.session.get("id"))
        else:
            return JsonResponse({'message': -1})

        forum_id = request.POST.get('forum_id')

        if not forum_id: return JsonResponse({'message': -1})

        forum_id = (int)(forum_id)

        User.update_time_of_last_action(cookie_user_id)

        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            forum_exists = cur.execute(f"SELECT COUNT(*) FROM forum WHERE id=?",
                        (forum_id,)).fetchall()[0][0]

            if not forum_exists: return JsonResponse({'message': -1})

            likes_count_from_user = cur.execute(f"SELECT COUNT(*) FROM forum_main_message_like WHERE forumId=? AND likerId=?",
                                                (forum_id, cookie_user_id)).fetchall()[0][0]
            likes_count_total = ForumMainMessageLike.get_forum_main_message_likes_count(forum_id)
            insert = True
            if likes_count_from_user:
                likes_count_total = likes_count_total - 1
                insert = False
            else:
                likes_count_total = likes_count_total + 1

            if ForumMainMessageLike.__update_forum_main_message_like(forum_id, cookie_user_id, insert):
                return JsonResponse({'message': likes_count_total})
            else:
                return JsonResponse({'message': -1})

        except sqlite3.Error as error:
            con.rollback()
            print(f"DataBase error {error.__str__()}")
            Log.write_log(error.__str__(), ForumMainMessageLike.set_forum_main_message_like.__name__)
            return JsonResponse({'message': -1})
        finally:
            con.close()

    @staticmethod
    def __update_forum_main_message_like(forum_id, cookie_user_id, insert):
        result = True
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()

            if insert:
                cur.execute(f"INSERT INTO forum_main_message_like(forumId,likerId,u_time) VALUES (?,?,?)",
                            (forum_id, cookie_user_id, (int)(time.time())))
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