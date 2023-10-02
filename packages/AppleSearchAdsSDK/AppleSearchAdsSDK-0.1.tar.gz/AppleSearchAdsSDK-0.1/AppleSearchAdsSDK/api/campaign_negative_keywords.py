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


class CampaignNegativeKeywords(ApiBase):
    def create_campaign_negative_keywords(self):
        """
        Creates negative keywords for a campaign.
        https://developer.apple.com/documentation/apple_search_ads/create_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/negativekeywords/bulk", data=data)

    def find_campaign_negative_keywords(self):
        """
        Fetches negative keywords for campaigns.
        https://developer.apple.com/documentation/apple_search_ads/find_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/negativekeywords/find", data=data)

    def get_a_campaign_negative_keyword(self):
        """
        Fetches a specific negative keyword in a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get_a_campaign_negative_keyword
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        keyword_id = self.payload['path_params']['keyword_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/negativekeywords/{keyword_id}", params=query_params)

    def get_all_campaign_negative_keywords(self):
        """
        Fetches all negative keywords in a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get_all_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/negativekeywords", params=query_params)

    def update_campaign_negative_keywords(self):
        """
        Updates negative keywords in a campaign.
        https://developer.apple.com/documentation/apple_search_ads/update_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("PUT", f"campaigns/{campaign_id}/negativekeywords/bulk", data=data)

    def delete_campaign_negative_keywords(self):
        """
        Deletes negative keywords from a campaign.
        https://developer.apple.com/documentation/apple_search_ads/delete_campaign_negative_keywords
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/negativekeywords/delete/bulk", data=data)
