# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : keyword
# Time       ：2023/7/26 17:26
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class KeywordModel:
    campaign_id: int
    ad_group_id: int
    keyword_id: int
    bid_amount: Dict
    creation_time: str
    deleted: bool
    match_type: str
    modification_time: str
    status: str
    text: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            campaign_id=apple_dict.get("campaignId"),
            ad_group_id=apple_dict.get("adGroupId"),
            keyword_id=apple_dict.get("id"),
            bid_amount=apple_dict.get("bidAmount"),
            creation_time=apple_dict.get("creationTime"),
            modification_time=apple_dict.get("modificationTime"),
            deleted=apple_dict.get("deleted"),
            match_type=apple_dict.get("matchType"),
            status=apple_dict.get("status"),
            text=apple_dict.get("text"),
        )

    def to_apple_dict(self):
        return {
            "campaignId": self.campaign_id,
            "adGroupId": self.ad_group_id,
            "id": self.keyword_id,
            "bidAmount": self.bid_amount,
            "creationTime": self.creation_time,
            "deleted": self.deleted,
            "matchType": self.match_type,
            "modificationTime": self.modification_time,
            "status": self.status,
            "text": self.text,
        }
