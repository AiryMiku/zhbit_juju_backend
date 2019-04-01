#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: MessageController.py
# @Software: PyCharm

from django.http import HttpRequest
from apps.http.db import models
from apps.Utils.validation.ParamValidation import validate_and_return
from apps.Utils import ReturnResult as rS
from apps.http.user.controller import UtilsController
from apps.http.decorator.LoginCheckDecorator import request_check
from apps.http.message.controller import SessionController


def create_message(request: HttpRequest):
    _param = validate_and_return(request,{
        'access_token':'',
        'type': '',
        'from_id':'',
        'to_id':'',
        'content':'',
    })
    user_id = UtilsController.get_id_by_token(_param['access_token'])
    _param.pop('access_token')
    if user_id == -1:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'该用户已在别处登录')
    rs = models.Message.objects.create(**_param)
    type = _param['type']
    if rs:
        if type == 0:
            session_id = SessionController.is_session_exist(_param['from_id'], 0)
            if session_id != -1:
                SessionController.update_session_time(session_id, rs.send_time)
            else:
                a_id = _param['from_id']
                b_id = _param['to_id']
                int(a_id)
                int(b_id)
                if a_id > b_id:
                    a_id, b_id = b_id, a_id
                SessionController.create_session(type, a_id, b_id, rs.id, rs.send_time)
        else:
            pass
        return rS.success()
    else:
        return rS.fail(rS.ReturnResult.UNKNOWN_ERROR,'发送失败')


def get_message_list(request: HttpRequest):
    pass

