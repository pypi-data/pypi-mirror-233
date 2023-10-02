# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : sdk.py
# Time       ：2023/7/26 17:24
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
import json

import requests
from retrying import retry

from AppleSearchAdsSDK.api.ad_group import AdGroup
from AppleSearchAdsSDK.api.budget_order import BudgetOrder
from AppleSearchAdsSDK.api.campaign import Campaign
from AppleSearchAdsSDK.api.user_acl import UserAcl
from AppleSearchAdsSDK.auth import Auth
from AppleSearchAdsSDK.exceptions import APIError, ParamsError
from AppleSearchAdsSDK.models.campaign_model import CampaignModel
from AppleSearchAdsSDK.models.user_acl_model import UserAclModel
from AppleSearchAdsSDK.settings import API_PATH

api_dict = {
    "UserAcl": UserAcl,
    "Campaign": Campaign,
    "BudgetOrder": BudgetOrder,
    "AdGroup": AdGroup,
}


class AppleSearchAdsSDK:
    def __init__(self, access_token, version="v4", environment='PRODUCTION', org_id=None):
        self.access_token = access_token
        self.api_base_url = f"{API_PATH}/{version}"
        self.org_id = org_id
        self.headers = None
        self.api_dict = api_dict

    def set_authorization(self, headers):
        self.headers = headers or {}
        if self.org_id:
            self.headers['X-AP-Context'] = f"orgId={self.org_id}"
        self.headers['Authorization'] = f"{self.access_token.get('token_type')} {self.access_token.get('access_token')}"
        self.headers['Content-Type'] = "application/json"

    @retry(retry_on_exception=lambda ex: isinstance(ex, APIError), stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def make_request(self, method, end_point, headers=None, params=None, data=None, timeout=180):
        self.set_authorization(headers)
        url = f"{self.api_base_url}/{end_point}"
        response = requests.request(method, url, headers=self.headers, params=params, data=json.dumps(data), timeout=timeout)
        return response

    def send(self, payload):
        api = self.api_dict[payload['api_type']](self, payload)  # 根据 api_type 从api_dict中获取对应的API实例
        return api.send()


if __name__ == '__main__':
    org_id = 123456
    payload = {'api_type': "UserAcl", 'api_name': 'get_user_acl'}
    # payload = {'api_type': "CampaignGroup", 'api_name': 'get_me_details'}
    # payload = {'api_type': "Campaign", 'api_name': 'get_a_campaign', 'path_params': {'campaign_id': 1070925755}, "query_params": {"fields": "id,name,status,displayStatus"}}
    # payload = {'api_type': "Campaign", 'api_name': 'get_a_campaign', 'path_params': {'campaign_id': 1070925755}}
    # payload = {'api_type': "Campaign", 'api_name': 'get_all_campaigns', "query_params": {"limit": "2", "offset": 0}}
    # payload = {'api_type': "Campaign", 'api_name': 'update_a_campaign', 'path_params': {'campaign_id': 1070925755}, "data": {
    #     "campaign": {
    #         "dailyBudgetAmount": {
    #             "amount": "0.01",
    #             "currency": "RMB"
    #         },
    #         "status": "PAUSED"
    #     }
    # }}
    # payload = {'api_type': "Campaign", 'api_name': 'delete_a_campaign', 'path_params': {'campaign_id': 1070925755}}
    # payload = {
    #     "api_type": "Campaign",
    #     "api_name": "find_campaigns",
    #     "data": {
    #         "pagination": {"offset": 0, "limit": 5000},
    #         "orderBy": [{"field": "id", "sortOrder": "ASCENDING"}],
    #         "conditions": [
    #             {"field": "deleted", "operator": "IN", "values": [True, False]},
    #         ]
    #     }
    # }
    # payload = {'api_type': "BudgetOrder", 'api_name': 'get_all_budget_orders', "query_params": {"limit": "2", "offset": 0}}
    # payload = {'api_type': "AdGroup", 'api_name': 'find_ad_groups', 'path_params': {'campaign_id': 584886016}, 'data': {
    #     "pagination": {"offset": 0, "limit": 5000},
    #     "orderBy": [{"field": "id", "sortOrder": "ASCENDING"}],
    # }}
    # payload = {'api_type': "AdGroup", 'api_name': 'find_ad_groups_org_level', 'data': {
    #     "pagination": {"offset": 0, "limit": 5000},
    #     "orderBy": [{"field": "id", "sortOrder": "ASCENDING"}],
    # }}
    # payload = {'api_type': "AdGroup", 'api_name': 'get_an_ad_group', 'path_params': {'campaign_id': 999908768, 'adgroup_id': 1403303995}, 'query_params': {'fields': "id,name"}}
    # payload = {'api_type': "AdGroup", 'api_name': 'get_all_ad_groups', 'path_params': {'campaign_id': 999908768}, 'query_params': {'fields': "id,name"}}

    resp = Auth.get_access_token(org_id)
    access_token = resp.get("data")
    sdk = AppleSearchAdsSDK(access_token, org_id=org_id)
    response = sdk.send(payload)

    for item in response.get("data"):
        # m = CampaignModel.from_apple_dict(item)
        m = UserAclModel.from_apple_dict(item)
        print(m)
