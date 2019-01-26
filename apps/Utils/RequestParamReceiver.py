#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-15 14:54
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : RequestParamReceiver.py
# @Software: PyCharm

from django.http import HttpRequest


def get_request_param(request: HttpRequest, request_key):
    val = None
    if not val:
        val = request.POST.get(request_key, None)
    if not val:
        val = request.GET.get(request_key, None)
    return val

