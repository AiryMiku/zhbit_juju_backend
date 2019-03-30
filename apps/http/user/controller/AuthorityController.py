from apps.http.db import models
from django.http import HttpRequest

from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from enum import Enum
from apps.http.user.controller import  UtilsController


class GroupPermission(Enum):
    modify_group_information = 'modify_group_information'
    modify_group_controller_list = 'modify_group_controller_list'
    delete_group = 'delete_group'


class MessagePermission(Enum):
    send_group_message = 'send_group_message'


def is_owner(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'group_id': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '此账号已在别处登陆')
    queryset = models.UserFollowGroupMapping.objects.filter(user=user_id, group=_param['group_id'])
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '该用户不在此群组')
    ans = (obj.role == 1)
    return rS.success({
        'is_admin': ans
    })


def is_admin(request: HttpRequest):
    _param = validate_and_return(request, {
        'access_token': '',
        'group_id': '',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    queryset = models.UserFollowGroupMapping.objects.filter(user=user_id, group=_param['group_id'])
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '该用户不在此群组')
    ans = ((obj.role == 1) | (obj.role == 2))
    return rS.success({
        'is_admin': ans
    })


def check_enable(user_id, group_id, permission_type):
    queryset = models.UserFollowGroupMapping.objects.filter(user=user_id, group=group_id)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is None:
        print('mapping not exists')
        return False
    permission = models.Permissions.objects.get(role=obj.role)
    _ = permission.to_list_dict()
    return _[permission_type]

