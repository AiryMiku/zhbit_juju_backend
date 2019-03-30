#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-08 16:25
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : LoginCheckDecorator.py
# @Software: PyCharm

import traceback
from functools import wraps
from django.http import HttpRequest
from apps.Utils import ReturnResult as rS
from apps.Utils.Log import Logger as Log
from apps.Utils.validation.ParamValidation import ParamMissingException


def request_check(*args, **kwargs):
    """

    :return:
    """
    _args = args
    _kwargs = kwargs

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request: HttpRequest, *args, **kwargs):
            try:
                # 判断是否需要登录
                # if _login_required(request):
                #     return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "用户未登录")

                # # 是否需要权限认证
                # if pl != '':
                #     _pl = pl.split(',')
                #     for _p in _pl:
                #         auth(request, _p, *_args, **_kwargs)
                #
                return func(request, *args, **kwargs)

            except ParamMissingException as e:
                Log.error('param missing', e.msg)
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, e.msg)

            except Exception as e:
                Log.critical('deco login check', str(e))
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "请刷新后重试~")

        return returned_wrapper

    return decorator


def _login_required(request: HttpRequest):
    user_id = request.META.get('HTTP_TOKEN', None)
    # 头部获取规则，系统自动加HTTP_前缀，postman直接写如上的🌰应该是TOKEN
    Log.debug('login_required', str(user_id))
    if user_id is None:     # 判断None必须用is
        return True
    return False
