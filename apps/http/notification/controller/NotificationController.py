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


@request_check()
def create_notification(notification_type, to_id, content):
    # 推送消息的类型 0 = 系统 1 = 给用户发 2 = 给群组的所有用户 3 = 给群组的管理员 4 = 给参与活动的人
    models.Notification.objects.create(notification_type=notification_type, to_id=to_id,notification_content=content)
    # 推送消息给用户


@request_check()
def get_notification_list(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
    })

    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登录')

    queryset = models.Notification.objects.all().order_by("-create_time")

    dict_data = {}
    for k in queryset:
        if k.notification_type == 0:
            dict_data.setdefault(str(k.id))
            dict_data[str(k.id)] = k.to_list_dict()

        if k.notification_type == 1:
            if k.to_id == user_id:
                dict_data.setdefault(str(k.id))
                dict_data[str(k.id)] = k.to_list_dict()

        if k.notification_type == 2:
            if models.UserFollowGroupMapping.objects.filter(group=k.to_id, user=user_id):
                dict_data.setdefault(str(k.id))
                dict_data[str(k.id)] = k.to_list_dict()

        if k.notification_type == 3:
            if models.UserFollowGroupMapping.objects.filter(group=k.to_id, user=user_id):
                if models.UserFollowGroupMapping.objects.get(group=k.to_id, user=user_id).role == 1 |     \
                        models.UserFollowGroupMapping.objects.get(group=k.to_id, user=user_id).role == 2:
                    dict_data.setdefault(str(k.id))
                    dict_data[str(k.id)] = k.to_list_dict()

        if k.notification_type == 4:
            if models.UserAttendActivityMapping.objects.filter(user=user_id, activity=k.to_id):
                dict_data.setdefault(str(k.id))
                dict_data[str(k.id)] = k.to_list_dict()

    return rS.success(dict_data)
