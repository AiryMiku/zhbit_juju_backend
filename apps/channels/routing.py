#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: routing.py
# @Software: PyCharm

from . import comsumers
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<group_name>[^/]+)/$', comsumers.ChatConsumer),
    url(r'^push/(?P<id>[0-9a-z]+)/$', comsumers.PushConsumer),
    url(r'^ws/$', comsumers.TestConsumer)
]