#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-15 15:03
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : ParamValidation.py
# @Software: PyCharm

from django.http import HttpRequest

from apps.Utils.Log import Logger as Log
from apps.Utils.RequestParamReceiver import get_request_param


def validate_and_return(request: HttpRequest, key_dict: dict):
    print('method：'+request.method)
    return _validate(request, get_request_param, key_dict)


def _validate(__source, __func, args_dict: dict):
    request_dict = {}
    for key in args_dict:

        var = __func(__source, key)
        # todo add rule check
        if args_dict[key] == 'nullable':
            if var is None:
                continue

        if var is None:
            Log.debug('validate', 'key:'+key+' is None')    # just show
            raise ParamMissingException(key=key, msg='缺少参数%s' % key)
        else:
            if args_dict[key].lower() == 'int':
                _var = int(var)
            else:
                _var = var
            request_dict[key] = _var

    return request_dict


class ParamMissingException(Exception):
    def __init__(self, key, msg):
        self.key = key,
        self.msg = msg
