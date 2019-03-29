#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: FollowController.py
# @Software: PyCharm

from django.http  import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import login_check

# @login_check()
def follow(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'user_id':'',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')
    p = 0
    b_id = _param['user_id']
    if a_id < b_id:
        a_id,b_id = b_id,a_id
        p = -1
    obj = models.FollowMapping.objects.get(user_left_id=a_id,user_right_id=b_id)
    if obj:
        if p == 0:
            obj.left_to_right = True
        else:
            obj.right_to_left = True
        if obj.save():
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')
    else:
        if p == 0:
            rs = models.FollowMapping.objects.create(user_right_id=a_id,user_left_id=b_id,left_to_right=True,right_to_left=False)
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')
        else:
            rs = models.FollowMapping.objects.create(user_right_id=a_id,user_left_id=b_id,left_to_right=False,right_to_left=True)
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')


# @login_check()
def follow_user(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'user_id':'',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'此账号已在别处登陆')
    p = 0
    b_id = _param['user_id']
    if a_id < b_id:
        a_id,b_id = b_id,a_id
        p = -1
    obj = models.FollowMapping.objects.get(user_left_id=a_id,user_right_id=b_id)
    if obj:
        if p == 0:
            obj.left_to_right = False
        else:
            obj.right_to_left = False
        if obj.save():
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')
    else:
        if p == 0:
            rs = models.FollowMapping.objects.create(user_right_id=a_id,user_left_id=b_id,left_to_right=True,right_to_left=False)
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')
        else:
            rs = models.FollowMapping.objects.create(user_right_id=a_id,user_left_id=b_id,left_to_right=False,right_to_left=True)
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')

# @login_check()
def is_follow(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'user_id':'',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')
    b_id = _param['user_id']
    p = 0
    if a_id > b_id:
        a_id,b_id = b_id,a_id
        p = -1
    obj = models.FollowMapping.objects.get(user_left_id=a_id,user_right_id=b_id)
    if obj is None:
        return rS.success({
            'is_follow':False,
        })

    if p == 0:
        return rS.success({
            'is_follow':obj.left_to_right,
        })
    else:
        return rS.success({
            'is_follow': obj.right_to_left,
        })