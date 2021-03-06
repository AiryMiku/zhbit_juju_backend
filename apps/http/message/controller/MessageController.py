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
from apps.http.notification.controller.NotificationController import create_notification

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
    if models.Session.objects.get(pk=_param['session_id']).type == 0:
        perminssion_check = models.UserFollowGroupMapping.objects.all();
        for k in perminssion_check:
            print(k.user_id)
            print(k.group_id)
            if k.user_id == user_id | k.group_id == models.Session.objects.get(pk=_param['session_id']).left_id:
                if k.role != 1 | k.role != 2:
                    return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "没有权限发信息")
    rs = models.Message.objects.create(**_param)
    rs.save()
    SessionController.update_session_time(_param['session_id'], rs)
    if rs:
        if models.Session.objects.get(pk=_param['session_id']).type == 0:
            create_notification(2, models.Session.objects.get(pk=_param['session_id']).left_id, \
                                "来自" + \
                                models.Group.objects.get(\
                                    pk=models.Session.objects.get(\
                                        pk=_param['session_id']).left_id).name\
                                + "的消息"+models.User.objects.get(pk=user_id).nickname \
                                         + " @全体成员 "+ _param['content'])
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
    print(_param['session_id'])
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
