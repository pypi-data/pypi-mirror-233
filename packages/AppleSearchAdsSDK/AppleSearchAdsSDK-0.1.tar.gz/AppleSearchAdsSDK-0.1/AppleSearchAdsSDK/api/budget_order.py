# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : budget_order
# Time       ：2023/8/2 18:53
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class BudgetOrder(ApiBase):
    def get_a_budget_order(self):
        """
        Fetches a specific budget order using a budget order identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_a_budget_order
        :return:
        """
        bo_id = self.payload["path_params"]['boId']
        return self.sdk.make_request("GET", f"budgetorders/{bo_id}")

    def get_all_budget_orders(self):
        """
        Fetches all assigned budget orders for an organization.
        https://developer.apple.com/documentation/apple_search_ads/get_all_budget_orders
        Query Parameters:
            limit int32
                The number of items to return per request. The maximum is 1000 for most objects.
                Default: 20
            offset int32
                The offset pagination that limits the number of returned records. The start of each page is offset by the specified number.
                Default: 0
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", "budgetorders", params=query_params)
