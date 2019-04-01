#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.user.controller import AuthorityController
from apps.http.user.controller import FollowController
from apps.http.user.controller import LoginController
from apps.http.user.controller import ModifyController
from apps.http.user.controller import RegisterController
from apps.http.user.controller import UserController

app_name = "user"

urlpatterns = [
    path('login/', LoginController.login),
    path('register/', RegisterController.register),
    path('get_information/', UserController.get_information),
    path('get_information_by_id/', UserController.get_information_by_id),
    path('is_admin/', AuthorityController.is_admin),
    path('is_owner/', AuthorityController.is_owner),
    path('follow/', FollowController.follow),
    path('dis_follow/',FollowController.dis_follow),
    path('is_follow/',FollowController.is_follow),
    path('modify_enable_searched/',ModifyController.modify_enable_searched),
    path('modify_enable_visited_list/',ModifyController.modify_enable_visited_list),
    path('modify_nickname/',ModifyController.modify_nickname),
    path('modify_sex/',ModifyController.modify_sex),
    path('modify_phone/',ModifyController.modify_phone),
    path('modify_status/',ModifyController.modify_status),
    path('modify_birth/',ModifyController.modify_birth),
    path('modify_password/',ModifyController.modify_password),
]
