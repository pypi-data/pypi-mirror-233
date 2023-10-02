# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : search_geolocations
# Time       ：2023/8/3 15:21
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class SearchGeolocations(ApiBase):
    def search_for_geolocations(self):
        """
        Fetches a list of geolocations for targeting.
        https://developer.apple.com/documentation/apple_search_ads/search_for_geolocations
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", "search/geo", params=query_params)

    def get_a_list_of_geolocations(self):
        """
        Gets geolocation details using a geoidentifier.
        https://developer.apple.com/documentation/apple_search_ads/get_a_list_of_geolocations
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload.get("data")
        return self.sdk.make_request("POST", "search/geo", params=query_params, data=data)
