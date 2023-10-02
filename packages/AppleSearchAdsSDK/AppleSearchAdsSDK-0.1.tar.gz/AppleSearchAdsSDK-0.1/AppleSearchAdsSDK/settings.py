# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : setting.py
# Time       ：2023/7/24 16:39
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
import os

APPLE_HOST = "appleid.apple.com"
BASE_URL = f"https://{APPLE_HOST}/auth/oauth2"
AUTH_ENDPOINT = f'{BASE_URL}/v2/authorize'
TOKEN_ENDPOINT = f'{BASE_URL}/token'
API_PATH = 'https://api.searchads.apple.com/api'
CLIENT_ID = os.environ['APPLE_SEARCHADS_CLIENT_ID']
TEAM_ID = os.environ['APPLE_SEARCHADS_TEAM_ID']
KEY_ID = os.environ['APPLE_SEARCHADS_KEY_ID']
