# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : negative_keywords
# Time       ：2023/8/3 11:57
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class AdGroupNegativeKeywords(ApiBase):
    def create_ad_group_negative_keywords(self):
        """
        Creates negative keywords in a specific ad group.
        https://developer.apple.com/documentation/apple_search_ads/create_ad_group_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/negativekeywords/bulk", data=data)

    def find_ad_group_negative_keywords(self):
        """
        Fetches negative keywords for campaigns.
        https://developer.apple.com/documentation/apple_search_ads/find_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/negativekeywords/find", data=data)

    def get_an_ad_group_negative_keyword(self):
        """
        Fetches a specific negative keyword in an ad group.
        https://developer.apple.com/documentation/apple_search_ads/get_an_ad_group_negative_keyword
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        keyword_id = self.payload['path_params']['keyword_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/negativekeywords/{keyword_id}", params=query_params)

    def get_all_ad_group_negative_keywords(self):
        """
        Fetches all negative keywords in ad groups.
        https://developer.apple.com/documentation/apple_search_ads/get_all_ad_group_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/negativekeywords", params=query_params)

    def update_ad_group_negative_keywords(self):
        """
        Updates negative keywords in an ad group.
        https://developer.apple.com/documentation/apple_search_ads/update_ad_group_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("PUT", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/negativekeywords/bulk", data=data)

    def delete_ad_group_negative_keywords(self):
        """
        Deletes negative keywords from an ad group.
        https://developer.apple.com/documentation/apple_search_ads/delete_ad_group_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/negativekeywords/delete/bulk", data=data)
