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


def search(request: HttpRequest):
    """
    搜索
        根据type
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'type': '',  # user group activity
        'key_word': '',
        'page': 'int',
        'size': 'int'
    })

    page = _param['page']
    size = _param['size']

    if _param['type'] is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '搜索未指定type')

    search_results = None

    if _param['type'] == 'activity':
        search_results = models.Activity.objects.filter(title__contains=_param['key_word'])
    elif _param['type'] == 'user':
        search_results = models.User.objects.filter(nickname__contains=_param['key_word'])
    elif _param['type'] == 'group':
        search_results = models.Group.objects.filter(name__contains=_param['key_word'])
    elif search_results is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '搜索是怎么可能运行到这里的？？？')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '搜索type不存在')

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
