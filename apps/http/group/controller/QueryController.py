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


def index(request: HttpRequest):
    """

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
            'list': None
        })
    page_groups = groups[(page - 1) * size:page * size]

    data_list = list
    for val in page_groups:
        var = val.to_list_dict()
        data_list.append(var)

    rS.success({
        'list': data_list
    })


def member_index(request: HttpRequest):
    """

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
        'list': data_list
    })




