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


def create(request: HttpRequest):
    """
    创建群组
    :return:
    """
    _param = validate_and_return(request, {
        'name': '',
        'introduction': ''
    })
    _param['create_time'] = datetime.now()
    cur_group = models.Group.objects.create(**_param)

    if cur_group:
        return rS.success({
            'group_id': cur_group.id
        })
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '创建群组失败')


def delete(request: HttpRequest):
    """
    删除群组
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': ''
    })

    user_id = request.META.get('HTTP_TOKEN', None)
    # permission check result
    pr = None
    if pr:
        cur_group = models.Group.objects.get(pk=_param['group_id'])
        cur_group.delete()
        rS.success()
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '删除群组失败')


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
        'name': '',
        'notice': '',
        'introduction': ''
    })

    # 编辑公告
    if _param['notice']:
        # notification
        Log.debug('GroupController', 'notification send')

    user_id = request.META.get('HTTP_TOKEN', None)
    # permission check result
    pr = None
    if pr:
        cur_group = models.Group.objects.update(**_param)
        cur_group.save()
        rS.success()
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '修改群组失败')


# member management
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
        # make require_user_id as admin
        rq_user_id = _param['require_user_id']

        rS.success()
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '设置管理员失败')


def invite(request: HttpRequest):
    """
    邀请人员
        发送通知
    :param request:
    :return:
    """

    _param = validate_and_return(request, {
        'group_id': '',
        'require_user_id': ''
    })

    # send notification
    send_result = None
    if send_result:
        rS.success()
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '邀请失败')


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
    user_id = request.META.get('HTTP_TOKEN', None)
    # permission check result
    pr = None
    if pr:
        mapping = models.UserFollowGroupMapping.objects.get(group_id=_param['group_id'],
                                                            user_id=_param['require_user_id'])
        if mapping is not None:
            mapping.delete()
            rS.success()
        else:
            rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '被操作用户不存在')
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '缺少权限操作')
