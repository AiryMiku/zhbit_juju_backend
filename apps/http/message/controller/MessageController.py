#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: MessageController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.message.controller import SessionController


@request_check()
def create_message(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'session_id': '',
        'content': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    _param.pop('access_token')
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '该用户已在别处登录')
    if len(_param['content']) == 0:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'内容为空，请输入信息再重新发送')
    _param.setdefault("from_id")
    _param["from_id"] = user_id
    rs = models.Message.objects.create(**_param)
    rs.save()
    SessionController.update_session_time(_param['session_id'], rs)
    if rs:
        return rS.success()
    else:
        return rS.fail((rS.ReturnResult.UNKNOWN_ERROR, "发送失败"))


def get_message_list_by_session_id(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'session_id': '',
        'page': 'int',
        'size': 'int',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '该用户已在别处登录')

    page = _param['page']
    size = _param['size']
    queryset = models.Session.objects.filter(pk=_param['session_id'])
    obj = None
    msg_list = models.Message.objects.all().order_by("send_time")
    list_data = []
    count = 0
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此会话不存在')
    for k in msg_list:
        # print(k.session_id == int(_param['session_id']))
        if k.session_id == int(_param['session_id']):
            # print(k.to_list_dict())
            data = k.to_list_dict()
            list_data.append(data)
            count += 1

    return rS.success({
        'count': count,
        'list': list_data[(page-1)*size:page*size],
    })
