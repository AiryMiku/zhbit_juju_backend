#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: ModifyController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import LoginController
from apps.http.decorator.LoginCheckDecorator import login_check


@login_check()
def modify_password(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'ex_password':'',
        'new_password':'',
        'confirm_password':'',
    })
    user_id = LoginController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')

    obj = models.User.objects.get(pk=user_id)
    pwd = obj.password
    if _param['password'] != pwd:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'密码错误')

    if _param['new_password'] != _param['confirm_password']:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'两次输出的密码不一致')

    obj.password = _param['new_password']
    obj.save()

    return rS.ReturnResult()

@login_check()
def get_information(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
    })
    user_id = LoginController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')

    obj = models.User.objects.get(pk=user_id)

    return rS.success(obj.to_list_dict())

@login_check()
def modify_information(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'nickname':'',
        'sex':'',
        'birth':'',
        'phone':'',
        'status':'',
    })

    user_id = LoginController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')

    models.User.objects.filter(pk=user_id).update(**_param)

    return rS.success()




