# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : creatives
# Time       ：2023/8/3 17:19
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class Creatives(ApiBase):
    def create_a_creative(self):
        """
        Creates a creative object within an organization.
        https://developer.apple.com/documentation/apple_search_ads/create_a_creative
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", "creatives", params=query_params, data=data)

    def find_creatives(self):
        """
        Finds creatives within an organization.
        https://developer.apple.com/documentation/apple_search_ads/find_creatives
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", "creatives/find", params=query_params, data=data)

    def get_a_creative(self):
        """
        Fetches a creative by identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_a_creative
        :return:
        """
        creative_id = self.payload['path_params']['creative_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"creatives/{creative_id}", params=query_params)

    def get_all_creatives(self):
        """
        Fetches all creatives within an organization.
        https://developer.apple.com/documentation/apple_search_ads/get_all_creatives
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", "creatives", params=query_params)
