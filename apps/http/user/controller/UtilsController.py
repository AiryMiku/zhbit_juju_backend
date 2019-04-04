#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: UtilsController.py
# @Software: PyCharm

from apps.http.db import models


def get_id_by_token(access_token):
    query = models.User.objects.filter(access_token=access_token)
    for k in query:
        return k.id
    return -1
