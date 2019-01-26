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

    page_groups = groups[(page - 1) * size:page * size]


