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


def index(request: HttpRequest):
    """

    :param request:
    :return:
    """