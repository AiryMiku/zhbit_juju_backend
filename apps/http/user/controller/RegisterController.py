from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.decorator.LoginCheckDecorator import request_check
import  re


@request_check()
def register(request: HttpRequest):
    _param = validate_and_return(request, {
        'account_name': '',
        'password': '',
        'nickname': '',
    })
    account_name = _param['account_name']
    password = _param['password']
    nickname = _param['nickname']
    if len(account_name) < 4 | len(account_name) > 16:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "用户名长度应在4到16之间，包括4和16")
    if re.match("^[A-Za-z0-9-]*$", account_name) is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "用户名应只包含数字，英文字母大小写")
    if len(password) < 4 | len(password) > 32:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "密码长度应在4到32之间，包括4和32")
    if re.match("^[A-Za-z0-9-]*$", password) is None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "密码应只包含数字，英文字母大小写")
    if len(nickname) == 0:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, "昵称不应为空")

    queryset = models.User.objects.filter(account_name=account_name)
    obj = None
    for k in queryset:
        obj = k
        break
    if obj is not None:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '用户名已存在')
    _user = models.User.objects.create(**_param)
    _user.save()
    if _user:
        return rS.success({
            'id': _user.id
            })
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR, '注册失败')


