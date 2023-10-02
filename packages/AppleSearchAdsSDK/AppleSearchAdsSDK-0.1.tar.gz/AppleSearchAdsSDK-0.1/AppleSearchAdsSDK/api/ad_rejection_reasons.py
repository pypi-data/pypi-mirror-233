# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ad_rejection_reasons
# Time       ：2023/8/3 16:59
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class AdRejectionReasons(ApiBase):
    def find_ad_creative_rejection_reasons(self):
        """
        Fetches ad creative rejection reasons.
        https://developer.apple.com/documentation/apple_search_ads/find_ad_creative_rejection_reasons
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f'product-page-reasons/find', params=query_params, data=data)

    def find_app_assets(self):
        """
        Fetches app asset metadata by adam ID.
        https://developer.apple.com/documentation/apple_search_ads/find_app_assets
        :return:
        """
        adam_id = self.payload['path_params']['adam_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f'apps/{adam_id}/assets/find', params=query_params, data=data)
