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
import hashlib
import os


def login(request: HttpRequest):
    _param = validate_and_return(request,{
        'account_name': '',
        'password': '',
    })

    queryset = models.User.objects.filter(account_name=_param['account_name'])
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

