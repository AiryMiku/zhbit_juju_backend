#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-08 08:57
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : ActivityController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check


@request_check()
def create(request: HttpRequest):
    """
    创建（发布）活动
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'title': '',
        'content': '',
        'place': '',
        'start_time': '',
        'end_time': '',
    })

    group_id = _param['group_id']
    _param.pop('group_id')
    _activity = models.Activity.objects.create(**_param)

    if _activity:
        group = models.Group.objects.get(pk=group_id)
        if group:
            mapping = models.ActivityBelongGroupMapping.objects.create(activity=_activity, group=group)
            if mapping:
                return rS.success({
                    'id': _activity.id
                })
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '创建活动mapping失败')
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '群组不存在')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '创建活动失败')


@request_check()
def delete(request: HttpRequest):
    """
    删除活动
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': ''
    })

    # permission check todo

    _activity = models.Activity.objects.get(pk=_param['activity_id'])

    if _activity:
        _activity.delete()
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '删除活动失败')


@request_check()
def modify(request: HttpRequest):
    """
    修改活动
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'title': 'nullable',
        'content': 'nullable',
        'place': 'nullable',
        'start_time': 'nullable',
        'end_time': 'nullable',
    })

    # permission check todo

    # check what change you can notify them

    _var = _param
    _var.pop('activity_id')
    models.Activity.objects.filter(pk=_param['activity_id']).update(**_var)

    return rS.success()

