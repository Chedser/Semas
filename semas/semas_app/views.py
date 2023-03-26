from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.shortcuts import render


def index(request):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    cookie_user_id = request.COOKIES.get("id")
    if cookie_user_id: return redirect(f"user/{cookie_user_id}")
    return render(request, "index.html")


def user(request, id):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    cookie_user_id = request.COOKIES.get("id")  # id зарегистрированного пользователя

    is_authed_user = False
    is_login_user_page = False
    user_info = User.get_info(id)

    if (not id) or (not user_info): return HttpResponse("<h1>Страница не найдена: 404</h1>")

    if cookie_user_id and id:  # Пользователь авторизован и id передано в качестве аргумента
        cookie_user_id = int(cookie_user_id)
        is_authed_user = True
        User.update_time_of_last_action(cookie_user_id)
        if cookie_user_id == id:  # И сидит на своей странице
            is_login_user_page = True

    friend_status = Friend.get_friend_request_status(cookie_user_id, id)

    if user_info["is_blocked"]:
        friend_status = FriendStatus.UNAUTHED.value

    wall_messages = MessageWall.get_wall_messages(id)
    friend_requests_count = Friend.get_friend_requests_count(cookie_user_id)
    friends = Friend.get_friends_user_page(id, 8)
    active_dialogs_count = Dialog.get_active_dialogs_count(cookie_user_id)
    data = {"cookie_user_id": cookie_user_id, "user_id": id, "is_login_user_page": is_login_user_page, \
            "is_authed_user": is_authed_user, "wall_messages": wall_messages, "user_info": user_info, \
            "friend_status": friend_status, "friend_requests_count": friend_requests_count, "friends": friends,\
            "friends_count": len(friends), "active_dialogs_count": active_dialogs_count}

    return render(request, "user.html", context=data)

def friends(request):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    cookie_user_id = request.COOKIES.get("id")
    if not cookie_user_id: return HttpResponse("<h1>Страница не найдена: 404</h1>", status=404)

    cookie_user_id = (int)(cookie_user_id)
    friend_requests = Friend.get_friend_requests(cookie_user_id)
    friends = Friend.get_friends(cookie_user_id)
    data = {"friends": friends, "friends_count": len(friends), "friend_requests": friend_requests, \
            "friend_requests_count": len(friend_requests),"cookie_user_id": cookie_user_id}
    return render(request,"friends.html", context=data)

def forum(request, id):
    if not id or request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    forum_info = Forum.get_forum_info(id)

    if not forum_info: return HttpResponse("<h1>Страница не найдена: 404</h1>")
    messages = Forum.get_messages(id)
    cookie_user_id = request.COOKIES.get("id")
    data = {"cookie_user_id": cookie_user_id, "forum_info": forum_info, "messages": messages}
    return render(request, "forum.html", context=data)

def forum_topics(request):
    if request.method != "GET": return HttpResponse("<h1>Страница не найдена: 404</h1>")
    cookie_user_id = request.COOKIES.get("id")
    forums = Forum.get_forums()
    data = {"cookie_user_id": cookie_user_id, "forums": forums, "forums_count": len(forums)}
    return render(request, "forum_topics.html", context=data)

def dialog(request, id):
    cookie_user_id = request.COOKIES.get("id")

    if not id or not cookie_user_id or \
            request.method != "GET":
        return HttpResponse("<h1>Страница не найдена: 404</h1>")

    dialog_info = Dialog.get_dialog_info(id)

    if not dialog_info: return HttpResponse("<h1>Страница не найдена: 404</h1>")

    cookie_user_id = int(cookie_user_id)

    if not(dialog_info["sender_id"] == cookie_user_id or dialog_info["receiver_id"] == cookie_user_id):
        return HttpResponse("<h1>Страница не найдена: 404</h1>")

    Dialog.update_status(cookie_user_id, id) #Обновление статуса о прочтении сообщения

    messages = Dialog.get_dialog_messages(id)
    data = {"messages":messages}

    return render(request, "dialog.html", context=data)

def dialogs(request):
    cookie_user_id = request.COOKIES.get("id")
    if request.method != "GET" or \
            not cookie_user_id:
        return HttpResponse("<h1>Страница не найдена: 404</h1>")
    else:
        cookie_user_id = int (cookie_user_id)

    dialogs = Dialog.get_dialogs(cookie_user_id)
    data = {"dialogs":dialogs}

    return render(request, "dialogs.html", context=data)




# API
def reg(request):
    if request.method == "POST":
        return Reg.reg(request)


def auth(request):
    if request.method == "POST":
        return Auth.auth(request)


def wall_message(request):
    if request.method == "POST":
        return MessageWall.send_wall_message(request)


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

def dialog_send_outer(request):
    if request.method == "POST":
        return Dialog.send_outer(request)
