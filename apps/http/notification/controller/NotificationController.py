#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: NotificationController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.user.controller import UtilsController
from apps.channels.comsumers import push
from apps.Utils.DateTimeUtil import format_time_to_str

@request_check()
def create_notification(notification_type, to_id, content):
    # 推送消息的类型 0 = 系统 1 = 给用户发 2 = 给群组的所有用户 3 = 给群组的管理员 4 = 给参与活动的人
    obj = models.Notification.objects.create(notification_type=notification_type, to_id=to_id, notification_content=content)
    # 推送消息给用户
    if notification_type == 0:
        arr = models.User.objects.all()
        for k in arr:
            push(k.id, format_time_to_str(obj.create_time) + " " + content)
    if notification_type == 1:
        push(to_id, format_time_to_str(obj.create_time) + " " + content)
    if notification_type == 2:
        arr = models.UserFollowGroupMapping.objects.filter(group=to_id)
        for k in arr:
            push(k.user_id, format_time_to_str(obj.create_time) + " " + content)
    if notification_type == 3:
        pass
    if notification_type == 4:
        arr = models.UserAttendActivityMapping.objects.filter(activity=to_id)
        for k in arr:
            push(k.user_id, format_time_to_str(obj.create_time) + " " + content)


@request_check()
def get_notification_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'page': 'int',
        'size': 'int',
    })

    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登录')

    queryset = models.Notification.objects.all().order_by("-create_time")

    list_data = []
    count = 0
    for k in queryset:
        if k.notification_type == 0:
            list_data.append(k.to_list_dict())
            count += 1

        if k.notification_type == 1:
            if k.to_id == user_id:
                list_data.append(k.to_list_dict())
                count += 1

        if k.notification_type == 2:
            if models.UserFollowGroupMapping.objects.filter(group=k.to_id, user=user_id):
                list_data.append(k.to_list_dict())
                count += 1

        if k.notification_type == 3:
            if models.UserFollowGroupMapping.objects.filter(group=k.to_id, user=user_id):
                if models.UserFollowGroupMapping.objects.get(group=k.to_id, user=user_id).role == 1 | \
                        models.UserFollowGroupMapping.objects.get(group=k.to_id, user=user_id).role == 2:
                    list_data.append(k.to_list_dict())
                    count += 1

        if k.notification_type == 4:
            if models.UserAttendActivityMapping.objects.filter(user=user_id, activity=k.to_id):
                list_data.append(k.to_list_dict())
                count += 1

    page = _param['page']
    size = _param['size']
    return rS.success({
        'count': count,
        'list': list_data[(page-1)*size:page*size],
    })


def push_all_notification(id):
    pass
