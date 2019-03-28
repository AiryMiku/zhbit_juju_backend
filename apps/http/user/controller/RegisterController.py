from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS


def register(request: HttpRequest):
    _param = validate_and_return(request, {
        'account_name': '',
        'password': '',
        'nickname': '',
    })
    # 验证 后续补

    _user = models.User.objects.create(**_param)

    if _user:
        return rS.success({
            'id': _user.id
            })
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '注册失败')


