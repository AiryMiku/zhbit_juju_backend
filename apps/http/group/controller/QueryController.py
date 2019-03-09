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
        'page': '',
        'size': ''
    })

    page = _param['page']
    size = _param['size']

    groups = models.Group.objects.all()
    count = groups.count()
    if count == 0:
        rS.success({
            'count': count,
            'list': None
        })
    page_groups = groups[(page - 1) * size:page * size]

    data_list = list
    for val in page_groups:
        var = val.to_list_dict()
        data_list.append(var)

    rS.success({
        'count': count,
        'list': data_list
    })


@login_check()
def index_follow(request: HttpRequest):
    _param = validate_and_return(request, {
        'page': '',
        'size': ''
    })

    # 假装有个user_id
    user_id = 1

    page = _param['page']
    size = _param['size']

    _groups_follow = models.UserFollowGroupMapping.objects.filter(user_id=user_id)
    # todo 跨表查询


def member_index(request: HttpRequest):
    """
    查看指定的群组人员
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'page': '',
        'size': ''
    })

    page = _param['page']
    size = _param['size']

    members = models.UserFollowGroupMapping.objects.filter(group_id=_param['group_id'])
    count = members.count()

    if count == 0:
        rS.success({
            'count': count,
            'list': None
        })

    page_members = members[(page - 1) * size:page * size]
    data_list = list

    for val in page_members:
        var = dict()
        var['user_id'] = val.user_id
        var['nickname'] = val.user.nickname
        data_list.append(var)

    rS.success({
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
        'group_id': ''
    })

    group = models.Group.objects.get(pk=_param['group_id'])

    if group:
        display_data = dict()
        display_data['name'] = group.name
        display_data['notice'] = group.notice


def base_info_activity_index(request: HttpRequest):
    """
    群组页面会展示的活动信息
    :param request: 
    :return: 
    """
    _param = validate_and_return(request, {
        'group_id': '',
        'page': '',
        'size': ''
    })

    page = _param['page']
    size = _param['size']

    group = models.Group.objects.get(pk=_param['group_id'])

    activities = models.Activity.objects.filter(group=group)
    count = activities.count()

    if count == 0:
        rS.success({
            'count': count,
            'list': None
        })

    page_activities = activities[(page - 1) * size:page * size]
    data_list = list

    for val in page_activities:
        var = dict()
        var['title'] = val.title
        var['start_time'] = val.start_time
        mapping = models.UserAttendActivityMapping.objects.filter(activity=val)
        var['follow_people_num'] = mapping.count()
        data_list.append(var)

    rS.success({
        'count': count,
        'list': data_list
    })
