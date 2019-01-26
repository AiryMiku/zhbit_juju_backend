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
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '删除群组失败')


def modify(request: HttpRequest):
    """
    修改群组
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'name': '',
        'notice': '',
        'introduction': ''
    })

    if _param['notice']:
        # notification
        Log.debug('GroupController', 'notification send')

    user_id = request.META.get('HTTP_TOKEN', None)
    # permission check result
    pr = None
    if pr:
        cur_group = models.Group.objects.update(**_param)
    else:
        rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '修改群组失败')
