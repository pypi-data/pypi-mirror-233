# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : search_app
# Time       ：2023/8/3 15:12
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class SearchApps(ApiBase):
    def search_for_iOS_apps(self):
        """
        Searches for iOS apps to promote in a campaign.
        https://developer.apple.com/documentation/apple_search_ads/search_for_ios_apps
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", "search/apps", params=query_params)
