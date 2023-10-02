# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ads_model
# Time       ：2023/9/4 15:27
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import List


@dataclass
class AdsModel:
    ad_group_id: int
    campaign_id: int
    creation_time: str
    creative_id: int
    creative_type: str
    deleted: bool
    ad_id: int
    modification_time: str
    name: str
    org_id: int
    serving_state_reasons: List
    serving_status: str
    status: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            ad_group_id=apple_dict.get('adGroupId'),
            campaign_id=apple_dict.get("campaignId"),
            creation_time=apple_dict.get("creationTime"),
            creative_id=apple_dict.get("creativeId"),
            creative_type=apple_dict.get("creativeType"),
            deleted=apple_dict.get("deleted"),
            ad_id=apple_dict.get("id"),
            modification_time=apple_dict.get("modificationTime"),
            name=apple_dict.get("name"),
            org_id=apple_dict.get("orgId"),
            serving_state_reasons=apple_dict.get("servingStateReasons"),
            serving_status=apple_dict.get("servingStatus"),
            status=apple_dict.get("status"),
        )

    def to_apple_dict(self):
        return {
            "adGroupId": self.ad_group_id,
            "campaignId": self.campaign_id,
            "creationTime": self.creation_time,
            "creativeId": self.creative_id,
            "creativeType": self.creative_type,
            "deleted": self.deleted,
            "id": self.ad_id,
            "modificationTime": self.modification_time,
            "name": self.name,
            "orgId": self.org_id,
            "servingStateReasons": self.serving_state_reasons,
            "servingStatus": self.serving_status,
            "status": self.status,
        }
