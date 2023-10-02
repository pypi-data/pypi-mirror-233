# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : setup
# Time       ：2023/9/17 08:11
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from setuptools import setup, find_packages

setup(
    name='AppleSearchAdsSDK',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
        "retrying",
        "PyJWT"
    ],
)
