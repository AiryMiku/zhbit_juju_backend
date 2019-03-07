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
    path('setAdmin/', GroupController.set_admin),
    path('invite/', GroupController.invite),
    path('remove_member/', GroupController.remove_member),
]