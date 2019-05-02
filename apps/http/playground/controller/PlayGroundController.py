#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-10 14:32
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : PlayGroundController.py
# @Software: PyCharm


from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check


@request_check()
def show(request: HttpRequest):
    """
    展示活动广场的活动消息
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    activities = models.Activity.objects.all().order_by('-id')
    count = activities.count()
    page_activities = activities[(page - 1) * size:page * size]

    data_list = list()
    for val in page_activities:
        var = val.to_list_dict()
        data_list.append(var)

    sorted_list = sorted(data_list, key=lambda x: x['like_number'], reverse=True)  # 降序

    return rS.success({
        'count': count,
        'list': sorted_list
    })
