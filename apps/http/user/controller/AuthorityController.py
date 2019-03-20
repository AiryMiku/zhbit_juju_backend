from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS


def get_role(user_id, group_id):
    obj = models.UserFollowGroupMapping.objects.get(user=user_id, group=group_id)
    return obj.role


def enable_modify_group(user,group):
    role_ = get_role(user.id, group.id)
    obj = models.Permissions.objects.get(role=role_)
    return obj['enable_modify_group']

