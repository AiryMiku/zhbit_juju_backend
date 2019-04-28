#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: routing.py
# @Software: PyCharm

from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})