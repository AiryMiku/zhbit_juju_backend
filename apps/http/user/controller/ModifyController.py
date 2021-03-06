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


@request_check()
def modify_password(request: HttpRequest):
    _param = validate_and_return(request, {
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
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "该用户不存在")
    pwd = obj.password
    if _param['ex_password'] != pwd:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '密码错误')

    if _param['new_password'] != _param['confirm_password']:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '两次输出的密码不一致')

    obj.password = _param['new_password']
    obj.save()

    return rS.success()


@request_check()
def modify_information(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'sex': 'nullable',
        'nickname': 'nullable',
        'phone': 'nullable',
        'status': 'nullable',
        'birth': 'nullable',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登录')
    _param.pop('access_token')
    models.User.objects.filter(pk=user_id).update(**_param)
    return rS.success()


# def modify_sex_enable_visited(request: HttpRequest):
#     _param = validate_and_return(request,{
#         'access_token':'',
#         'sex':'',
#     })
#     user_id = UtilsController.get_id_by_token(_param['access_token'])
#     if user_id == -1:
#         return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登录')
#     _param.pop('access_token')
#     models.User.objects.filter(id=user_id).update(**_param)


def modify_enable_visited_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'birth': '',
        'phone': '',
        'status': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')

    enable_visited_list = 0
    list_dict = {
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
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此用户不存在')
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
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '用户不存在')
    obj.enable_searched = _param['enable_searched']
    obj.save()
    return rS.success()
