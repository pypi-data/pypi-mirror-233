# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ad_group
# Time       ：2023/7/26 17:26
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AdGroupModel:
    org_id: int
    campaign_id: int
    ad_group_id: int
    automated_keywords_opt_in: bool
    cpa_goal: Dict
    default_bid_amount: Dict
    deleted: bool
    display_status: str
    start_time: str
    end_time: str
    modification_time: str
    name: str
    payment_model: str
    pricing_model: str
    serving_state_reasons: List
    serving_status: str
    status: str
    targeting_dimensions: Dict

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            org_id=apple_dict.get("orgId"),
            campaign_id=apple_dict.get("campaignId"),
            ad_group_id=apple_dict.get("id"),
            automated_keywords_opt_in=apple_dict.get("automatedKeywordsOptIn"),
            cpa_goal=apple_dict.get("cpaGoal"),
            default_bid_amount=apple_dict.get("defaultBidAmount"),
            deleted=apple_dict.get("deleted"),
            display_status=apple_dict.get("displayStatus"),
            start_time=apple_dict.get("startTime"),
            end_time=apple_dict.get("endTime"),
            modification_time=apple_dict.get("modificationTime"),
            name=apple_dict.get("name"),
            payment_model=apple_dict.get("paymentModel"),
            pricing_model=apple_dict.get("pricingModel"),
            serving_state_reasons=apple_dict.get("servingStateReasons"),
            serving_status=apple_dict.get("servingStatus"),
            status=apple_dict.get("status"),
            targeting_dimensions=apple_dict.get("targetingDimensions")
        )

    def to_apple_dict(self):
        return {
            "orgId": self.org_id,
            "campaignId": self.campaign_id,
            "id": self.ad_group_id,
            "automatedKeywordsOptIn": self.automated_keywords_opt_in,
            "cpaGoal": self.cpa_goal,
            "defaultBidAmount": self.default_bid_amount,
            "deleted": self.deleted,
            "displayStatus": self.display_status,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "modificationTime": self.modification_time,
            "name": self.name,
            "paymentModel": self.payment_model,
            "pricingModel": self.pricing_model,
            "servingStateReasons": self.serving_state_reasons,
            "servingStatus": self.serving_status,
            "status": self.status,
            "targetingDimensions": self.targeting_dimensions
        }
