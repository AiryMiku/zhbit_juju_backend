#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-07 15:59
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.activity.controller import ActivityController, QueryController, InteractiveController

app_name = "activity"

urlpatterns = [
    path('create/', ActivityController.create),
    path('delete/', ActivityController.delete),
    path('modify/', ActivityController.modify),
    # Query
    path('indexAll/', QueryController.index),
    path('indexAttend/', QueryController.index_attend),
    path('info/', QueryController.info),
    path('indexComment/', QueryController.index_comment),
    # Interactive
    path('leaveComment/', InteractiveController.leave_comment),
    path('deleteComment/', InteractiveController.del_comment),
    path('like/', InteractiveController.like),
    path('dislike/', InteractiveController.dislike),
    path('follow/', InteractiveController.follow),
    path('disFollow/', InteractiveController.dis_follow)
]
