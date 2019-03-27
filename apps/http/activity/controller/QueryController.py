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
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    activities = models.Activity.objects.all()
    count = activities.count()
    page_activities = activities[(page - 1) * size:page * size]

    data_list = list()
    for val in page_activities:
        group_name = models.ActivityBelongGroupMapping.objects.get(activity=val).group.name
        var = val.to_list_dict()
        var['group_name'] = group_name
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
        'page': 'int',
        'size': 'int'
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
    _group = models.ActivityBelongGroupMapping.objects.filter(activity=_activity).first().group

    display_data = _activity.to_list_dict()
    display_data['group_name'] = _group.name

    if _activity and _group:
        return rS.success(display_data)
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '活动不存在')


def index_comment(request: HttpRequest):
    """
    活动留下的评论
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    _comment_act = models.ActivityBelongComment.objects.filter(activity_id=_param['activity_id'])
    count = _comment_act

    _act_comment_page = _comment_act[(page - 1) * size:page * size]

    data_list = list()
    for val in _act_comment_page:
        _user = models.User.objects.get(pk=val.user_id)
        var = val.to_list_dict()
        var['user_nickname'] = _user.nickname
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })
