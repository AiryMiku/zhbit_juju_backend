from apps.http.db import models
from django.http import HttpRequest

from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from enum import Enum


class GroupPermission(Enum):
    modify_group_information = 'modify_group_information'
    modify_group_controller_list = 'modify_group_controller_list'
    delete_group = 'delete_group'


class MessagePermission(Enum):
    send_group_message = 'send_group_message'


def is_owner(request: HttpRequest):
    _param = validate_and_return(request, {
        'user_id': '',
        'group_id': '',
    })
    obj = models.UserFollowGroupMapping.objects.get(user=_param['user_id'], group=_param['group_id'])
    ans = (obj.role == 1)
    return rS.success({
        'is_admin': ans
    })


def is_admin(request: HttpRequest):
    _param = validate_and_return(request, {
        'user_id': '',
        'group_id': '',
    })
    obj = models.UserFollowGroupMapping.objects.get(user=_param['user_id'], group=_param['group_id'])
    ans = ((obj.role == 1) | (obj.role == 2))
    return rS.success({
        'is_admin': ans
    })


def check_enable(user_id, group_id, permission_type):
    obj = models.UserFollowGroupMapping.objects.get(user=user_id, group=group_id)
    if obj is None:
        print('mapping not exists')
    permission = models.Permissions.objects.get(role=obj.role)
    return permission[permission_type]

