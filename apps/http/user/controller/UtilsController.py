#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: UtilsController.py
# @Software: PyCharm

from apps.http.db import models


def get_id_by_token(access_token):
    obj = models.User.objects.get(access_token=access_token)
    if obj is None:
        return -1
    return obj.id