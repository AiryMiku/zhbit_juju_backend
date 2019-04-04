#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: urls.py
# @Software: PyCharm


from django.urls import path, include

from apps.http.notification.controller import NotificationController

app_name = "notification"

urlpatterns = [
    path('get_notification_list/', NotificationController.get_notification_list)
]
