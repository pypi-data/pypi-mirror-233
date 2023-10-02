# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py
# Time       ：2023/7/26 17:17
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""


class ApiBase:
    def __init__(self, sdk, payload):
        self.sdk = sdk
        self.payload = payload

    def send(self):
        return getattr(self, self.payload['api_name'])()
