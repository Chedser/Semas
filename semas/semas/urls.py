from django.urls import path, re_path, include
from django.contrib import admin
from semas_app import views

urlpatterns = [
    path("", views.index),
    re_path(r"^index", views.index),
    path('admin/', admin.site.urls),
    path('api/reg', views.reg),
    path('api/auth', views.auth),
    path('api/forum_create', views.forum_create),
    path('api/forum_send_message', views.forum_send_message),

    path('user/<int:id>', views.user),
    path('user/api/wall_message', views.wall_message),
    path('user/api/friend_request', views.friend_request),
    path('user/api/cancel_friend_request', views.cancel_friend_request),
    path('user/api/accept_friend_request', views.accept_friend_request),
    path('user/api/delete_friend', views.delete_friend),
    path('user/api/change_avatar', views.change_avatar),
    path('user/api/dialog_send_outer', views.dialog_send_outer),
    path('friends', views.friends),

    path('dialogs', views.dialogs),
    path('dialog/<int:id>', views.dialog),
    path('forum/<int:id>', views.forum),
    re_path(r'forum/?', views.forum_topics),




]
