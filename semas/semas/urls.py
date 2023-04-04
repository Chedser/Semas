from django.urls import path, re_path, include
from django.contrib import admin
from semas_app import views

urlpatterns = [
    path("su", views.su),
    path("", views.index),
    path("/", views.index),
    re_path(r"^index", views.index),
    path('admin', views.admin),
    path('admin/forum', views.admin_forum),
    path('black_list', views.black_list),
    path('api/reg', views.reg),
    path('api/auth', views.auth),
    path('api/exit', views.exit),
    path('api/forum_create', views.forum_create),
    path('api/forum_send_message', views.forum_send_message),
    path('api/forum_delete_message', views.forum_delete_message),
    path('api/dialog_send_inner', views.dialog_send_inner),
    path('api/accept_friend_request', views.accept_friend_request),
    path('api/suauth', views.suauth),
    path('api/su/block_user', views.block_user_su),
    path('api/su/block_forum', views.block_forum_su),
    path('api/block_user', views.block_user),
    path('api/su/find_user', views.find_user_by_link_su),
    path('api/su/find_forum', views.find_forum_by_link_su),
    path('api/find_user', views.find_user_by_link_for_block),
    path('api/su/exit', views.exit_su),
    path('api/cancel_friend_request', views.cancel_friend_request),

    path('user/<int:id>', views.user),
    path('user/api/send_wall_message', views.send_wall_message),
    path('user/api/delete_wall_message', views.delete_wall_message),
    path('user/api/friend_request', views.friend_request),
    path('user/api/cancel_friend_request', views.cancel_friend_request),
    path('user/api/accept_friend_request', views.accept_friend_request),
    path('user/api/delete_friend', views.delete_friend),
    path('user/api/change_avatar', views.change_avatar),
    path('user/api/dialog_send_outer', views.dialog_send_outer),
    path('user/api/set_page_like', views.set_page_like),
    path('friends', views.friends),

    path('dialogs', views.dialogs),
    path('dialog/<int:id>', views.dialog),
    path('forum/<int:id>', views.forum),
    re_path(r'forum/?', views.forum_topics),

]

