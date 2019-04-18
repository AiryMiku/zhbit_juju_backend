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


def create_session(session_type, left_id,right_id, msg_id, latest_update_time):
    rs = models.Session.objects.create(type=session_type,
                                       left_id=left_id,
                                       right_id=right_id,
                                       latest_message=msg_id,
                                       latest_update_time=latest_update_time)


def is_session_exist(l_id,r_id):
    queryset = models.Session.objects.filter(left_id=l_id, right_id=r_id)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return -1
    return obj.id


def update_session_time(session_id, message):
    obj = models.Session.objects.get(pk=session_id)
    obj.latest_message = message
    obj.latest_update_time = message.send_time
    obj.save()


def get_session_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登录')
    # obj = models.User.objects.get(pk=user_id)
    session_list = models.Session.objects.all().order_by("-latest_update_time")
    count = 1
    list_data = list()
    for k in session_list:
        if k.type == 0:
            queryset = models.UserFollowGroupMapping.objects.filter(user_id=user_id, group_id=k.left_id)
            if queryset:
                dict_data = k.to_list_dict()
                dict_data.setdefault("last_message")
                dict_data['last_message'] = k.latest_message.content
                dict_data.pop('last_message')
        else:
            if k.left_id == user_id | k.right_id == user_id:
                dict_data.setdefault(str(k.id))
                dict_data[str(k.id)] = k.to_list_dict()

    return rS.success({"count":count,"list":list_data})

