#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-08 19:11
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : QueryController.py
# @Software: PyCharm


from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import login_check


def index(request: HttpRequest):
    """
    返回所有的Act
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'page': '',
        'size': ''
    })

    page = _param['page']
    size = _param['size']

    groups = models.Group.objects.all()
    count = groups.count()
    page_groups = groups[(page - 1) * size:page * size]

    data_list = list
    for val in page_groups:
        var = val.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


@login_check()
def index_attend(request: HttpRequest):
    """
    返回用户参加的活动列表
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'page': '',
        'size': ''
    })

    # 假装有个user_id todo
    user_id = 1

    page = _param['page']
    size = _param['size']

    _act_attended = models.UserAttendActivityMapping.objects.filter(user_id=user_id)
    count = _act_attended.count()

    _act_attended_page = _act_attended[(page - 1) * size:page * size]

    data_list = list()
    for val in _act_attended_page:
        _act = models.Activity.objects.get(pk=val.activity_id)
        var = _act.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


def info(request: HttpRequest):
    """
    返回活动的详细信息
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': ''
    })

    _activity = models.Activity.objects.get(pk=_param['activity_id'])

    if _activity:
        return rS.success(_activity.to_list_dict())
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '活动不存在')

