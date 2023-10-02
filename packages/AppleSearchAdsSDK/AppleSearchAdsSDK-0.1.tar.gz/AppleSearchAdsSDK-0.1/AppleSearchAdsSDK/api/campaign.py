# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : campaign
# Time       ：2023/7/26 17:33
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class Campaign(ApiBase):

    def create_a_campaign(self):
        """
        Creates a campaign to promote an app.
        https://developer.apple.com/documentation/apple_search_ads/create_a_campaign
        :return:
        """
        return self.sdk.make_request("POST", "campaigns")

    def find_campaigns(self):
        """
        Fetches campaigns with selector operators.
        https://developer.apple.com/documentation/apple_search_ads/find_campaigns
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("POST", "campaigns/find", params=query_params)

    def get_a_campaign(self):
        """
        Fetches a specific campaign by campaign identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_a_campaign
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}", params=query_params)

    def get_all_campaigns(self):
        """
        Fetches all of an organization’s assigned campaigns.
        https://developer.apple.com/documentation/apple_search_ads/get_all_campaigns
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns", params=query_params)

    def update_a_campaign(self):
        """
        Updates a campaign with a campaign identifier.
        https://developer.apple.com/documentation/apple_search_ads/update_a_campaign
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        data = self.payload["data"]
        return self.sdk.make_request("PUT", f"campaigns/{campaign_id}", data=data)

    def delete_a_campaign(self):
        """
        Deletes a specific campaign by campaign identifier.
        https://developer.apple.com/documentation/apple_search_ads/delete_a_campaign
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        return self.sdk.make_request("DELETE", f"campaigns/{campaign_id}")
