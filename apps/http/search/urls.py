#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-07 15:57
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include

from apps.http.search.controller import SearchController

app_name = "search"

urlpatterns = [
    path('', SearchController.search)
]
