# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : AdGroup
# Time       ：2023/8/2 19:06
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class AdGroup(ApiBase):
    def create_an_ad_group(self):
        """
        Creates an ad group as part of a campaign.
        https://developer.apple.com/documentation/apple_search_ads/create_an_ad_group
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups", data=data)

    def find_ad_groups(self):
        """
        Fetches ad groups within a campaign.
        https://developer.apple.com/documentation/apple_search_ads/find_ad_groups
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/find", data=data)

    def find_ad_groups_org_level(self):
        """
        Fetches ad groups within an organization.
        https://developer.apple.com/documentation/apple_search_ads/find_ad_groups_org-level
        :return:
        """
        data = self.payload['data']
        return self.sdk.make_request("POST", f"adgroups/find", data=data)

    def get_an_ad_group(self):
        """
        Fetches a specific ad group with a campaign and ad group identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_an_ad_group
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups/{adgroup_id}", params=query_params)

    def get_all_ad_groups(self):
        """
        Fetches all ad groups with a campaign identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_all_ad_groups
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"campaigns/{campaign_id}/adgroups", params=query_params)

    def update_an_ad_groups(self):
        """
        Updates an ad group with an ad group identifier.
        https://developer.apple.com/documentation/apple_search_ads/update_an_ad_group
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        data = self.payload['data']
        return self.sdk.make_request("PUT", f"campaigns/{campaign_id}/adgroups/{adgroup_id}", data=data)

    def delete_an_ad_group(self):
        """
        Deletes an ad group with a campaign and ad group identifier.
        https://developer.apple.com/documentation/apple_search_ads/delete_an_adgroup
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        return self.sdk.make_request("DELETE", f"campaigns/{campaign_id}/adgroups/{adgroup_id}")
