# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : exceptions
# Time       ：2023/7/26 17:27
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""


class AppleSearchAdsSDKException(Exception):
    pass


class AuthenticationError(AppleSearchAdsSDKException):
    pass


class ParamsError(AppleSearchAdsSDKException):
    pass


class APIError(AppleSearchAdsSDKException):
    pass
