# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : reports
# Time       ：2023/8/4 16:57
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class Reports(ApiBase):
    def get_campaign_level_reports(self):
        """
        Fetches reports for campaigns.
        https://developer.apple.com/documentation/apple_search_ads/get_campaign-level_reports
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", "reports/campaigns", params=query_params, data=data)

    def get_ad_group_level_reports(self):
        """
        Fetches reports for ad groups within a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get__ad_group-level_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/adgroups", params=query_params, data=data)

    def get_keyword_level_reports(self):
        """
        Fetches reports for targeting keywords within a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get_keyword-level_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/keywords", params=query_params, data=data)

    def get_keyword_level_within_an_ad_group_reports(self):
        """
        Fetches reports for targeting keywords within an ad group.
        https://developer.apple.com/documentation/apple_search_ads/get_keyword-level_within_an_ad_group_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        adgroup_id = self.payload["path_params"]['adgroup_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/adgroups/{adgroup_id}/keywords", params=query_params, data=data)

    def get_search_term_level_reports(self):
        """
        Fetches reports for search terms within a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get_search_term-level_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/searchterms", params=query_params, data=data)

    def get_search_term_level_within_an_ad_group_reports(self):
        """
        Fetches reports for search terms within an ad group.
        https://developer.apple.com/documentation/apple_search_ads/get_search_term-level_within_an_ad_group_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        adgroup_id = self.payload["path_params"]['adgroup_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/adgroups/{adgroup_id}/searchterms", params=query_params, data=data)

    def get_ad_level_reports(self):
        """
        Fetches ad performance data within a campaign.
        https://developer.apple.com/documentation/apple_search_ads/get_ad-level_reports
        :return:
        """
        campaign_id = self.payload["path_params"]['campaign_id']
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"reports/campaigns/{campaign_id}/ads", params=query_params, data=data)
