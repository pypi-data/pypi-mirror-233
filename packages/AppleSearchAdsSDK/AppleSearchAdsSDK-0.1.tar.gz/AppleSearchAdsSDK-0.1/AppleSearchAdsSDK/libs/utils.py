# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils
# Time       ：2023/6/20 18:54
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
import logging
import sys
from logging import handlers

import urllib3


def get_logger(level=logging.WARNING, log_path=None):
    """
    :param level: 默认WARNING
    :param log_path: 日志保存路径 如果为空时直接将日志 打到 sys.stdout
    :return: logger
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.basicConfig(format='[%(asctime)s]\t%(filename)s\t[line:%(lineno)d]\t%(levelname)s\t%(message)s', level=level, stream=sys.stdout)
    log = logging.getLogger()
    log.setLevel(level)
    if log_path:
        fh = handlers.RotatingFileHandler(log_path, maxBytes=5000000, backupCount=2, encoding='utf8')
        log.addHandler(fh)

    return log
