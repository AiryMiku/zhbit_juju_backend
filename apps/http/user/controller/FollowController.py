#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: FollowController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.notification.controller import NotificationController


@request_check()
def follow(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'user_id': '',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')
    p = 0
    b_id = _param['user_id']
    if int(a_id) > int(b_id):
        a_id, b_id = b_id, a_id
        p = -1
    queryset = models.FollowMapping.objects.filter(user_left_id=a_id).filter(user_right_id=b_id)
    obj = None
    for k in queryset:
        obj = k
        break
    print(obj)
    if obj is not None:
        print(obj.to_list_dict())
        if p == 0:
            obj.left_to_right = True
        else:
            obj.right_to_left = True
        obj.save()
        return rS.success()
    else:
        if p == 0:
            rs = models.FollowMapping.objects.create(user_left_id=a_id,
                                                     user_right_id=b_id,
                                                     left_to_right=True,
                                                     right_to_left=False)
            NotificationController.create_notification(1, b_id, str(a_id)+'关注了你')
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'关注失败')
        else:
            rs = models.FollowMapping.objects.create(user_left_id=a_id,
                                                     user_right_id=b_id,
                                                     left_to_right=False,
                                                     right_to_left=True)
            NotificationController.create_notification(1, a_id, str(b_id) + '关注了你')
            if rs:
                return rS.success()
            else:
                return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '关注失败')


@request_check()
def dis_follow(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'user_id': '',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')
    p = 0
    b_id = _param['user_id']
    if int(a_id) > int(b_id):
        a_id, b_id = b_id, a_id
        p = -1
    print(a_id)
    print(b_id)
    queryset = models.FollowMapping.objects.filter(user_left_id=a_id, user_right_id=b_id)
    obj = None
    for k in queryset:
        obj = k
        break
    print(obj.to_list_dict())
    if obj:
        if p == 0:
            obj.left_to_right = False
        else:
            obj.right_to_left = False
        print(obj.to_list_dict())
        obj.save()
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '关系不存在')


@request_check()
def is_follow(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'user_id': '',
    })
    a_id = UtilsController.get_id_by_token(_param['access_token'])
    if a_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')
    b_id = _param['user_id']
    p = 0
    if int(a_id) > int(b_id):
        a_id, b_id = b_id, a_id
        p = -1
    print(a_id)
    print(b_id)
    queryset = models.FollowMapping.objects.filter(user_left_id=a_id).filter(user_right_id=b_id)
    print(queryset)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        print('关系不存在')
        return rS.success({
            'is_follow': False,
        })

    if p == 0:
        return rS.success({
            'is_follow': obj.left_to_right,
        })
    else:
        return rS.success({
            'is_follow': obj.right_to_left,
        })


@request_check()
def get_follow_list(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token': '',
        'page': 'int',
        'size': 'int'
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "此账号已在别处登陆")

    page = _param['page']
    size = _param['size']

    list_data = []
    follow_mapping_list = models.FollowMapping.objects.filter(user_left_id=user_id)
    count = follow_mapping_list.count()
    for k in follow_mapping_list:
        if not k.left_to_right:
            continue
        data = {
            'id': k.user_right_id,
            'nickname': models.User.objects.get(id=k.user_right_id).nickname,
        }
        list_data.append(data)

    follow_mapping_list = models.FollowMapping.objects.filter(user_right_id=user_id)
    count += follow_mapping_list.count()
    for k in follow_mapping_list:
        if not k.right_to_left:
            continue
        data = {
            'id': k.user_left_id,
            'nickname': models.User.objects.get(id=k.user_left_id).nickname,
        }
        list_data.append(data)
    list_data.sort(key=sort_nickname)

    return rS.success({
        'count': count,
        'list_data': list_data[(page-1)*size:page*size],
    })


def sort_nickname(self):
    return self[1]
