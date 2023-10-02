# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : campaign_group
# Time       ：2023/7/26 17:33
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class UserAcl(ApiBase):
    def get_user_acl(self):
        """
        Fetches details of an API caller.
        https://developer.apple.com/documentation/apple_search_ads/get_user_acl
        :return:
        """
        return self.sdk.make_request("GET", "acls")

    def get_me_details(self):
        """
        Fetches details of an API caller.
        https://developer.apple.com/documentation/apple_search_ads/get_me_details
        :return:
        """
        return self.sdk.make_request("GET", "me")
