#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.message.controller import MessageController
from apps.http.message.controller import SessionController

app_name = "message"

urlpatterns = [
    path('create_message/', MessageController.create_message),
    path('get_message_list_by_session_id/', MessageController.get_message_list_by_session_id),
    path('create_session/', SessionController.create_session),
    path('get_session_list/', SessionController.get_session_list),
]
