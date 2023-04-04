from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import *
from django.views.decorators.cache import never_cache

@never_cache
def index(request):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>", status_code=404)
    if request.session.get("id"):
        cookie_user_id = int(request.session.get("id"))
        return redirect(f"user/{cookie_user_id}")
    return render(request, "index.html")

@never_cache
def user(request, id):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    is_authed_user = False
    is_login_user_page = False
    user_info = User.get_info(id)

    if (not id) or (not user_info): return HttpResponse("<h1>Страница не найдена: 404</h1>")

    cookie_user_id = None
    friend_status = None
    friend_requests_count = None
    active_dialogs_count = None
    user_is_in_black_list = None
    if request.session.get("id") and id:  # Пользователь авторизован и id передано в качестве аргумента
        cookie_user_id = int(request.session.get("id"))
        is_authed_user = True
        User.update_time_of_last_action(cookie_user_id)
        friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)
        active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
        if id != cookie_user_id:
            user_is_in_black_list = User.user_is_in_black_list(id, cookie_user_id)
        else:
            user_is_in_black_list = -1
        friend_status = Friend.get_friend_request_status(cookie_user_id, id)
        if user_info["is_blocked"]:
            friend_status = FriendStatus.UNAUTHED.value
        if cookie_user_id == id:  # И сидит на своей странице
            is_login_user_page = True

    wall_messages = MessageWall.get_wall_messages(id)
    friends = Friend.get_friends_user_page(id, 8)
    page_likes_count = UserPageLike.get_page_likes_count(id)

    data = {"cookie_user_id": cookie_user_id, "user_id": id, "is_login_user_page": is_login_user_page, \
            "is_authed_user": is_authed_user, "wall_messages": wall_messages, "user_info": user_info, \
            "friend_status": friend_status, "friend_requests_count": friend_requests_count, "friends": friends, \
            "friends_count": len(friends), "active_dialogs_count": active_dialogs_count,
            "page_likes_count": page_likes_count, "user_is_in_black_list": user_is_in_black_list}

    return render(request, "user.html", context=data)


def su(request):
    if request.method != "GET": return redirect("/")
    return render(request, "su.html")


def admin(request):
    if not request.session.get("su") or request.method != "GET": return redirect("/su")
    users = Superuser.get_users()
    data = {"users": users, "users_count": len(users)}
    return render(request, "admin.html", context=data)

def admin_forum(request):
    if not request.session.get("su") or request.method != "GET": return redirect("/su")
    forums = Superuser.get_forums()
    data = {"forums": forums, "forums_count": len(forums)}

    return render(request, "admin_forum.html", context=data)


def black_list(request):
    if not request.session.get("id") or request.method != "GET": return redirect("/")
    cookie_user_id = int(request.session.get("id"))
    friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)
    active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
    blocked_users = User.get_blocked_users(cookie_user_id)
    user_info = User.get_info(cookie_user_id)

    if user_info["is_blocked"]: return redirect("/")

    data = {"cookie_user_id": cookie_user_id, "friend_requests_count": friend_requests_count,
            "active_dialogs_count": active_dialogs_count, "blocked_users": blocked_users,
            "user_info": user_info}
    return render(request, "black_list.html", context=data)


def friends(request):
    if request.method != "GET" or not request.session.get("id"): return redirect("/index")
    cookie_user_id = request.session.get("id")

    cookie_user_id = (int)(cookie_user_id)
    is_blocked = User.get_info(cookie_user_id)["is_blocked"]
    if is_blocked: return redirect(f"/user/{cookie_user_id}")
    friend_requests = Friend.get_friend_requests(cookie_user_id)
    friends = Friend.get_friends(cookie_user_id)
    data = {"friends": friends, "friends_count": len(friends), "friend_requests": friend_requests, \
            "friend_requests_count": len(friend_requests), "cookie_user_id": cookie_user_id}
    return render(request, "friends.html", context=data)


def forum(request, id):
    if not id or request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>", status_code=404)
    forum_info = Forum.get_forum_info(id)

    if not forum_info: return redirect("/index")
    forum_is_blocked = forum_info["is_blocked"]
    if forum_is_blocked: return redirect("/forum")
    messages = Forum.get_messages(id)
    cookie_user_id = None
    user_is_blocked = None
    active_dialogs_count = None
    friend_requests_count = None
    if request.session.get("id"):
        cookie_user_id = request.session.get("id")
        cookie_user_id = int(cookie_user_id)
        user_is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
        active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
        friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)

    data = {"cookie_user_id": cookie_user_id, "forum_info": forum_info, "messages": messages,
            "active_dialogs_count": active_dialogs_count, "friend_requests_count": friend_requests_count,
            "user_is_blocked": user_is_blocked}

    return render(request, "forum.html", context=data)


def forum_topics(request):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    forums = Forum.get_forums()
    cookie_user_id = None
    is_blocked = None
    active_dialogs_count = None
    friend_requests_count = None
    if request.session.get("id"):
        cookie_user_id = request.session.get("id")
        is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
        active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
        friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)

    data = {"cookie_user_id": cookie_user_id, "forums": forums, "forums_count": len(forums),
            "active_dialogs_count": active_dialogs_count, "friend_requests_count": friend_requests_count,
            "is_blocked": is_blocked}

    return render(request, "forum_topics.html", context=data)


def dialog(request, id):

    if not id or request.method != "GET" or not request.session.get("id"):
        print(f"Не ид и не гет {request.method} {id} {request.session.get('id')}")
        return redirect("/index")

    cookie_user_id = int(request.session.get("id"))

    is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
    if is_blocked: return redirect(f"/user/{cookie_user_id}")

    dialog_info = Dialog.get_dialog_info(id)

    if not dialog_info: return HttpResponse("<h1>Страница не найдена: 404</h1>")

    if not (dialog_info["sender_id"] == cookie_user_id or \
            dialog_info["receiver_id"] == cookie_user_id):
        return redirect(f"/user/{cookie_user_id}")

    Dialog.update_status(cookie_user_id, id)  # Обновление статуса о прочтении сообщения

    messages = Dialog.get_dialog_messages(id)
    opponent = Dialog.get_dialog_opponent_info(cookie_user_id, id)
    active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
    friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)
    user_is_in_black_list = User.user_is_in_black_list(opponent["id"], cookie_user_id)
    data = {"messages": messages, "dialog_id": id, "cookie_user_id": cookie_user_id, "opponent": opponent,
            "active_dialogs_count": active_dialogs_count, "friend_requests_count": friend_requests_count,
            "user_is_in_black_list": user_is_in_black_list}

    return render(request, "dialog.html", context=data)


def dialogs(request):
    if request.method != "GET" or not request.session.get("id"):
        return redirect("/index")
    cookie_user_id = int(request.session.get("id"))
    is_blocked = User.get_info((int)(cookie_user_id))["is_blocked"]
    if is_blocked:
        return redirect(f"/user/{cookie_user_id}")
    else:
        dialogs = Dialog.get_dialogs(cookie_user_id)
        dialogs_count = Dialog.get_dialogs_count(cookie_user_id)
        active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
        friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)

    data = {"dialogs": dialogs, "cookie_user_id": cookie_user_id, "dialogs_count": dialogs_count,
            "active_dialogs_count": active_dialogs_count, "friend_requests_count": friend_requests_count}

    return render(request, "dialogs.html", context=data)


# API
def reg(request):
    if request.method == "POST":
        return Reg.reg(request)


def auth(request):
    if request.method == "POST":
        return Auth.auth(request)


def suauth(request):
    if request.method == "POST":
        result = Superuser.auth(request)
        return JsonResponse({"message": result})


def find_user_by_link_su(request):
    if request.method == "POST":
        result = Superuser.find_user(request)
        return result


def find_user_by_link_for_block(request):
    if request.method == "POST":
        result = User.find_user_for_block(request)
        return result

def find_forum_by_link_su(request):
    if request.method == "POST":
        result = Superuser.find_forum(request)
        return result


def block_user_su(request):
    if request.method == "POST":
        result = Superuser.block_user(request)
        return result

def block_forum_su(request):
    if request.method == "POST":
        result = Superuser.block_forum(request)
        return result

def block_user(request):
    if request.method == "POST":
        result = User.block_user(request)
        return result


def exit(request):
    if request.method == "POST" and request.session["id"]:
        del request.session["id"]
        response = render(request, 'index.html')
        return response


def exit_su(request):
    if request.method == "POST" and request.session["su"]:
        del request.session["su"]
        response = render(request, 'index.html')
        return response


def send_wall_message(request):
    if request.method == "POST":
        return MessageWall.send_wall_message(request)


def delete_wall_message(request):
    if request.method == "POST":
        return MessageWall.delete_wall_message(request)


def friend_request(request):
    if request.method == "POST":
        return Friend.send_friend_request(request)


def cancel_friend_request(request):
    if request.method == "POST":
        return Friend.cancel_friend_request(request)


def accept_friend_request(request):
    if request.method == "POST":
        return Friend.accept_friend_request(request)


def delete_friend(request):
    if request.method == "POST":
        return Friend.delete_friend(request)


def change_avatar(request):
    if request.method == "POST":
        return File.change_avatar(request)


def forum_create(request):
    if request.method == "POST":
        return Forum.create_forum(request)


def forum_send_message(request):
    if request.method == "POST":
        return Forum.send_message(request)


def forum_delete_message(request):
    if request.method == "POST":
        return Forum.delete_message(request)


def dialog_send_outer(request):
    if request.method == "POST":
        return Dialog.send_outer(request)


def dialog_send_inner(request):
    if request.method == "POST":
        return Dialog.send_inner(request)


def set_page_like(request):
    if request.method == "POST":
        return UserPageLike.set_page_like(request)
