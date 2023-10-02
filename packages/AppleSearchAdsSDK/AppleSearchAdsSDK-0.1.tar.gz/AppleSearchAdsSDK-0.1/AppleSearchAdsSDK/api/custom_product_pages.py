# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : custom_product_pages
# Time       ：2023/8/3 18:14
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from AppleSearchAdsSDK.api import ApiBase


class CustomProductPages(ApiBase):
    def get_product_pages(self):
        """
        Fetches metadata of all your custom product pages.
        https://developer.apple.com/documentation/apple_search_ads/get_product_pages
        :return:
        """
        adam_id = self.payload['path_params']['adam_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'apps/{adam_id}/product-pages', params=query_params)

    def get_product_pages_by_identifier(self):
        """
        Fetches metadata for a specific product page.
        https://developer.apple.com/documentation/apple_search_ads/get_product_pages_by_identifier
        :return:
        """
        adam_id = self.payload['path_params']['adam_id']
        product_page_id = self.payload['path_params']['product_page_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'apps/{adam_id}/product-pages/{product_page_id}', params=query_params)

    def get_product_page_locales(self):
        """
        Fetches product page locales by identifier.
        https://developer.apple.com/documentation/apple_search_ads/get_product_page_locales
        :return:
        """
        adam_id = self.payload['path_params']['adam_id']
        product_page_id = self.payload['path_params']['product_page_id']
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'apps/{adam_id}/product-pages/{product_page_id}/locale-details', params=query_params)

    def get_supported_countries_or_regions(self):
        """
        Fetches supported languages and language codes.
        https://developer.apple.com/documentation/apple_search_ads/get_supported_countries_or_regions
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", f'countries-or-regions', params=query_params)

    def get_app_preview_device_sizes(self):
        """
        Fetches supported app preview device-size mappings.
        https://developer.apple.com/documentation/apple_search_ads/get_app_preview_device_sizes
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("GET", 'creativeappmappings/devices', params=query_params)


