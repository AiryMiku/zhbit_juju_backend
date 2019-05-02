#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-08 14:44
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : GroupController.py
# @Software: PyCharm

from django.http import HttpRequest

from apps.Utils.validation.ParamValidation import validate_and_return
from apps.http.db import models
from datetime import datetime
from apps.Utils import ReturnResult as rS
from apps.Utils.Log import Logger as Log
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.user.controller.UtilsController import get_id_by_token
from apps.http.notification.controller.NotificationController import create_notification

@request_check()
def create(request: HttpRequest):
    """
    创建群组
    :return:
    """
    _param = validate_and_return(request, {
        'name': '',
        'introduction': '',
        'access_token': ''
    })
    _param['create_time'] = datetime.now()

    _param['owner_user_id'] = get_id_by_token(_param['access_token'])
    _param.pop('access_token')
    cur_group = models.Group.objects.create(**_param)

    if cur_group:
        return rS.success({
            'id': cur_group.id
        })
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '创建群组失败')


@request_check()
def delete(request: HttpRequest):
    """
    删除群组
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'access_token': ''
    })

    user_id = get_id_by_token(_param['access_token'])
    cur_group = models.Group.objects.get(pk=_param['group_id'])
    if user_id == cur_group.owner_user_id:
        cur_group.delete()
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '删除群组失败')


@request_check()
def modify(request: HttpRequest):
    """
    修改群组
        包含功能
            编辑公告
            编辑简介
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'name': 'nullable',
        'notice': 'nullable',
        'introduction': 'nullable'
    })

    group_id = _param['group_id']

    # 编辑公告
    if _param.get('notice', None) is not None:
        # notification
        create_notification(2, group_id, models.Group.objects.get(pk=group_id).notice + ' 更改为 ' + _param['notice'])
        Log.debug('GroupController', 'notification send')

    if _param.get('name', None) is not None:
        # notification
        create_notification(2, group_id, models.Group.objects.get(pk=group_id).name + ' 更改为 ' + _param['name'])
        Log.debug('GroupController', 'notification send')

    if _param.get('introduction', None) is not None:
        # notification
        create_notification(2, group_id, models.Group.objects.get(pk=group_id).introduction + ' 更改为 ' + \
                            _param['introduction'])
        Log.debug('GroupController', 'notification send')

    # permission check result todo
    pr = True
    if pr:
        _param.pop('group_id')
        models.Group.objects.filter(pk=group_id).update(**_param)
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '修改群组失败')


# member management
@request_check()
def set_admin(request: HttpRequest):
    """
    设置管理员
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'require_user_id': ''
    })

    user_id = request.META.get('HTTP_TOKEN', None)
    owner_id = models.Group.objects.get(pk=_param['group_id'])
    if user_id == owner_id:
        # make require_user_id as admin todo
        rq_user_id = _param['require_user_id']

        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '设置管理员失败')


@request_check()
def invite(request: HttpRequest):
    """
    邀请人员
        发送通知(need notification model
    :param request:
    :return:
    """

    _param = validate_and_return(request, {
        'group_id': '',
        'require_user_id': ''
    })

    # permission check result todo
    pr = None

    # send notification todo
    send_result = None
    if send_result:
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '邀请失败')


@request_check()
def remove_member(request: HttpRequest):
    """
    删除人员
    :param request:
    :return:
    """

    _param = validate_and_return(request, {
        'group_id': '',
        'require_user_id': ''
    })

    pr = True
    if pr:
        mapping = models.UserFollowGroupMapping.objects.get(group_id=_param['group_id'],
                                                            user_id=_param['require_user_id'])
        if mapping is not None:
            mapping.delete()
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '被操作用户不存在')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '缺少权限操作')
