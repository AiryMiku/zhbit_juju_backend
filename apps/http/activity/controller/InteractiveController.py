#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-07 22:48
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : InteractiveController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from datetime import datetime
from apps.http.decorator.LoginCheckDecorator import request_check


@request_check()
def leave_comment(request: HttpRequest):
    """
    活动下的评论
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': '',
        'content': ''
    })

    user_id = _param['require_user_id']
    _comment_param = dict()
    _comment_param['user_id'] = user_id
    _comment_param['content'] = _param['content']
    _comment_param['time'] = datetime.now()
    _comment = models.Comment.objects.create(**_comment_param)

    if _comment is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '评论失败')

    _activity = models.Activity.objects.get(pk=_param['activity_id'])

    if _activity is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '没有该活动')

    mapping = models.ActivityBelongComment.objects.create(activity=_activity, comment=_comment)

    if mapping:
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '评论失败')


@request_check()
def del_comment(request: HttpRequest):
    """
    删除评论
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'comment_id': ''
    })
    _comment = models.Comment.objects.get(pk=_param['comment_id'])
    mapping = models.ActivityBelongComment.objects.get(comment_id=_param['comment_id'])
    if mapping:
        mapping.delete()
        _comment.delete()
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '删除评论失败')


@request_check()
def like(request: HttpRequest):
    """
    点赞功能
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': ''
    })

    _activity = models.Activity.objects.get(pk=_param['activity_id'])
    if _activity:
        mapping = models.ActivityLikeMapping.objects.create(activity=_activity, user_id=_param['require_user_id'])
        if mapping:
            _activity.like_number += 1
            _activity.save()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '点赞失败')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '点赞失败')


@request_check()
def dislike(request: HttpRequest):
    """
    点赞功能
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': ''
    })

    _activity = models.Activity.objects.get(pk=_param['activity_id'])
    if _activity:
        mapping = models.ActivityLikeMapping.objects.get(activity=_activity, user_id=_param['require_user_id'])
        if mapping:
            _activity.like_number -= 1
            _activity.save()
            mapping.delete()
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '取消点赞失败')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '取消点赞失败')


@request_check()
def follow(request: HttpRequest):
    """
    关注活动
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': ''
    })

    _activity = models.Activity.objects.get(pk=_param['activity_id'])
    if _activity:
        mapping = models.UserAttendActivityMapping.objects.create(activity=_activity, user_id=_param['require_user_id'])
        if mapping:
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '关注失败')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '关注失败')


@request_check()
def dis_follow(request: HttpRequest):
    """
    取消关注活动
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': ''
    })

    _activity = models.Activity.objects.get(pk=_param['activity_id'])
    if _activity:
        mapping = models.UserAttendActivityMapping.objects.filter(activity=_activity, user_id=_param['require_user_id'])
        if mapping.count() != 0:
            mapping.delete()
            return rS.success()
        else:
            return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '取消关注失败')
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '取消关注失败')


@request_check()
def is_follow(request: HttpRequest):
    """
    是否关注
    :param request:
    :return:
    """
    _param = validate_and_return(request, {
        'activity_id': '',
        'require_user_id': ''
    })

    user = models.User.objects.get(pk=_param['require_user_id'])
    activity = models.Activity.objects.get(pk=_param['activity_id'])

    if user is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '没有找到用户')

    if activity is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '没有该活动')

    mapping = models.UserAttendActivityMapping.objects.filter(user=user, activity=activity)

    data = dict()
    data['is_follow'] = False
    if mapping.count() != 0:
        data['is_follow'] = True

    return rS.success(data)
