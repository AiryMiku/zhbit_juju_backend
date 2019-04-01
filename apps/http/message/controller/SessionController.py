#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: SessionController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import request_check

#
# def create_session(request: HttpRequest):
#     _param = validate_and_return(request, {
#         'group_id': '',
#     })


def create_session(type, left_id,right_id, msg_id, latest_update_time):
    rs = models.Session.objects.create(type=type,
                                       left_id=left_id,
                                       right_id=right_id,
                                       latest_message=msg_id,
                                       latest_update_time=latest_update_time)
    if rs:
        print("success build session")
    else:
        print("fail to build session")


def is_session_exist(l_id,r_id):
    queryset = models.Session.objects.filter(left_id=l_id, right_id=r_id)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return -1
    return obj.id


def update_session_time(session_id, update_time):
    obj = models.Session.objects.get(pk=session_id)
    obj.latest_update_time = update_time
    obj.save()


def get_session_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
    })
