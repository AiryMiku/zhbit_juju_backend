#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.message.controller import MessageController

app_name = "message"

urlpatterns = [
    path('create_message/', MessageController.create_message)
]
