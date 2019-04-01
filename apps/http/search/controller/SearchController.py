#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-10 14:31
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : SearchController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check


@request_check()
def search_activity(request: HttpRequest):
    """
    搜索
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'key_word': '',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    search_results = models.Activity.objects.filter(title__icontains=_param['key_word'])
    count = search_results.count()
    page_search_results = search_results[(page - 1) * size:page * size]

    data_list = list()
    for val in page_search_results:
        var = val.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


@request_check()
def search_group(request: HttpRequest):
    """
    搜索
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'key_word': '',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    search_results = models.Group.objects.filter(name__icontains=_param['key_word'])
    count = search_results.count()
    page_search_results = search_results[(page - 1) * size:page * size]

    data_list = list()
    for val in page_search_results:
        var = val.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })


@request_check()
def search_user(request: HttpRequest):
    """
    搜索
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'key_word': '',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    search_results = models.User.objects.filter(nickname__icontains=_param['key_word'])
    count = search_results.count()
    page_search_results = search_results[(page - 1) * size:page * size]

    data_list = list()
    for val in page_search_results:
        var = val.to_list_dict()
        data_list.append(var)

    return rS.success({
        'count': count,
        'list': data_list
    })
