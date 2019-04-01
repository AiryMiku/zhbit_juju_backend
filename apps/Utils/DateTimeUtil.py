#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-25 20:06
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : DateTimeUtil.py
# @Software: PyCharm

from datetime import datetime


def format_datetime_to_str(dt: datetime):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date_to_str(dt: datetime):
    return dt.strftime("%Y-%m-%d")
