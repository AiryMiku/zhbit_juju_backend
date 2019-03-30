#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: ModifyController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import request_check


# @login_check()
def modify_password(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'ex_password': '',
        'new_password': '',
        'confirm_password': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')

    queryset = models.User.objects.filter(pk=user_id)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,"该用户不存在")
    pwd = obj.password
    if _param['ex_password'] != pwd:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '密码错误')

    if _param['new_password'] != _param['confirm_password']:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '两次输出的密码不一致')

    obj.password = _param['new_password']
    obj.save()

    return rS.success()


# @login_check()
def modify_information(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'nickname': '',
        'sex': '',
        'birth': '',
        'phone': '',
        'status': '',
    })

    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')

    models.User.objects.filter(pk=user_id).update(**_param)
    return rS.success()


def modify_enable_visited_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'sex': '',
        'phone': '',
        'status': '',
        'birth': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')

    enable_visited_list = 0
    list_dict = {
        'sex': _param['sex'],
        'birth': _param['birth'],
        'phone': _param['phone'],
        'status': _param['status'],
    }

    for v in list_dict:
        print(v)
        enable_visited_list = enable_visited_list << 1 | int(list_dict[v])

    queryset = models.User.objects.filter(pk=user_id)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此用户不存在')
    obj.enable_visited_list = enable_visited_list
    obj.save()
    return rS.success()


def modify_enable_searched(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'enable_searched': '',
    })

    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')

    queryset = models.User.objects.filter(pk=user_id)
    obj = None
    for k in queryset:
        obj = k
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '用户不存在')
    obj.enable_searched = _param['enable_searched']
    obj.save()
    return rS.success()








