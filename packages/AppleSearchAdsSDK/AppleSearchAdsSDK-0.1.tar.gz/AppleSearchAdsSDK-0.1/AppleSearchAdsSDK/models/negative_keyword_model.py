# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : negative_keyword
# Time       ：2023/9/4 15:21
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class NegativeKeywordModel:
    campaign_id: int
    adgroup_id: int
    keyword_id: int
    deleted: bool
    match_type: str
    modification_time: str
    status: str
    text: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            campaign_id=apple_dict.get("campaignId"),
            adgroup_id=apple_dict.get("adGroupId"),
            keyword_id=apple_dict.get("id"),
            modification_time=apple_dict.get("modificationTime"),
            deleted=apple_dict.get("deleted"),
            match_type=apple_dict.get("matchType"),
            status=apple_dict.get("status"),
            text=apple_dict.get("text"),
        )

    def to_apple_dict(self):
        return {
            "campaignId": self.campaign_id,
            "adGroupId": self.adgroup_id,
            "id": self.keyword_id,
            "deleted": self.deleted,
            "matchType": self.match_type,
            "modificationTime": self.modification_time,
            "status": self.status,
            "text": self.text,
        }
