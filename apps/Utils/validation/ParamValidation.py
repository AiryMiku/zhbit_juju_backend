#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-15 15:03
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : ParamValidation.py
# @Software: PyCharm

from django.http import HttpRequest

from apps.Utils.RequestParamReceiver import get_request_param


def validate_and_return(request: HttpRequest, key_dict: dict):
    return _validate(request, get_request_param, key_dict)


def _validate(__source, __func, args_dict: dict):
    request_dict = {}
    for key in args_dict:
        # todo add rule check
        if args_dict[key]: # only key has value will add to the dict
            request_dict[key] = __func(request_key=key)
    return request_dict
