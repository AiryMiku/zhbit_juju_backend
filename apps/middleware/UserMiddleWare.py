#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-15 15:47
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : UserMiddleWare.py
# @Software: PyCharm
from django.utils.deprecation import MiddlewareMixin


class UserMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET' or request.method == "POST":
            try:
                token = request.META.get('HTTP_TOKEN', None)
                if not token:
                    print('wtf you dont have token')
            except Exception as e:
                print(e)
