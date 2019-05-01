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
from datetime import datetime


def get_session_by_id(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'session_id': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "该用户已在别处登录")
    queryset = models.Session.objects.filter(pk=_param['session_id'])
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,"该会话不存在")
    if obj.left_id == user_id:
        session_name = models.User.objects.get(pk=obj.right_id)
    else:
        session_name = models.User.objects.get(pk=obj.left_id)
    return rS.success({
        "id": obj.id,
        'type': obj.type,
        'title': session_name,
    })


def get_session(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'type': '',
        'left_id': '',  # type  = 0 left_id = group_id else = cur_user_id
        'right_id': '',  # type = 0 right = 0 else = to_id
    })
    if UtilsController.get_id_by_token(_param['access_token']) == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "该用户已在别处登录")
    l_id, r_id = _param['left_id'], _param['right_id']
    int(l_id)
    int(r_id)
    session_type = _param['type']
    if session_type == 1:
        if l_id > r_id:
            l_id, r_id = r_id, l_id
    session_id = is_session_exist(l_id, r_id)
    if session_id == -1:
        session_id = create_session(session_type, l_id, r_id)
        if session_id == -1:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "此会话不存在，请重新尝试")
        else:
            return rS.success({"session_id": session_id})
    return rS.success({
        "id": session_id,
        'type': _param['type'],
        'title': models.User.objects.get(id=_param['right_id']).nickname,
    })


def create_session(session_type, left_id, right_id):
    rs = models.Session.objects.create(type=session_type,
                                       left_id=left_id,
                                       right_id=right_id,
                                       latest_update_time=datetime.now()
                                       )
    if rs:
        return rs.id
    else:
        return -1


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
    obj.latest_message_content = message.content
    obj.latest_update_time = message.send_time
    obj.is_active = True
    obj.save()


def get_session_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'page': 'int',
        'size': 'int',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登录')

    page = _param['page']
    size = _param['size']

    # obj = models.User.objects.get(pk=user_id)
    session_list = models.Session.objects.all().order_by("-latest_update_time")
    count = 0
    list_data = list()
    for k in session_list:
        if not k.is_active:
            continue
        if k.type == 0:
            queryset = models.UserFollowGroupMapping.objects.filter(user_id=user_id, group_id=k.left_id)
            if queryset:
                dict_data = k.to_list_dict()
                dict_data.setdefault("title")
                dict_data['latest_update_time'] = str(dict_data['latest_update_time'])
                dict_data['title'] = models.Group.objects.get(id=k.left_id).name
                list_data.append(dict_data)
                count += 1
        else:
            dict_data = k.to_list_dict()
            dict_data.setdefault("title")
            dict_data['latest_update_time'] = str(dict_data['latest_update_time'])
            if k.left_id == user_id:
                dict_data['title'] = models.User.objects.get(id=k.right_id).nickname
                list_data.append(dict_data)
                count += 1
            if k.right_id == user_id:
                dict_data['title'] = models.User.objects.get(id=k.left_id).nickname
                list_data.append(dict_data)
                count += 1

    return rS.success({
        "count": count,
        "list": list_data[(page-1)*size:page*size]
    })

