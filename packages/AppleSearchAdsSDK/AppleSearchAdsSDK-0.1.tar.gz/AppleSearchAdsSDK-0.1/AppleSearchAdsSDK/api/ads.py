# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ads
# Time       ：2023/8/3 15:42
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""

from AppleSearchAdsSDK.api import ApiBase


class Ads(ApiBase):
    def create_an_ad(self):
        """
        Creates an ad in an ad group with a creative.
        https://developer.apple.com/documentation/apple_search_ads/create_an_ad
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"campaigns/{campaign_id}/adgroups/{adgroup_id}/ads", params=query_params, data=data)

    def find_ads(self):
        """
        Finds ads within a campaign by selector criteria.
        https://developer.apple.com/documentation/apple_search_ads/find_ads
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f'campaigns/{campaign_id}/ads/find', params=query_params, data=data)

    def find_ads_org_level(self):
        """
        Fetches ads within an organization by selector criteria.
        https://developer.apple.com/documentation/apple_search_ads/find_ads_org-level
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f'ads/find', params=query_params, data=data)

    def get_an_ad(self):
        """
        Fetches an ad assigned to an ad group by identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_an_ad
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        ad_id = self.payload['path_params']['ad_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'campaigns/{campaign_id}/adgroups/{adgroup_id}/ads/{ad_id}', params=query_params)

    def get_all_ads(self):
        """
        Fetches all ads assigned to an ad group.
        https://developer.apple.com/documentation/apple_search_ads/get_all_ads
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'campaigns/{campaign_id}/adgroups/{adgroup_id}/ads', params=query_params)

    def update_an_ad(self):
        """
        Updates an ad in an ad group.
        https://developer.apple.com/documentation/apple_search_ads/update_an_ad
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        ad_id = self.payload['path_params']['ad_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("PUT", f'campaigns/{campaign_id}/adgroups/{adgroup_id}/ads/{ad_id}', params=query_params, data=data)

    def delete_an_ad(self):
        """
        Deletes an ad from an ad group.
        https://developer.apple.com/documentation/apple_search_ads/delete_an_ad
        :return:
        """
        campaign_id = self.payload['path_params']['campaign_id']
        adgroup_id = self.payload['path_params']['adgroup_id']
        ad_id = self.payload['path_params']['ad_id']
        return self.sdk.make_request("DELETE", f'campaigns/{campaign_id}/adgroups/{adgroup_id}/ads/{ad_id}')
