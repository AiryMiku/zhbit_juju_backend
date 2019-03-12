#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 18:05
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
    群组列表查看（全部）
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    groups = models.Group.objects.all()
    count = groups.count()
    page_groups = groups[(page - 1) * size:page * size]

    data_list = list()
    for val in page_groups:
        var = val.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


@login_check()
def index_follow(request: HttpRequest):
    """
    查找user follow的group
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'page': 'int',
        'size': 'int'
    })

    # 假装有个user_id
    user_id = 1

    page = _param['page']
    size = _param['size']

    _groups_followed = models.UserFollowGroupMapping.objects.filter(user_id=user_id)
    count = _groups_followed.count()

    _groups_followed_page = _groups_followed[(page - 1) * size:page * size]

    data_list = list()
    for val in _groups_followed_page:
        _group = models.Group.objects.get(pk=val.group_id)
        var = _group.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


def member_index(request: HttpRequest):
    """
    查看指定的群组人员
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': 'int',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    members = models.UserFollowGroupMapping.objects.filter(group_id=_param['group_id'])
    count = members.count()

    page_members = members[(page - 1) * size:page * size]
    data_list = list()

    for val in page_members:
        var = dict()
        var['user_id'] = val.user_id
        var['nickname'] = val.user.nickname
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


def base_info(request: HttpRequest):
    """
    群组页面的基础信息
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': 'int'
    })

    group = models.Group.objects.get(pk=_param['group_id'])

    if group:
        display_data = group.to_list_dict()
        return rS.success(display_data)


def base_info_activity_index(request: HttpRequest):
    """
    群组页面会展示的活动信息
    :param request: 
    :return: 
    """
    _param = validate_and_return(request, {
        'group_id': 'int',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    group = models.Group.objects.get(pk=_param['group_id'])

    activities = models.Activity.objects.filter(group=group)
    count = activities.count()

    page_activities = activities[(page - 1) * size:page * size]
    data_list = list()

    for val in page_activities:
        var = dict()
        var['title'] = val.title
        var['start_time'] = val.start_time
        mapping = models.UserAttendActivityMapping.objects.filter(activity=val)
        var['follow_people_num'] = mapping.count()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })
