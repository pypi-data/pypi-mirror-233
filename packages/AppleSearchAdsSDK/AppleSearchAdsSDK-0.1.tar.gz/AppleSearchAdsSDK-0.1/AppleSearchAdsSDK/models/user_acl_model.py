# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : campaign_group
# Time       ：2023/7/26 17:26
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import List


@dataclass
class UserAclModel:
    org_id: int
    currency: str
    org_name: str
    parent_org_id: int
    payment_model: str
    role_names: List
    time_zone: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            org_id=apple_dict.get("orgId"),
            currency=apple_dict.get("currency"),
            org_name=apple_dict.get("orgName"),
            parent_org_id=apple_dict.get("parentOrgId"),
            payment_model=apple_dict.get("paymentModel"),
            role_names=apple_dict.get("roleNames"),
            time_zone=apple_dict.get("timeZone")
        )

    def to_apple_dict(self):
        return {
            "orgId": self.org_id,
            "currency": self.currency,
            "orgName": self.org_name,
            "parentOrgId": self.parent_org_id,
            "paymentModel": self.payment_model,
            "roleNames": self.role_names,
            "timeZone": self.time_zone,
        }
