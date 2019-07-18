#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-08 14:48
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : ReturnResult.py
# @Software: PyCharm

import json
from enum import Enum

from django.http import HttpResponse


class ReturnResult(Enum):
    # RespondCode
    SUCCESS = 0

    # SystemError
    UNKNOWN_ERROR = 1

    # GroupError 10-30

    # ActivityError 30-50


def success(data=None, msg='success'):
    if data is None:
        data = {}
    response = {
        'code': 0,
        'msg': msg,
        'data': data
    }
    # Log.info(response, 'response')
    return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json", charset='utf-8')


def fail(return_value, msg=''):
    response = {
        'code': return_value.value,
        'msg': msg
    }
    # Log.info(response, 'response')
    return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json", charset='utf-8')
