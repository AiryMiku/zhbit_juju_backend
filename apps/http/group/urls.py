#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-07 15:47
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.group.controller import (GroupController, InteractiveController, QueryController)

app_name = "Group"

urlpatterns = [
    path('create/', GroupController.create),
    path('delete/', GroupController.delete),
    path('modify/', GroupController.modify),
    # Member Manger
    path('setAdmin/', GroupController.set_admin),
    path('invite/', GroupController.invite),
    path('remove_member/', GroupController.remove_member),
    # Query
    path('indexAll/', QueryController.index),
    path('indexFollow', QueryController.index_follow),
    path('memberIndex/', QueryController.member_index),
    path('baseInfo/', QueryController.base_info),
    path('baseActivityIndex', QueryController.base_info_activity_index),
    # Interactive
    path('follow/', InteractiveController.follow),
    path('disFollow/', InteractiveController.dis_follow)
]