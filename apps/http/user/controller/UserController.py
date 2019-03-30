#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: UserController.py
# @Software: PyCharm

# 获取用户相关的信息

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.user.controller import UtilsController


# @login_check()
def get_information(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')

    obj = models.User.objects.get(pk=user_id)

    return rS.success(obj.to_list_dict())


# @login_check()
def get_information_by_id(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'user_id': '',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')
    obj = models.User.objects.get(pk=_param['user_id'])
    _ = obj.to_list_dict()
    return rS.success(_)




