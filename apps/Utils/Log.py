#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/26/2018 16:48
# @Author  : ┏ (゜ω゜)=☞ Airy
# @Email   : a532710813@gmail.com
# @File    : Log.py
# @Software: PyCharm
import logging
import sys

logger_server = logging.getLogger('juju_server')


class Logger(object):
    @staticmethod
    def get_logger():
        return logger_server

    @staticmethod
    def print_log(log_type, tag, msg):
        """
        :param log_type: string
        :param tag: string
        :param msg: string
        :return:
        """
        print("Log-" + log_type + "-" + tag + "-" + msg + "\n")

    @classmethod
    def debug(cls, tag, msg):
        cls.get_logger().debug(cls.print_log("debug", tag, msg))

    @classmethod
    def warn(cls, tag, msg):
        cls.get_logger().warning(cls.print_log("warn", tag, msg))

    @classmethod
    def info(cls, tag, msg):
        cls.get_logger().info(cls.print_log("info", tag, msg))

    @classmethod
    def critical(cls, tag, msg):
        cls.get_logger().critical(cls.print_log("critical", tag, msg))

    @classmethod
    def fatal(cls, tag, msg):
        cls.get_logger().fatal(cls.print_log("fatal", tag, msg))


