# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : targeting_keywords
# Time       ：2023/8/3 11:02
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class TargetingKeywords(ApiBase):
    def create_targeting_keywords(self):
        """
        Creates targeting keywords in ad groups.
        https://developer.apple.com/documentation/apple_search_ads/create_targeting_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords/bulk", data=data)

    def find_targeting_keywords_in_a_campaign(self):
        """
        Fetches targeting keywords in a campaign’s ad groups.
        https://developer.apple.com/documentation/apple_search_ads/find_targeting_keywords_in_a_campaign
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/targetingkeywords/find", data=data)

    def get_a_targeting_keyword_in_an_ad_group(self):
        """
        Fetches a specific targeting keyword in an ad group.
        https://developer.apple.com/documentation/apple_search_ads/get_a_targeting_keyword_in_an_ad_group
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        keyword_id = self.payload['path_params']['keyword_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords/{keyword_id}", params=query_params)

    def get_all_targeting_keywords_in_an_ad_group(self):
        """
        Fetches all targeting keywords in ad groups.
        https://developer.apple.com/documentation/apple_search_ads/get_all_targeting_keywords_in_an_ad_group
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords", params=query_params)

    def update_targeting_keywords(self):
        """
        Updates targeting keywords in ad groups.
        https://developer.apple.com/documentation/apple_search_ads/update_targeting_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("PUT", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords/bulk", data=data)

    def delete_a_targeting_keyword(self):
        """
        Deletes a targeting keyword in an ad group.
        https://developer.apple.com/documentation/apple_search_ads/delete_a_targeting_keyword
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        keyword_id = self.payload['path_params']['keyword_id']
        return self.sdk.make_request("DELETE", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords/{keyword_id}")

    def delete_targeting_keywords(self):
        """
        Deletes targeting keywords from ad groups.
        https://developer.apple.com/documentation/apple_search_ads/delete_targeting_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("DELETE", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/targetingkeywords/delete/bulk", data=data)
