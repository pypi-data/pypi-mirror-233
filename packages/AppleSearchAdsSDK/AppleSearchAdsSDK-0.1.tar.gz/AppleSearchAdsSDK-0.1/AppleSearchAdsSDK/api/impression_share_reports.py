# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : impression_share_reports
# Time       ：2023/8/4 18:27
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class ImpressionShareReports(ApiBase):
    def impression_share_report(self):
        """
        Obtain a report ID.
        https://developer.apple.com/documentation/apple_search_ads/impression_share_report
        :return:
        """
        query_params = self.payload.get("query_params")
        data = self.payload['data']
        return self.sdk.make_request("POST", f"custom-reports", params=query_params, data=data)

    def get_a_single_impression_share_report(self):
        """
        Fetches a single Impression Share report containing metrics and metadata.
        https://developer.apple.com/documentation/apple_search_ads/get_a_single_impression_share_report
        :return:
        """
        report_id = self.payload['path_params']['report_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"custom-reports/{report_id}", params=query_params)

    def get_all_impression_share_reports(self):
        """
        Fetches all Impression Share reports containing metrics and metadata.
        https://developer.apple.com/documentation/apple_search_ads/get_all_impression_share_reports
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f"custom-reports", params=query_params)