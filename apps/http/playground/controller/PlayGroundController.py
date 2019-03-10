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


def show(request: HttpRequest):
    """
    展示活动广场的群组活动消息
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



    rS.success({
        'count': count,
        'list': data_list
    })