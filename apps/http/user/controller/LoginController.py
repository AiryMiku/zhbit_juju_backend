#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: LoginController.py
# @Software: PyCharm

from django.http import HttpRequest

from apps.Utils.validation.ParamValidation import validate_and_return
from apps.http.db import models
from datetime import datetime
from apps.Utils import ReturnResult as rS
from apps.Utils.Log import Logger as Log
from apps.http.decorator.LoginCheckDecorator import request_check
import hashlib
import os
import re

@request_check()
def login(request: HttpRequest):
    _param = validate_and_return(request,{
        'account_name': '',
        'password': '',
    })
    account_name = _param['account_name']
    password = _param['password']

    # if len(account_name) < 4 | len(account_name) > 16:
    #     return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "用户名长度应在4到16之间，包括4和16")
    # if re.match("^[A-Za-z0-9-]*$", account_name) is None:
    #     return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "用户名应只包含数字，英文字母大小写")
    # if len(password) < 4 | len(password) > 32:
    #     return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "密码长度应在4到32之间，包括4和32")
    # if re.match("^[A-Za-z0-9-]*$", password) is None:
    #     return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "密码应只包含数字，英文字母大小写")

    queryset = models.User.objects.filter(account_name=account_name)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'该用户不存在')

    if _param['password'] != obj.password:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'密码不正确')

    access_token = hashlib.sha1(os.urandom(24)).hexdigest()

    obj.access_token = access_token
    obj.save()

    return rS.success({
        'access_token': access_token,
        'user_id': obj.id,
    })


